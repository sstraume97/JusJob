"""Henter kjennelser fra Trygderetten.

Trygderetten er en ankeinstans for trygde- og pensjonssaker. Kjennelser
publiseres på Lovdata, men Trygderetten publiserer også utvalgte avgjørelser.

Scraper:
  https://www.trygderetten.no/kjennelser/
  https://www.trygderetten.no/avgjorelser/

Rettsområde: Pensjons- og trygderett
Output: data/trygderetten.jsonl.gz
"""
from __future__ import annotations

import re
from dataclasses import asdict, dataclass

from _scraper_base import (
    DATA_DIR, get_soup, load_cache, load_existing, make_session, save_cache, write_jsonl_gz,
)

BASE = "https://www.trygderetten.no"

LIST_URLS = [
    f"{BASE}/kjennelser/",
    f"{BASE}/avgjorelser/",
    f"{BASE}/no/kjennelser/",
]

SUBJECTS = ["Pensjons-/trygderett"]

OUT_PATH = DATA_DIR / "trygderetten.jsonl.gz"
CACHE_FILE = DATA_DIR / "trygderetten_cache.json"


@dataclass
class Document:
    url: str
    doc_type: str
    title: str
    date: str
    case_number: str
    snippet: str
    subjects: list


def _extract_case_number(text: str) -> str:
    m = re.search(r"\bTR[- ]\d{4}[- ]\d+\b|\b\d{2}/\d{5}\b", text, re.I)
    return m.group(0) if m else ""


def _scrape_list(session, list_url: str) -> list[dict]:
    items, seen, url, page = [], set(), list_url, 0
    while url and page < 100:
        soup = get_soup(session, url)
        if not soup:
            break
        page += 1
        found = 0
        for a in soup.find_all("a", href=True):
            href, text = a["href"], a.get_text(strip=True)
            if not text or len(text) < 5:
                continue
            full = href if href.startswith("http") else BASE + href
            if full in seen or not full.startswith(BASE):
                continue
            if full.rstrip("/") == list_url.rstrip("/"):
                continue
            if not re.search(r"/kjennels|/avgjorel|/\d{4}[/-]", full, re.I):
                continue
            seen.add(full)
            found += 1
            parent_text = a.parent.get_text(" ", strip=True) if a.parent else ""
            date_m = re.search(r"\d{1,2}\.\d{1,2}\.\d{4}|\d{4}-\d{2}-\d{2}", parent_text)
            items.append({"url": full, "title": text,
                          "date": date_m.group(0) if date_m else "",
                          "case_number": _extract_case_number(text + " " + parent_text)})
        if found == 0:
            break
        neste = soup.find("a", string=re.compile(r"neste|next|›|»", re.I)) \
            or soup.find("a", href=re.compile(r"[?&](page|side)=\d+"))
        if neste and neste.get("href"):
            nxt = neste["href"]
            nxt_full = nxt if nxt.startswith("http") else BASE + nxt
            if nxt_full != url:
                url = nxt_full
                continue
        break
    return items


def _fetch_snippet(session, url: str) -> tuple[str, str]:
    soup = get_soup(session, url)
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
    session = make_session()
    cache = load_cache(CACHE_FILE)
    existing = load_existing(OUT_PATH)

    all_new: list[Document] = []
    for list_url in LIST_URLS:
        print(f"\n📋 Trygderetten — {list_url}", flush=True)
        items = _scrape_list(session, list_url)
        if not items:
            continue
        print(f"  {len(items)} kjennelser funnet", flush=True)
        new_count = 0
        for item in items:
            url = item["url"]
            if url in cache or url in existing:
                continue
            snippet, date = _fetch_snippet(session, url)
            all_new.append(Document(url=url, doc_type="kjennelse", title=item["title"],
                                    date=date or item["date"], case_number=item["case_number"],
                                    snippet=snippet, subjects=list(SUBJECTS)))
            new_count += 1
        print(f"  {new_count} nye", flush=True)

    print(f"\nTotalt {len(all_new)} nye", flush=True)
    if not all_new:
        print("Ingen nye — ferdig.", flush=True)
        return
    all_docs = list(existing.values()) + [asdict(d) for d in all_new]
    write_jsonl_gz(OUT_PATH, all_docs)
    save_cache(CACHE_FILE, cache | {d.url for d in all_new})
    print(f"Lagret {len(all_docs)} dokumenter i {OUT_PATH.name}", flush=True)


if __name__ == "__main__":
    main()
