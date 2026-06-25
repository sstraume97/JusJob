# Relaterte ressurser og referanserepoer

Vurdert 2026-06-25. Relevans og gjenbruksvurdering for JusJob.

---

## Relevansmatrise

| Repo | Relevans | Kategori | Gjenbruk |
|---|---|---|---|
| [NationalLibraryOfNorway/lovdata-public-conversion-script](https://github.com/NationalLibraryOfNorway/lovdata-public-conversion-script) | ⭐⭐⭐ Kritisk | Lovdata XML → JSONL | XPath-parser, JSONL-skjema — studer før lovdata.py ferdigstilles |
| [HNygard/lovdata-openapi-copy](https://github.com/HNygard/lovdata-openapi-copy) | ⭐⭐⭐ Høy | Lovdata pakkeliste | Bekrefter alle filnavn + OpenAPI-spec |
| [sstraume97/Rettskildesok](https://github.com/sstraume97/Rettskildesok) | ⭐⭐⭐ Høy | 65-kilde katalog | sources.js: autoritativ liste over alle norske rettskilder med URL-mønster |
| [sondreskarsten/norwegian-laws](https://github.com/sondreskarsten/norwegian-laws) | ⭐⭐⭐ Kritisk | Lovkilde | Konsumeres direkte som datakilde |
| [khjohns/paragraf-mcp](https://github.com/khjohns/paragraf-mcp) | ⭐⭐⭐ Høy | Lovdata-parser + MCP | XML-parser, alias-løser, søkelogikk |
| [bartoszkobylinski/lovspor](https://github.com/bartoszkobylinski/lovspor) | ⭐⭐⭐ Høy | Endringshistorikk + MCP | Endringshistorikk-mønster, MCP-verktøy |
| [Majac999/lov-radar-berekraft](https://github.com/Majac999/lov-radar-berekraft) | ⭐⭐⭐ Høy | Lovdata API + endringssporing | Fungerende `lovradar.py`: Lovdata API, diff-sporing, GHA |
| [Majac999/Lovsonar](https://github.com/Majac999/Lovsonar) | ⭐⭐⭐ Høy | Regulatorisk horisontskanning | `lovsonar.py`: Stortinget+reg.no RSS/API, SQLite, GHA |
| [aiantech/legal-sources /sources/NO](https://github.com/aiantech/legal-sources/tree/main/sources/NO) | ⭐⭐⭐ Høy | Kildekartlegging | Gapanalyse for norske rettskilder — direkte brukbar |
| [ngu-tek/Norwegian-law-mcp](https://github.com/ngu-tek/Norwegian-law-mcp) | ⭐⭐ God | MCP-server | MCP-arkitektur for Zotero-plugin |
| [StianOby/claude-legal-tools](https://github.com/StianOby/claude-legal-tools) | ⭐⭐ God | Lovdata API-ref | `api.lovdata.no` endepunkter |
| [worldwidelaw/legal-sources](https://github.com/worldwidelaw/legal-sources) | ⭐⭐ God | Arkitektur | Modulær pipeline-struktur |
| [willchen96/mike](https://github.com/willchen96/mike) | ⭐⭐ God | Sitatsjekk-arkitektur | CourtListener-mønster → adapteres for norske domstoler |
| [EULexNET/EULex.NET](https://github.com/EULexNET/EULex.NET) | ⭐⭐ God | EUR-Lex / ELI | .NET-referanse for ELI-integrasjon; bruk SPARQL direkte |
| [juss-ai/juss-ai.github.io](https://github.com/juss-ai/juss-ai.github.io) | ⭐⭐ God | Norsk legal AI | Les whitepaper manuelt — mulig overlap/inspirasjon |
| [einarra/lovdata-assistent](https://github.com/einarra/lovdata-assistent) | ⭐ Delvis | Lovdata+AI | Node.js Lovdata-integrasjon |
| [EivindKjosbakken/LegalShare](https://github.com/EivindKjosbakken/LegalShare) | ⭐ Delvis | Høyesterett-scraper | Pipeline-mønster for domstol.no |
| [KevinJohannesen/catchwise-backend](https://github.com/KevinJohannesen/catchwise-backend) | ⭐ Delvis | Søketeknologi | Norwegian-aware BM25-tokenisering |
| [doantumy/LegSum](https://github.com/doantumy/Efficiently-Summarizing-Norwegian-Legal-Texts) | ⭐ Delvis | ML/summering | Lovdata XML-struktur |
| [tullebulle/intellegal](https://github.com/tullebulle/intellegal) | ⭐ Delvis | Ukjent legal app | Inspiser Python-backend — mulig norsk kildedekning |
| [sondrele/etterlevelse](https://github.com/sondrele/etterlevelse) | ⭐ Delvis | NAV compliance-tracker | Loven→system-mapping som referansekatalog |
| [HNygard/sivilombudet-uttalelser](https://github.com/HNygard/sivilombudet-uttalelser) | ⭐⭐ God | Sivilombudet-data | 1000+ uttalelser JSON-datasett + skraperdesign |
| [HNygard/norsk-lovtidend](https://github.com/HNygard/norsk-lovtidend) | ⭐⭐ God | Lovtiend-arkiv | JSON/CSV med endringshistorikk + lisensavklaring |
| [digdir/nasjonal-arkitektur](https://github.com/digdir/nasjonal-arkitektur) | ⭐ Delvis | Digital arkitektur | Kartlegger autoritative datakilder i offentlig sektor |
| [GizzZmo/loven](https://github.com/GizzZmo/loven) | ⭐ Delvis | Lovdata søke-API | LovDataClient-mønster for api.lovdata.no søk |
| [ZachLaik/LegalFactory](https://github.com/ZachLaik/LegalFactory) | ⭐ Delvis | EU-scraper | Pipeline-arkitektur (YAML konfig, CI dry-run) |
| [HNygard/open-norwegian-law](https://github.com/HNygard/open-norwegian-law) | ⭐ Delvis | Java-lib (2022) | Utdatert, ikke portabel |
| [GmailHelene/rettbot](https://github.com/GmailHelene/rettbot) | – Ikke relevant | Kryptert PWA | Ingen gjenbrukbar kode |
| [HNygard/offpost](https://github.com/HNygard/offpost) | – Ikke relevant | E-post til offentlige | Ingen relevans |
| [openlegaldata/awesome-legal-data](https://github.com/openlegaldata/awesome-legal-data) | – Ikke relevant | Liste | Lite norsk dekning |
| [JoelNiklaus/LegalDatasets](https://github.com/JoelNiklaus/LegalDatasets) | – Ukjent | ML-datasett | Mulig norsk dekning ubekreftet |
| [fpvetleseter/mike](https://github.com/fpvetleseter/mike) | – Ikke relevant | Fork av mike | Ingen tillegg over upstream |
| [willchen96/openjuris-temp-landing-page](https://github.com/willchen96/openjuris-temp-landing-page) | – Ikke relevant | US legal landing page | Ingen kode, US-fokus |
| [suphiro-arch/NA-kunnskap](https://github.com/suphiro-arch/NA-kunnskap) | – Ikke relevant | IT-arkitektur | Ingen juridisk innhold |

---

## Detaljerte vurderinger

### [khjohns/paragraf-mcp](https://github.com/khjohns/paragraf-mcp)
**Relevans: ⭐⭐⭐ Høy — direkte gjenbrukbar kode**

MCP-server med 92 000+ paragrafer fra 773 lover + 3 673 forskrifter. PostgreSQL tsvector-søk (~6ms). Data fra `api.lovdata.no` (ZIP-filer med XML, NLOD 2.0).

**Gjenbrukbar kode:**

- **`structure_parser.py`** — Parser Lovdata-HTML til hierarkisk struktur (Del → Kapittel → Avsnitt → Paragraf). Finner `<section class="section">` og `<article class="legalArticle">`, matcher heading-typer med regex. Kan brukes direkte i vår `lovdata.py`-scraper.

- **`service.py` — `_resolve_id()`** — Fire-lags alias-løser: hardkodede forkortelser (45+ som "aml", "strl") → eksakt DB-match → fuzzy pg_trgm-match → passthrough. Relevant for sitatsjekk-funksjonen i Zotero-pluginen.

- **Felter vi bør adoptere:**
  ```python
  dok_id        # "LOV-1992-07-03-93"
  doc_type      # "lov" / "forskrift"
  is_current    # bool
  based_on      # referanselover (hjemmel)
  section_id    # "3-9"
  address       # "/kapittel/1/paragraf/1-1/"
  ```

- **`search()`-logikken** — AND-søk med automatisk fallback til OR når ingen treff. Inkluderer `ministry_filter`, `doc_type_filter`, `legal_area_filter`. Relevant for søkepanel i Zotero-plugin.

- **`find_related_regulations()`** — Finner forskrifter som siterer en gitt lov. Direkte relevant for lenking lov↔forskrift i `build_index.py`.

**Hva vi IKKE trenger:** Supabase/PostgreSQL-infrastrukturen (vi bruker JSONL/GitHub Pages), Flask-appen, embedding-generering (ikke nødvendig for søkeindeksen).

---

### [bartoszkobylinski/lovspor](https://github.com/bartoszkobylinski/lovspor)
**Relevans: ⭐⭐⭐ Høy — endringshistorikk-mønster**

Tracker for 4 522 norske lover/forskrifter. Git-basert historikk, 15 MCP-verktøy. Data fra Lovdata (daglig GitHub Actions, 04:00 UTC). MIT-lisens.

**Gjenbrukbar kode/mønstre:**

- **Datainnhentingsmønster** — Henter Lovdata-tarballer daglig via GitHub Actions, klassifiserer som ny/oppdatert/omdøpt/fjernet. Dette er nøyaktig det vi trenger for `endringshistorikk-varsling`-funksjonen.

- **Historikkstruktur** — `<dataset>/history/<slug>.json` med strukturert endringshistorikk per lov. Kan adapteres som tilleggsdata i vår `lovdata.jsonl.gz`.

- **MCP-verktøy vi bør implementere:**
  - `validate_citation` — valider at "Rt. 2013 s. 1170" er korrekt (anti-hallusinasjon)
  - `verify_quote` — verifiser at et sitat faktisk finnes i angitt paragraf
  - `list_recent_changes` / `get_law_history` — endringshistorikk
  - `semantic_search` / `search_body` — søk i lovtekst

- **Anti-hallusinasjon-lag** — fire-lags verifisering mot lovtekst. Viktig for sitatsjekk.

**Hva vi IKKE trenger:** Embedding-generering (Gemini), per-seksjons-embeddings (overkill for v1).

---

### [sondreskarsten/norwegian-laws](https://github.com/sondreskarsten/norwegian-laws)
**Relevans: ⭐⭐⭐ Kritisk — konsumeres direkte**

794 lover + 3 438 forskrifter, oppdatert daglig. Publisert som `laws.json` på GitHub Pages.

**Nøkkelfelter:**
```json
{
  "refid": "lov/1687-04-15",
  "eli":   "/eli/lov/1687/04/15",
  "tittel": "Kong Christian Den Femtis Norske Lov",
  "korttittel": "Norske Lov – NL",
  "forkortelse": "NL",
  "departement": "Justis- og beredskapsdepartementet",
  "rettsomrade": "Strafferett",
  "ikrafttredelse": "1687-04-15",
  "sist_endret": "lov/2023-06-16-40",
  "github": "https://github.com/sondreskarsten/norwegian-laws/blob/main/lover/lov-1687-04-15.md",
  "lovdata": "https://lovdata.no/dokument/NL/lov/1687-04-15"
}
```

**Gjenbruk:** Hent `laws.json` direkte i `pipeline/lovdata.py`. `eli`-feltet er koblingsnøkkelen mot Stortinget-saker og rettspraksis.

---

### [ngu-tek/Norwegian-law-mcp](https://github.com/ngu-tek/Norwegian-law-mcp)
**Relevans: ⭐⭐ God — MCP-arkitektur**

MCP-server for 3 400 lover + 25 301 forarbeider. Lovdata + Stortinget + EUR-Lex. BM25 i SQLite. Relevant som referanse for MCP-eksponering av JusJob-indeksen.

**Gjenbruk:** Arkitekturmønster for å eksponere `search-index.json` som MCP-server. Aktuelt når vi skal integrere med Claude/AI-assistenter.

---

### [EivindKjosbakken/LegalShare](https://github.com/EivindKjosbakken/LegalShare)
**Relevans: ⭐ Delvis**

Høyesterett-scraper → AWS Lambda → Pinecone. Interessant for domstol.no-scraping, men AWS-infrastruktur er irrelevant.

**Gjenbruk:** Scrapemønster for Høyesterett-avgjørelser kan adapteres for domstol.no. Se `/Scraping`-mappen.

---

### [einarra/lovdata-assistent](https://github.com/einarra/lovdata-assistent)
**Relevans: ⭐ Delvis**

Node.js/TypeScript fullstack med Lovdata API + OpenAI. Bekrefter at `https://api.lovdata.no` er korrekt base-URL. Stripe-abonnement og LangSmith er irrelevante.

**Gjenbruk:** Bekrefter API-adresse og autentiseringsmønster for Lovdata.

---

### [KevinJohannesen/catchwise-backend](https://github.com/KevinJohannesen/catchwise-backend)
**Relevans: ⭐ Delvis**

FastAPI + BM25 + RAG for norske juridiske dokumenter. "Norwegian-aware tokenization" for BM25.

**Gjenbruk:** Tokeniseringslogikk for norsk juridisk tekst ved evt. server-side søk. Ikke nødvendig nå (vi søker client-side).

---

### [doantumy/LegSum](https://github.com/doantumy/Efficiently-Summarizing-Norwegian-Legal-Texts)
**Relevans: ⭐ Delvis**

Automatisk summering av Høyesterettsavgjørelser. Lovdata XML-struktur: `<sammendrag>`, `<premiss>`, `<slutning>`.

**Gjenbruk:** XML-struktur for rettsavgjørelser bekrefter feltene vi bør hente (sammendrag, premiss, slutning). Relevant for utvidelse av rettspraksis-scraper.

---

### [Majac999/lov-radar-berekraft](https://github.com/Majac999/lov-radar-berekraft)
**Relevans: ⭐⭐⭐ Høy — fungerende Lovdata API-integrasjon**

Python-script (`lovradar.py`) med GitHub Actions som ukentlig overvåker norske lover og forskrifter relevant for byggematerialesektoren. Henter fra **Lovdata Public Data API** (NLOD 2.0), gjør diff-basert endringssporing mot cacht baseline-tekst, og genererer compliance-rapporter. To JSON-cacher (~198 KB og ~579 KB) bekrefter at pipelinen kjører i produksjon.

**Gjenbrukbar kode:**
- Fungerende Lovdata API-integrasjon under åpen lisens (NLOD 2.0) — det vi trenger for `pipeline/lovdata.py`
- Diff-basert endringssporing per lov — kjernen i planlagt `endringshistorikk-varsling`-funksjon
- GitHub Actions-oppsett med ukentlig kjøring og JSON-caching

**Hva vi IKKE trenger:** Domenefilter for byggematerialer — pipelinen er generisk.

---

### [Majac999/Lovsonar](https://github.com/Majac999/Lovsonar)
**Relevans: ⭐⭐⭐ Høy — regulatorisk horisontskanning**

Søsterprosjekt til lov-radar. `lovsonar.py` overvåker kommende norske og EU-reguleringer *før* de blir obligatoriske, ved å scanne stortingsproposisjoner, regjeringsdokumenter og EU Green Deal-kilder via API og RSS. Bruker aiohttp, SQLite og GitHub Actions. Genererer ukentlige JSON + Markdown-rapporter (bekreftet aktiv feb–jun 2026).

**Gjenbrukbar kode:**
- Stortinget + regjeringen.no RSS/API-scraping med nøkkelordfiltrering — direkte brukbart for vår `stortinget.py`-utvidelse
- SQLite-lagringsmodell for incremental fetching
- Horisontskanning (lovforslag som ikke er vedtatt ennå) — planlagt JusJob-funksjon vi ikke har ennå

---

### [aiantech/legal-sources — sources/NO](https://github.com/aiantech/legal-sources/tree/main/sources/NO)
**Relevans: ⭐⭐⭐ Høy — ferdig kildekartlegging**

Strukturert inventarrepo som katalogiserer norske juridiske datakilder per institusjon. `/sources/NO` har undermapper for: Høyesterett, Lagmannsrett, Lovdata, Stortinget, Trygderetten, Skatteetaten-Uttalelser, SKD (Skattedirektoratet), KONKURR (Konkurransetilsynet), DTIL.

**Gjenbruk:** Gapanalysen (hva er indeksert vs. hva mangler) er direkte handlingsbar for JusJobs veikart. Bekrefter vår kildeliste og avdekker mulige nye kilder: Trygderetten, KONKURR, SKD. Bør bidras tilbake til når vi har scrapere for de manglende kildene.

---

### [willchen96/mike](https://github.com/willchen96/mike)
**Relevans: ⭐⭐ God — sitatsjekk-arkitektur**

Fullstack juridisk dokumentassistent (Next.js + Express + Supabase) med **CourtListener API-integrasjon** for US-sitatverifisering. Tilsvarer nøyaktig det JusJob vil bygge for norske domstoler. Multi-LLM-abstraksjon (Claude, Gemini, OpenAI) er ren og gjenbrukbar.

**Gjenbruk:** CourtListener-mønsteret (API-oppslag → verifiser sitat → returnere bekreftelse/avvisning) adapteres for Høyesterett/rettspraksis.no-søk i vår sitatsjekk-funksjon.

---

### [EULexNET/EULex.NET](https://github.com/EULexNET/EULex.NET)
**Relevans: ⭐⭐ God — EUR-Lex / ELI-referanse**

Open-source .NET-bibliotek for programmatisk tilgang til EUR-Lex (EUs offisielle lovdatabase). EUR-Lex bruker ELI-URI-er nativt.

**Gjenbruk:** Referanseimplementasjon for ELI-basert EUR-Lex-spørring. For JusJobs Python-stack: bruk EUR-Lex SPARQL-endepunkt direkte (`https://publications.europa.eu/webapi/rdf/sparql`) med ELI-spørringer fremfor å portere dette .NET-biblioteket.

---

### [juss-ai/juss-ai.github.io](https://github.com/juss-ai/juss-ai.github.io)
**Relevans: ⭐⭐ God — norsk legal AI-plattform**

GitHub Pages-nettsted for Juss-AI med whitepaper (`JussaiWhitepaperV5.pdf`). Ingen kildekode for pipeline. Høy domeneoverlapp med JusJob.

**Anbefalt handling:** Last ned og les whitepaper manuelt for å vurdere om de har indeksert samme kilder, bruker kompatible dataformater, eller har fattet arkitekturbeslutninger JusJob kan lære av eller differensiere mot.

---

### [NationalLibraryOfNorway/lovdata-public-conversion-script](https://github.com/NationalLibraryOfNorway/lovdata-public-conversion-script)
**Relevans: ⭐⭐⭐ Kritisk — studer før lovdata.py ferdigstilles**

Offisielt Python-script fra Nasjonalbiblioteket som konverterer Lovdata XML → JSONL med lxml/XPath. Produsert av Stiftelsen Lovdata / Nasjonalbiblioteket.

**JSONL-skjema (alle felter):**
- `datokode` — dato-kode
- `dokumentID` — "NL/lov/2005-06-17-62"
- `departement` — ansvarlig departement
- `title` / `titleShort` — fulltittel og korttittel
- `fulltext` — innhold som tekstarray (seksjonsnivå)
- `lastChangeInForce` — ikrafttredelse av siste endring
- `lastupdated` — sist oppdatert

**Handling:** Tilpass XPath-logikken fra `convert_lovdata_xpath.py` til vår `pipeline/lovdata.py` for mer robust XML-parsing.

---

### [HNygard/lovdata-openapi-copy](https://github.com/HNygard/lovdata-openapi-copy)
**Relevans: ⭐⭐⭐ Høy — bekrefter faktiske filnavn**

Shell-downloader + kopi av Lovdata OpenAPI-spec og pakkeliste. Bekrefter at de faktiske filnavnene fra `api.lovdata.no/v1/publicData/list` er:

| Filnavn | Beskrivelse |
|---|---|
| `gjeldende-lover.tar.bz2` | Gjeldende lover, ajourført |
| `gjeldende-sentrale-forskrifter.tar.bz2` | **NB: ikke** `sentrale-forskrifter.tar.bz2` |
| `lovtidend-avd1-YYYY.tar.bz2` | Norsk Lovtidend avd. I (løpende år) |
| `lovtidend-avd1-2001-2024.tar.bz2` | **Historisk arkiv 2001–2024** (vi manglet denne!) |

**Merknad:** Avdeling 2 (lokale/private forskrifter) er *ikke* i det åpne API-et — kun avdeling 1. Vår `lovdata.py` er korrigert for riktige filnavn.

---

### [sstraume97/Rettskildesok](https://github.com/sstraume97/Rettskildesok)
**Relevans: ⭐⭐⭐ Høy — eget prosjekt, mulig frontend for JusJob**

Brukerens eget prosjekt: statisk søkeaggregator (GitHub Pages, Vanilla JS) som bygger Boolean-søkstrenger mot 65+ norske og internasjonale rettskilder via URL deep-linking. `js/sources.js` er den sentrale ressursen.

**Rettskildesok som mulig JusJob-frontend:**

Rettskildesok og JusJob er naturlige komplementer. I dag sender Rettskildesok brukeren videre til eksterne søkesider (URL deep-linking) — brukeren forlater tjenesten for hvert søk. JusJob bygger en lokal søkeindeks over de samme kildene. Disse to kan kombineres på minst to måter:

1. **Integrert frontend:** Rettskildesok kan bytte fra URL-dispatching til å søke i JusJobs `search-index.json` for de kildene JusJob har indeksert, og beholde URL-dispatching som fallback for resten. Resultatet: brukeren forblir i grensesnittet, ser faktiske dokumenter, og kan eksportere til Zotero.

2. **UX-inspirasjon for Zotero-plugin:** Rettskildesoks kildekataloger (8 kategorier, Boolean-søk, kilde-filtrering) er direkte relevant som UI-mønster for søkepanelet i Zotero-pluginen. Kategoriseringen (lovverk / forarbeider / domstolsinstanser / nemnder / EU-EØS) er juridisk velfundert og bør speiles i JusJobs kildefilter.

**Viktig:** `sources.js`-katalogen med 65 kilder brukes som autoritativ referanseliste for hvilke rettskilder JusJob bør dekke (se [docs/kilder.md](./kilder.md)).

**Hva som mangler i Rettskildesok som JusJob løser:**
- Ingen faktisk dokumenthenting — kun videresending
- Ingen offline-støtte / Zotero-integrasjon
- Ingen strukturert indeks med metadata (dato, instans, type, snippet)
- Ingen cross-source lenking via ELI-identifikatorer

**Alle 65 kilder fordelt på 8 kategorier i sources.js:**

*Lover og lovsamlinger (6):* Lovdata NL, SF, LTI, HIST, Norgeslover, SNL Jus

*Forarbeider og stortingsdokumenter (8):* Regjeringen NOU, Prop./Meld., Ot.prp., tolkningsuttalelser; Stortinget innst./saker og forhandlinger; KUDOS, Riksrevisjonen

*Domstolsinstanser (7):* Lovdata HR, lagmannsrett, tingrett, Arbeidsretten, Trygderetten; Høyesterett.no; rettspraksis.no

*Nemnder og tilsynsorganer (18):* Sivilombudet, KOFA, Skatteetaten, **Skatteklagenemnda**, Arbeidstilsynet, NAV, **UNE (Utlendingsnemnda)**, Diskrimineringsnemnda, Datatilsynet, **Finanstilsynet**, **Konkurransetilsynet**, Forbrukertilsynet, Forbrukerklageutvalget, **Nkom**, **NVE**, **Patentstyret**, **Statsforvalteren**, Lovdata Rundskriv

*Akademisk (5):* Juridika, Idunn, UiO Jus, UiB BORA, Cristin

*EU/EØS (4):* EUR-Lex, Curia, EFTA-domstolen, ESA

*Menneskerettigheter (4):* HUDOC/EMD, Europarådet, UN Treaty, OHCHR

*Internasjonal/komparativ (5):* ICJ, ITLOS, WTO, Retsinformation.dk, Riksdagen.se

**Nye kilder vi mangler i JusJob** (uthevet over): Skatteklagenemnda, UNE, Finanstilsynet, Konkurransetilsynet, Nkom, NVE, Patentstyret, Statsforvalteren

---

### [HNygard/sivilombudet-uttalelser](https://github.com/HNygard/sivilombudet-uttalelser)
**Relevans: ⭐⭐ God — seed-datasett og skraperdesign**

PHP-scraper + JSON/CSV-datasett med 1000+ sivilombudet-uttalelser. Lisensavklaring: åpent. Nyttig som testfikstur for vår `pipeline/sivilombudet.py` og som sammenligningsdata. PHP-koden er ikke portabel, men skrapemønsteret (paginering, lovhenvisningsekstraksjon) er relevant.

---

### [HNygard/norsk-lovtidend](https://github.com/HNygard/norsk-lovtidend)
**Relevans: ⭐⭐ God — historisk endringshistorikk**

~250 MB datadump av alle Lovtiend-kunngjøringer i CSV/JSON. Bekrefter at kunngjøringstekster er fritt brukbare (NLOD, bekreftet av Lovdata i e-post sitert i README) mens konsoliderte/ajourførte tekster ikke er det. `norsk-lovtidend.json` gir amendment-historikk per lov — relevant for endringshistorikk-varsling.

---

## Anbefalt handlingsplan

### Umiddelbart
1. **Studer `convert_lovdata_xpath.py`** (NationalLibraryOfNorway) — tilpass XPath-logikken til `pipeline/lovdata.py` for robust XML-parsing
2. **Fiks lovdata.py** — riktig filnavn `gjeldende-sentrale-forskrifter.tar.bz2` (allerede fikset), legg til `lovtidend-avd1-2001-2024.tar.bz2` (historisk arkiv)
3. **Mine `sources.js`** (Rettskildesok) — bruk som autoritativ sjekkliste for hvilke sources som mangler i JusJob

### Nye kilder å legge til (fra Rettskildesok-katalogen)
- Skatteklagenemnda (`skatteklagenemnda.no`)
- UNE — Utlendingsnemnda (`une.no/praksis`)
- Finanstilsynet (`finanstilsynet.no/nyheter-og-publikasjoner`)
- Konkurransetilsynet (`konkurransetilsynet.no/vedtak-og-uttalelser`)
- Nkom (`nkom.no/vedtak`)
- NVE (`nve.no/juridiske-dokumenter`)
- Patentstyret
- Statsforvalteren
- Justisdep. tolkningsuttalelser (`regjeringen.no/no/dokumenter/tolkningsuttalelser`)
- Stortingstidende (forhandlinger)
- Arbeidsretten (Lovdata ARD)
- KOFA (`kofa.no/praksis`)

### Etter pipeline-utvidelse
4. **Studer `lovradar.py`** (Majac999) — endringshistorikk-mønster for `endringshistorikk-varsling`
5. **Studer `lovsonar.py`** (Majac999) — horisontskanning av lovforslag
6. **Les Juss-AI whitepaper** manuelt
7. **Implementer `validate_citation`** (ref. lovspor-mønsteret)
8. **EUR-Lex SPARQL-integrasjon** med ELI-spørringer (ref. EULex.NET)
