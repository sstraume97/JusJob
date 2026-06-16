"""Henter saker fra Stortingets offisielle API (data.stortinget.no).

API gir kun XML. Henvisning-feltet ("Dokument 12:13 (2023-2024), Innst. 87 S
(2025-2026)") gir oss kjeden Dokument/Prop. -> Innst. -> vedtak/lov, som er
nyttig for "forarbeidskjede"-funksjonen i pluginen senere.

Dokumentasjon: https://data.stortinget.no/dokumentasjon-og-hjelp/saker/
"""
from __future__ import annotations

import time
from dataclasses import dataclass, asdict
from typing import Iterator
from xml.etree import ElementTree as ET

import requests

BASE_URL = "https://data.stortinget.no/eksport/saker"
USER_AGENT = "JusJob-DataPipeline/0.1 (+https://github.com/sstraume97/JusJob)"
REQUEST_DELAY_SECONDS = 0.5

XMLNS = "http://data.stortinget.no"


def _q(tag: str) -> str:
    return f"{{{XMLNS}}}{tag}"


@dataclass
class Sak:
    id: str
    sesjon: str
    type: str
    status: str
    dokumentgruppe: str
    tittel: str
    korttittel: str
    henvisning: str
    komite: str | None
    sist_oppdatert: str | None


def _text(elem: ET.Element, tag: str) -> str | None:
    child = elem.find(_q(tag))
    return child.text if child is not None else None


def _parse_sak(sak_elem: ET.Element, sesjon: str) -> Sak:
    komite_elem = sak_elem.find(_q("komite"))
    komite = _text(komite_elem, "navn") if komite_elem is not None else None
    return Sak(
        id=_text(sak_elem, "id") or "",
        sesjon=sesjon,
        type=_text(sak_elem, "type") or "",
        status=_text(sak_elem, "status") or "",
        dokumentgruppe=_text(sak_elem, "dokumentgruppe") or "",
        tittel=_text(sak_elem, "tittel") or "",
        korttittel=_text(sak_elem, "korttittel") or "",
        henvisning=_text(sak_elem, "henvisning") or "",
        komite=komite,
        sist_oppdatert=_text(sak_elem, "sist_oppdatert_dato"),
    )


def iter_saker(sesjoner: list[str]) -> Iterator[Sak]:
    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT

    for sesjon in sesjoner:
        resp = session.get(BASE_URL, params={"sesjonid": sesjon}, timeout=30)
        resp.raise_for_status()
        time.sleep(REQUEST_DELAY_SECONDS)
        root = ET.fromstring(resp.content)
        for sak_elem in root.findall(f"{_q('saker_liste')}/{_q('sak')}"):
            yield _parse_sak(sak_elem, sesjon)


def _default_sesjoner(antall: int = 5) -> list[str]:
    """Genererer de N siste stortingssesjonene, f.eks. ["2021-2022", ...]."""
    import datetime

    now = datetime.date.today()
    start_year = now.year if now.month >= 10 else now.year - 1
    return [f"{start_year - i}-{start_year - i + 1}" for i in range(antall)]


def main() -> None:
    import json
    import gzip
    from pathlib import Path

    sesjoner = _default_sesjoner()
    out_path = Path(__file__).resolve().parent.parent / "data" / "stortinget.jsonl.gz"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    count = 0
    with gzip.open(out_path, "wt", encoding="utf-8") as f:
        for sak in iter_saker(sesjoner):
            f.write(json.dumps(asdict(sak), ensure_ascii=False) + "\n")
            count += 1
    print(f"Skrev {count} saker til {out_path}")


if __name__ == "__main__":
    main()
