"""Henter avgjørelser fra KFIR — Klagenemnda for industrielle rettigheter.

KFIR behandler klager på Patentstyrets avgjørelser (patent, varemerke, design).

Scraper:
  https://www.kfir.no/avgjorelser/

Rettsområde: Immaterialrett
Output: data/kfir.jsonl.gz
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

BASE = "https://www.kfir.no"
USER_AGENT = "JusJob-DataPipeline/0.1 (+https://github.com/sstraume97/JusJob)"
DELAY = 1.2

LIST_URLS = [
    f"{BASE}/avgjorelser/",
    f"{BASE}/avgjørelser/",   # norsk tegnsett-variant
]

SUBJECTS = ["Immaterialrett"]

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
OUT_PATH = DATA_DIR / "kfir.jsonl.gz"
CACHE_FILE = DATA_DIR / "kfir_cache.json"


@dataclass
class Document:
    url: str
    doc_type: str
    title: str
    date: str
    case_number: str
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
    CACHE_FILE.write_text(json.dumps(sorted(seen), ensure_ascii=False, indent=2), encoding="utf-8")


def _get(session: requests.Session, url: str) -> BeautifulSoup | None:
    for attempt in range(4):
        try:
            r = session.get(url, timeout=30)
            if r.status_code == 404:
                return None
            r.raise_for_status()
            time.sleep(DELAY)
            return BeautifulSoup(r.text, "html.parser")
        except Exception as e:
            if attempt == 3:
                print(f"  FEIL ved {url}: {e}", flush=True)
                return None
            time.sleep(5 * (attempt + 1))
    return None


def _extract_case_number(text: str, url: str) -> str:
    # KFIR-saker: typisk "kfir-YYYY-NNN" eller "Patent YYYY-NNN"
    m = re.search(r"KFIR[- ]\d{4}[- ]\d+|\d{4}[/-]\d{3,4}", text + " " + url, re.I)
    return m.group(0) if m else url.rstrip("/").split("/")[-1][:50]


def _scrape_list(session: requests.Session, list_url: str) -> list[dict]:
    items = []
    seen = set()
    url = list_url
    page = 0

    while url and page < 150:
        soup = _get(session, url)
        if not soup:
            break
        page += 1
        found = 0

        for a in soup.find_all("a", href=True):
            href = a["href"]
            text = a.get_text(strip=True)
            if not text or len(text) < 4:
                continue
            full = href if href.startswith("http") else BASE + href
            if full in seen or not full.startswith(BASE):
                continue
            if full.rstrip("/") == list_url.rstrip("/"):
                continue
            if not re.search(r"/avgjor|/\d{4}[/-]|kfir", full, re.I):
                continue
            seen.add(full)
            found += 1
            parent_text = a.parent.get_text(" ", strip=True) if a.parent else ""
            date_m = re.search(r"\d{1,2}\.\d{1,2}\.\d{4}|\d{4}-\d{2}-\d{2}", parent_text)
            case_number = _extract_case_number(text + " " + parent_text, full)
            items.append({
                "url": full, "title": text,
                "date": date_m.group(0) if date_m else "",
                "case_number": case_number,
            })

        if found == 0:
            break
        neste = soup.find("a", string=re.compile(r"neste|next|›|»", re.I))
        if not neste:
            neste = soup.find("a", href=re.compile(r"[?&](page|side)=\d+"))
        if neste and neste.get("href"):
            next_url = neste["href"]
            next_full = next_url if next_url.startswith("http") else BASE + next_url
            if next_full != url:
                url = next_full
                continue
        break

    return items


def _fetch_snippet(session: requests.Session, url: str) -> tuple[str, str]:
    soup = _get(session, url)
    if not soup:
        return "", ""
    date = ""
    time_el = soup.find("time")
    if time_el:
        date = time_el.get("datetime", time_el.get_text(strip=True))[:10]
    snippet = ""
    for sel in [".ingress", ".lead", ".article-body", "article", "main"]:
        el = soup.select_one(sel)
        if el:
            snippet = el.get_text(" ", strip=True)[:400]
            break
    return snippet, date


def main() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    session = _session()
    cache = _load_cache()

    existing: dict[str, dict] = {}
    if OUT_PATH.exists():
        with gzip.open(OUT_PATH, "rt", encoding="utf-8") as f:
            for line in f:
                d = json.loads(line.strip())
                existing[d["url"]] = d

    all_new: list[Document] = []

    for list_url in LIST_URLS:
        print(f"\n📋 KFIR — {list_url}", flush=True)
        items = _scrape_list(session, list_url)
        if not items:
            continue
        print(f"  {len(items)} avgjørelser funnet", flush=True)
        new_count = 0
        for item in items:
            url = item["url"]
            if url in cache or url in existing:
                continue
            snippet, date = _fetch_snippet(session, url)
            all_new.append(Document(
                url=url, doc_type="avgjørelse", title=item["title"],
                date=date or item["date"], case_number=item["case_number"],
                snippet=snippet, subjects=list(SUBJECTS),
            ))
            new_count += 1
        print(f"  {new_count} nye", flush=True)
        break  # Stopp etter første fungerende URL

    print(f"\nTotalt {len(all_new)} nye", flush=True)
    if not all_new:
        print("Ingen nye — ferdig.", flush=True)
        return

    all_docs = list(existing.values()) + [asdict(d) for d in all_new]
    with gzip.open(OUT_PATH, "wt", encoding="utf-8") as f:
        for doc in all_docs:
            f.write(json.dumps(doc, ensure_ascii=False) + "\n")
    _save_cache(cache | {d.url for d in all_new})
    print(f"Lagret {len(all_docs)} dokumenter i {OUT_PATH.name}", flush=True)


if __name__ == "__main__":
    main()
