# Relaterte ressurser og referanserepoer

Vurdert 2026-06-25. Relevans og gjenbruksvurdering for JusJob.

---

## Relevansmatrise

| Repo | Relevans | Kategori | Gjenbruk |
|---|---|---|---|
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
| [digdir/nasjonal-arkitektur](https://github.com/digdir/nasjonal-arkitektur) | ⭐ Delvis | Digital arkitektur | Kartlegger autoritative datakilder i offentlig sektor |
| [GmailHelene/rettbot](https://github.com/GmailHelene/rettbot) | – Ikke relevant | Kryptert PWA | Ingen gjenbrukbar kode |
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

## Anbefalt handlingsplan

1. **Nå:** Studer `lovradar.py` (Majac999) — fungerende Lovdata API-integrasjon under NLOD 2.0
2. **Nå:** Studer `lovsonar.py` (Majac999) — Stortinget/reg.no RSS-scraping og horisontskanning
3. **Nå:** Hent `laws.json` fra `norwegian-laws` som primær lovkilde
4. **Nå:** Bruk `aiantech/legal-sources/sources/NO` som gapanalyse-sjekkliste
5. **Hent og les:** Juss-AI whitepaper manuelt
6. **Etter alle kilder er på plass:** Implementer `validate_citation` og `verify_quote` fra `lovspor`-mønsteret
7. **Fremtidig:** Eksponer `search-index.json` som MCP-server (ref. `ngu-tek` og `lovspor`-arkitektur)
8. **Fremtidig:** EUR-Lex SPARQL-integrasjon med ELI-spørringer (ref. EULex.NET som referanse)
