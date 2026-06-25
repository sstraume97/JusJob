# JusJob

Et verktøy for juridisk research som henter og indekserer norske rettskilder automatisk, og gjør dem søkbare direkte i Zotero.

**[→ Åpne datasiden](https://sstraume97.github.io/JusJob/)** · **[→ Indeks-skjema](docs/indeks-skjema.md)** · **[→ Relaterte ressurser](docs/relaterte-ressurser.md)**

---

## Arkitektur

```mermaid
flowchart TD
    subgraph Kilder["📚 Rettskilder"]
        A1([rettspraksis.no\nMediaWiki API])
        A2([data.stortinget.no\nXML-API])
        A3([sivilombudet.no\nSitemap + HTML])
        A4([kudos.dfo.no\nREST API])
        A5([norwegian-laws\nGitHub Pages JSON])
    end

    subgraph Actions["⚙️ GitHub Actions"]
        B1[pipeline/rettspraksis.py]
        B2[pipeline/stortinget.py]
        B3[pipeline/sivilombudet.py]
        B4[pipeline/kudos.py]
        B5[pipeline/lovdata.py]
        B6[pipeline/build_index.py]
    end

    subgraph Data["💾 data/  ← committes til repo"]
        C1[(rettspraksis.jsonl.gz\n~70 000 avgjørelser)]
        C2[(stortinget.jsonl.gz\n~17 000 saker)]
        C3[(sivilombudet.jsonl.gz\n~1 950 uttalelser)]
        C4[(kudos.jsonl.gz\n~44 000 dokumenter)]
        C5[(lovdata.jsonl.gz\n794 lover + 3 438 forskrifter)]
        C6[(search-index.json)]
    end

    subgraph Pages["🌐 GitHub Pages"]
        D[search-index.json\nsstraume97.github.io/JusJob/]
    end

    subgraph Zotero["🔍 Zotero-plugin"]
        E[Søkevindu\nclient-side filtrering]
        F[Importer som Zotero-item]
    end

    A1 -->|inkrementell, revid-cache| B1
    A2 -->|5 siste sesjoner| B2
    A3 -->|inkrementell via lastmod| B3
    A4 -->|inkrementell via UUID-cache| B4
    A5 -->|laws.json daglig| B5

    B1 --> C1
    B2 --> C2
    B3 --> C3
    B4 --> C4
    B5 --> C5

    C1 & C2 & C3 & C4 & C5 --> B6
    B6 --> C6

    C6 -->|publiseres| D
    D -->|fetch over HTTPS| E
    E -->|velg treff| F
```

Alle datafiler committes til repoet og publiseres via GitHub Pages. Zotero-pluginen søker client-side — ingen server å drifte.

---

## Kilder

| Kilde | Type | Status | Kategori |
|---|---|---|---|
| [rettspraksis.no](https://www.rettspraksis.no) | Høyesterett, lagmannsretter, tingretter | ✅ | Rettsavgjørelser |
| [Stortinget](https://data.stortinget.no) | Saker, Prop., Innst., vedtak | ✅ | Lovverk og forarbeider |
| [Sivilombudet](https://www.sivilombudet.no) | Uttalelser | ✅ | Tilsyn og ombud |
| [KUDOS (DFØ)](https://kudos.dfo.no) | NOU-er, studier, rapporter | ✅ | Forvaltning |
| [norwegian-laws](https://github.com/sondreskarsten/norwegian-laws) | 794 lover + 3 438 forskrifter | ⏳ | Lovverk |
| [Regjeringen.no](https://www.regjeringen.no) | NOU-er, høringer, rundskriv | ⏳ | Lovverk og forarbeider |
| [Domstol.no](https://www.domstol.no) | Fritt tilgjengelige dommer | ⏳ | Rettsavgjørelser |
| [Datatilsynet](https://www.datatilsynet.no) | Vedtak, veiledninger | ⏳ | Tilsyn |
| [Helsetilsynet](https://www.helsetilsynet.no) | Tilsynsrapporter, vedtak | ⏳ | Tilsyn |
| [Riksrevisjonen](https://www.riksrevisjonen.no) | Revisjonsrapporter | ⏳ | Tilsyn |
| [Forbrukertilsynet](https://www.forbrukertilsynet.no) | Vedtak | ⏳ | Tilsyn |
| [LDO / Diskrimineringsnemnda](https://www.diskrimineringsnemnda.no) | Vedtak, uttalelser | ⏳ | Tilsyn |
| [Klagenemdsekretariatet](https://www.klagenemndssekretariatet.no/) | KOFA, Konkurranseklagenemnda m.fl. | ⏳ | Klage og nemnd |
| [Trygderetten](https://www.trygderetten.no) | Kjennelser | ⏳ | Klage og nemnd |
| [Pasientskadenemnda (NPE)](https://www.npe.no) | Vedtak | ⏳ | Klage og nemnd |
| [Husleietvistutvalget](https://www.htu.no) | Avgjørelser | ⏳ | Klage og nemnd |
| [EMD / HUDOC](https://hudoc.echr.coe.int) | Menneskerettsdomstolen | ⏳ | Internasjonal |
| [EFTA/EU-domstolen](https://www.eftacourt.int) | EØS-avgjørelser | ⏳ | Internasjonal |
| [EUR-Lex](https://eur-lex.europa.eu) | EU-forordninger, direktiver | ⏳ | Internasjonal |

Se [docs/indeks-skjema.md](docs/indeks-skjema.md) for detaljert feltdefinisjon og lenkestrategi mellom kilder.

---

## Zotero-plugin

Plugin-en er et skjelett under utvikling. Planlagte funksjoner:

- Søkepanel med filtrering per kilde og kildetyp
- Norsk juridisk sitatstil (CSL): `Rt. 2013 s. 1`, `NOU 2020: 4`, `Lov 1902-05-22 nr 10`
- Zotero Connector-translators per kilde
- Sitatsjekk, forarbeidskjede-bygger, endringshistorikk-varsling
- Eksport til juridisk notat (Word/PDF)
- Automatisk kobling mellom lover, forarbeider og dommer

---

## Kom i gang

```bash
pip install -r requirements.txt
python pipeline/stortinget.py
python pipeline/sivilombudet.py
python pipeline/kudos.py
python pipeline/rettspraksis.py   # tar ~30 min første gang
python pipeline/build_index.py
```

GitHub Actions kjører dette automatisk daglig kl. 03:00 UTC og publiserer til [GitHub Pages](https://sstraume97.github.io/JusJob/).
