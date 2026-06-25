"""Henter vedtak og veiledninger fra Forbrukertilsynet.

Scraped fra:
  https://www.forbrukertilsynet.no/lov-og-rett/vedtak
  https://www.forbrukertilsynet.no/lov-og-rett/markedsradets-vedtak
  https://www.forbrukertilsynet.no/forbrukerklageutvalget/vedtak-i-forbrukerklageutvalget-etter-mai-2025-2
  https://www.forbrukertilsynet.no/lov-og-rett/veiledninger-og-retningslinjer

Vedtak har referanseformat FOV-YYYY-NNNNNN (Forbrukertilsynets vedtak).
Inkrementell: oppdager nye referansenumre mot cache.
Output: data/forbrukertilsynet.jsonl.gz
"""
from __future__ import annotations

import gzip
import json
import re
import time
from dataclasses import asdict, dataclass
from pathlib import Path

import requests
from bs4 import BeautifulSoup

BASE = "https://www.forbrukertilsynet.no"
USER_AGENT = "JusJob-DataPipeline/0.1 (+https://github.com/sstraume97/JusJob)"
DELAY = 1.5

PAGES = [
    ("vedtak",           f"{BASE}/lov-og-rett/vedtak",                    "vedtak"),
    ("markedsradet",     f"{BASE}/lov-og-rett/markedsradets-vedtak",      "markedsrådets vedtak"),
    ("fku",              f"{BASE}/forbrukerklageutvalget/vedtak-i-forbrukerklageutvalget-etter-mai-2025-2", "FKU-vedtak"),
    ("veiledninger",     f"{BASE}/lov-og-rett/veiledninger-og-retningslinjer", "veiledning"),
]

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
OUT_PATH = DATA_DIR / "forbrukertilsynet.jsonl.gz"
CACHE_FILE = DATA_DIR / "forbrukertilsynet_cache.json"


@dataclass
class Document:
    ref_id: str          # "FOV-2025-235041" eller URL-slug
    type: str            # vedtak / markedsrådets vedtak / FKU-vedtak / veiledning
    title: str
    url: str
    date: str            # fra liste-tekst når tilgjengelig
    snippet: str


def _session() -> requests.Session:
    s = requests.Session()
    s.headers["User-Agent"] = USER_AGENT
    return s


def _load_cache() -> set[str]:
    if CACHE_FILE.exists():
        return set(json.loads(CACHE_FILE.read_text(encoding="utf-8")))
    return set()


def _save_cache(seen: set[str]) -> None:
    CACHE_FILE.write_text(json.dumps(sorted(seen), ensure_ascii=False, indent=2), encoding="utf-8")


def _get(session: requests.Session, url: str) -> BeautifulSoup | None:
    for attempt in range(4):
        try:
            r = session.get(url, timeout=30)
            r.raise_for_status()
            time.sleep(DELAY)
            return BeautifulSoup(r.text, "html.parser")
        except Exception as e:
            if attempt == 3:
                print(f"  FEIL ved {url}: {e}", flush=True)
                return None
            time.sleep(5 * (attempt + 1))
    return None


def _extract_ref(url: str, title: str) -> str:
    m = re.search(r"(FOV-\d{4}-\d+)", url + " " + title, re.IGNORECASE)
    if m:
        return m.group(1).upper()
    # Fallback: siste del av URL-slug
    slug = url.rstrip("/").split("/")[-1]
    return slug[:80]


def _scrape_list_page(session: requests.Session, url: str, doc_type: str) -> list[Document]:
    """Scraper en listeside og returnerer dokumenter med URL og tittel."""
    soup = _get(session, url)
    if not soup:
        return []

    docs = []
    # Finn lenker som peker til enkeltdokumenter
    for a in soup.find_all("a", href=True):
        href = a["href"]
        text = a.get_text(strip=True)
        if not text or len(text) < 5:
            continue
        # Filtrer: interne lenker som ikke er navigasjon
        if href.startswith("/") or href.startswith(BASE):
            full_url = href if href.startswith("http") else BASE + href
            # Hopp over toppnivå-sider og navigasjonslenker
            if any(full_url.rstrip("/") == (BASE + p).rstrip("/") for _, p, _ in PAGES):
                continue
            if re.search(r"\d{4}", text + full_url):  # sannsynlig vedtak/dokument
                ref_id = _extract_ref(full_url, text)
                # Prøv å finne dato i tekst nær lenken
                parent_text = a.parent.get_text(" ", strip=True) if a.parent else ""
                date_m = re.search(r"\d{1,2}\.\d{1,2}\.\d{4}", parent_text)
                date = date_m.group(0) if date_m else ""

                docs.append(Document(
                    ref_id=ref_id,
                    type=doc_type,
                    title=text,
                    url=full_url,
                    date=date,
                    snippet="",
                ))

    # Dedupliser på ref_id
    seen = set()
    unique = []
    for d in docs:
        if d.ref_id not in seen:
            seen.add(d.ref_id)
            unique.append(d)

    return unique


def _fetch_snippet(session: requests.Session, doc: Document) -> str:
    """Henter snippet fra enkeltdokument (kun for nye dokumenter)."""
    soup = _get(session, doc.url)
    if not soup:
        return ""
    # Prøv article / main / .content
    for sel in ["article", "main", ".entry-content", ".page-content", ".content"]:
        el = soup.select_one(sel)
        if el:
            text = el.get_text(" ", strip=True)
            return text[:400]
    return ""


def main() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    session = _session()
    cache = _load_cache()

    # Les eksisterende data
    existing: dict[str, dict] = {}
    if OUT_PATH.exists():
        with gzip.open(OUT_PATH, "rt", encoding="utf-8") as f:
            for line in f:
                d = json.loads(line.strip())
                existing[d["ref_id"]] = d

    new_docs: list[Document] = []
    total_found = 0

    for page_id, url, doc_type in PAGES:
        print(f"\n📋 {doc_type} — {url}", flush=True)
        docs = _scrape_list_page(session, url, doc_type)
        print(f"  {len(docs)} dokumenter funnet på listeside", flush=True)
        total_found += len(docs)

        new_on_page = 0
        for doc in docs:
            if doc.ref_id in cache or doc.ref_id in existing:
                continue
            # Hent snippet for nye dokumenter
            doc.snippet = _fetch_snippet(session, doc)
            new_docs.append(doc)
            new_on_page += 1

        print(f"  {new_on_page} nye dokumenter", flush=True)

    print(f"\nTotalt: {total_found} funnet, {len(new_docs)} nye", flush=True)

    if not new_docs:
        print("Ingen nye dokumenter — ferdig.", flush=True)
        return

    # Slå sammen eksisterende + nye
    all_docs = list(existing.values()) + [asdict(d) for d in new_docs]
    with gzip.open(OUT_PATH, "wt", encoding="utf-8") as f:
        for doc in all_docs:
            f.write(json.dumps(doc, ensure_ascii=False) + "\n")

    # Oppdater cache
    new_ids = cache | {d.ref_id for d in new_docs}
    _save_cache(new_ids)
    print(f"Lagret {len(all_docs)} dokumenter totalt i {OUT_PATH.name}", flush=True)


if __name__ == "__main__":
    main()
