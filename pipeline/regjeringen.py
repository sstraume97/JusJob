"""Henter dokumenter fra regjeringen.no.

Henter følgende dokumenttyper med juridisk verdi:
  - Proposisjoner (Prop. L / Prop. LS / Prop. S)
  - NOU-er (Norges offentlige utredninger)
  - Meldinger til Stortinget (Meld. St.)
  - Rundskriv
  - Høringer (høringsnotater)

Bruker regjeringen.no sin søke-/liste-API med paginering.
Inkrementell: nye URL-er sammenlignes mot cache.
Output: data/regjeringen.jsonl.gz
"""
from __future__ import annotations

import gzip
import json
import re
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from urllib.parse import urlencode, urljoin

import requests
from bs4 import BeautifulSoup

BASE = "https://www.regjeringen.no"
USER_AGENT = "JusJob-DataPipeline/0.1 (+https://github.com/sstraume97/JusJob)"
DELAY = 1.2
PAGE_SIZE = 25

# Dokumenttyper: (kilde-id, listing-url, type-etikett, subjects)
DOC_TYPES = [
    (
        "prop",
        f"{BASE}/no/dokumenter/proposisjoner/id2506404/",
        "proposisjon",
        ["Stats-/statsforfatnings-/statsborgerrett"],
    ),
    (
        "nou",
        f"{BASE}/no/dokumenter/nou-er/id2506398/",
        "NOU",
        [],
    ),
    (
        "meld",
        f"{BASE}/no/dokumenter/meldinger-stortinget/id2506405/",
        "stortingsmelding",
        [],
    ),
    (
        "rundskriv",
        f"{BASE}/no/dokumenter/rundskriv/id2506401/",
        "rundskriv",
        [],
    ),
    (
        "horing",
        f"{BASE}/no/dokumenter/horing/id2506400/",
        "høring",
        [],
    ),
]

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
OUT_PATH = DATA_DIR / "regjeringen.jsonl.gz"
CACHE_FILE = DATA_DIR / "regjeringen_cache.json"

# Maks antall sider per dokumenttype per kjøring (unngå for lang kjøretid)
MAX_PAGES_PER_TYPE = 100


@dataclass
class Document:
    url: str
    doc_type: str          # proposisjon / NOU / stortingsmelding / rundskriv / høring
    title: str
    date: str
    department: str
    doc_number: str        # f.eks. "Prop. 1 L (2024–2025)" eller "NOU 2024: 7"
    snippet: str
    subjects: list


def _session() -> requests.Session:
    s = requests.Session()
    s.headers["User-Agent"] = USER_AGENT
    return s


def _load_cache() -> set[str]:
    if CACHE_FILE.exists():
        return set(json.loads(CACHE_FILE.read_text(encoding="utf-8")))
    return set()


def _save_cache(seen: set[str]) -> None:
    CACHE_FILE.write_text(
        json.dumps(sorted(seen), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def _get(session: requests.Session, url: str, params: dict | None = None) -> BeautifulSoup | None:
    for attempt in range(4):
        try:
            r = session.get(url, params=params, timeout=30)
            r.raise_for_status()
            time.sleep(DELAY)
            return BeautifulSoup(r.text, "html.parser")
        except Exception as e:
            if attempt == 3:
                print(f"  FEIL ved {url}: {e}", flush=True)
                return None
            time.sleep(5 * (attempt + 1))
    return None


def _extract_doc_number(text: str, url: str) -> str:
    """Trekk ut dokumentnummer som 'NOU 2024: 7', 'Prop. 1 L (2024–2025)', osv."""
    patterns = [
        r"NOU\s+\d{4}:\s*\d+",
        r"Prop\.?\s+\d+\s+[A-Z]+\s*\(\d{4}[–-]\d{4}\)",
        r"Meld\.?\s+St\.?\s+\d+\s*\(\d{4}[–-]\d{4}\)",
        r"St\.meld\.?\s+nr\.?\s+\d+\s*\(\d{4}[–-]\d{4}\)",
        r"Prop\.?\s+\d+\s+[A-Z]+",
    ]
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            return m.group(0).strip()
    # Fallback: siste del av URL-path
    slug = url.rstrip("/").split("/")[-1]
    return slug[:60]


def _extract_department(soup: BeautifulSoup, fallback: str = "") -> str:
    """Finn departement/utgiver fra enkeltside."""
    for sel in [
        ".byline-department",
        ".article-header-meta .publisher",
        ".department",
        "[class*='department']",
        "[class*='publisher']",
    ]:
        el = soup.select_one(sel)
        if el:
            return el.get_text(strip=True)[:120]
    # Prøv meta-tag
    meta = soup.find("meta", {"name": re.compile(r"department|publisher", re.I)})
    if meta and meta.get("content"):
        return meta["content"][:120]
    return fallback


def _scrape_list_page(
    session: requests.Session,
    base_url: str,
    start: int,
) -> tuple[list[dict], bool]:
    """
    Henter én listeside med offset `start`.
    Returnerer (liste av {url, title, date, department, doc_number}, has_more).
    """
    params = {"startCount": start, "stopCount": start + PAGE_SIZE}
    soup = _get(session, base_url, params=params)
    if not soup:
        return [], False

    items = []
    # regjeringen.no bruker ulike liste-strukturer — prøv flere selektorer
    links_found = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        text = a.get_text(strip=True)
        if not text or len(text) < 8:
            continue
        # Interne lenker til enkeltdokumenter (inneholder årstall i URL eller tekst)
        if not (href.startswith("/") or href.startswith(BASE)):
            continue
        full_url = href if href.startswith("http") else BASE + href
        # Filtrer ut navigasjons- og listelenker
        if full_url.rstrip("/") == base_url.rstrip("/"):
            continue
        if not re.search(r"/id\d+|/\d{4}[/-]", full_url):
            continue
        if full_url in links_found:
            continue
        links_found.add(full_url)

        # Dato
        parent_text = a.parent.get_text(" ", strip=True) if a.parent else ""
        date_m = re.search(r"\d{1,2}\.\d{1,2}\.\d{4}", parent_text)
        date = date_m.group(0) if date_m else ""

        # Departement fra nærliggende tekst
        dept_m = re.search(r"departement|direktorat|statsråd", parent_text, re.I)
        dept_text = parent_text[:80] if dept_m else ""

        doc_number = _extract_doc_number(text + " " + parent_text, full_url)

        items.append({
            "url": full_url,
            "title": text,
            "date": date,
            "department": dept_text,
            "doc_number": doc_number,
        })

    # Sjekk om det er en "neste side"-lenke
    has_more = bool(
        soup.find("a", string=re.compile(r"neste|next|>", re.I))
        or len(items) >= PAGE_SIZE
    )
    return items, has_more


def _fetch_detail(session: requests.Session, url: str) -> tuple[str, str, str]:
    """Henter (snippet, department, date) fra enkeltdokumentside."""
    soup = _get(session, url)
    if not soup:
        return "", "", ""

    dept = _extract_department(soup)

    # Dato fra <time> eller meta
    date = ""
    time_el = soup.find("time")
    if time_el:
        date = time_el.get("datetime", time_el.get_text(strip=True))[:10]
    if not date:
        meta_date = soup.find("meta", {"name": re.compile(r"date|published", re.I)})
        if meta_date and meta_date.get("content"):
            date = meta_date["content"][:10]

    # Snippet fra ingress/sammendrag eller article-body
    snippet = ""
    for sel in [
        ".ingress", ".lead", ".article-lead",
        ".article-body", "article .text", "main .text",
        "article", "main",
    ]:
        el = soup.select_one(sel)
        if el:
            snippet = el.get_text(" ", strip=True)[:400]
            break

    return snippet, dept, date


def _scrape_type(
    session: requests.Session,
    type_id: str,
    listing_url: str,
    doc_type: str,
    default_subjects: list,
    cache: set[str],
    existing: dict[str, dict],
) -> list[Document]:
    """Henter alle nye dokumenter for én dokumenttype."""
    new_docs: list[Document] = []
    start = 0

    for page_num in range(MAX_PAGES_PER_TYPE):
        print(f"  Side {page_num + 1} (offset {start})...", end=" ", flush=True)
        items, has_more = _scrape_list_page(session, listing_url, start)
        print(f"{len(items)} lenker", flush=True)

        if not items:
            break

        new_on_page = 0
        for item in items:
            url = item["url"]
            if url in cache or url in existing:
                continue
            # Hent detaljer for nye dokumenter
            snippet, dept, date = _fetch_detail(session, url)
            title = item["title"]
            new_docs.append(Document(
                url=url,
                doc_type=doc_type,
                title=title,
                date=date or item["date"],
                department=dept or item["department"],
                doc_number=item["doc_number"],
                snippet=snippet,
                subjects=list(default_subjects),
            ))
            new_on_page += 1

        if not has_more or new_on_page == 0:
            # Stopp når vi treffer bare kjente dokumenter
            break
        start += PAGE_SIZE

    return new_docs


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
                existing[d["url"]] = d

    all_new: list[Document] = []

    for type_id, listing_url, doc_type, default_subjects in DOC_TYPES:
        print(f"\n📋 {doc_type.upper()} — {listing_url}", flush=True)
        new_docs = _scrape_type(
            session, type_id, listing_url, doc_type,
            default_subjects, cache, existing,
        )
        print(f"  {len(new_docs)} nye {doc_type}-dokumenter", flush=True)
        all_new.extend(new_docs)

    print(f"\nTotalt: {len(all_new)} nye dokumenter", flush=True)

    if not all_new:
        print("Ingen nye dokumenter — ferdig.", flush=True)
        return

    # Slå sammen eksisterende + nye
    all_docs = list(existing.values()) + [asdict(d) for d in all_new]
    with gzip.open(OUT_PATH, "wt", encoding="utf-8") as f:
        for doc in all_docs:
            f.write(json.dumps(doc, ensure_ascii=False) + "\n")

    new_ids = cache | {d.url for d in all_new}
    _save_cache(new_ids)
    print(f"Lagret {len(all_docs)} dokumenter totalt i {OUT_PATH.name}", flush=True)


if __name__ == "__main__":
    main()
