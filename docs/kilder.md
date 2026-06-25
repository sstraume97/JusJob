# Kilder — teknisk vurdering og integrasjonsplan

Sist oppdatert: 2026-06-25.

---

## Status-oversikt

| Kilde | Type | Prioritet | Tilgang | Status |
|---|---|---|---|---|
| rettspraksis.no | Rettsavgjørelser | ✅ Live | MediaWiki API | Ferdig |
| data.stortinget.no | Stortingssaker/forarbeider | ✅ Live | XML-API | Ferdig |
| sivilombudet.no | Uttalelser | ✅ Live | Sitemap + HTML | Ferdig |
| kudos.dfo.no | Offentlige dok. (KUDOS) | ✅ Live | REST API | Ferdig |
| Lovdata gjeldende lover | ~782 konsoliderte lover (XML, NLOD 2.0) | ✅ Implementert | api.lovdata.no tar.bz2 | Ferdig |
| Lovdata sentrale forskrifter | ~3 733 konsoliderte forskrifter (XML) | ✅ Implementert | api.lovdata.no tar.bz2 | Ferdig |
| Norsk Lovtiend avd. 1 | Kunngjøringer: lover + sentrale forskrifter | ✅ Implementert | api.lovdata.no tar.bz2 | Ferdig |
| Norsk Lovtiend avd. 1 (historisk 2001–2024) | Alle kunngjøringer fra 2001 til 2024 | ✅ Implementert | api.lovdata.no tar.bz2 | Ferdig |
| Norsk Lovtiend avd. 2 | Kunngjøringer: lokale + private forskrifter | ℹ️ Ikke i åpent API | — ikke tilgjengelig | Ikke mulig |
| Forbrukertilsynet | Vedtak, markedsråd, FKU, veiledninger | ✅ Implementert | HTML-scraping | Ferdig |
| norwegian-laws (GitHub) | Metadata: ELI, departement, rettsområde | 🔲 Planlagt | GitHub Pages JSON | Middels (metadata-beriker) |
| Skatteetaten rettsinformasjon API | Skattehåndboken, MVA-håndboken m.fl. | 🔲 Planlagt | Maskinporten REST API | Høy (krever org.nr.) |
| Skatteetaten rettskilder (web) | BFU, vedtak, retningslinjer | 🔲 Planlagt | HTML-scraping (fallback) | Høy |
| Norges domstoler (domstolene) | Dommer (Høyesterett, lagmanns-, tingretter) | ℹ️ Ingen publik API | — kun Lovdata | Ikke mulig direkte |
| Datatilsynet | Vedtak, veiledere | 🔲 Planlagt | HTML-scraping | Høy |
| Helsetilsynet | Publikasjoner, regelverk | 🔲 Planlagt | HTML-scraping | Høy |
| Helsedirektoratet | Rundskriv, lovfortolkninger | 🔲 Planlagt | HTML + mulig API | Høy |
| Forbrukertilsynet | Vedtak, markedsråd, veiledninger | 🔲 Planlagt | HTML-scraping | Høy |
| UDI regelverk | Retningslinjer, instrukser | 🔲 Planlagt | HTML-scraping | Middels |
| Bufdir | Fagstøtte, barnevern | 🔲 Planlagt | HTML-scraping | Middels |
| Arbeidstilsynet | Regelverk, veiledere | 🔲 Planlagt | HTML-scraping | Middels |
| IMDi | Regelverk | 🔲 Planlagt | HTML-scraping | Middels |
| Medietilsynet | Regelverk | 🔲 Planlagt | HTML-scraping | Lav |
| Lovdata NAV | NAV-praksis | 🔲 Planlagt | HTML-scraping | Lav |
| Kriminalomsorgen | Lovverk | 🔲 Planlagt | HTML-scraping | Lav |
| Lottstift | Lover og regelverk | 🔲 Planlagt | HTML-scraping | Lav |
| NPE | Vedtak/erstatning | 🔲 Planlagt | HTML-scraping | Lav |
| Helsedirektoratet API | Åpne data | 🔲 Planlagt | REST API | Undersøkes |
| data.norge.no | Begrepskatalog, datasett | 🔲 Planlagt | CKAN/Felles API | Undersøkes |
| Sivilrett.no | Juridisk database | 🔲 Planlagt | HTML (403 nå) | Blokkert |

---

## Detaljerte kildebeskrivelser

### Skatteetaten — https://www.skatteetaten.no/rettskilder/

**Type:** Skatterettskilder  
**Tilgang:** HTML-navigasjon, ingen API  
**Innhold (6 kategorier):**
- Regelverk — lover, forskrifter, internasjonale avtaler
- Høringer — høringsnotater fra Skattedirektoratet
- Håndbøker — skattehåndboken, MVA, lønns-ABC
- Uttalelser — bindende forhåndsuttalelser (BFU), direktiver, prinsipputtalelser
- Vedtak — Skatteklagenemnda, tidligere klageinstanser
- Retningslinjer — gjennomføringsveiledning

**Scraping-tilnærming:** Hent kategorilister → parse enkeltdokumenter. BFU-ene er særlig relevante (søkbar praksis).

---

### data.norge.no — https://data.norge.no/

**Type:** Åpent datakatalog  
**Tilgang:** Felles datakatalog har SPARQL/REST API  
**Relevante datasett:**
- Begrepskatalog (juridiske begreper fra offentlig sektor)
- Datatilsynet datasett
- Brønnøysundregistrene
- Kartverket

**Scraping-tilnærming:** Undersøk `https://data.norge.no/api` og SPARQL-endepunkt for begrepskatalogen. Kan hente strukturerte juridiske begreper.

---

### Lovdata offentlige datapakker — https://api.lovdata.no/v1/publicData/list

**Type:** Gjeldende lover, sentrale forskrifter, Norsk Lovtiend  
**Tilgang:** Åpent REST API, ingen autentisering (NLOD 2.0)  
**Status:** ✅ Implementert i `pipeline/lovdata.py`

**Pakker tilgjengelig:**

| Filnavn | Innhold | Størrelse |
|---|---|---|
| `gjeldende-lover.tar.bz2` | ~782 konsoliderte, gjeldende lover | ~6 MB |
| `sentrale-forskrifter.tar.bz2` | ~3 733 sentrale forskrifter | ~21 MB |
| `lovtidend-avd1-YYYY.tar.bz2` | **Norsk Lovtiend avd. 1** — kunngjøringer av lover og sentrale forskrifter (løpende) | varierer |
| `lovtidend-avd2-YYYY.tar.bz2` | **Norsk Lovtiend avd. 2** — kunngjøringer av lokale og private forskrifter | varierer |

**Norsk Lovtiend** er den offisielle norske lovtidenden, publisert av Lovdata. Avd. 1 inneholder kunngjøringer av alle nye og endrede lover og sentrale forskrifter. Avd. 2 inneholder lokale og private forskrifter (kommunale forskrifter, vedtekter m.m.).

**XML-struktur:**
- `doc_id`: "NL/lov/2005-06-17-62" → ELI `/eli/lov/2005-06-17-62`
- `<title>`: fulltittel
- `class="kortTittel"`: korttittel/populærnavn
- `class="departement"`: ansvarlig departement
- `<article data-name="§ X-Y">`: enkeltparagrafer

**Inkrementell logikk:** sammenligner `lastModified` fra API mot `data/lovdata_cache.json` — laster kun ned ved endring.

**Output:** `data/lovdata-lover.jsonl.gz`, `data/lovdata-forskrifter.jsonl.gz`, `data/lovdata-lovtiend1.jsonl.gz`, `data/lovdata-lovtiend2.jsonl.gz`

**Lovdata som autoritær kilde:** Lovdata er den juridisk autoritative kilden for norsk lovtekst. `norwegian-laws` er et nyttig metadata-supplement (ELI, departement, rettsområde) men Lovdata-pakkene er primærkilden for faktisk lovtekst.

---

### Skatteetaten rettsinformasjon API — https://skatteetaten.github.io/api-dokumentasjon/

**Type:** Skatterettskilder (juridiske håndbøker)  
**Tilgang:** Maskinporten REST API (`skatteetaten:rettsinformasjon`-scope)  
**Autentisering:** Krever norsk organisasjonsnummer + Maskinporten-klientregistrering. Tilgang innvilges av Skatteetaten og kan delegeres via Altinn.  
**OpenAPI-spec:** Tilgjengelig på SwaggerHub.

**Innhold (strukturert JSON med HTML-tekst):**
- Skatteforvaltningshåndboken — inkl. kap. 6 om BFU (bindende forhåndsuttalelser)
- Merverdiavgiftshåndboken
- Skattebetalingshåndboken
- Folkeregisterhåndboken
- Innkrevingsloven

**Viktig begrensning:** BFU-beslutninger er *referert til* i håndbokstekst, men finnes ikke som eget søkbart datasett i API-et. Fullstendige BFU-tekster er på Lovdata og skatteetaten.no/rettskilder/.

**Scraping-tilnærming:**
- Primær: Maskinporten REST API (strukturert, maskinlesbar)
- Sekundær fallback: HTML-scraping av `skatteetaten.no/rettskilder/` (BFU, vedtak, uttalelser)

**Maskinporten-mønster** — gjelder for alle Maskinporten-sikrede API-er (inkl. fremtidige domstol-API-er):
```python
# Krever: org.nr., virksomhetssertifikat (Buypass/Commfides), Maskinporten-klient
# Flyt: JWS-signert JWT → Maskinporten token → Bearer token i API-kall
# Scope eksempel: "skatteetaten:rettsinformasjon"
```

---

### Norges domstoler — https://github.com/orgs/domstolene/repositories

**Viktig funn:** Domstolene tilbyr **ingen publik API for henting av dommer eller rettsavgjørelser**.

Det eneste publiserte API-et (`domstolene/api-docs`) er `digital-innsending` — en ren *innsendingstjeneste* for å levere dokumenter *til* domstoler via Maskinporten. Det finnes ingen endepunkter for å hente, søke eller laste ned dommer.

**Konsekvens for JusJob:** Norske rettsavgjørelser hentes via:
1. **rettspraksis.no** (MediaWiki API) — allerede implementert ✅
2. **Lovdata** (krev. abonnement for bulk; NLOD 2.0 for åpne dokumenter)
3. **domstol.no** (HTML-scraping av offentlig tilgjengelige dommer)

Domstolene publiserer sine dommer gjennom Lovdata-samarbeidet — ikke via egne API-er.

---

### UDI regelverk — https://udiregelverk.no/no/rettskilder/

**Type:** Utlendingsrett  
**Tilgang:** HTML-navigasjon, ingen API  
**Innhold:**
- Lover og forskrifter (utlendingsloven, statsborgerloven)
- UDI-retningslinjer (RS, GI, PN)
- Høyesterettsavgjørelser
- Departementenes rundskriv og instrukser
- Internasjonale rettskilder (EMD, EF-domstolen)

**Scraping-tilnærming:** Parse retningslinjekategorier, hent RS/GI/PN-dokumenter med tittel + dato + kategori.

---

### Medietilsynet — https://www.medietilsynet.no/regelverk/

**Type:** Medierett  
**Tilgang:** HTML-navigasjon  
**Scraping-tilnærming:** Hent regelverkssider, lover og forskrifter.

---

### Lovdata NAV — https://lovdata.no/nav/

**Type:** NAV-praksis og trygderett  
**Tilgang:** Lovdata-HTML (krever ikke innlogging for NAV-rundskriv)  
**Scraping-tilnærming:** Kategorisidene på lovdata.no/nav/ har lister med rundskriv og retningslinjer som er åpent tilgjengelige.

---

### Arbeidstilsynet — https://www.arbeidstilsynet.no/regelverk/

**Type:** Arbeidsrett og HMS  
**Tilgang:** HTML-navigasjon  
**Innhold:** Regelverk, veiledere, tilsynsrapporter  
**Scraping-tilnærming:** Parse regelverkssider etter seksjonstype.

---

### Bufdir — https://www.bufdir.no/fagstotte/

**Type:** Barnevern, familie og likestilling  
**Tilgang:** HTML-navigasjon  
**Relevante undersider:**
- `/fagstotte/produkter/` — faglige produkter
- `/fagstotte/barnevern-oppvekst/lover-og-regelverk/` — lover og regelverk
- `/fagstotte/produkter/saksbehandlingsrundskrivet/` — saksbehandlingsrundskrivet (særlig viktig)

**Scraping-tilnærming:** Hent saksbehandlingsrundskrivet kapittelvis. Parse regelverkssider for lenkelister.

---

### Datatilsynet — https://www.datatilsynet.no/

**Type:** Personvern og GDPR  
**Tilgang:** HTML-navigasjon  
**Innhold:**
- Lover og regler (personopplysningsloven, politiregisterloven, pasientjournalloven)
- Sentrale avgjørelser
- Sentrale høringsuttalelser
- Veiledere og verktøy

**Scraping-tilnærming:** Parse `https://www.datatilsynet.no/regelverk-og-verktoy/` → avgjørelser og veiledere.

---

### Forbrukertilsynet — https://www.forbrukertilsynet.no/

**Type:** Forbrukerrett  
**Tilgang:** HTML-lister + mulig Onacos/wfinnsyn-API  

**Undersider og innhold:**
- `/lov-og-rett/vedtak` — vedtak siste 5 år, kronologisk liste, ref-format: `FOV-2025-235041`
- `/lov-og-rett/markedsradets-vedtak` — Markedsrådets vedtak
- `/forbrukerklageutvalget/vedtak-i-forbrukerklageutvalget-etter-mai-2025-2` — Forbrukerklageutvalget
- `/lov-og-rett/veiledninger-og-retningslinjer` — veiledninger

**Onacos/wfinnsyn-API:**  
- Prod: `https://innsyn.onacos.no/forbrukertilsynet/prod/wfinnsyn.ashx`
- Hist: `https://innsyn.onacos.no/forbrukertilsynet/hist/wfinnsyn.ashx`
- API-dokumentasjon: https://acosas.github.io/index.html — REST, trolig JSON-retur, minimal autentisering
- Status: API returnerte 500 ved første test — prøv videre med korrekte parametere

**Scraping-tilnærming:** Prøv Onacos-API først. Fallback: parse HTML-lister for vedtak.

---

### IMDi — https://www.imdi.no/regelverk/

**Type:** Integrering og mangfold  
**Tilgang:** HTML-navigasjon  
**Scraping-tilnærming:** Parse regelverkssider.

---

### Kriminalomsorgen — https://kriminalomsorgen.vercel.app/ressurser

**Type:** Straffegjennomføring  
**Tilgang:** Uoffisiell Vercel-app — kan forsvinne  
**Merknad:** Bør hentes direkte fra Kriminalomsorgens offisielle nettside i stedet.

---

### Helsedirektoratet — https://www.helsedirektoratet.no/lov-og-forskrift

**Type:** Helserett  
**Tilgang:** HTML + mulig åpent API  
**Innhold:**
- Lov og forskrift
- Rundskriv og veiledere til lov og forskrift
- Lovfortolkninger

**Merknad:** Footeren på helsedirektoratet.no nevner "Åpne data (API)" — undersøk dette endepunktet nærmere. URL-kandidat: `https://www.helsedirektoratet.no/api/`.

**Scraping-tilnærming:** Undersøk API-dokumentasjon → parse rundskriv/veilederliste.

---

### Lottstift — https://lottstift.no/lover-og-regelverk/

**Type:** Lotteri og pengespill  
**Tilgang:** HTML-navigasjon  
**Scraping-tilnærming:** Parse regelverkssider.

---

### NPE — https://www.npe.no/

**Type:** Pasientskadeerstatning  
**Tilgang:** HTML-navigasjon  
**Innhold:** Vedtak, erstatningsutmålinger, statistikk  
**Scraping-tilnærming:** Finn vedtakslister og statistikksider.

---

### Helsetilsynet — https://www.helsetilsynet.no/

**Type:** Tilsyn med helse- og omsorgstjenester  
**Tilgang:** HTML-navigasjon  
**Undersider:**
- `/regelverk/` — kategorisert etter virksomhetstype (barnevern, sosiale tjenester, helse)
- `/publikasjoner/` — rapporter og tilsynsresultater
- `/rettigheter-klagemuligheter/` — pasientrettigheter

**Scraping-tilnærming:** Parse `/regelverk/` og `/publikasjoner/` for lenkelister.

---

### Sivilrett.no — https://www.sivilrett.no/

**Type:** Sivilrettslig database  
**Tilgang:** Returnerte 403 — muligens krever innlogging eller er blokkert for crawler  
**Status:** Blokkert — undersøk manuelt om det er gratis tilgang.

---

### Nye kilder identifisert via Rettskildesok (sources.js)

Rettskildesok-katalogen avdekket følgende planlagte kilder som ikke var i opprinnelig liste:

| Kilde | URL | Type | Prioritet |
|---|---|---|---|
| Skatteklagenemnda | skatteklagenemnda.no | Vedtak (skatterett) | Høy |
| UNE — Utlendingsnemnda | une.no/praksis | Praksis (utlendingsrett) | Høy |
| Finanstilsynet | finanstilsynet.no | Vedtak, rundskriv (finansrett) | Høy |
| Konkurransetilsynet | konkurransetilsynet.no | Vedtak (konkurranserett) | Høy |
| KOFA | kofa.no/praksis | Praksis (offentlige anskaffelser) | Middels |
| Nkom | nkom.no/vedtak | Vedtak (ekomrett) | Middels |
| NVE | nve.no/juridiske-dokumenter | Juridiske dokumenter (energirett) | Middels |
| Patentstyret | patentstyret.no | Vedtak (immaterialrett) | Middels |
| Statsforvalteren | statsforvalteren.no | Vedtak, klagebehandling | Middels |
| Justisdep. tolkningsuttalelser | regjeringen.no/no/dokumenter/tolkningsuttalelser | Tolkningsuttalelser | Middels |
| Stortingstidende | stortinget.no/Stortingstidende | Stortingsforhandlinger | Lav |
| Arbeidsretten | lovdata.no/dokument/ARD | Arbeidsrettsdommer | Lav |

---

## Implementeringsrekkefølge (forslag)

### Gruppe 1 — Høy verdi, enkelt å scrape
1. **norwegian-laws** (GitHub Pages JSON) — ett API-kall
2. **Forbrukertilsynet vedtak** — enkel HTML-liste med ref-numre
3. **Datatilsynet vedtak** — HTML-liste
4. **Helsetilsynet publikasjoner** — HTML-liste

### Gruppe 2 — Høy verdi, litt mer kompleks
5. **Skatteetaten uttalelser/vedtak** — BFU + Skatteklagenemnda
6. **Helsedirektoratet rundskriv** — undersøk API først
7. **UDI retningslinjer** — RS/GI/PN-format

### Gruppe 3 — Middels verdi
8. **Bufdir saksbehandlingsrundskrivet**
9. **Arbeidstilsynet regelverk**
10. **IMDi regelverk**

### Gruppe 4 — Lavere prioritet
11. **Medietilsynet**
12. **Lovdata NAV**
13. **Kriminalomsorgen** (finn offisiell kilde)
14. **Lottstift**
15. **NPE**
16. **data.norge.no begrepskatalog**
