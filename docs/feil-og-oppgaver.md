# JusJob — feil og oppgaver (logggjennomgang 2026-06-26)

Basert på gjennomgang av GitHub Actions-logger fra kjøringen 2026-06-26.
Bygget index: **117 077 elementer** — deploy til GitHub Pages: OK.

---

## Prioriteringsnivåer

- **[KRITISK]** — scraper henter 0 dokumenter, kilden er helt ute av indeksen
- **[URL-FEIL]** — deler av en scraper feiler pga. endret URL
- **[STRUKTURFEIL]** — HTTP-forespørselen lykkes, men HTML-parsingen finner ingen lenker
- **[WORKFLOW]** — feil i CI/CD-oppsettet

---

## Kritiske feil

### 1. `stortinget.py` — Network unreachable, exit code 1

**Feiltype:** Nettverksfeil (forbigående?)

**Loggutdrag:**
```
urllib3.exceptions.NewConnectionError: HTTPSConnection(host='data.stortinget.no', port=443):
  Failed to establish a new connection: [Errno 101] Network is unreachable
requests.exceptions.ConnectionError: Max retries exceeded with url: /eksport/saker?sesjonid=2025-2026
##[error]Process completed with exit code 1.
```

**Vurdering:** Sannsynligvis forbigående nettverksfeil på GitHub Actions-runner (ikke DNS-blokkering — siden gikk gjennom med exit code 1 og ikke 403/404). Bør verifiseres ved neste kjøring. Hvis det skjer igjen, kan det tyde på at Stortinget blokkerer GitHub Actions IP-range.

**Tiltak:**
- [ ] Kjør manuelt for å verifisere om feilen er vedvarende
- [ ] Legg til `continue-on-error: true` på steget i workflow så én scraper-feil ikke markerer hele jobben som feilet
- [ ] Vurder retry-logikk med eksponentiell backoff i scriptet

---

### 2. `lovdata.py` — alle 4 pakker returnerer 404, 0 dokumenter

**Feiltype:** 404 Not Found på alle pakker

**Loggutdrag:**
```
📦 Norsk Lovtidend avd. I (lovtidend-avd1-2001-2025.tar.bz2)
  ADVARSEL: lovtidend-avd1-2001-2025.tar.bz2 finnes ikke ennå (404) — hopper over
  → lovdata-lovtiend1.jsonl.gz: 0 dokumenter

📦 Norsk Lovtidend avd. I (lovtidend-avd1-2026.tar.bz2)
  ADVARSEL: lovtidend-avd1-2026.tar.bz2 finnes ikke ennå (404) — hopper over

📦 Gjeldende sentrale forskrifter (gjeldende-sentrale-forskrifter.tar.bz2)
  ADVARSEL: gjeldende-sentrale-forskrifter.tar.bz2 finnes ikke ennå (404) — hopper over
  → lovdata-forskrifter.jsonl.gz: 0 dokumenter

📦 Gjeldende lover (gjeldende-lover.tar.bz2)
  ADVARSEL: gjeldende-lover.tar.bz2 finnes ikke ennå (404) — hopper over
  → lovdata-lover.jsonl.gz: 0 dokumenter
```

**Vurdering:** Filnavnene stemmer ikke med det Lovdata faktisk tilbyr i API-et. Tidligere virket `lovtidend-avd1-2001-2024.tar.bz2`, men nå forsøkes `lovtidend-avd1-2001-2025.tar.bz2`. Sannsynligvis har Lovdata oppdatert pakkenavnet, men det er ikke publisert ennå — eller pakkenavn-logikken i scriptet er feil. **Konsekvens: gjeldende lover, sentrale forskrifter og lovtidend er helt ute av indeksen.**

**Tiltak:**
- [ ] Sjekk pakkelisten fra `api.lovdata.no` manuelt for å se hvilke filnavn som faktisk er tilgjengelige
- [ ] Fiks logikken som bestemmer pakkenavn (trolig et år-suffix som nå er feil)
- [ ] Vurder om den historiske filen (2001–2024) fremdeles er tilgjengelig og bør brukes som fallback

---

### 3. `regjeringen.py` — 403 Forbidden på alle 5 dokumentkategorier

**Feiltype:** 403 Forbidden (bot-blokkering)

**Loggutdrag:**
```
📋 PROPOSISJON — https://www.regjeringen.no/no/dokumenter/proposisjoner/id2506404/
  Side 1 (offset 0)...   FEIL: 403 Client Error: Forbidden for url: ...?startCount=0&stopCount=25
  0 lenker — 0 nye proposisjon-dokumenter

📋 NOU — ... 403 Forbidden — 0 nye
📋 STORTINGSMELDING — ... 403 Forbidden — 0 nye
📋 RUNDSKRIV — ... 403 Forbidden — 0 nye
📋 HØRING — ... 403 Forbidden — 0 nye
```

**Vurdering:** `regjeringen.no` blokkerer scriptet — trolig fordi scriptet mangler `User-Agent`-header, eller fordi `?startCount=N&stopCount=N`-query-mønsteret er gjenkjent og blokkert. Siden bruker ~30 sekunder per URL (bot-deteksjon/rate limiting) før den svarer 403.

**Tiltak:**
- [ ] Legg til realistisk `User-Agent`-header (f.eks. Mozilla/5.0) og `Referer`-header
- [ ] Sjekk om `regjeringen.no` har et åpent API eller sitemap som kan brukes i stedet for paginert HTML-scraping
- [ ] Vurder å legge til `time.sleep()` mellom sideforespørsler
- [ ] Test manuelt om URLene fungerer i nettleser

---

### 4. `datatilsynet.py` — alle 3 URLer gir 404

**Feiltype:** 404 Not Found (URL-er endret)

**Loggutdrag:**
```
📋 VEDTAK — https://www.datatilsynet.no/rettigheter-og-plikter/virksomhetenes-plikter/vedtak/
  FEIL: 404 Client Error: Not Found

📋 VARSEL OM VEDTAK — https://www.datatilsynet.no/rettigheter-og-plikter/virksomhetenes-plikter/varsler-om-vedtak/
  FEIL: 404 Client Error: Not Found

📋 UTTALELSE — https://www.datatilsynet.no/regelverk-og-verktoy/uttalelser/
  FEIL: 404 Client Error: Not Found
```

**Tiltak:**
- [ ] Besøk `datatilsynet.no` og finn nye URLer for vedtak, varsler og uttalelser
- [ ] Oppdater URL-konstantene i `pipeline/datatilsynet.py`
- [ ] Sjekk om sidemalen har endret seg slik at HTML-parsingen også må oppdateres

---

### 5. `finanstilsynet.py` — alle 4 URLer gir 404

**Feiltype:** 404 Not Found (URL-struktur endret)

**Loggutdrag:**
```
📋 VEDTAK — https://www.finanstilsynet.no/nyheter/?type=vedtak  →  404
📋 TILLATELSE — https://www.finanstilsynet.no/nyheter/?type=tillatelser  →  404
📋 BREV/UTTALELSE — https://www.finanstilsynet.no/nyheter/?type=brev-og-uttalelser  →  404
📋 RUNDSKRIV — https://www.finanstilsynet.no/nyheter/?type=rundskriv  →  404
```

**Vurdering:** URL-mønsteret `?type=vedtak` fungerer ikke lenger. Finanstilsynet har byttet til en annen listestruktur.

**Tiltak:**
- [ ] Besøk `finanstilsynet.no` og finn nye URLer
- [ ] Oppdater URL-konstantene i `pipeline/finanstilsynet.py`
- [ ] Sjekk ny sidemale og oppdater HTML-parsingen om nødvendig

---

### 6. `une.py` — SSL-sertifikat utløpt på une.no

**Feiltype:** SSL-sertifikat utløpt

**Loggutdrag:**
```
📋 PRAKSISNOTAT — https://une.no/praksis/
  FEIL: SSLError(SSLCertVerificationError(1,
    '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: certificate has expired (_ssl.c:1010)'))

📋 REFERANSEVEDTAK — https://une.no/praksisbase/
  FEIL: SSLError ... certificate has expired
```

**Vurdering:** `une.no` har et utløpt SSL-sertifikat. Dette er UNEs problem å fikse, men vi kan midlertidig omgå det med `verify=False`.

**Tiltak (kortsiktig):**
- [ ] Legg til `session.verify = False` + `urllib3.disable_warnings()` i `une.py`, og logg tydelig advarsel

**Tiltak (langsiktig):**
- [ ] Fjern workaround så snart UNE fikser sertifikatet
- [ ] Sjekk om `http://une.no` (HTTP) er tilgjengelig som alternativ

---

### 7. `skatteklagenemnda.py` — Network unreachable på alle 3 URLer

**Feiltype:** Nettverksfeil (forbigående?)

**Loggutdrag:**
```
📋 https://www.skatteklagenemnda.no/vedtak/
  FEIL: NewConnectionError: Failed to establish a new connection: [Errno 101] Network is unreachable

📋 https://www.skatteklagenemnda.no/avgjorelser/  →  Network is unreachable
📋 https://www.skatteklagenemnda.no/nyheter/vedtak/  →  Network is unreachable
```

**Tiltak:**
- [ ] Verifiser ved neste automatiske kjøring
- [ ] Vurder retry-logikk i `_scraper_base.py`

---

## URL-feil (deler av scraper)

### 8. `helsetilsynet.py` — /klage-og-tilsynssaker/ gir 404

**Loggutdrag:**
```
📋 TILSYNSRAPPORT — https://www.helsetilsynet.no/tilsyn/tilsynsrapporter/  →  40 lenker ✅
📋 PUBLIKASJON — https://www.helsetilsynet.no/publikasjoner/  →  28 lenker ✅
📋 KLAGE/TILSYNSSAK — https://www.helsetilsynet.no/klage-og-tilsynssaker/  →  404
```

**Tiltak:**
- [ ] Finn ny URL for klage- og tilsynssaker på `helsetilsynet.no`
- [ ] Oppdater URL i `pipeline/helsetilsynet.py`

---

### 9. `konkurransetilsynet.py` — uttalelser-URL gir 404

**Loggutdrag:**
```
📋 VEDTAK — https://www.konkurransetilsynet.no/vedtak-og-uttalelser/vedtak/  →  0 lenker (strukturfeil?)
📋 UTTALELSE — https://www.konkurransetilsynet.no/vedtak-og-uttalelser/uttalelser/  →  404
📋 BREV — https://www.konkurransetilsynet.no/vedtak-og-uttalelser/brev/  →  0 lenker (strukturfeil?)
```

**Tiltak:**
- [ ] Finn ny URL for uttalelser på `konkurransetilsynet.no`
- [ ] Se også strukturfeil-oppgaven nedenfor (vedtak + brev)

---

## Strukturfeil (HTTP OK, men 0 lenker funnet)

### 10. `kofa.py` — 0 vedtak funnet på begge URLer

**Loggutdrag:**
```
📋 KOFA — https://www.kofa.no/praksis/    →  0 vedtak funnet, 0 nye
📋 KOFA — https://www.kofa.no/avgjorelser/  →  0 vedtak funnet, 0 nye
```

**Tiltak:**
- [ ] Inspiser `kofa.no/praksis/` og `kofa.no/avgjorelser/` manuelt
- [ ] Finn ny CSS-selektor og oppdater `pipeline/kofa.py`

---

### 11. `konkurransetilsynet.py` — vedtak og brev: 0 lenker

**Loggutdrag:**
```
📋 VEDTAK — https://www.konkurransetilsynet.no/vedtak-og-uttalelser/vedtak/  →  0 lenker
📋 BREV — https://www.konkurransetilsynet.no/vedtak-og-uttalelser/brev/  →  0 lenker
```

**Tiltak:**
- [ ] Inspiser sidene manuelt og oppdater HTML-selektoren i `pipeline/konkurransetilsynet.py`

---

### 12. `skatteetaten.py` — BFU, prinsipputtalelser og meldinger: 0 lenker

**Loggutdrag:**
```
📋 BINDENDE FORHÅNDSUTTALELSE — https://www.skatteetaten.no/rettskilder/type/bindende-forhåndsuttalelser/  →  0 lenker
📋 PRINSIPPUTTALELSE — https://www.skatteetaten.no/rettskilder/type/prinsipputtalelser/  →  0 lenker
📋 UTTALELSE — https://www.skatteetaten.no/rettskilder/type/uttalelser/  →  7 lenker ✅
📋 MELDING — https://www.skatteetaten.no/rettskilder/type/meldinger/  →  0 lenker
```

**Vurdering:** At uttalelser fungerer, tyder på at sidene for BFU, prinsipputtalelser og meldinger faktisk er tomme, eller at HTML-strukturen er ulik.

**Tiltak:**
- [ ] Sjekk om sidene inneholder dokumentlister i nettleser
- [ ] Oppdater HTML-selektoren i `pipeline/skatteetaten.py` om nødvendig

---

### 13. `diskriminering.py` — LDO og Diskrimineringsnemnda: 0 lenker

**Loggutdrag:**
```
📋 Likestillings- og diskrimineringsombudet — https://www.ldo.no/uttalelser-og-avgjorelser/  →  0 lenker
📋 Diskrimineringsnemnda — https://www.diskrimineringsnemnda.no/avgjorelser/  →  0 lenker
```

**Tiltak:**
- [ ] Inspiser begge sidene manuelt
- [ ] Oppdater HTML-selektoren i `pipeline/diskriminering.py`

---

### 14. `arbeidstilsynet.py` — alle 3 kategorier: 0 lenker

**Loggutdrag:**
```
📋 VEDTAK — https://www.arbeidstilsynet.no/om-oss/nyheter/?type=vedtak  →  0 lenker
📋 TILSYNSRAPPORT — https://www.arbeidstilsynet.no/om-oss/nyheter/?type=tilsynsrapport  →  0 lenker
📋 BREV — https://www.arbeidstilsynet.no/om-oss/nyheter/?type=brev  →  0 lenker
```

**Vurdering:** URL-mønsteret `?type=vedtak` minner om finanstilsynet.no — mulig at query-parameteret ikke lenger støttes, eller at siden krever JavaScript-rendering.

**Tiltak:**
- [ ] Sjekk om URL-mønsteret fungerer i nettleser
- [ ] Finn alternativ URL-struktur på `arbeidstilsynet.no`
- [ ] Oppdater `pipeline/arbeidstilsynet.py`

---

### 15. `domstol.py` — alle 3 URLer returnerer ingen lenker

**Loggutdrag:**
```
📋 Domstol.no — https://www.domstol.no/no/domsavgjorelser/   →  (tom, ingen lenketall)
📋 Domstol.no — https://www.domstol.no/domsavgjorelser/      →  (tom, ingen lenketall)
📋 Domstol.no — https://www.domstol.no/no/aktuelt/nyheter/   →  (tom, ingen lenketall)
Totalt 0 nye
```

**Vurdering:** Scriptet prøver tre URL-varianter, men finner ingenting. Trolig bruker `domstol.no` JavaScript til å rendre innholdet (React/Angular SPA), slik at BeautifulSoup ikke finner lenker.

**Tiltak:**
- [ ] Sjekk om `domstol.no` har et søke-API eller sitemap
- [ ] Undersøk om siden er JavaScript-rendret — i så fall kan ikke BeautifulSoup brukes
- [ ] Vurder alternativ tilgang (RSS, Lovdata som kilde for Høyesterettsdommer)

---

### 16. `helsedirektoratet.py` — tolkninger: 0 lenker

**Loggutdrag:**
```
📋 RUNDSKRIV — https://www.helsedirektoratet.no/rundskriv  →  41 lenker ✅
📋 VEILEDER — https://www.helsedirektoratet.no/veiledere  →  100 lenker ✅
📋 LOVFORTOLKNING — https://www.helsedirektoratet.no/tolkninger  →  0 lenker
```

**Tiltak:**
- [ ] Besøk `helsedirektoratet.no/tolkninger` manuelt og sjekk om det er innhold
- [ ] Sammenlign HTML-struktur med rundskriv-siden (som fungerer)
- [ ] Oppdater selektoren i `pipeline/helsedirektoratet.py` om nødvendig

---

### 17. `trygderetten.py` — alle 3 URLer returnerer ingen lenker

**Loggutdrag:**
```
📋 Trygderetten — https://www.trygderetten.no/kjennelser/    →  (tom)
📋 Trygderetten — https://www.trygderetten.no/avgjorelser/   →  (tom)
📋 Trygderetten — https://www.trygderetten.no/no/kjennelser/ →  (tom)
Totalt 0 nye
```

**Vurdering:** Trolig JavaScript-rendret innhold — BeautifulSoup finner ingenting.

**Tiltak:**
- [ ] Sjekk om `trygderetten.no` har søke-API eller sitemap
- [ ] Undersøk om siden er JavaScript-rendret

---

### 18. `husleietvistutvalget.py` — alle 3 URLer returnerer ingen lenker

**Loggutdrag:**
```
📋 Husleietvistutvalget — https://www.htu.no/avgjorelser/  →  (tom)
📋 Husleietvistutvalget — https://www.htu.no/vedtak/       →  (tom)
📋 Husleietvistutvalget — https://www.htu.no/sakstyper/    →  (tom)
Totalt 0 nye
```

**Tiltak:**
- [ ] Besøk `htu.no` manuelt og finn korrekt URL for avgjørelser
- [ ] Sjekk HTML-struktur og oppdater selektor i `pipeline/husleietvistutvalget.py`

---

### 19. `npe.py` — Pasientskadenemnda og NPE: ingen lenker

**Loggutdrag:**
```
📋 Pasientskadenemnda — https://www.helseklage.no/avgjorelser/  →  (tom)
📋 NPE — https://www.npe.no/no/Om-NPE/rettsavgjorelser/        →  (tom)
Totalt 0 nye
```

**Tiltak:**
- [ ] Besøk begge sidene manuelt og finn korrekte URLer og HTML-struktur
- [ ] Oppdater `pipeline/npe.py`

---

### 20. `udi.py` — praksisnotater: 0 lenker

**Loggutdrag:**
```
📋 UDI-RUNDSKRIV — https://udiregelverk.no/no/rettskilder/udi-rundskriv/  →  20 lenker ✅
📋 PRAKSISNOTAT — https://udiregelverk.no/no/rettskilder/udi-praksisnotater/  →  0 lenker
📋 INSTRUKS — https://udiregelverk.no/no/rettskilder/departementets-rundskriv-og-instrukser/  →  20 lenker ✅
```

**Tiltak:**
- [ ] Besøk `udiregelverk.no/no/rettskilder/udi-praksisnotater/` manuelt
- [ ] Sjekk om URL er korrekt og om HTML-strukturen er ulik de andre kategoriene

---

## Workflow-feil

### 21. Exit code 1 fra enkeltscrapere markerer hele jobben som feilet

**Problem:** `stortinget.py` avslutter med exit code 1 (ukontrollert exception), noe som markerer hele GitHub Actions-jobben som failed — selv om alle andre scrapere kjørte og indeksen ble bygget OK.

**Konsekvens:** GitHub-jobben vises som rød selv om 95 % av pipelinen fungerte. Gjør det vanskelig å skille "total feil" fra "én scraper feilet".

**Tiltak:**
- [ ] Legg til `continue-on-error: true` på alle enkelt-scraper-steg i workflow-filen
- [ ] Alternativt: wrap alle scrapere i try/except og exit med code 0, men logg feilen
- [ ] Vurder å aggregere feil og skrive en feiltabell til slutt i loggen

---

## Status per kilde — kjøring 2026-06-26

| Scraper | Status | Dokumenter i indeks |
|---|---|---|
| `rettspraksis.py` | ✅ OK | 70 377 (cachet) |
| `kudos.py` | ✅ OK | 43 844 (6 nye) |
| `sivilombudet.py` | ✅ OK | 1 957 (cachet) |
| `norwegian_laws.py` | ✅ OK | 794 |
| `forbrukertilsynet.py` | ✅ OK | 470 (0 nye) |
| `kfir.py` | ✅ OK | 147 (0 nye) |
| `riksrevisjonen.py` | ✅ OK | 26 (0 nye) |
| `helsedirektoratet.py` | ⚠️ Delvis | Rundskriv + veiledere OK, tolkninger: 0 |
| `helsetilsynet.py` | ⚠️ Delvis | Tilsynsrapporter + publikasjoner OK, klagesaker: 404 |
| `udi.py` | ⚠️ Delvis | Rundskriv + instruks OK, praksisnotater: 0 |
| `skatteetaten.py` | ⚠️ Delvis | Uttalelser OK (7), resten: 0 |
| `konkurransetilsynet.py` | ⚠️ Delvis | Uttalelser: 404, vedtak + brev: 0 |
| `stortinget.py` | ❌ Kritisk | 0 — Network unreachable |
| `lovdata.py` | ❌ Kritisk | 0 — alle pakker 404 |
| `regjeringen.py` | ❌ Kritisk | 0 — 403 Forbidden |
| `datatilsynet.py` | ❌ Kritisk | 0 — alle URLer 404 |
| `finanstilsynet.py` | ❌ Kritisk | 0 — alle URLer 404 |
| `une.py` | ❌ Kritisk | 0 — SSL-sertifikat utløpt |
| `skatteklagenemnda.py` | ❌ Kritisk | 0 — Network unreachable |
| `kofa.py` | ❌ Strukturfeil | 0 |
| `diskriminering.py` | ❌ Strukturfeil | 0 |
| `arbeidstilsynet.py` | ❌ Strukturfeil | 0 |
| `domstol.py` | ❌ Strukturfeil | 0 — trolig JS-rendret |
| `trygderetten.py` | ❌ Strukturfeil | 0 — trolig JS-rendret |
| `husleietvistutvalget.py` | ❌ Strukturfeil | 0 |
| `npe.py` | ❌ Strukturfeil | 0 |
