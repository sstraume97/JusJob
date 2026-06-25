"""Henter offentlige dokumenter fra KUDOS (DFØ) via åpent REST API.

KUDOS inneholder ~44 000 offentlige dokumenter fra norske statlige virksomheter:
NOU-er, kartlegginger, studier, statusrapporter, evalueringer m.m.

API: https://kudos.dfo.no/apne-data
Base-URL: https://kudos.dfo.no/api/v0
Ingen autentisering. Maks 180 req/min (standard), 2 req/min (CSV).

Inkrementell: bruker publish_date til å oppdage nye dokumenter.
"""
from __future__ import annotations

import gzip
import json
import os
import time
from dataclasses import dataclass, asdict
from pathlib import Path

import requests

BASE_URL = "https://kudos.dfo.no/api/v0"
USER_AGENT = "JusJob-DataPipeline/0.1 (+https://github.com/sstraume97/JusJob)"
DELAY_SECONDS = 0.4          # godt under 180 req/min-grensen
MAX_NEW_PAGES = int(os.environ.get("KUDOS_MAX_PAGES", "0"))  # 0 = ubegrenset


@dataclass
class Document:
    uuid: str
    type: str
    title: str
    abstract: str | None
    language: str | None
    publish_date: str | None
    url: str | None
    owners: str | None      # kommaseparert liste over eiere


def _session() -> requests.Session:
    s = requests.Session()
    s.headers["User-Agent"] = USER_AGENT
    return s


def _get(session: requests.Session, url: str, **params) -> dict:
    for attempt in range(5):
        try:
            resp = session.get(url, params=params, timeout=30)
            resp.raise_for_status()
            time.sleep(DELAY_SECONDS)
            return resp.json()
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            if attempt == 4:
                raise
            wait = 10 * 2 ** attempt
            print(f"  Nettverksfeil (forsøk {attempt+1}/5), venter {wait}s: {e}", flush=True)
            time.sleep(wait)


def _parse(doc: dict) -> Document:
    owners = doc.get("owners") or []
    owner_names = ", ".join(
        o.get("name", "") for o in owners if o.get("name")
    ) or None

    files = doc.get("files") or []
    url = doc.get("external_public_url") or None
    if not url and files:
        url = files[0].get("url") or None

    return Document(
        uuid=doc["uuid"],
        type=doc.get("type") or "Ukjent",
        title=doc.get("title") or "",
        abstract=(doc.get("abstract") or "")[:300] or None,
        language=doc.get("language") or None,
        publish_date=doc.get("publish_date") or None,
        url=url,
        owners=owner_names,
    )


def iter_documents(existing_uuids: set[str]) -> iter:
    session = _session()
    page = 1
    fetched = 0
    skipped = 0

    while True:
        data = _get(session, f"{BASE_URL}/documents", page=page)
        meta = data.get("meta", {})
        last_page = meta.get("last_page", 1)
        docs = data.get("data", [])

        print(f"\r  Side {page}/{last_page} ({len(existing_uuids) + fetched} totalt)", end="", flush=True)

        all_cached = True
        for doc in docs:
            uuid = doc.get("uuid")
            if not uuid:
                continue
            if uuid in existing_uuids:
                skipped += 1
            else:
                all_cached = False
                yield _parse(doc)
                fetched += 1

        if page >= last_page:
            break

        if MAX_NEW_PAGES and fetched >= MAX_NEW_PAGES:
            break

        # Hvis alle på denne siden var cachet, og vi sorterer nyeste først,
        # kan vi stoppe tidlig (alt eldre er også cachet)
        if all_cached and existing_uuids:
            print(f"\n  Alle på side {page} er cachet — stopper tidlig", flush=True)
            break

        page += 1

    print(flush=True)
    print(f"  Hentet {fetched} nye, {skipped} uendrede gjenbrukt", flush=True)


def _load_existing(path: Path) -> dict[str, Document]:
    if not path.exists():
        return {}
    existing = {}
    with gzip.open(path, "rt", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                d = json.loads(line)
                existing[d["uuid"]] = Document(**d)
    return existing


def main() -> None:
    out_path = Path(__file__).resolve().parent.parent / "data" / "kudos.jsonl.gz"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    print("=" * 50, flush=True)
    print("JusJob — henter dokumenter fra KUDOS (DFØ)", flush=True)
    print("=" * 50, flush=True)

    existing = _load_existing(out_path)
    print(f"  {len(existing)} dokumenter i cache", flush=True)

    all_docs = list(existing.values())
    existing_uuids = set(existing.keys())

    for doc in iter_documents(existing_uuids):
        all_docs.append(doc)

    with gzip.open(out_path, "wt", encoding="utf-8") as f:
        for d in all_docs:
            f.write(json.dumps(asdict(d), ensure_ascii=False) + "\n")

    print(f"Ferdig: {len(all_docs)} dokumenter totalt i {out_path.name}", flush=True)


if __name__ == "__main__":
    main()
