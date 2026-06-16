# JusJob – data

Datapipeline som henter norske rettskilder fra kilder uten egnet API, og
publiserer dem som statiske JSON-filer via GitHub Pages. JusJob
Zotero-pluginen søker mot denne statiske "API"-en.

## Kilder

| Kilde | Status | Metode |
|---|---|---|
| rettspraksis.no | ✅ implementert | MediaWiki API (`/w/api.php`), CC-lisens |
| Stortinget | 🚧 stub | Offisielt API (data.stortinget.no) |
| Sivilombudet | 🚧 stub | Skraping (ingen API) |
| Lovdata (lover/forskrifter) | ⏳ ikke startet | NLOD 2.0 åpne data |
| Regjeringen.no | ⏳ ikke startet | Skraping |
| Helsetilsynet / Riksrevisjonen | ⏳ ikke startet | Skraping |

## Kjøre lokalt

```bash
pip install -r requirements.txt
python pipeline/rettspraksis.py   # skriver data/rettspraksis.jsonl.gz
python pipeline/build_index.py    # skriver data/search-index.json
```

## Arkitektur

GitHub Actions (`.github/workflows/update.yml`) kjører pipelinen daglig,
committer rådata til `data/`, og publiserer mappen til GitHub Pages slik at
`search-index.json` blir tilgjengelig på en stabil URL for pluginen.
