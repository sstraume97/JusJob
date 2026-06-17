# JusJob

Et verktøy for juridisk research som henter og indekserer norske rettskilder automatisk, og gjør dem søkbare direkte inni Zotero.

Prosjektet består av to deler:

- **Datapipeline** (`pipeline/`) — Python-skript som henter data fra ulike rettskilder, kjøres automatisk via GitHub Actions og publiserer resultatet til GitHub Pages
- **Zotero-plugin** (`plugin/`) — en utvidelse for Zotero 7 som søker i den publiserte indeksen og lar deg importere treff som Zotero-items

---

## Arkitektur

```
GitHub Actions (daglig cron)
        │
        ▼
pipeline/rettspraksis.py    ──► data/rettspraksis.jsonl.gz
pipeline/stortinget.py      ──► data/stortinget.jsonl.gz
pipeline/sivilombudet.py    ──► data/sivilombudet.jsonl.gz
        │
        ▼
pipeline/build_index.py     ──► data/search-index.json
        │
        ▼
GitHub Pages  (https://sstraume97.github.io/JusJob/search-index.json)
        │
        ▼
Zotero-plugin søker i search-index.json
```

Alle data-filer committes til repoet og publiseres som statiske filer via GitHub Pages. Zotero-pluginen henter `search-index.json` over HTTPS og søker client-side — ingen server å drifte.

---

## Kilder

| Kilde | Type rettskilder | Status | Metode |
|---|---|---|---|
| [rettspraksis.no](https://www.rettspraksis.no) | Rettsavgjørelser (Høyesterett, lagmannsretter, tingretter) | ✅ Implementert | MediaWiki API (`/w/api.php`), CC-lisens |
| [Stortinget](https://data.stortinget.no) | Saker, forarbeider, vedtak (Prop., Innst., Dok. 8 m.m.) | ✅ Implementert | Offisielt XML-API |
| [Sivilombudet](https://www.sivilombudet.no) | Uttalelser | ✅ Implementert | HTML-skraping via sitemap.xml |
| Lovdata (gratis) | Lover og forskrifter | ⏳ Ikke startet | NLOD 2.0 åpne data |
| Regjeringen.no | NOU-er, høringer, rundskriv | ⏳ Ikke startet | HTML-skraping |
| Helsetilsynet / Riksrevisjonen | Tilsynsrapporter, riksrevisjonsrapporter | ⏳ Ikke startet | HTML-skraping |

---

## Datapipeline i detalj

### Inkrementell henting

Ingen scraper henter alt fra bunnen av ved hver kjøring. I stedet lagres tilstandsinformasjon i data-filene mellom kjøringer:

- **rettspraksis.no**: MediaWiki-APIet brukes til å hente revisjons-ID (`lastrevid`) for alle sider i batch (50 sider per API-kall). Sideinnhold hentes kun for sider der revisjons-ID har endret seg siden forrige kjøring.
- **Sivilombudet**: Sitemap-filene (`uttalelser-sitemap.xml`, `uttalelser-sitemap2.xml`) inneholder `<lastmod>`-tidspunkt for hver uttalelse. HTML hentes kun for sider med nyere `lastmod` enn det som er lagret.
- **Stortinget**: Henter alle saker per sesjon fra det offisielle XML-APIet. Kjøres for de fem siste sesjonene.

Den daglige cron-jobben er begrenset til `MAX_NEW_PAGES=2000` nye sider fra rettspraksis.no per kjøring, slik at den holder seg godt under en time. Bootstrapping (første gangs full henting) gjøres via en separat manuell workflow.

### Søkeindeksen

`pipeline/build_index.py` slår sammen alle kilde-filer til én `search-index.json`. Hvert element har disse feltene:

```json
{
  "id":           "rettspraksis-192647",
  "source":       "rettspraksis.no",
  "type":         "rettsavgjørelse",
  "title":        "HR-1815-1",
  "court_or_body": "Høyesterett",
  "url":          "https://www.rettspraksis.no/wiki/HR-1815-1",
  "snippet":      "Første 300 tegn av sideteksten …"
}
```

Alle kildetyper konverteres til dette felles formatet, slik at Zotero-pluginen kan søke og vise treff uavhengig av hvilken kilde de kommer fra.

### Filstørrelser

Rådata lagres som komprimerte JSONL-filer (`.jsonl.gz`). Kun metadata og et kort tekstutdrag (snippet) lagres — ikke fulltekst — for å holde filene under GitHubs 100 MB-grense:

| Fil | Innhold |
|---|---|
| `data/rettspraksis.jsonl.gz` | ~60 000 rettsavgjørelser med tittel, domstol, revisjons-ID, snippet og URL |
| `data/stortinget.jsonl.gz` | ~3 000–4 000 saker per sesjon × 5 sesjoner |
| `data/sivilombudet.jsonl.gz` | ~1 950 uttalelser med saksnummer, dato, sammendrag og URL |
| `data/search-index.json` | Alle kilder slått sammen til ett søkbart JSON-array |

---

## GitHub Actions-workflows

| Workflow | Trigger | Hva den gjør |
|---|---|---|
| `update.yml` | Daglig kl. 03:00 UTC + manuelt | Kjører alle skraperne (maks 2 000 nye rettspraksis-sider), bygger indeks, committer data og publiserer til Pages |
| `bootstrap-rettspraksis.yml` | Manuelt | Henter alle sider fra rettspraksis.no uten begrensning — kjøres én gang for å etablere den første fullstendige databasen |

---

## Zotero-plugin

Pluginen er et skjelett og er **ikke ferdig testet**. Se [`plugin/README.md`](plugin/README.md) for status og instruksjoner for å teste i Zotero.

Kort om hva den gjør:
- Legger til "Søk i rettskilder (JusJob)…" under Verktøy-menyen i Zotero
- Åpner et søkevindu som henter `search-index.json` fra GitHub Pages
- Lar deg søke på tittel, domstol og tekstutdrag
- Importerer valgte treff som Zotero-items (bruker Zoteros innebygde "Case"-type for rettsavgjørelser)

---

## Kjøre lokalt

```bash
pip install -r requirements.txt

python pipeline/stortinget.py     # skriver data/stortinget.jsonl.gz
python pipeline/sivilombudet.py   # skriver data/sivilombudet.jsonl.gz
python pipeline/rettspraksis.py   # skriver data/rettspraksis.jsonl.gz  (tar ~15 min første gang)
python pipeline/build_index.py    # skriver data/search-index.json
```

Miljøvariabelen `MAX_NEW_PAGES` begrenser antall nye sider rettspraksis-scraperen henter. Sett den til f.eks. `500` for en rask test:

```bash
MAX_NEW_PAGES=500 python pipeline/rettspraksis.py
```

---

## Sette opp GitHub Pages (én gang)

1. Gå til **Settings → Pages** i dette repoet
2. Under "Build and deployment" → Source: velg **GitHub Actions**
3. Kjør `bootstrap-rettspraksis.yml` manuelt én gang via Actions-fanen
4. Deretter kjører `update.yml` daglig automatisk
