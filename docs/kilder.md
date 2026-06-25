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
| norwegian-laws (GitHub) | Lover + forskrifter | 🔲 Planlagt | GitHub Pages JSON | Høy |
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
