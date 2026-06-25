"""Delte hjelpefunksjoner for HTML-baserte tilsyns-/nemnd-scrapere.

Brukes av de nyere scraperne (helsedirektoratet, trygderetten, npe, osv.)
for å unngå duplisering av session-, cache- og henteoppsett. De eldre
scraperne (datatilsynet, kofa, ...) har egne kopier av disse og endres ikke.
"""
from __future__ import annotations

import gzip
import json
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

USER_AGENT = "JusJob-DataPipeline/0.1 (+https://github.com/sstraume97/JusJob)"
DEFAULT_DELAY = 1.2

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def make_session() -> requests.Session:
    s = requests.Session()
    s.headers["User-Agent"] = USER_AGENT
    return s


def load_cache(cache_file: Path) -> set[str]:
    if cache_file.exists():
        return set(json.loads(cache_file.read_text(encoding="utf-8")))
    return set()


def save_cache(cache_file: Path, seen: set[str]) -> None:
    cache_file.write_text(json.dumps(sorted(seen), ensure_ascii=False, indent=2), encoding="utf-8")


def get_soup(session: requests.Session, url: str, delay: float = DEFAULT_DELAY) -> BeautifulSoup | None:
    """Hent en side med retry og 404-håndtering. Returnerer None ved feil/404."""
    for attempt in range(4):
        try:
            r = session.get(url, timeout=30)
            if r.status_code == 404:
                return None
            r.raise_for_status()
            time.sleep(delay)
            return BeautifulSoup(r.text, "html.parser")
        except Exception as e:
            if attempt == 3:
                print(f"  FEIL ved {url}: {e}", flush=True)
                return None
            time.sleep(5 * (attempt + 1))
    return None


def load_existing(out_path: Path, key: str = "url") -> dict[str, dict]:
    existing: dict[str, dict] = {}
    if out_path.exists():
        with gzip.open(out_path, "rt", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    d = json.loads(line)
                    existing[d[key]] = d
    return existing


def write_jsonl_gz(out_path: Path, docs: list[dict]) -> None:
    with gzip.open(out_path, "wt", encoding="utf-8") as f:
        for doc in docs:
            f.write(json.dumps(doc, ensure_ascii=False) + "\n")
