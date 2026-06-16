# JusJob – data

Datapipeline som henter norske rettskilder fra kilder uten egnet API, og
publiserer dem som statiske JSON-filer via GitHub Pages. JusJob
Zotero-pluginen søker mot denne statiske "API"-en.

## Kilder

| Kilde | Status | Metode |
|---|---|---|
| rettspraksis.no | ✅ implementert (inkrementell) | MediaWiki API (`/w/api.php`), CC-lisens |
| Stortinget | ✅ implementert | Offisielt API (data.stortinget.no), XML |
| Sivilombudet | ✅ implementert (inkrementell) | Skraping via sitemap.xml + lastmod |
| Lovdata (lover/forskrifter) | ⏳ ikke startet | NLOD 2.0 åpne data |
| Regjeringen.no | ⏳ ikke startet | Skraping |
| Helsetilsynet / Riksrevisjonen | ⏳ ikke startet | Skraping |

## Kjøre lokalt

```bash
pip install -r requirements.txt
python pipeline/rettspraksis.py   # skriver data/rettspraksis.jsonl.gz
python pipeline/stortinget.py     # skriver data/stortinget.jsonl.gz
python pipeline/sivilombudet.py   # skriver data/sivilombudet.jsonl.gz
python pipeline/build_index.py    # skriver data/search-index.json
```

## Arkitektur

GitHub Actions (`.github/workflows/update.yml`) kjører pipelinen daglig,
committer rådata til `data/`, og publiserer mappen til GitHub Pages slik at
`search-index.json` blir tilgjengelig på en stabil URL for pluginen.

## Kjent begrensning

Begge skraperne er nå inkrementelle: `rettspraksis.py` henter kun
revisjons-id i bulk (billig) og laster bare ned sideinnhold for nye/endrede
sider; `sivilombudet.py` bruker `lastmod` fra sitemap.xml på samme måte. Det
betyr at *førstegangs*-kjøringen fortsatt er tung (revinfo for 40 000+ sider
i Høyesterett-kategorien alene tar i størrelsesorden 10–15 minutter), men
alle senere kjøringer i praksis kun behandler det som faktisk er endret.
Output-filene (`data/*.jsonl.gz`) må derfor committes til repoet mellom
kjøringer for at gjenbruken skal fungere — det gjør allerede
`update.yml`-workflowen.
