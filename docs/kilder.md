# Kilder — teknisk vurdering og integrasjonsplan

Sist oppdatert: 2026-06-25. Basert på Rettskildesok (sstraume97/Rettskildesok) som autoritativ referanseliste.

---

## Status-oversikt

### ✅ Aktive kilder (implementert)

| Kilde | Type | Tilgang | Output-fil |
|---|---|---|---|
| rettspraksis.no | Rettsavgjørelser (~70 000) | MediaWiki API | `rettspraksis.jsonl.gz` |
| data.stortinget.no | Stortingssaker/forarbeider (~17 000) | XML-API | `stortinget.jsonl.gz` |
| sivilombudet.no | Uttalelser (~1 950) | Sitemap + HTML | `sivilombudet.jsonl.gz` |
| kudos.dfo.no | Offentlige dok. KUDOS (~44 000) | REST API | `kudos.jsonl.gz` |
| Lovdata gjeldende lover | ~782 konsoliderte lover (XML) | api.lovdata.no tar.bz2 | `lovdata-lover.jsonl.gz` |
| Lovdata sentrale forskrifter | ~3 733 forskrifter (XML) | api.lovdata.no tar.bz2 | `lovdata-forskrifter.jsonl.gz` |
| Norsk Lovtiend avd. 1 (løpende) | Kunngjøringer inneværende år | api.lovdata.no tar.bz2 | `lovdata-lovtiend1.jsonl.gz` |
| Norsk Lovtiend avd. 1 (2001–2024) | Historisk arkiv | api.lovdata.no tar.bz2 | `lovdata-lovtiend1.jsonl.gz` |
| Forbrukertilsynet | Vedtak, markedsråd, FKU, veiledninger | HTML-scraping | `forbrukertilsynet.jsonl.gz` |

### ℹ️ Utilgjengelig (bekreftet)

| Kilde | Årsak |
|---|---|
| Norsk Lovtiend avd. 2 | Ikke i åpent API (kun avd. 1 tilgjengelig) |
| Domstolene direkte API | Kun innsendingstjeneste (digital-innsending) — ingen henting |
| Lovdata HR/LG/TRS (bulk) | Krever Lovdata-abonnement — bruk rettspraksis.no i stedet |
| Sivilrett.no | Returnerer 403 Forbidden |

---

## Planlagte kilder

### Gruppe 1 — Lovtekst og forarbeider (høy prioritet)

| Kilde | URL | Type | Tilgang | Merknad |
|---|---|---|---|---|
| norwegian-laws | github.com/sondreskarsten/norwegian-laws | Metadata: ELI, dept., rettsområde | GitHub Pages JSON | Supplement til Lovdata |
| Regjeringen NOU | regjeringen.no/no/dokumenter/nou | NOU-er | HTML-scraping | |
| Regjeringen Prop./Meld. | regjeringen.no/no/dokumenter/prop | Proposisjoner, meldinger | HTML-scraping | |
| Regjeringen Ot.prp. | regjeringen.no/no/dokumenter/otprp | Odelstingsproposisjoner | HTML-scraping | Eldre forarbeider |
| Justisdep. tolkningsuttalelser | regjeringen.no/no/dokumenter/tolkningsuttalelser | Tolkningsuttalelser | HTML-scraping | |
| Lovdata Rundskriv | lovdata.no/dokument/RUNDSKRIV | Rundskriv | HTML-scraping | |
| Lovdata NAV | lovdata.no/nav | NAV-rundskriv og retningslinjer | HTML-scraping | |
| Stortingstidende | stortinget.no/Stortingstidende | Stortingsforhandlinger | HTML-scraping | |

### Gruppe 2 — Domstolsinstanser (høy prioritet)

| Kilde | URL | Type | Tilgang | Merknad |
|---|---|---|---|---|
| Domstol.no (Høyesterett) | domstol.no/no/hoyesterett/avgjorelser | Høyesterettsavgjørelser | HTML-scraping | Supplement til rettspraksis.no |
| Arbeidsretten | lovdata.no/dokument/ARD | Arbeidsrettsdommer | HTML-scraping | |
| Trygderetten | trygderetten.no | Kjennelser | HTML-scraping | |
| EFTA-domstolen | eftacourt.int/cases | EØS-avgjørelser | API | |
| EMD / HUDOC | hudoc.echr.coe.int | Menneskerettsdomstolen | HUDOC JSON API | |

### Gruppe 3 — Nemnder og tilsyn (høy/middels prioritet)

| Kilde | URL | Type | Tilgang | Merknad |
|---|---|---|---|---|
| Datatilsynet | datatilsynet.no/regelverk-og-verktoy | Vedtak, veiledere (GDPR) | HTML-scraping | |
| Helsetilsynet | helsetilsynet.no | Tilsynsrapporter, vedtak | HTML-scraping | |
| Skatteetaten rettskilder | skatteetaten.no/rettskilder | BFU, vedtak, håndbøker | HTML-scraping | |
| Skatteetaten API | skatteetaten.github.io/api-dokumentasjon | Juridiske håndbøker | Maskinporten API | Krever org.nr. |
| Skatteklagenemnda | skatteklagenemnda.no | Vedtak (skatterett) | HTML-scraping | |
| UNE — Utlendingsnemnda | une.no/praksis | Praksis (utlendingsrett) | HTML-scraping | |
| Finanstilsynet | finanstilsynet.no/nyheter-og-publikasjoner | Vedtak, rundskriv (finansrett) | HTML-scraping | |
| Konkurransetilsynet | konkurransetilsynet.no/vedtak-og-uttalelser | Vedtak (konkurranserett) | HTML-scraping | |
| LDO / Diskrimineringsnemnda | diskrimineringsnemnda.no | Vedtak, uttalelser | HTML-scraping | |
| KOFA | kofa.no/praksis | Praksis (offentlige anskaffelser) | HTML-scraping | |
| Nkom | nkom.no/vedtak | Vedtak (ekomrett) | HTML-scraping | |
| NVE | nve.no/juridiske-dokumenter | Juridiske dok. (energirett) | HTML-scraping | |
| Patentstyret | patentstyret.no | Vedtak (immaterialrett) | HTML-scraping | |
| Riksrevisjonen | riksrevisjonen.no | Revisjonsrapporter | HTML-scraping | |
| Statsforvalteren | statsforvalteren.no | Vedtak, klagebehandling | HTML-scraping | |

### Gruppe 4 — Fagdirektorater og sektormyndigheter (middels prioritet)

| Kilde | URL | Type | Tilgang | Merknad |
|---|---|---|---|---|
| Helsedirektoratet | helsedirektoratet.no/lov-og-forskrift | Rundskriv, lovfortolkninger | HTML + mulig API | Åpent API i footer |
| Arbeidstilsynet | arbeidstilsynet.no/regelverk | Regelverk, veiledere, HMS | HTML-scraping | |
| UDI regelverk | udiregelverk.no/no/rettskilder | RS/GI/PN-retningslinjer | HTML-scraping | |
| Bufdir | bufdir.no/fagstotte | Fagstøtte, barnevern, saksbehandlingsrundskrivet | HTML-scraping | |
| Klagenemdsekretariatet | klagenemndssekretariatet.no | KOFA, Konkurranseklagenemnda m.fl. | HTML-scraping | |
| IMDi | imdi.no/regelverk | Regelverk, integrering | HTML-scraping | |
| Medietilsynet | medietilsynet.no/regelverk | Medierett | HTML-scraping | |
| Lottstift | lottstift.no/lover-og-regelverk | Pengespill og lotteri | HTML-scraping | |
| NPE / Pasientskadenemnda | npe.no | Vedtak, erstatningsutmålinger | HTML-scraping | |
| Husleietvistutvalget | htu.no | Avgjørelser | HTML-scraping | |
| Kriminalomsorgen | kriminalomsorgen.no | Lovverk | HTML-scraping | Bruk offisiell side |

### Gruppe 5 — Internasjonale og komparative kilder (lav prioritet)

| Kilde | URL | Type | Tilgang | Merknad |
|---|---|---|---|---|
| EUR-Lex | eur-lex.europa.eu | EU-forordninger, direktiver, EØS | SPARQL / REST API | ELI-basert |
| Curia | curia.europa.eu | EU-domstolsavgjørelser | API | |
| ESA | esa.int | EØS-tilsyn | HTML-scraping | |
| Europarådet | coe.int | Konvensjoner | HTML-scraping | |
| UN Treaty Collection | treaties.un.org | FN-traktater | API | |
| Retsinformation.dk | retsinformation.dk | Dansk lovgivning (komparativ) | API | |
| Riksdagen.se | riksdagen.se | Svensk lovgivning (komparativ) | API | |

### Gruppe 6 — Åpne datasett og kataloger

| Kilde | URL | Type | Tilgang | Merknad |
|---|---|---|---|---|
| data.norge.no | data.norge.no | Begrepskatalog, åpne datasett | CKAN/Felles API | |
| Lovdata Historiske versjoner | lovdata.no/dokument/HIST | Opphevede og historiske lover | HTML-scraping | |

### Ikke relevant for JusJob

| Kilde | Årsak |
|---|---|
| Juridika.no | Betalt tjeneste |
| Idunn.no | Betalt akademisk database |
| SNL Jus | Encyklopedi, ikke primærkilder |
| ICJ / ITLOS / WTO | For spesialisert for generell bruk |

---

## Kildebeskrivelser

### Lovdata offentlige datapakker

**Tilgang:** Åpent REST API, ingen autentisering (NLOD 2.0)  
**API:** `https://api.lovdata.no/v1/publicData/list`  
**Status:** ✅ Implementert i `pipeline/lovdata.py`

Faktiske filnavn (bekreftet via HNygard/lovdata-openapi-copy):

| Filnavn | Innhold |
|---|---|
| `gjeldende-lover.tar.bz2` | ~782 konsoliderte gjeldende lover |
| `gjeldende-sentrale-forskrifter.tar.bz2` | ~3 733 sentrale forskrifter |
| `lovtidend-avd1-YYYY.tar.bz2` | Norsk Lovtiend avd. 1, løpende år |
| `lovtidend-avd1-2001-2024.tar.bz2` | Norsk Lovtiend avd. 1, historisk 2001–2024 |

**Viktig:** Avdeling 2 er ikke i det åpne API. `gjeldende-sentrale-forskrifter` — ikke `sentrale-forskrifter`.

**XML-struktur (fra NationalLibraryOfNorway/lovdata-public-conversion-script):**
- `dokumentID`: "NL/lov/2005-06-17-62" → ELI `/eli/lov/2005-06-17-62`
- `<title>` / `class="kortTittel"`: fulltittel og korttittel
- `class="departement"`: ansvarlig departement
- `fulltext`: seksjonsvis tekst-array
- `lastChangeInForce`: ikrafttredelse av siste endring

**Lovdata som autoritær kilde:** Lovdata er den juridisk autoritative kilden. `norwegian-laws` brukes kun som metadata-supplement (ELI, rettsområde).

---

### Skatteetaten rettsinformasjon API

**Tilgang:** Maskinporten REST API (scope: `skatteetaten:rettsinformasjon`)  
**Autentisering:** Krever norsk org.nr. + Maskinporten-klient + Altinn-delegering.

**Innhold:** Skatteforvaltningshåndboken (inkl. BFU-referanser), MVA-håndboken, Skattebetalingshåndboken, Folkeregisterhåndboken.  
**Begrensning:** BFU-fulltekster er ikke eget datasett — bruk HTML-scraping av `skatteetaten.no/rettskilder/` som supplement.

---

### Skatteklagenemnda

**URL:** `https://www.skatteklagenemnda.no`  
**Type:** Vedtak i skatterettslige klagesaker  
**Tilgang:** HTML-scraping  
**Merknad:** Separat organ fra Skatteetaten. Vedtakene er særlig relevante for skatterettslig praksis.

---

### UNE — Utlendingsnemnda

**URL:** `https://www.une.no/praksis`  
**Type:** Praksisbase for utlendingsrettslige vedtak  
**Tilgang:** HTML-scraping  
**Merknad:** Klageorgan for UDI-vedtak. Praksisbasen er søkbar og strukturert.

---

### Finanstilsynet

**URL:** `https://www.finanstilsynet.no/nyheter-og-publikasjoner`  
**Type:** Vedtak, rundskriv, tolkningsuttalelser (finansrett)  
**Tilgang:** HTML-scraping

---

### Konkurransetilsynet

**URL:** `https://www.konkurransetilsynet.no/vedtak-og-uttalelser`  
**Type:** Vedtak i konkurranserettslige saker  
**Tilgang:** HTML-scraping

---

### KOFA — Klagenemnda for offentlige anskaffelser

**URL:** `https://www.kofa.no/praksis`  
**Type:** Praksis for offentlige anskaffelser  
**Tilgang:** HTML-scraping  
**Merknad:** Strukturert praksisbase med søkefunksjon.

---

### Nkom — Nasjonal kommunikasjonsmyndighet

**URL:** `https://www.nkom.no/vedtak`  
**Type:** Vedtak (ekomrett, post)  
**Tilgang:** HTML-scraping

---

### NVE — Norges vassdrags- og energidirektorat

**URL:** `https://www.nve.no/juridiske-dokumenter`  
**Type:** Juridiske dokumenter (energirett, vassdragsrett)  
**Tilgang:** HTML-scraping

---

### Patentstyret

**URL:** `https://www.patentstyret.no`  
**Type:** Vedtak (patent, varemerke, design — immaterialrett)  
**Tilgang:** HTML-scraping

---

### Statsforvalteren

**URL:** `https://www.statsforvalteren.no`  
**Type:** Vedtak og klagebehandling på vegne av departementene  
**Tilgang:** HTML-scraping  
**Merknad:** 15 statsforvaltere — bør aggregeres per embete eller samles via nasjonal portal.

---

### Justisdepartementet tolkningsuttalelser

**URL:** `https://www.regjeringen.no/no/dokumenter/tolkningsuttalelser`  
**Type:** Tolkningsuttalelser fra Justis- og beredskapsdepartementet  
**Tilgang:** HTML-scraping  
**Merknad:** Særlig relevante for forvaltningsrett og offentlig rett.

---

### Norges domstoler — ingen publik API

Domstolene tilbyr **ingen API for henting av dommer**. `domstolene/api-docs` (GitHub) er en ren innsendingstjeneste. Dommer distribueres via Lovdata. JusJob henter via:
1. **rettspraksis.no** (MediaWiki API) ✅
2. **domstol.no** (HTML-scraping, planlagt)

---

## Implementeringsrekkefølge

### Neste steg (bygger på eksisterende pipeline)
1. **norwegian-laws** — ett API-kall, beriker ELI-kobling
2. **Datatilsynet vedtak** — enkel HTML-liste
3. **Helsetilsynet publikasjoner** — enkel HTML-liste
4. **UNE praksisbase** — strukturert søkbar base
5. **KOFA praksisbase** — strukturert søkbar base
6. **Skatteklagenemnda** — vedtaksliste
7. **Finanstilsynet** — vedtaksliste
8. **Konkurransetilsynet** — vedtaksliste

### Deretter
9. **Skatteetaten rettskilder** (BFU, uttalelser)
10. **Helsedirektoratet rundskriv**
11. **Regjeringen.no** (NOU, Prop., tolkningsuttalelser)
12. **UDI retningslinjer** (RS/GI/PN)
13. **Arbeidsretten** (Lovdata ARD)

### Lavere prioritet
14. Bufdir, Arbeidstilsynet, IMDi, Medietilsynet, Nkom, NVE, Patentstyret
15. Lovdata NAV, Trygderetten, NPE, Husleietvistutvalget, Statsforvalteren
16. Stortingstidende, Lovdata HIST, Lovdata Rundskriv
17. EUR-Lex (SPARQL), EFTA-domstolen, HUDOC/EMD
18. Komparative kilder (DK, SE)
