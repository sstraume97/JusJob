"""Slår sammen alle kildedatafiler i data/ til én søkeindeks (search-index.json).

Zotero-pluginen henter denne ene filen og søker client-side i den, i stedet
for å laste hver enkelt .jsonl.gz-kilde selv.

Hvert element i indeksen har et minimumssett med felter som er felles for
alle kildetyper, slik at pluginen kan vise og filtrere uavhengig av kilde:
  - id, source, type, title, date, court_or_body, url, snippet
"""
from __future__ import annotations

import gzip
import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _read_jsonl_gz(path: Path):
    if not path.exists():
        return
    with gzip.open(path, "rt", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


def _rettspraksis_entries():
    for d in _read_jsonl_gz(DATA_DIR / "rettspraksis.jsonl.gz"):
        yield {
            "id": f"rettspraksis-{d['page_id']}",
            "source": "rettspraksis.no",
            "type": "rettsavgjørelse",
            "title": d["title"],
            "court_or_body": d["court"],
            "url": d["url"],
            "snippet": d["snippet"],
        }


def _stortinget_entries():
    for d in _read_jsonl_gz(DATA_DIR / "stortinget.jsonl.gz"):
        yield {
            "id": f"stortinget-{d['id']}",
            "source": "stortinget.no",
            "type": d["dokumentgruppe"] or d["type"],
            "title": d["tittel"],
            "court_or_body": d["komite"] or "Stortinget",
            "url": f"https://www.stortinget.no/no/Saker-og-publikasjoner/Saker/Sak/?p={d['id']}",
            "snippet": d["henvisning"],
        }


def _sivilombudet_entries():
    for d in _read_jsonl_gz(DATA_DIR / "sivilombudet.jsonl.gz"):
        yield {
            "id": f"sivilombudet-{d['case_number'] or d['url']}",
            "source": "sivilombudet.no",
            "type": "uttalelse",
            "title": d["title"],
            "court_or_body": "Sivilombudet",
            "url": d["url"],
            "snippet": d["summary"] or d["body"][:300],
        }


SOURCE_BUILDERS = [
    _rettspraksis_entries,
    _stortinget_entries,
    _sivilombudet_entries,
]


def main() -> None:
    index = []
    for builder in SOURCE_BUILDERS:
        index.extend(builder())

    out_path = DATA_DIR / "search-index.json"
    out_path.write_text(json.dumps(index, ensure_ascii=False, indent=0), encoding="utf-8")
    print(f"Skrev {len(index)} elementer til {out_path}")


if __name__ == "__main__":
    main()
