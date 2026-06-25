# Kilder — teknisk vurdering og integrasjonsplan

Sist oppdatert: 2026-06-25.
Rettsområde-taksonomi: [sondreskarsten/norwegian-laws](https://github.com/sondreskarsten/norwegian-laws).

---

## Rettsområder (offisiell taksonomi)

| # | Rettsområde |
|---|---|
| 1 | Anskaffelser, avtaler, bygg og entrepriser |
| 2 | Arbeidsrett |
| 3 | Bank, finans og regnskapsrett |
| 4 | EU/EØS-rett |
| 5 | Energirett |
| 6 | Erstatnings- og forsikringsrett |
| 7 | Familie-, person- og barnerett |
| 8 | Fast eiendoms rettsforhold |
| 9 | Fiskeri- og fangstrett og havbruk |
| 10 | Forbruker-, kjøps- og konkurranserett |
| 11 | Forurensninger, klima og utslipp |
| 12 | Forvaltnings- og kommunalrett |
| 13 | HMS og beredskaps- og sikkerhetsrett |
| 14 | Helse- og omsorgsrett |
| 15 | IKT- og medierett |
| 16 | Immaterialrett |
| 17 | Internasjonal rett |
| 18 | Konkurs, gjeld og pant |
| 19 | Kultur, idrett og underholdning |
| 20 | Landbruk, jakt og skogbruk |
| 21 | Menneskerettigheter |
| 22 | Miljøvern, natur og friluftsliv |
| 23 | Næringsrett |
| 24 | Pensjons- og trygderett |
| 25 | Samerett |
| 26 | Selskaper, fond og foreninger |
| 27 | Sivil- og straffeprosess |
| 28 | Skatte- og avgiftsrett |
| 29 | Skoler, universiteter og forskning |
| 30 | Stats-, statsforfatnings- og statsborgerrett |
| 31 | Strafferett |
| 32 | Svalbard og biland |
| 33 | Transport og kommunikasjoner |
| 34 | Tvangsfullbyrdelse |
| 35 | Utlendingsrett |

---

## Kilderegister

### ✅ Aktive kilder

| Kilde | Rettsområde(r) | Tilgang | Output-fil |
|---|---|---|---|
| rettspraksis.no (~70 000) | Alle | MediaWiki API | `rettspraksis.jsonl.gz` |
| data.stortinget.no (~17 000) | Alle | XML-API | `stortinget.jsonl.gz` |
| sivilombudet.no (~1 950) | Forvaltnings- og kommunalrett | Sitemap + HTML | `sivilombudet.jsonl.gz` |
| kudos.dfo.no (~44 000) | Alle (offentlig sektor) | REST API | `kudos.jsonl.gz` |
| Lovdata gjeldende lover (~782) | Alle | api.lovdata.no tar.bz2 | `lovdata-lover.jsonl.gz` |
| Lovdata sentrale forskrifter (~3 733) | Alle | api.lovdata.no tar.bz2 | `lovdata-forskrifter.jsonl.gz` |
| Norsk Lovtiend avd. 1 (løpende) | Alle | api.lovdata.no tar.bz2 | `lovdata-lovtiend1.jsonl.gz` |
| Norsk Lovtiend avd. 1 (2001–2024) | Alle | api.lovdata.no tar.bz2 | `lovdata-lovtiend1.jsonl.gz` |
| Forbrukertilsynet | Forbruker-, kjøps- og konkurranserett | HTML-scraping | `forbrukertilsynet.jsonl.gz` |
| Regjeringen.no | Alle | HTML-scraping | `regjeringen.jsonl.gz` |
| Datatilsynet | IKT- og medierett | HTML-scraping | `datatilsynet.jsonl.gz` |
| Helsetilsynet | Helse- og omsorgsrett | HTML-scraping | `helsetilsynet.jsonl.gz` |
| UNE — Utlendingsnemnda | Utlendingsrett | HTML-scraping | `une.jsonl.gz` |
| KOFA | Anskaffelser, avtaler, bygg og entrepriser | HTML-scraping | `kofa.jsonl.gz` |
| Konkurransetilsynet | Forbruker-, kjøps- og konkurranserett; Næringsrett | HTML-scraping | `konkurransetilsynet.jsonl.gz` |
| Finanstilsynet | Bank, finans og regnskapsrett | HTML-scraping | `finanstilsynet.jsonl.gz` |
| Skatteklagenemnda | Skatte- og avgiftsrett | HTML-scraping | `skatteklagenemnda.jsonl.gz` |
| Skatteetaten | Skatte- og avgiftsrett | HTML-scraping | `skatteetaten.jsonl.gz` |
| LDO + Diskrimineringsnemnda | Menneskerettigheter | HTML-scraping | `diskriminering.jsonl.gz` |
| KFIR | Immaterialrett | HTML-scraping | `kfir.jsonl.gz` |
| Arbeidstilsynet | Arbeidsrett; HMS og beredskaps- og sikkerhetsrett | HTML-scraping | `arbeidstilsynet.jsonl.gz` |
| Riksrevisjonen | Stats-, statsforfatnings- og statsborgerrett; Forvaltnings- og kommunalrett | HTML-scraping | `riksrevisjonen.jsonl.gz` |
| Domstol.no | Alle | HTML-scraping | `domstol.jsonl.gz` |
| Helsedirektoratet | Helse- og omsorgsrett | HTML-scraping | `helsedirektoratet.jsonl.gz` |
| Trygderetten | Pensjons- og trygderett | HTML-scraping | `trygderetten.jsonl.gz` |
| Husleietvistutvalget | Fast eiendoms rettsforhold | HTML-scraping | `husleietvistutvalget.jsonl.gz` |
| UDI regelverk | Utlendingsrett | HTML-scraping | `udi.jsonl.gz` |
| NPE / Pasientskadenemnda | Helse- og omsorgsrett; Erstatnings- og forsikringsrett | HTML-scraping | `npe.jsonl.gz` |

**Note:** Regjeringen.no dekker proposisjoner, NOU-er, meldinger til Stortinget, rundskriv og høringer i én scraper (`pipeline/regjeringen.py`). De nyeste scraperne deler oppsett via `pipeline/_scraper_base.py` (session, cache, henting med 404-håndtering).

### 🔲 Planlagte kilder

| Kilde | Rettsområde(r) | Tilgang | Prioritet |
|---|---|---|---|
| **Lovverk og forarbeider** | | | |
| norwegian-laws (metadata) | Alle | GitHub Pages JSON | Implementert som subjects-berikelse i `lovdata.py` |
| Justisdep. tolkningsuttalelser | Forvaltnings- og kommunalrett; Strafferett | HTML-scraping | Middels |
| Lovdata Rundskriv | Alle | HTML-scraping | Middels |
| Lovdata NAV-rundskriv | Pensjons- og trygderett | HTML-scraping | Middels |
| Stortingstidende | Stats-, statsforfatnings- og statsborgerrett | HTML-scraping | Lav |
| **Domstolsinstanser** | | | |
| Arbeidsretten (ARD) | Arbeidsrett | HTML-scraping | Middels |
| EFTA-domstolen | EU/EØS-rett | API | Lav |
| EMD / HUDOC | Menneskerettigheter | HUDOC JSON API | Lav |
| **Skatt og finans** | | | |
| Skatteetaten rettsinformasjon API | Skatte- og avgiftsrett | Maskinporten | Supplement (krever org.nr.) |
| **Utlendingsrett** | | | |
| IMDi | Utlendingsrett | HTML-scraping | Middels |
| **Personvern og IKT** | | | |
| Nkom | IKT- og medierett | HTML-scraping | Middels |
| Medietilsynet | IKT- og medierett | HTML-scraping | Middels |
| **Familie og barn** | | | |
| Bufdir | Familie-, person- og barnerett | HTML-scraping | Middels |
| **Eiendom og husleie** | | | |
| Husleietvistutvalget | Fast eiendoms rettsforhold | HTML-scraping | Middels |
| **Energi og miljø** | | | |
| NVE | Energirett; Miljøvern, natur og friluftsliv | HTML-scraping | Middels |
| Patentstyret | Immaterialrett | HTML-scraping | Lav (KFIR dekker klageinstans) |
| **Forvaltning og kommunalrett** | | | |
| Statsforvalteren | Forvaltnings- og kommunalrett | HTML-scraping | Middels |
| Klagenemdsekretariatet | Anskaffelser, avtaler, bygg og entrepriser; Forbruker-, kjøps- og konkurranserett | HTML-scraping | Middels |
| **Nærings- og sektortilsyn** | | | |
| Lottstift | Næringsrett | HTML-scraping | Lav |
| Kriminalomsorgen | Strafferett | HTML-scraping | Lav |
| **Åpne datasett** | | | |
| data.norge.no | Alle (begrepskatalog) | CKAN/Felles API | Lav |
| Lovdata HIST | Alle | HTML-scraping | Lav |
| **Internasjonal og komparativ rett** | | | |
| EUR-Lex | EU/EØS-rett | SPARQL / REST API | Lav |
| Curia (EU-domstolen) | EU/EØS-rett | API | Lav |
| ESA | EU/EØS-rett | HTML-scraping | Lav |
| Europarådet | Menneskerettigheter; Internasjonal rett | HTML-scraping | Lav |
| UN Treaty Collection | Internasjonal rett; Menneskerettigheter | API | Lav |
| Retsinformation.dk | Internasjonal rett (komparativ) | API | Lav |
| Riksdagen.se | Internasjonal rett (komparativ) | API | Lav |

### ℹ️ Utilgjengelig (bekreftet)

| Kilde | Årsak |
|---|---|
| Norsk Lovtiend avd. 2 | Ikke i åpent API |
| Domstolene direkte API | Kun innsendingstjeneste |
| Lovdata HR/LG/TRS (bulk) | Krever Lovdata-abonnement |
| Sivilrett.no | 403 Forbidden |
| Juridika.no | Betalt tjeneste |
| Idunn.no | Betalt akademisk database |

---

## Tekniske detaljer

### Lovdata offentlige datapakker

**API:** `https://api.lovdata.no/v1/publicData/list` (åpent, NLOD 2.0)  
**Status:** ✅ Implementert i `pipeline/lovdata.py`

Faktiske filnavn (bekreftet via HNygard/lovdata-openapi-copy):

| Filnavn | Innhold |
|---|---|
| `gjeldende-lover.tar.bz2` | ~782 konsoliderte gjeldende lover |
| `gjeldende-sentrale-forskrifter.tar.bz2` | ~3 733 sentrale forskrifter |
| `lovtidend-avd1-YYYY.tar.bz2` | Norsk Lovtiend avd. 1, løpende år |
| `lovtidend-avd1-2001-2024.tar.bz2` | Norsk Lovtiend avd. 1, historisk arkiv |

**Viktig:** Avdeling 2 er ikke i det åpne API. Filnavnet er `gjeldende-sentrale-forskrifter`, ikke `sentrale-forskrifter`.

**XML-feltstruktur (fra NationalLibraryOfNorway/lovdata-public-conversion-script):**
- `dokumentID`: "NL/lov/2005-06-17-62" → ELI `/eli/lov/2005-06-17-62`
- `<title>` / `class="kortTittel"`: fulltittel og korttittel
- `class="departement"`: ansvarlig departement
- `fulltext`: seksjonsvis tekst-array
- `lastChangeInForce`: ikrafttredelse av siste endring

**Lovdata som autoritær kilde:** Lovdata er den juridisk autoritative kilden for norsk lovtekst. `norwegian-laws` brukes kun som metadata-supplement (rettsområde, departement, forkortelse).

---

### Skatteetaten rettsinformasjon API

**Tilgang:** Maskinporten (`skatteetaten:rettsinformasjon`). Krever org.nr. + Altinn-delegering.  
**Innhold:** Skatteforvaltningshåndboken, MVA-håndboken, Skattebetalingshåndboken, m.fl.  
**Begrensning:** BFU-fulltekster ikke eget datasett — bruk `skatteetaten.no/rettskilder/` som supplement.

---

### Norges domstoler — ingen publik API

Domstolene tilbyr ingen API for henting av dommer. Dommer distribueres via Lovdata. JusJob henter via rettspraksis.no (implementert ✅) og domstol.no (planlagt).

---

## Implementeringsrekkefølge

### Gruppe 1 — ✅ Ferdig
1. ✅ **norwegian-laws** — beriker rettsområde-feltet (`subjects`) i `lovdata.py`
2. ✅ **Datatilsynet** — vedtak, varsler, uttalelser
3. ✅ **Helsetilsynet** — tilsynsrapporter, publikasjoner
4. ✅ **UNE praksisbase** — praksisnotater, referansevedtak
5. ✅ **KOFA praksisbase** — vedtak offentlige anskaffelser
6. ✅ **Skatteklagenemnda** — vedtaksliste
7. ✅ **Finanstilsynet** — vedtak, tillatelser, rundskriv
8. ✅ **Konkurransetilsynet** — vedtak, uttalelser, brev

### Gruppe 2 — ✅ Ferdig
9. ✅ **Regjeringen.no** — proposisjoner, NOU-er, meldinger, rundskriv, høringer
10. ✅ **Skatteetaten** — BFU, prinsipputtalelser, uttalelser
11. ✅ **LDO + Diskrimineringsnemnda** — uttalelser og vedtak
12. ✅ **KFIR** — avgjørelser immaterialrett
13. ✅ **Arbeidstilsynet** — vedtak, tilsynsrapporter
14. ✅ **Riksrevisjonen** — forvaltningsrevisjoner, rapporter

### Gruppe 3 — ✅ Ferdig (delvis)
15. ✅ **Domstol.no** — utvalgte avgjørelser
16. ✅ **Helsedirektoratet** — rundskriv, veiledere, tolkninger
17. ✅ **Trygderetten** — kjennelser
18. ✅ **Husleietvistutvalget** — avgjørelser
19. ✅ **UDI regelverk** — RS/PN/GI
20. ✅ **NPE / Pasientskadenemnda** — vedtak

### Gruppe 4 — Neste (gjenstående)
21. Arbeidsretten (Lovdata ARD), Statsforvalteren
22. Bufdir, IMDi, Medietilsynet, Nkom, NVE, Patentstyret
23. Lovdata NAV, Stortingstidende, Lovdata HIST, Lovdata Rundskriv
24. EUR-Lex (SPARQL), EFTA-domstolen, HUDOC/EMD
25. Komparative kilder (DK, SE)

**Merknad:** Skatteetaten `rettsinformasjon`-API (Maskinporten) er fortsatt et mulig supplement, men krever org.nr. og Altinn-delegering. Gjeldende `skatteetaten.py` bruker åpen HTML-scraping av `/rettskilder/`.
