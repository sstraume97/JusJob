"""Henter rettsområde-metadata fra sondreskarsten/norwegian-laws.

Laster ned hele repoet som ZIP (én nedlasting), parser YAML frontmatter
fra lover/*.md, og bygger en oppslagstabell refid → rettsomrade[].

Kjøres FØR lovdata.py slik at lovdata.py kan berike parsede lover med
rettsområde-felt fra den autoritative taksonomikilden.

Output: data/norwegian_laws_index.json
  { "lov/2005-06-17-62": ["Arbeidsrett", "HMS og beredskaps- og sikkerhetsrett"], ... }
"""
from __future__ import annotations

import io
import json
import re
import zipfile
from pathlib import Path

import requests

REPO_ZIP_URL = "https://github.com/sondreskarsten/norwegian-laws/archive/refs/heads/main.zip"
USER_AGENT = "JusJob-DataPipeline/0.1 (+https://github.com/sstraume97/JusJob)"

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
INDEX_FILE = DATA_DIR / "norwegian_laws_index.json"

# Matcher "  - Arbeidsrett>Underkategori" eller "  - Arbeidsrett"
_RETTSOMRADE_ITEM_RE = re.compile(r"^\s+-\s+(.+)$")
_FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
_REFID_RE = re.compile(r"^refid:\s*(.+)$", re.MULTILINE)


def _parse_rettsomrade_block(yaml_text: str) -> list[str]:
    """Parser rettsomrade-blokken fra YAML frontmatter.

    Returnerer unike toppnivå-rettsområder (teksten FØR '>').
    Eksempel:
      rettsomrade:
        - Arbeidsrett>Ansettelse. Avskjed. Oppsigelse
        - HMS og beredskaps- og sikkerhetsrett>HMT
      → ["Arbeidsrett", "HMS og beredskaps- og sikkerhetsrett"]
    """
    # Finn rettsomrade-blokken: alt fra "rettsomrade:" til neste felt (linje uten innrykk)
    block_m = re.search(r"^rettsomrade:\s*\n((?:\s+-[^\n]+\n?)+)", yaml_text, re.MULTILINE)
    if not block_m:
        return []

    seen: set[str] = set()
    result: list[str] = []
    for line in block_m.group(1).splitlines():
        m = _RETTSOMRADE_ITEM_RE.match(line)
        if m:
            full = m.group(1).strip()
            # Toppnivå er teksten før '>'
            top = full.split(">")[0].strip()
            if top and top not in seen:
                seen.add(top)
                result.append(top)
    return result


def _parse_md_file(content: str) -> tuple[str, list[str]] | None:
    """Returnerer (refid, [rettsomrade, ...]) eller None hvis ikke parsbart."""
    fm_m = _FRONTMATTER_RE.match(content)
    if not fm_m:
        return None
    yaml_text = fm_m.group(1)

    refid_m = _REFID_RE.search(yaml_text)
    if not refid_m:
        return None
    refid = refid_m.group(1).strip()

    subjects = _parse_rettsomrade_block(yaml_text)
    return refid, subjects


def build_index(session: requests.Session) -> dict[str, list[str]]:
    """Last ned norsk-lover ZIP, parser frontmatter, returner oppslagstabell."""
    print(f"Laster ned norwegian-laws repo fra {REPO_ZIP_URL} ...", flush=True)
    resp = session.get(REPO_ZIP_URL, timeout=120, stream=True)
    resp.raise_for_status()
    print("  Nedlasting fullført — parser Markdown-filer ...", flush=True)

    index: dict[str, list[str]] = {}
    with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
        md_files = [n for n in zf.namelist() if re.search(r"/lover/[^/]+\.md$", n)]
        print(f"  {len(md_files)} lovfiler funnet", flush=True)
        for name in md_files:
            with zf.open(name) as f:
                text = f.read().decode("utf-8", errors="replace")
            result = _parse_md_file(text)
            if result:
                refid, subjects = result
                index[refid] = subjects

    print(f"  {len(index)} lover med rettsområde-data", flush=True)
    return index


def main() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT

    index = build_index(session)
    INDEX_FILE.write_text(json.dumps(index, ensure_ascii=False, indent=None), encoding="utf-8")
    print(f"Skrev {len(index)} oppslag til {INDEX_FILE.name}", flush=True)


def load_index() -> dict[str, list[str]]:
    """Hjelpefunksjon: les ferdig bygget indeks fra disk (brukes av lovdata.py)."""
    if not INDEX_FILE.exists():
        return {}
    return json.loads(INDEX_FILE.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
