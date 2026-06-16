"""Henter rettsavgjørelser fra rettspraksis.no (MediaWiki, CC-lisensiert).

Går gjennom Kategori:Rettsavgjørelser -> underkategorier (Høyesterett,
Lagmannsretter, Tingretter) og henter sidetekst + metadata for hver dom.

Inkrementell: kategorimedlemskap + revisjons-info hentes alltid (billig,
batch-spørringer uten innhold), men selve sidetekst (wikitext) hentes kun
for sider som er nye eller har en annen lastrevid enn det vi allerede har
lagret fra forrige kjøring. Det gjør at en daglig kjøring i praksis kun
laster ned innholdet til sider som faktisk er endret siden i går, i stedet
for å hente alt fra bunnen hver gang.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, asdict
from typing import Iterator

import requests

API_URL = "https://www.rettspraksis.no/w/api.php"
USER_AGENT = "JusJob-DataPipeline/0.1 (+https://github.com/sstraume97/JusJob)"
ROOT_CATEGORY = "Kategori:Rettsavgjørelser"
DECISION_SUBCATEGORIES = {"Kategori:Høyesterett", "Kategori:Lagmannsretter", "Kategori:Tingretter"}
REQUEST_DELAY_SECONDS = 0.5  # vær skånsom mot kilden
INFO_BATCH_SIZE = 50  # MediaWiki sin standardgrense for antall titler per spørring


@dataclass
class Decision:
    page_id: int
    title: str
    court: str
    revid: int
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


def _batched(items: list, size: int) -> Iterator[list]:
    for i in range(0, len(items), size):
        yield items[i : i + size]


def _pages_revinfo(session: requests.Session, titles: list[str]) -> dict[str, int]:
    """Henter kun siste revisjons-id for en liste titler -- ingen sideinnhold."""
    result: dict[str, int] = {}
    for batch in _batched(titles, INFO_BATCH_SIZE):
        data = _api_get(session, action="query", prop="info", titles="|".join(batch))
        for page in data["query"]["pages"].values():
            if "lastrevid" in page:
                result[page["title"]] = page["lastrevid"]
    return result


def iter_decisions(existing: dict[int, Decision] | None = None) -> Iterator[Decision]:
    """Yter Decision for hver side i kategoriene.

    Sider som finnes i `existing` med samme revid gjenbrukes uten nytt
    innholdskall. Resten (nye sider eller endrede revid) hentes på nytt.
    """
    existing = existing or {}
    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT

    for subcategory in DECISION_SUBCATEGORIES:
        court = subcategory.removeprefix("Kategori:")
        members = [m for m in _category_members(session, subcategory) if m["ns"] == 0]
        revinfo = _pages_revinfo(session, [m["title"] for m in members])

        for member in members:
            title = member["title"]
            page_id = member["pageid"]
            current_revid = revinfo.get(title)
            cached = existing.get(page_id)

            if cached is not None and current_revid is not None and cached.revid == current_revid:
                yield cached
                continue

            wikitext, categories = _page_wikitext(session, title)
            yield Decision(
                page_id=page_id,
                title=title,
                court=court,
                revid=current_revid or 0,
                wikitext=wikitext,
                categories=categories,
                url=f"https://www.rettspraksis.no/wiki/{title.replace(' ', '_')}",
            )


def _load_existing(path) -> dict[int, Decision]:
    import json
    import gzip

    if not path.exists():
        return {}
    existing: dict[int, Decision] = {}
    with gzip.open(path, "rt", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            existing[d["page_id"]] = Decision(**d)
    return existing


def main() -> None:
    import json
    import gzip
    from pathlib import Path

    out_path = Path(__file__).resolve().parent.parent / "data" / "rettspraksis.jsonl.gz"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    existing = _load_existing(out_path)
    reused, refetched = 0, 0
    decisions: list[Decision] = []
    for decision in iter_decisions(existing):
        decisions.append(decision)
        if existing.get(decision.page_id) is decision:
            reused += 1
        else:
            refetched += 1

    with gzip.open(out_path, "wt", encoding="utf-8") as f:
        for decision in decisions:
            f.write(json.dumps(asdict(decision), ensure_ascii=False) + "\n")

    print(
        f"Skrev {len(decisions)} avgjørelser til {out_path} "
        f"({reused} gjenbrukt fra forrige kjøring, {refetched} nye/endrede hentet på nytt)"
    )


if __name__ == "__main__":
    main()
