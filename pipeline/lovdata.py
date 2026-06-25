"""Henter gjeldende lover, sentrale forskrifter og Norsk Lovtiend fra Lovdata.

Kilde: api.lovdata.no/v1/publicData/list (åpent, ingen autentisering)
Data:  tar.bz2-pakker med XML-filer i Lovdata-format (NLOD 2.0)

Pakker som hentes:
  gjeldende-lover.tar.bz2                — konsoliderte gjeldende lover (~6 MB)
  gjeldende-sentrale-forskrifter.tar.bz2 — sentrale forskrifter (~21 MB)
  lovtidend-avd1-YYYY.tar.bz2            — Norsk Lovtiend avd. 1 (løpende)
  lovtidend-avd1-2001-2024.tar.bz2       — Norsk Lovtiend avd. 1 (historisk)

Rettsområde-berikelse: laster norwegian_laws_index.json (bygget av
norwegian_laws.py) og tilføyer subjects-felt til gjeldende lover.

Inkrementell: sammenligner lastModified fra API mot cache, laster bare ned
hvis endret siden sist.

Output: data/lovdata-lover.jsonl.gz, data/lovdata-forskrifter.jsonl.gz,
        data/lovdata-lovtiend1.jsonl.gz
"""
from __future__ import annotations

import gzip
import json
import re
import tarfile
import tempfile
import time
from io import BytesIO
from pathlib import Path

import requests

from norwegian_laws import load_index as _load_nlo_index

API_LIST_URL = "https://api.lovdata.no/v1/publicData/list"
DOWNLOAD_BASE = "https://api.lovdata.no/v1/publicData/"
USER_AGENT = "JusJob-DataPipeline/0.1 (+https://github.com/sstraume97/JusJob)"
SNIPPET_LENGTH = 400
DELAY_SECONDS = 2.0

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
CACHE_FILE = DATA_DIR / "lovdata_cache.json"


# ── XML-parsing ────────────────────────────────────────────────────────────────

_TAG_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"\s+")


def _strip(html: str) -> str:
    return _WS_RE.sub(" ", _TAG_RE.sub("", html)).strip()


def _find(text: str, pattern: str) -> str:
    m = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    return _strip(m.group(1)) if m else ""


def parse_xml(xml_bytes: bytes) -> dict | None:
    try:
        text = xml_bytes.decode("utf-8", errors="replace")
    except Exception:
        return None

    # Hopp over svært store filer (>2 MB) — typisk konsoliderte utgaver med full tekst
    if len(text) > 2_000_000:
        text = text[:2_000_000]

    doc_id = _find(text, r'class="dokid"[^>]*>([^<]+)</dd>')
    if not doc_id:
        doc_id = _find(text, r'<dt[^>]*class="dokid"[^>]*>.*?<dd[^>]*>([^<]+)</dd>')

    title = _find(text, r"<title>([^<]+)</title>")
    if not title:
        title = _find(text, r'class="tittel"[^>]*>([^<]*)</[a-z]+>')

    short_title = _find(text, r'class="kortTittel"[^>]*>([^<]+)<')
    if not short_title:
        short_title = _find(text, r"<shortTitle>([^<]+)</shortTitle>")

    ministry = _find(text, r'class="departement"[^>]*>([^<]+)<')
    if not ministry:
        ministry = _find(text, r"<ministry>([^<]+)</ministry>")

    doc_type = _find(text, r'class="(lov|forskrift|lovtidend[12]?)"')
    if not doc_type:
        # Utled fra dokid
        if "/lov/" in doc_id:
            doc_type = "lov"
        elif "/forskrift/" in doc_id:
            doc_type = "forskrift"
        else:
            doc_type = "ukjent"

    # ELI fra dok-ID: "NL/lov/2005-06-17-62" → "/eli/lov/2005-06-17-62"
    eli = ""
    if doc_id:
        m = re.search(r"(lov|forskrift)/(\d{4}-\d{2}-\d{2}-\d+)", doc_id)
        if m:
            eli = f"/eli/{m.group(1)}/{m.group(2)}"

    # URL
    url = ""
    if doc_id:
        url = f"https://lovdata.no/dokument/{doc_id.replace('NL/', 'NL/').replace('SF/', 'SF/')}"
        # Normaliser til standard Lovdata-format
        url = f"https://lovdata.no/dokument/{doc_id}"

    # Snippet: første avsnitt med meningsfullt innhold
    snippet = ""
    # Prøv <ingress> eller <formlEtterTittel>
    for pat in [r"<ingress[^>]*>(.*?)</ingress>",
                r'class="formlEtterTittel"[^>]*>(.*?)</[a-z]+'
                r'class="section"[^>]*>(.*?)</section>']:
        s = _find(text, pat)
        if s and len(s) > 30:
            snippet = s[:SNIPPET_LENGTH]
            break
    if not snippet:
        # Fallback: rens og ta de første 400 tegnene av body-tekst
        body_m = re.search(r"<body[^>]*>(.*)", text, re.DOTALL | re.IGNORECASE)
        if body_m:
            snippet = _strip(body_m.group(1))[:SNIPPET_LENGTH]

    if not title or not doc_id:
        return None

    return {
        "doc_id": doc_id,
        "eli": eli,
        "type": doc_type,
        "title": title,
        "short_title": short_title,
        "ministry": ministry,
        "url": url,
        "snippet": snippet,
        # subjects berikes fra norwegian_laws_index etter parsing (se main())
        "subjects": [],
    }


# ── Lovdata public data API ───────────────────────────────────────────────────

def _session() -> requests.Session:
    s = requests.Session()
    s.headers["User-Agent"] = USER_AGENT
    return s


def _load_cache() -> dict:
    if CACHE_FILE.exists():
        return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
    return {}


def _save_cache(cache: dict) -> None:
    CACHE_FILE.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")


def _list_packages(session: requests.Session) -> list[dict]:
    """Hent manifest fra Lovdata API."""
    resp = session.get(API_LIST_URL, timeout=30)
    resp.raise_for_status()
    return resp.json()


def _download_and_parse(session: requests.Session, filename: str) -> list[dict]:
    """Last ned tar.bz2-pakke og parser alle XML-filer."""
    url = DOWNLOAD_BASE + filename
    print(f"  Laster ned {filename} ...", flush=True)
    resp = session.get(url, timeout=300, stream=True)
    if resp.status_code == 404:
        print(f"  ADVARSEL: {filename} finnes ikke ennå (404) — hopper over", flush=True)
        return []
    resp.raise_for_status()

    data = BytesIO(resp.content)
    results = []

    with tarfile.open(fileobj=data, mode="r:bz2") as tar:
        members = [m for m in tar.getmembers() if m.name.endswith(".xml")]
        total = len(members)
        print(f"  {total} XML-filer i pakken", flush=True)
        for i, member in enumerate(members, 1):
            if i % 500 == 0 or i == total:
                print(f"  Parser {i}/{total} ({100*i//total}%)...", end="\r", flush=True)
            try:
                f = tar.extractfile(member)
                if f is None:
                    continue
                doc = parse_xml(f.read())
                if doc:
                    results.append(doc)
            except Exception:
                pass

    print(f"\n  Hentet {len(results)} dokumenter fra {filename}", flush=True)
    time.sleep(DELAY_SECONDS)
    return results


def _write_jsonl_gz(path: Path, docs: list[dict]) -> None:
    with gzip.open(path, "wt", encoding="utf-8") as f:
        for doc in docs:
            f.write(json.dumps(doc, ensure_ascii=False) + "\n")


# ── Pakke-til-fil-mapping ─────────────────────────────────────────────────────

def _output_file(filename: str) -> Path:
    # Faktiske filnavn fra api.lovdata.no/v1/publicData/list (bekreftet nov 2025):
    #   gjeldende-lover.tar.bz2
    #   gjeldende-sentrale-forskrifter.tar.bz2   ← NB: ikke "sentrale-forskrifter"
    #   lovtidend-avd1-2025.tar.bz2              ← løpende år
    #   lovtidend-avd1-2001-2024.tar.bz2         ← historisk arkiv
    if "gjeldende-lover" in filename:
        return DATA_DIR / "lovdata-lover.jsonl.gz"
    if "gjeldende-sentrale-forskrifter" in filename or "sentrale-forskrifter" in filename:
        return DATA_DIR / "lovdata-forskrifter.jsonl.gz"
    if "avd1" in filename or "avd-1" in filename:
        return DATA_DIR / "lovdata-lovtiend1.jsonl.gz"
    if "avd2" in filename or "avd-2" in filename:
        return DATA_DIR / "lovdata-lovtiend2.jsonl.gz"
    return DATA_DIR / f"lovdata-{filename.replace('.tar.bz2','')}.jsonl.gz"


# ── Hovedflyt ─────────────────────────────────────────────────────────────────

def _make_refid(doc_id: str) -> str:
    """Konverter Lovdata doc_id til norwegian-laws refid-format.

    "NL/lov/2005-06-17-62"  → "lov/2005-06-17-62"
    "SF/forskrift/2001-..."  → "forskrift/2001-..."
    """
    # Fjern landkode-prefiks (NL/, SF/, osv.)
    parts = doc_id.split("/", 1)
    return parts[1] if len(parts) == 2 else doc_id


def _enrich_with_subjects(docs: list[dict], nlo_index: dict[str, list[str]]) -> list[dict]:
    """Berik hvert dokument med rettsområder fra norwegian_laws_index."""
    enriched = 0
    for doc in docs:
        refid = _make_refid(doc.get("doc_id", ""))
        subjects = nlo_index.get(refid, [])
        doc["subjects"] = subjects
        if subjects:
            enriched += 1
    if docs:
        print(f"  Rettsområde-berikelse: {enriched}/{len(docs)} dokumenter fikk subjects", flush=True)
    return docs


def main() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    session = _session()
    cache = _load_cache()

    # Last rettsområde-indeks fra norwegian_laws.py (kjøres separat i workflow)
    nlo_index = _load_nlo_index()
    if nlo_index:
        print(f"Lastet norwegian-laws indeks: {len(nlo_index)} lover med rettsområde", flush=True)
    else:
        print("Ingen norwegian-laws indeks funnet — kjører uten subjects-berikelse", flush=True)

    print("\nHenter Lovdata pakkeliste ...", flush=True)
    packages = _list_packages(session)
    print(f"  {len(packages)} pakker tilgjengelig", flush=True)

    updated = False
    for pkg in packages:
        filename = pkg.get("filename", "")
        last_modified = pkg.get("lastModified", "")
        description = pkg.get("description", filename)

        if not filename.endswith(".tar.bz2"):
            continue

        # Hopp over hvis ikke endret siden sist
        if cache.get(filename) == last_modified:
            print(f"  [{filename}] Uendret siden {last_modified} — hopper over", flush=True)
            continue

        print(f"\n📦 {description} ({filename})", flush=True)
        docs = _download_and_parse(session, filename)

        # Berik gjeldende lover med rettsområde (forskrifter og lovtiend har ikke refid i indeksen)
        if "gjeldende-lover" in filename and nlo_index:
            docs = _enrich_with_subjects(docs, nlo_index)

        out_path = _output_file(filename)
        _write_jsonl_gz(out_path, docs)
        print(f"  → {out_path.name}: {len(docs)} dokumenter", flush=True)

        cache[filename] = last_modified
        updated = True

    if updated:
        _save_cache(cache)
        print("\nCache oppdatert.", flush=True)
    else:
        print("\nIngen endringer — alle pakker er oppdaterte.", flush=True)


if __name__ == "__main__":
    main()
