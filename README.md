# JusJob

Et verktøy for juridisk research som henter og indekserer norske rettskilder automatisk, og gjør dem søkbare direkte i Zotero.

**[→ Åpne datasiden](https://sstraume97.github.io/JusJob/)** · **[→ Indeks-skjema](docs/indeks-skjema.md)** · **[→ Relaterte ressurser](docs/relaterte-ressurser.md)**

---

## Arkitektur

```mermaid
flowchart TD
    subgraph Kilder["📚 Rettskilder (30 aktive)"]
        A1([rettspraksis.no\nMediaWiki API])
        A2([data.stortinget.no\nXML-API])
        A4([kudos.dfo.no\nREST API])
        A5([api.lovdata.no\ntar.bz2 + XML])
        A6([regjeringen.no\nProp./NOU/Meld./rundskriv])
        A7([20 tilsyn, nemnder og domstoler\nDatatilsynet, UNE, KOFA, Domstol.no,\nTrygderetten, NPE, UDI, m.fl.])
    end

    subgraph Actions["⚙️ GitHub Actions"]
        B1[rettspraksis.py / stortinget.py\nsivilombudet.py / kudos.py]
        B5[lovdata.py + norwegian_laws.py\nsubjects-berikelse]
        B6[regjeringen.py + 20 tilsyn-scrapere\n(deler _scraper_base.py)]
        B7[pipeline/build_index.py]
    end

    subgraph Data["💾 data/  ← committes til repo"]
        C1[(rettspraksis / stortinget /\nsivilombudet / kudos .jsonl.gz)]
        C5[(lovdata-lover / -forskrifter /\n-lovtiend1 .jsonl.gz)]
        C6[(regjeringen, datatilsynet, une,\nkofa, domstol, npe … — 21 filer)]
        C9[(search-index.json)]
    end

    subgraph Pages["🌐 GitHub Pages"]
        D[search-index.json\nsstraume97.github.io/JusJob/]
    end

    subgraph Zotero["🔍 Zotero-plugin"]
        E[Søkevindu\nclient-side filtrering]
        F[Importer som Zotero-item]
    end

    A1 & A2 & A4 -->|inkrementell cache| B1
    A5 -->|daglig, lastModified-cache| B5
    A6 & A7 -->|inkrementell URL-cache| B6

    B1 --> C1
    B5 --> C5
    B6 --> C6

    C1 & C5 & C6 --> B7
    B7 --> C9

    C9 -->|publiseres| D
    D -->|fetch over HTTPS| E
    E -->|velg treff| F
```

Alle datafiler committes til repoet og publiseres via GitHub Pages. Zotero-pluginen søker client-side — ingen server å drifte.

---

## Kilder

**30 aktive datakilder.** Se [docs/kilder.md](docs/kilder.md) for full integrasjonsplan og teknisk vurdering per kilde.

### ✅ Aktive

| Kilde | Type | Kategori |
|---|---|---|
| [rettspraksis.no](https://www.rettspraksis.no) | Høyesterett, lagmannsretter, tingretter (~70 000) | Rettsavgjørelser |
| [Stortinget](https://data.stortinget.no) | Saker, Prop., Innst., vedtak (~17 000) | Lovverk og forarbeider |
| [Sivilombudet](https://www.sivilombudet.no) | Uttalelser (~1 950) | Tilsyn og ombud |
| [KUDOS (DFØ)](https://kudos.dfo.no) | NOU-er, studier, rapporter (~44 000) | Forvaltning |
| [Lovdata](https://lovdata.no) | ~782 lover, ~3 733 forskrifter, Norsk Lovtiend avd. 1 | Lovverk |
| [Forbrukertilsynet](https://www.forbrukertilsynet.no) | Vedtak, Markedsrådet, FKU, veiledninger | Tilsyn |
| [Regjeringen.no](https://www.regjeringen.no) | Proposisjoner, NOU-er, meldinger, rundskriv, høringer | Lovverk og forarbeider |
| [Datatilsynet](https://www.datatilsynet.no) | Vedtak, varsler, uttalelser | Tilsyn |
| [Helsetilsynet](https://www.helsetilsynet.no) | Tilsynsrapporter, publikasjoner | Tilsyn |
| [UNE](https://une.no) | Praksisnotater, referansevedtak | Klage og nemnd |
| [KOFA](https://www.kofa.no) | Vedtak — offentlige anskaffelser | Klage og nemnd |
| [Konkurransetilsynet](https://www.konkurransetilsynet.no) | Vedtak, uttalelser, brev | Tilsyn |
| [Finanstilsynet](https://www.finanstilsynet.no) | Vedtak, tillatelser, rundskriv | Tilsyn |
| [Skatteklagenemnda](https://www.skatteklagenemnda.no) | Vedtak (skatterett) | Klage og nemnd |
| [Skatteetaten](https://www.skatteetaten.no/rettskilder/) | BFU, prinsipputtalelser, uttalelser | Skatt |
| [LDO + Diskrimineringsnemnda](https://www.diskrimineringsnemnda.no) | Uttalelser, vedtak | Klage og nemnd |
| [KFIR](https://www.kfir.no) | Avgjørelser — patent, varemerke, design | Klage og nemnd |
| [Arbeidstilsynet](https://www.arbeidstilsynet.no) | Vedtak, tilsynsrapporter | Tilsyn |
| [Riksrevisjonen](https://www.riksrevisjonen.no) | Forvaltningsrevisjoner, rapporter | Tilsyn |
| [Domstol.no](https://www.domstol.no) | Utvalgte/prinsipielle avgjørelser | Rettsavgjørelser |
| [Helsedirektoratet](https://www.helsedirektoratet.no) | Rundskriv, veiledere, lovfortolkninger | Forvaltning |
| [Trygderetten](https://www.trygderetten.no) | Kjennelser | Klage og nemnd |
| [Husleietvistutvalget](https://www.htu.no) | Avgjørelser i husleietvister | Klage og nemnd |
| [UDI regelverk](https://udiregelverk.no) | Rundskriv (RS), praksisnotater (PN), instrukser (GI) | Forvaltning |
| [NPE / Pasientskadenemnda](https://www.helseklage.no) | Vedtak, erstatningsutmålinger | Klage og nemnd |

### ⏳ Planlagte (utvalg)

Arbeidsretten · Statsforvalteren · Bufdir · IMDi · Medietilsynet · Nkom · NVE · Patentstyret · Lovdata NAV · [EMD/HUDOC](https://hudoc.echr.coe.int) · [EFTA-domstolen](https://www.eftacourt.int) · [EUR-Lex](https://eur-lex.europa.eu)

Se [docs/indeks-skjema.md](docs/indeks-skjema.md) for detaljert feltdefinisjon og lenkestrategi mellom kilder.

---

## Zotero-plugin

Plugin-en er et skjelett under utvikling. Planlagte funksjoner:

- Søkepanel med filtrering per kilde og kildetyp
- Norsk juridisk sitatstil (CSL): `Rt. 2013 s. 1`, `NOU 2020: 4`, `Lov 1902-05-22 nr 10`
- Zotero Connector-translators per kilde (se [`translators/`](translators/))
- Sitatsjekk, forarbeidskjede-bygger, endringshistorikk-varsling
- Eksport til juridisk notat (Word/PDF)
- Automatisk kobling mellom lover, forarbeider og dommer

---

## Kom i gang

```bash
pip install -r requirements.txt

# Lovverk og forarbeider
python pipeline/stortinget.py
python pipeline/kudos.py
python pipeline/rettspraksis.py        # tar ~30 min første gang
python pipeline/norwegian_laws.py      # bygger rettsområde-indeks (kjør før lovdata)
python pipeline/lovdata.py             # lover, forskrifter, Lovtiend avd. 1
python pipeline/regjeringen.py         # proposisjoner, NOU, meldinger, rundskriv, høringer

# Tilsyn og nemnder
python pipeline/sivilombudet.py
python pipeline/forbrukertilsynet.py
python pipeline/datatilsynet.py
python pipeline/helsetilsynet.py
python pipeline/une.py
python pipeline/kofa.py
python pipeline/konkurransetilsynet.py
python pipeline/finanstilsynet.py
python pipeline/skatteklagenemnda.py
python pipeline/skatteetaten.py
python pipeline/diskriminering.py
python pipeline/kfir.py
python pipeline/arbeidstilsynet.py
python pipeline/riksrevisjonen.py
python pipeline/domstol.py
python pipeline/helsedirektoratet.py
python pipeline/trygderetten.py
python pipeline/husleietvistutvalget.py
python pipeline/udi.py
python pipeline/npe.py

# Bygg samlet søkeindeks
python pipeline/build_index.py
```

GitHub Actions kjører dette automatisk daglig kl. 03:00 UTC og publiserer til [GitHub Pages](https://sstraume97.github.io/JusJob/). Alle scraper-steg er inkrementelle (URL-/cache-basert) og kjører med `continue-on-error`, så én kilde som er nede stopper ikke de andre.
