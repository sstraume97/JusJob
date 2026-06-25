# Relaterte ressurser og referanserepoer

Vurdert 2026-06-25. Notater om relevans for JusJob nå og fremover.

---

## Direkte relevante (bruk nå)

### [sondreskarsten/norwegian-laws](https://github.com/sondreskarsten/norwegian-laws)
**Status: Integreres som lovkilde**
- 794 lover + 3 438 forskrifter, oppdatert daglig fra Lovdata (NLOD 2.0)
- Publisert som `laws.json` på GitHub Pages
- Nøkkelfelter: `refid`, `eli`, `korttittel`, `forkortelse`, `departement`, `rettsomrade`, `ikrafttredelse`, `sist_endret`
- `eli`-identifikatorer (`/eli/lov/1902/05/22`) er nøkkelen til automatisk lenking mot forarbeider og rettspraksis
- Inneholder også `amendments.jsonl.gz` (~91 000 endringsrecords) og `amendment-acts.jsonl.gz` (~38 000)
- **Bruk**: Hent `laws.json` direkte i pipeline, bruk `eli` som lenkenøkkel

---

## Potensielt relevante (fremtidig bruk)

### [ngu-tek/Norwegian-law-mcp](https://github.com/ngu-tek/Norwegian-law-mcp)
**Status: Relevant for MCP-integrasjon**
- MCP-server som gjør 3 400 norske lover + 25 301 forarbeider søkbare via AI
- Datakilder: Lovdata, Stortinget, EUR-Lex
- BM25-søk i SQLite, oppdateres daglig
- **Fremtidig bruk**: Vurder å eksponere JusJob-indeksen som MCP-server for AI-integrasjon
- Lovdata API-endepunkt: `https://api.lovdata.no/v1/publicData/list` (gratis, ingen nøkkel for gjeldende lovtekst)

### [StianOby/claude-legal-tools](https://github.com/StianOby/claude-legal-tools/tree/main/skills/lovdata-api)
**Status: Referanse for Lovdata API**
- Dokumenterer Lovdata API: `https://api.lovdata.no/v1/publicData/list`
- Gratis uten API-nøkkel for gjeldende lovtekst; nøkkel gir tilgang til flere endepunkter (historikk, live-søk)
- `lastModified`-tidsstempler for inkrementell oppdatering
- **Fremtidig bruk**: Dersom vi ønsker fulltekst direkte fra Lovdata istedet for norwegian-laws

### [worldwidelaw/legal-sources](https://github.com/worldwidelaw/legal-sources)
**Status: Arkitekturinspirasjon**
- 960+ skript for juridiske data fra 110+ land (AGPL-3.0)
- Standardisert skjema: `_id`, `_source`, `_type`, `title`, `text`, `date`, `url`
- To datamodeller: Lovgivning (mutable/versjonert) og rettspraksis (immutable/append-only)
- Modulær arkitektur: `bootstrap.py`, `config.yaml`, `retrieve.py` per kilde
- **Fremtidig bruk**: Referanse ved utvidelse til europeiske rettskilder; vurder bidrag med norsk modul

### [KevinJohannesen/catchwise-backend](https://github.com/KevinJohannesen/catchwise-backend)
**Status: Referanse for søketeknologi**
- FastAPI + BM25 + RAG for norske juridiske dokumenter
- "Norwegian-aware tokenization" for BM25-indeksering
- Håndterer Lovdata og J-meldinger (Fiskeridirektoratet)
- Ingestion parsers for RSS, HTML og PDF
- **Fremtidig bruk**: Norwegian-aware tokenization ved implementasjon av server-side søk

### [doantumy/Efficiently-Summarizing-Norwegian-Legal-Texts](https://github.com/doantumy/Efficiently-Summarizing-Norwegian-Legal-Texts)
**Status: Referanse for tekstanalyse**
- Automatisk summering av norske rettsavgjørelser (Høyesterett, fra Lovdata XML)
- Lovdata XML-struktur: `<sammendrag>`, `<premiss>`, `<slutning>`
- Teknikker for segmentering og likhetsmåling (ROUGE, BERTScore)
- **Fremtidig bruk**: Dersom vi ønsker automatisk genererte sammendrag av rettsavgjørelser uten offisielt sammendrag

### [JoelNiklaus/LegalDatasets](https://github.com/JoelNiklaus/LegalDatasets)
**Status: Mulig datasett-kilde**
- Samling av juridiske datasett for ML-trening
- Felles skjema: `id`, `type`, `language`, `jurisdiction`, `title`, `date`, `url`, `metadata`, `text`
- Dekker muligens norske kilder (ikke bekreftet)
- **Fremtidig bruk**: Dersom vi ønsker treningsdata for norsk juridisk NLP/søk

---

## Lovdata API (gratis)
- Base: `https://api.lovdata.no/v1/publicData/`
- `/list` — liste over oppdaterte dokumenter med `lastModified`
- Ingen API-nøkkel nødvendig for gjeldende lovtekst
- Nøkkel gir tilgang til historikk og live-søk
