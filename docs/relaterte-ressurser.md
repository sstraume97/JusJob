# Relaterte ressurser og referanserepoer

Vurdert 2026-06-25. Relevans og gjenbruksvurdering for JusJob.

---

## Relevansmatrise

| Repo | Relevans | Kategori | Gjenbruk |
|---|---|---|---|
| [sondreskarsten/norwegian-laws](https://github.com/sondreskarsten/norwegian-laws) | ⭐⭐⭐ Kritisk | Lovkilde | Konsumeres direkte som datakilde |
| [khjohns/paragraf-mcp](https://github.com/khjohns/paragraf-mcp) | ⭐⭐⭐ Høy | Lovdata-parser + MCP | XML-parser, alias-løser, søkelogikk |
| [bartoszkobylinski/lovspor](https://github.com/bartoszkobylinski/lovspor) | ⭐⭐⭐ Høy | Endringshistorikk + MCP | Endringshistorikk-mønster, MCP-verktøy |
| [ngu-tek/Norwegian-law-mcp](https://github.com/ngu-tek/Norwegian-law-mcp) | ⭐⭐ God | MCP-server | MCP-arkitektur for Zotero-plugin |
| [StianOby/claude-legal-tools](https://github.com/StianOby/claude-legal-tools) | ⭐⭐ God | Lovdata API-ref | `api.lovdata.no` endepunkter |
| [worldwidelaw/legal-sources](https://github.com/worldwidelaw/legal-sources) | ⭐⭐ God | Arkitektur | Modulær pipeline-struktur |
| [einarra/lovdata-assistent](https://github.com/einarra/lovdata-assistent) | ⭐ Delvis | Lovdata+AI | Node.js Lovdata-integrasjon |
| [EivindKjosbakken/LegalShare](https://github.com/EivindKjosbakken/LegalShare) | ⭐ Delvis | Høyesterett-scraper | Pipeline-mønster for domstol.no |
| [KevinJohannesen/catchwise-backend](https://github.com/KevinJohannesen/catchwise-backend) | ⭐ Delvis | Søketeknologi | Norwegian-aware BM25-tokenisering |
| [doantumy/LegSum](https://github.com/doantumy/Efficiently-Summarizing-Norwegian-Legal-Texts) | ⭐ Delvis | ML/summering | Lovdata XML-struktur |
| [GmailHelene/rettbot](https://github.com/GmailHelene/rettbot) | – Ikke relevant | Kryptert PWA | Ingen gjenbrukbar kode |
| [openlegaldata/awesome-legal-data](https://github.com/openlegaldata/awesome-legal-data) | – Ikke relevant | Liste | Lite norsk dekning |
| [JoelNiklaus/LegalDatasets](https://github.com/JoelNiklaus/LegalDatasets) | – Ukjent | ML-datasett | Mulig norsk dekning ubekreftet |

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

## Anbefalt handlingsplan

1. **Nå:** Hent `structure_parser.py` og `_resolve_id()`-logikk fra `paragraf-mcp` til vår `lovdata.py`
2. **Nå:** Hent `laws.json` fra `norwegian-laws` som primær lovkilde
3. **Etter alle kilder er på plass:** Implementer `validate_citation` og `verify_quote` fra `lovspor`-mønsteret i sitatsjekk-funksjonen
4. **Fremtidig:** Eksponer `search-index.json` som MCP-server (ref. `ngu-tek` og `lovspor`-arkitektur)
