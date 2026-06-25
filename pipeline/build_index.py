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


def _kudos_entries():
    for d in _read_jsonl_gz(DATA_DIR / "kudos.jsonl.gz"):
        yield {
            "id": f"kudos-{d['uuid']}",
            "source": "kudos.dfo.no",
            "type": d["type"],
            "title": d["title"],
            "court_or_body": d["owners"] or "Ukjent virksomhet",
            "url": d["url"] or "",
            "snippet": d["abstract"] or "",
        }


def _lovdata_entries(filename: str, source_label: str):
    for d in _read_jsonl_gz(DATA_DIR / filename):
        entry = {
            "id": f"lovdata-{d['doc_id'].replace('/', '-')}",
            "source": "lovdata.no",
            "type": d.get("type", "lov"),
            "title": d["title"],
            "court_or_body": d.get("ministry") or "Lovdata",
            "url": d["url"],
            "snippet": d.get("snippet") or d.get("short_title") or "",
            "eli": d.get("eli") or "",
        }
        subjects = d.get("subjects")
        if subjects:
            entry["subjects"] = subjects
        yield entry


def _lovdata_lover_entries():
    yield from _lovdata_entries("lovdata-lover.jsonl.gz", "Gjeldende lover")


def _lovdata_forskrifter_entries():
    yield from _lovdata_entries("lovdata-forskrifter.jsonl.gz", "Sentrale forskrifter")


def _lovdata_lovtiend1_entries():
    yield from _lovdata_entries("lovdata-lovtiend1.jsonl.gz", "Norsk Lovtiend avd. 1")


def _lovdata_lovtiend2_entries():
    yield from _lovdata_entries("lovdata-lovtiend2.jsonl.gz", "Norsk Lovtiend avd. 2")


def _forbrukertilsynet_entries():
    for d in _read_jsonl_gz(DATA_DIR / "forbrukertilsynet.jsonl.gz"):
        yield {
            "id": f"forbrukertilsynet-{d['ref_id']}",
            "source": "forbrukertilsynet.no",
            "type": d.get("type") or "vedtak",
            "title": d["title"],
            "court_or_body": "Forbrukertilsynet",
            "url": d["url"],
            "snippet": d.get("snippet") or "",
        }


def _datatilsynet_entries():
    for d in _read_jsonl_gz(DATA_DIR / "datatilsynet.jsonl.gz"):
        entry = {
            "id": f"datatilsynet-{d['url'].rstrip('/').split('/')[-1]}",
            "source": "datatilsynet.no",
            "type": d.get("doc_type") or "vedtak",
            "title": d["title"],
            "court_or_body": "Datatilsynet",
            "url": d["url"],
            "snippet": d.get("snippet") or "",
        }
        if d.get("subjects"):
            entry["subjects"] = d["subjects"]
        yield entry


def _helsetilsynet_entries():
    for d in _read_jsonl_gz(DATA_DIR / "helsetilsynet.jsonl.gz"):
        entry = {
            "id": f"helsetilsynet-{d['url'].rstrip('/').split('/')[-1]}",
            "source": "helsetilsynet.no",
            "type": d.get("doc_type") or "rapport",
            "title": d["title"],
            "court_or_body": "Helsetilsynet",
            "url": d["url"],
            "snippet": d.get("snippet") or "",
        }
        if d.get("subjects"):
            entry["subjects"] = d["subjects"]
        yield entry


def _une_entries():
    for d in _read_jsonl_gz(DATA_DIR / "une.jsonl.gz"):
        title = d["title"]
        if d.get("tema"):
            title = f"{title} – {d['tema']}"
        entry = {
            "id": f"une-{d['url'].rstrip('/').split('/')[-1]}",
            "source": "une.no",
            "type": d.get("doc_type") or "praksisnotat",
            "title": title,
            "court_or_body": "Utlendingsnemnda",
            "url": d["url"],
            "snippet": d.get("snippet") or "",
        }
        if d.get("subjects"):
            entry["subjects"] = d["subjects"]
        yield entry


def _kofa_entries():
    for d in _read_jsonl_gz(DATA_DIR / "kofa.jsonl.gz"):
        entry = {
            "id": f"kofa-{d.get('case_number') or d['url'].rstrip('/').split('/')[-1]}",
            "source": "kofa.no",
            "type": "vedtak",
            "title": d["title"],
            "court_or_body": "KOFA",
            "url": d["url"],
            "snippet": d.get("snippet") or "",
        }
        if d.get("subjects"):
            entry["subjects"] = d["subjects"]
        yield entry


def _konkurransetilsynet_entries():
    for d in _read_jsonl_gz(DATA_DIR / "konkurransetilsynet.jsonl.gz"):
        entry = {
            "id": f"ktil-{d['url'].rstrip('/').split('/')[-1]}",
            "source": "konkurransetilsynet.no",
            "type": d.get("doc_type") or "vedtak",
            "title": d["title"],
            "court_or_body": "Konkurransetilsynet",
            "url": d["url"],
            "snippet": d.get("snippet") or "",
        }
        if d.get("subjects"):
            entry["subjects"] = d["subjects"]
        yield entry


def _finanstilsynet_entries():
    for d in _read_jsonl_gz(DATA_DIR / "finanstilsynet.jsonl.gz"):
        entry = {
            "id": f"finanstilsynet-{d['url'].rstrip('/').split('/')[-1]}",
            "source": "finanstilsynet.no",
            "type": d.get("doc_type") or "vedtak",
            "title": d["title"],
            "court_or_body": "Finanstilsynet",
            "url": d["url"],
            "snippet": d.get("snippet") or "",
        }
        if d.get("subjects"):
            entry["subjects"] = d["subjects"]
        yield entry


def _skatteklagenemnda_entries():
    for d in _read_jsonl_gz(DATA_DIR / "skatteklagenemnda.jsonl.gz"):
        entry = {
            "id": f"skn-{d.get('case_ref') or d['url'].rstrip('/').split('/')[-1]}",
            "source": "skatteklagenemnda.no",
            "type": "vedtak",
            "title": d["title"],
            "court_or_body": "Skatteklagenemnda",
            "url": d["url"],
            "snippet": d.get("snippet") or "",
        }
        if d.get("subjects"):
            entry["subjects"] = d["subjects"]
        yield entry


def _regjeringen_entries():
    for d in _read_jsonl_gz(DATA_DIR / "regjeringen.jsonl.gz"):
        entry = {
            "id": f"regjeringen-{d['url'].rstrip('/').split('/')[-1]}",
            "source": "regjeringen.no",
            "type": d.get("doc_type") or "dokument",
            "title": d["title"],
            "court_or_body": d.get("department") or "Regjeringen",
            "url": d["url"],
            "snippet": d.get("snippet") or "",
            "doc_number": d.get("doc_number") or "",
        }
        subjects = d.get("subjects")
        if subjects:
            entry["subjects"] = subjects
        yield entry


SOURCE_BUILDERS = [
    _rettspraksis_entries,
    _stortinget_entries,
    _sivilombudet_entries,
    _kudos_entries,
    _lovdata_lover_entries,
    _lovdata_forskrifter_entries,
    _lovdata_lovtiend1_entries,
    _lovdata_lovtiend2_entries,
    _forbrukertilsynet_entries,
    _datatilsynet_entries,
    _helsetilsynet_entries,
    _une_entries,
    _kofa_entries,
    _konkurransetilsynet_entries,
    _finanstilsynet_entries,
    _skatteklagenemnda_entries,
    _regjeringen_entries,
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
