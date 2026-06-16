# JusJob – data

Datapipeline som henter norske rettskilder fra kilder uten egnet API, og
publiserer dem som statiske JSON-filer via GitHub Pages. JusJob
Zotero-pluginen søker mot denne statiske "API"-en.

## Kilder

| Kilde | Status | Metode |
|---|---|---|
| rettspraksis.no | ✅ implementert | MediaWiki API (`/w/api.php`), CC-lisens |
| Stortinget | ✅ implementert | Offisielt API (data.stortinget.no), XML |
| Sivilombudet | 🚧 stub | Skraping (ingen API) |
| Lovdata (lover/forskrifter) | ⏳ ikke startet | NLOD 2.0 åpne data |
| Regjeringen.no | ⏳ ikke startet | Skraping |
| Helsetilsynet / Riksrevisjonen | ⏳ ikke startet | Skraping |

## Kjøre lokalt

```bash
pip install -r requirements.txt
python pipeline/rettspraksis.py   # skriver data/rettspraksis.jsonl.gz
python pipeline/stortinget.py     # skriver data/stortinget.jsonl.gz
python pipeline/build_index.py    # skriver data/search-index.json
```

## Arkitektur

GitHub Actions (`.github/workflows/update.yml`) kjører pipelinen daglig,
committer rådata til `data/`, og publiserer mappen til GitHub Pages slik at
`search-index.json` blir tilgjengelig på en stabil URL for pluginen.

## Kjent begrensning

`pipeline/rettspraksis.py` henter for øyeblikket *alle* sider i hver
underkategori (40 000+ for Høyesterett alene) hver gang den kjøres, med en
fast pause mellom hvert kall. Det er trygt mot kilden, men for tidkrevende
til daglig cron i denne formen. Før den daglige jobben skrus på i praksis bør
den gjøres inkrementell (kun hente nye/endrede sider siden forrige kjøring,
f.eks. via MediaWikis `recentchanges`-API).
