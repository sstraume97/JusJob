"""Henter rettsavgjørelser fra rettspraksis.no (MediaWiki, CC-lisensiert).

Går gjennom Kategori:Rettsavgjørelser -> underkategorier (Høyesterett,
Lagmannsretter, Tingretter) og henter sidetekst + metadata for hver dom.

Inkrementell og batch-optimalisert:
- Kategorimedlemskap og revisjons-id hentes alltid i bulk (billige kall).
- Sidetekst hentes i batch på 50 sider per API-kall (MediaWiki-grensen), så
  bootstrapping av 60k+ sider tar ~15 min i stedet for ~8 timer.
- Kun sider med endret revid siden forrige kjøring trenger nye kall.
- MAX_NEW_PAGES (env-variabel, 0 = ubegrenset) begrenser antall nye
  innholdshentinger per kjøring for den daglige cron-jobben.
"""
from __future__ import annotations

import os
import time
from dataclasses import dataclass, asdict
from typing import Iterator

import requests

API_URL = "https://www.rettspraksis.no/w/api.php"
USER_AGENT = "JusJob-DataPipeline/0.1 (+https://github.com/sstraume97/JusJob)"
DECISION_SUBCATEGORIES = {"Kategori:Høyesterett", "Kategori:Lagmannsretter", "Kategori:Tingretter"}
CONTENT_DELAY_SECONDS = 2.0   # mellom batch-kall med sideinnhold (tunge kall)
INFO_DELAY_SECONDS = 0.1      # mellom billige revinfo/kategorikall
REVINFO_BATCH_SIZE = 50       # MediaWikis maks — revinfo er lett metadata
CONTENT_BATCH_SIZE = 10       # mindre batch for innhold pga. store responser


SNIPPET_LENGTH = 300  # lagrer kun de første tegnene av sideteksten

@dataclass
class Decision:
    page_id: int
    title: str
    court: str
    revid: int
    snippet: str          # første SNIPPET_LENGTH tegn av wikitext
    url: str


def _api_get(session: requests.Session, delay: float = INFO_DELAY_SECONDS, **params) -> dict:
    params.setdefault("format", "json")
    for attempt in range(5):
        try:
            resp = session.get(API_URL, params=params, timeout=60)
            resp.raise_for_status()
            time.sleep(delay)
            return resp.json()
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            if attempt == 4:
                raise
            wait = 10 * 2 ** attempt  # 10, 20, 40, 80 sekunder
            print(f"  Timeout/feil (forsøk {attempt+1}/5), venter {wait}s: {e}", flush=True)
            time.sleep(wait)


def _category_members(session: requests.Session, category: str) -> Iterator[dict]:
    cont = None
    while True:
        params = {
            "action": "query", "list": "categorymembers",
            "cmtitle": category, "cmlimit": 100,
        }
        if cont:
            params["cmcontinue"] = cont
        data = _api_get(session, **params)
        yield from data["query"]["categorymembers"]
        cont = data.get("continue", {}).get("cmcontinue")
        if not cont:
            break


def _pages_revinfo(session: requests.Session, titles: list[str], label: str = "") -> dict[str, int]:
    """Henter siste revisjons-id for opp til mange titler – ingen sideinnhold."""
    result: dict[str, int] = {}
    total = len(titles)
    for i in range(0, total, REVINFO_BATCH_SIZE):
        batch = titles[i : i + REVINFO_BATCH_SIZE]
        data = _api_get(session, action="query", prop="info", titles="|".join(batch))
        for page in data["query"]["pages"].values():
            if "lastrevid" in page:
                result[page["title"]] = page["lastrevid"]
        done = min(i + REVINFO_BATCH_SIZE, total)
        print(f"\r  [{label}] Sjekker revisjoner: {done}/{total} ({100*done//total}%)", end="", flush=True)
    print(flush=True)
    return result


def _pages_snippet_batch(session: requests.Session, titles: list[str]) -> dict[str, str]:
    """Henter første SNIPPET_LENGTH tegn av wikitext for opp til BATCH_SIZE titler."""
    data = _api_get(
        session,
        delay=CONTENT_DELAY_SECONDS,
        action="query",
        prop="revisions",
        rvprop="content",
        rvslots="main",
        titles="|".join(titles),
    )
    result: dict[str, str] = {}
    for page in data["query"]["pages"].values():
        title = page["title"]
        revisions = page.get("revisions")
        if not revisions:
            continue
        wikitext = revisions[0]["slots"]["main"]["*"]
        result[title] = wikitext[:SNIPPET_LENGTH]
    return result


def iter_decisions(
    existing: dict[int, Decision] | None = None,
    max_new_pages: int = 0,
) -> Iterator[Decision]:
    """Yter Decision for alle sider i kategoriene.

    Eksisterende sider med uendret revid returneres direkte fra `existing`
    uten API-kall. Nye/endrede sider hentes i batch (50 om gangen).
    max_new_pages: maks antall nye/endrede sider som hentes per kjøring
                   (0 = ubegrenset).
    """
    existing = existing or {}
    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT

    fetched_new = 0

    for subcategory in DECISION_SUBCATEGORIES:
        if max_new_pages and fetched_new >= max_new_pages:
            break

        court = subcategory.removeprefix("Kategori:")
        print(f"\n=== {court} ===", flush=True)
        print(f"  Henter sideliste ...", end="", flush=True)
        members = [m for m in _category_members(session, subcategory) if m["ns"] == 0]
        print(f" {len(members)} sider funnet", flush=True)
        revinfo = _pages_revinfo(session, [m["title"] for m in members], label=court)

        # Yield cached pages umiddelbart
        needs_fetch: list[dict] = []
        for member in members:
            cached = existing.get(member["pageid"])
            current_revid = revinfo.get(member["title"])
            if cached is not None and current_revid is not None and cached.revid == current_revid:
                yield cached
            else:
                needs_fetch.append(member)

        # Begrens antall nye hentinger
        if max_new_pages:
            remaining = max_new_pages - fetched_new
            needs_fetch = needs_fetch[:remaining]

        # Batch-hent snippet for nye/endrede sider
        total_needs = len(needs_fetch)
        cached_count = len(members) - total_needs
        print(f"  {cached_count} uendrede (gjenbrukes), {total_needs} nye/endrede hentes", flush=True)
        for i in range(0, total_needs, CONTENT_BATCH_SIZE):
            batch = needs_fetch[i : i + CONTENT_BATCH_SIZE]
            title_map = {m["title"]: m for m in batch}
            snippet_map = _pages_snippet_batch(session, list(title_map.keys()))
            for title, snippet in snippet_map.items():
                member = title_map[title]
                yield Decision(
                    page_id=member["pageid"],
                    title=title,
                    court=court,
                    revid=revinfo.get(title, 0),
                    snippet=snippet,
                    url=f"https://www.rettspraksis.no/wiki/{title.replace(' ', '_')}",
                )
            fetched_new += len(snippet_map)
            done = min(i + CONTENT_BATCH_SIZE, total_needs)
            print(f"\r  [{court}] Henter innhold: {done}/{total_needs} ({100*done//total_needs if total_needs else 0}%)", end="", flush=True)

        print(flush=True)
        print(f"  {court} ferdig: {len(members)} sider totalt", flush=True)


def _load_existing(path) -> dict[int, Decision]:
    import json, gzip

    if not path.exists():
        return {}
    existing: dict[int, Decision] = {}
    with gzip.open(path, "rt", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                d = json.loads(line)
                existing[d["page_id"]] = Decision(**d)
    return existing


def main() -> None:
    import json, gzip
    from pathlib import Path

    max_new = int(os.environ.get("MAX_NEW_PAGES", "0"))
    print("=" * 50, flush=True)
    print("JusJob — henter rettsavgjørelser fra rettspraksis.no", flush=True)
    print(f"Kategorier: {', '.join(c.removeprefix('Kategori:') for c in DECISION_SUBCATEGORIES)}", flush=True)
    if max_new:
        print(f"Maks nye sider denne kjøringen: {max_new}")
    else:
        print("Maks nye sider: ubegrenset (full bootstrap)")
    print("=" * 50, flush=True)

    out_path = Path(__file__).resolve().parent.parent / "data" / "rettspraksis.jsonl.gz"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    existing = _load_existing(out_path)
    decisions: list[Decision] = []
    reused = refetched = 0

    for decision in iter_decisions(existing, max_new_pages=max_new):
        decisions.append(decision)
        if existing.get(decision.page_id) is decision:
            reused += 1
        else:
            refetched += 1

    with gzip.open(out_path, "wt", encoding="utf-8") as f:
        for d in decisions:
            f.write(json.dumps(asdict(d), ensure_ascii=False) + "\n")

    print(
        f"Ferdig: {len(decisions)} avgjørelser totalt "
        f"({reused} gjenbrukt, {refetched} nye/endrede hentet)"
    )


if __name__ == "__main__":
    main()