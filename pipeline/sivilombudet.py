"""Henter uttalelser fra Sivilombudet (sivilombudet.no).

Ingen offentlig API -- bruker WordPress/Yoast sine sitemaps
(uttalelser-sitemap.xml, uttalelser-sitemap2.xml) for å finne alle URL-er
samt deres lastmod-tidspunkt. Inkrementell på samme måte som
pipeline/rettspraksis.py: en side hentes kun på nytt hvis lastmod fra
sitemap er nyere enn det vi har lagret fra forrige kjøring.

Vær skånsom mot kilden: REQUEST_DELAY_SECONDS mellom hver sidehenting.
"""
from __future__ import annotations

import re
import time
from dataclasses import dataclass, asdict
from typing import Iterator

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.sivilombudet.no"
SITEMAP_URLS = [
    f"{BASE_URL}/uttalelser-sitemap.xml",
    f"{BASE_URL}/uttalelser-sitemap2.xml",
]
USER_AGENT = "JusJob-DataPipeline/0.1 (+https://github.com/sstraume97/JusJob)"
REQUEST_DELAY_SECONDS = 1.0


@dataclass
class Statement:
    url: str
    lastmod: str
    title: str
    case_number: str | None
    published: str | None
    updated: str | None
    summary: str | None
    body: str


def _sitemap_entries(session: requests.Session) -> Iterator[tuple[str, str]]:
    """Returnerer (url, lastmod) for hver uttalelse-side, hoppet over selve indekssiden."""
    for sitemap_url in SITEMAP_URLS:
        resp = session.get(sitemap_url, timeout=30)
        resp.raise_for_status()
        locs = re.findall(r"<loc>(.*?)</loc>", resp.text)
        lastmods = re.findall(r"<lastmod>(.*?)</lastmod>", resp.text)
        for url, lastmod in zip(locs, lastmods):
            if url.rstrip("/") == f"{BASE_URL}/uttalelser":
                continue  # selve listesiden, ikke en enkeltuttalelse
            yield url, lastmod


def _parse_statement(html: str, url: str, lastmod: str) -> Statement:
    soup = BeautifulSoup(html, "html.parser")

    title_elem = soup.select_one("h1.article-h1")
    title = title_elem.get_text(strip=True) if title_elem else url

    case_number = None
    case_number_elem = soup.select_one(".post-meta-field.case-number")
    if case_number_elem and case_number_elem.get("data-case-number"):
        case_number = case_number_elem["data-case-number"].split(",")[0].strip()

    published = updated = None
    for p in soup.select(".post-date p"):
        text = p.get_text(strip=True)
        if text.startswith("Publisert:"):
            published = text.removeprefix("Publisert:").strip()
        elif text.startswith("Sist oppdatert:"):
            updated = text.removeprefix("Sist oppdatert:").strip()

    summary_elem = soup.select_one("section.summary .text-content")
    summary = summary_elem.get_text(" ", strip=True) if summary_elem else None

    body_elem = soup.select_one(".article-body")
    body = body_elem.get_text("\n", strip=True) if body_elem else ""

    return Statement(
        url=url,
        lastmod=lastmod,
        title=title,
        case_number=case_number,
        published=published,
        updated=updated,
        summary=summary,
        body=body,
    )


def iter_statements(existing: dict[str, Statement] | None = None) -> Iterator[Statement]:
    existing = existing or {}
    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT

    for url, lastmod in _sitemap_entries(session):
        cached = existing.get(url)
        if cached is not None and cached.lastmod == lastmod:
            yield cached
            continue

        resp = session.get(url, timeout=30)
        resp.raise_for_status()
        time.sleep(REQUEST_DELAY_SECONDS)
        yield _parse_statement(resp.text, url, lastmod)


def _load_existing(path) -> dict[str, Statement]:
    import json
    import gzip

    if not path.exists():
        return {}
    existing: dict[str, Statement] = {}
    with gzip.open(path, "rt", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            existing[d["url"]] = Statement(**d)
    return existing


def main() -> None:
    import json
    import gzip
    from pathlib import Path

    out_path = Path(__file__).resolve().parent.parent / "data" / "sivilombudet.jsonl.gz"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    existing = _load_existing(out_path)
    reused, refetched = 0, 0
    statements: list[Statement] = []
    for statement in iter_statements(existing):
        statements.append(statement)
        if existing.get(statement.url) is statement:
            reused += 1
        else:
            refetched += 1

    with gzip.open(out_path, "wt", encoding="utf-8") as f:
        for statement in statements:
            f.write(json.dumps(asdict(statement), ensure_ascii=False) + "\n")

    print(
        f"Skrev {len(statements)} uttalelser til {out_path} "
        f"({reused} gjenbrukt, {refetched} nye/endrede hentet på nytt)"
    )


if __name__ == "__main__":
    main()
