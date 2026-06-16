"""Henter rettsavgjørelser fra rettspraksis.no (MediaWiki, CC-lisensiert).

Går gjennom Kategori:Rettsavgjørelser -> underkategorier (Høyesterett,
Lagmannsretter, Tingretter) og henter sidetekst + metadata for hver dom.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, asdict
from typing import Iterator

import requests

API_URL = "https://www.rettspraksis.no/w/api.php"
USER_AGENT = "JusJob-DataPipeline/0.1 (+https://github.com/<din-bruker>/jusjob-data)"
ROOT_CATEGORY = "Kategori:Rettsavgjørelser"
DECISION_SUBCATEGORIES = {"Kategori:Høyesterett", "Kategori:Lagmannsretter", "Kategori:Tingretter"}
REQUEST_DELAY_SECONDS = 0.5  # vær skånsom mot kilden


@dataclass
class Decision:
    page_id: int
    title: str
    court: str
    wikitext: str
    categories: list[str]
    url: str


def _api_get(session: requests.Session, **params) -> dict:
    params.setdefault("format", "json")
    resp = session.get(API_URL, params=params, timeout=30)
    resp.raise_for_status()
    time.sleep(REQUEST_DELAY_SECONDS)
    return resp.json()


def _category_members(session: requests.Session, category: str) -> Iterator[dict]:
    cont = None
    while True:
        params = {"action": "query", "list": "categorymembers", "cmtitle": category, "cmlimit": 100}
        if cont:
            params["cmcontinue"] = cont
        data = _api_get(session, **params)
        yield from data["query"]["categorymembers"]
        cont = data.get("continue", {}).get("cmcontinue")
        if not cont:
            break


def _page_wikitext(session: requests.Session, title: str) -> tuple[str, list[str]]:
    data = _api_get(
        session,
        action="query",
        prop="revisions|categories",
        rvprop="content",
        rvslots="main",
        titles=title,
    )
    pages = data["query"]["pages"]
    page = next(iter(pages.values()))
    revision = page["revisions"][0]
    wikitext = revision["slots"]["main"]["*"]
    categories = [c["title"] for c in page.get("categories", [])]
    return wikitext, categories


def iter_decisions() -> Iterator[Decision]:
    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT

    for subcategory in DECISION_SUBCATEGORIES:
        court = subcategory.removeprefix("Kategori:")
        for member in _category_members(session, subcategory):
            if member["ns"] != 0:
                continue  # hopp over under-underkategorier
            title = member["title"]
            wikitext, categories = _page_wikitext(session, title)
            yield Decision(
                page_id=member["pageid"],
                title=title,
                court=court,
                wikitext=wikitext,
                categories=categories,
                url=f"https://www.rettspraksis.no/wiki/{title.replace(' ', '_')}",
            )


def main() -> None:
    import json
    import gzip
    from pathlib import Path

    out_path = Path(__file__).resolve().parent.parent / "data" / "rettspraksis.jsonl.gz"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    count = 0
    with gzip.open(out_path, "wt", encoding="utf-8") as f:
        for decision in iter_decisions():
            f.write(json.dumps(asdict(decision), ensure_ascii=False) + "\n")
            count += 1
    print(f"Skrev {count} avgjørelser til {out_path}")


if __name__ == "__main__":
    main()
