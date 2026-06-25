"""Henter uttalelser fra LDO og vedtak fra LDN.

LDO — Likestillings- og diskrimineringsombudet:
  https://www.ldo.no/uttalelser-og-avgjorelser/

LDN — Likestillings- og diskrimineringsnemnda:
  https://www.diskrimineringsnemnda.no/avgjorelser/

Rettsområde: Menneskerettigheter
Output: data/diskriminering.jsonl.gz
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

USER_AGENT = "JusJob-DataPipeline/0.1 (+https://github.com/sstraume97/JusJob)"
DELAY = 1.2

SOURCES = [
    (
        "ldo",
        "https://www.ldo.no",
        "https://www.ldo.no/uttalelser-og-avgjorelser/",
        "LDO-uttalelse",
        "Likestillings- og diskrimineringsombudet",
    ),
    (
        "ldn",
        "https://www.diskrimineringsnemnda.no",
        "https://www.diskrimineringsnemnda.no/avgjorelser/",
        "LDN-vedtak",
        "Diskrimineringsnemnda",
    ),
]

SUBJECTS = ["Menneskerettigheter"]

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
OUT_PATH = DATA_DIR / "diskriminering.jsonl.gz"
CACHE_FILE = DATA_DIR / "diskriminering_cache.json"


@dataclass
class Document:
    url: str
    doc_type: str
    title: str
    date: str
    body: str
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


def _scrape_list(session: requests.Session, base: str, list_url: str) -> list[dict]:
    items = []
    seen = set()
    url = list_url
    page = 0

    while url and page < 200:
        soup = _get(session, url)
        if not soup:
            break
        page += 1
        found = 0

        for a in soup.find_all("a", href=True):
            href = a["href"]
            text = a.get_text(strip=True)
            if not text or len(text) < 5:
                continue
            full = href if href.startswith("http") else base + href
            if full in seen or not full.startswith(base):
                continue
            if full.rstrip("/") == list_url.rstrip("/"):
                continue
            if not re.search(r"/\d{4}[/-]|/uttalels|/avgjorel|/vedtak|/sak", full, re.I):
                continue
            seen.add(full)
            found += 1
            parent_text = a.parent.get_text(" ", strip=True) if a.parent else ""
            date_m = re.search(r"\d{1,2}\.\d{1,2}\.\d{4}|\d{4}-\d{2}-\d{2}", parent_text)
            items.append({"url": full, "title": text, "date": date_m.group(0) if date_m else ""})

        if found == 0:
            break
        neste = soup.find("a", string=re.compile(r"neste|next|›|»", re.I))
        if not neste:
            neste = soup.find("a", href=re.compile(r"[?&](page|side)=\d+"))
        if neste and neste.get("href"):
            next_url = neste["href"]
            next_full = next_url if next_url.startswith("http") else base + next_url
            if next_full != url:
                url = next_full
                continue
        break

    return items


def _fetch_detail(session: requests.Session, url: str) -> tuple[str, str, str]:
    """Returnerer (snippet, body_short, date)."""
    soup = _get(session, url)
    if not soup:
        return "", "", ""
    date = ""
    time_el = soup.find("time")
    if time_el:
        date = time_el.get("datetime", time_el.get_text(strip=True))[:10]
    snippet = body = ""
    for sel in [".ingress", ".lead", ".article-lead"]:
        el = soup.select_one(sel)
        if el:
            snippet = el.get_text(" ", strip=True)[:300]
            break
    for sel in [".article-body", "article", "main"]:
        el = soup.select_one(sel)
        if el:
            body = el.get_text(" ", strip=True)[:800]
            break
    return snippet or body[:300], body, date


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

    for src_id, base, list_url, doc_type, body_name in SOURCES:
        print(f"\n📋 {body_name} — {list_url}", flush=True)
        items = _scrape_list(session, base, list_url)
        print(f"  {len(items)} lenker funnet", flush=True)
        new_count = 0
        for item in items:
            url = item["url"]
            if url in cache or url in existing:
                continue
            snippet, body, date = _fetch_detail(session, url)
            all_new.append(Document(
                url=url, doc_type=doc_type, title=item["title"],
                date=date or item["date"], body=body,
                snippet=snippet, subjects=list(SUBJECTS),
            ))
            new_count += 1
        print(f"  {new_count} nye", flush=True)

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
