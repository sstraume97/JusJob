# JusJob – Zotero-plugin (skjelett)

Søker mot `search-index.json` (generert av [`/pipeline`](../pipeline) og
publisert via GitHub Pages) direkte inni Zotero, og lar deg importere treff
som Zotero-items.

## Status: **utestet**

Dette er bygget etter Zotero 7 sin dokumenterte bootstrap-konvensjon
(manifest.json + bootstrap.js + chrome.manifest), men er ikke kjørt i en
faktisk Zotero-installasjon ennå. Sannsynlige feilkilder ved første test:

- `Components.classes["@zotero.org/Zotero;1"]`-trikset for å nå
  `Zotero`-objektet fra et `openDialog`-vindu kan måtte justeres avhengig av
  Zotero 7s nøyaktige Gecko-versjon.
- `INDEX_URL` i `chrome/content/jusjob/search.js` peker på
  `https://sstraume97.github.io/JusJob/search-index.json`, som ikke
  eksisterer før GitHub Pages er satt opp for `jusjob-data`-pipelinen.
- Item-type-mapping (`case` for rettsavgjørelser, `document` for resten) er
  et utgangspunkt, ikke ferdig tilpasset norsk juridisk sitering.

## Hvordan teste i Zotero 7

1. Åpne Zotero → **Verktøy → Innstillinger → Avansert → Generelt** → kryss av
   "Vis menyen Feilsøking i menylinjen".
2. **Feilsøking → Last inn tillegg fra disk…** → velg `plugin/`-mappen
   (den som inneholder `manifest.json`).
3. Sjekk **Verktøy**-menyen i Zotero for "Søk i rettskilder (JusJob)…".
4. Åpne feilsøkingskonsollen (**Feilsøking → Vis feilsøkingsutgang**) for å
   se eventuelle JavaScript-feil hvis vinduet ikke åpnes eller søket ikke
   fungerer.

## Struktur

```
plugin/
  manifest.json        – Zotero 7 plugin-manifest
  chrome.manifest       – registrerer chrome://jusjob/content/
  bootstrap.js          – legger til menyvalg i Verktøy-menyen
  chrome/content/jusjob/
    search.xhtml         – søkevindu (XUL + HTML)
    search.js             – henter search-index.json, filtrerer, importerer
```
