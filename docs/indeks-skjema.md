# JusJob søkeindeks — feltskjema

Definerer hvilke felter som indekseres per kilde og det felles søkeindeks-formatet.

---

## Felles søkeindeks (search-index.json)

Alle kilder konverteres til dette formatet. Felter merket `*` er nye (ikke implementert ennå).

```json
{
  "id":           "rettspraksis-12345",
  "source":       "rettspraksis.no",
  "type":         "rettsavgjørelse",
  "title":        "HR-2020-123-A",
  "court_or_body": "Høyesterett",
  "url":          "https://...",
  "snippet":      "Første 300 tegn ...",

  "date":         "2020-03-15",          // *
  "eli":          "/eli/lov/1902/05/22", // * kun for lover/forskrifter
  "citation":     "HR-2020-123-A",       // * offisiell sitering
  "keywords":     ["erstatning", "..."], // *
  "pdf_url":      "https://...",         // * der tilgjengelig
  "authors":      "Dommer Bergsjø",      // *

  "links": {                             // * koblinger til andre dokumenter
    "eli":        "/eli/lov/1902/05/22",      // lov dette gjelder
    "hjemmel":    ["LOV-2001-06-15-59-§7"],   // hjemmelsreferanser
    "relaterte":  ["stortinget-12345"]         // relaterte saker i indeksen
  }
}
```

---

## Per kilde

### Lover — norwegian-laws (laws.json)

| Felt (rådata) | Indeksert som | Merknad |
|---|---|---|
| `refid` | `id` → `lov-{refid}` | |
| `eli` | `eli` | Nøkkel for lenking |
| `tittel` | `title` | |
| `korttittel` | `citation` | |
| `forkortelse` | `keywords[0]` | f.eks. "aml", "strl" |
| `departement` | `court_or_body` | |
| `rettsomrade` | `keywords` | |
| `ikrafttredelse` | `date` | |
| `sist_endret` (refid) | `links.relaterte` | Peker til endringslov |
| `lovdata`-URL | `url` | |

### Forskrifter — norwegian-laws

Samme som lover, pluss:

| Felt | Indeksert som | Merknad |
|---|---|---|
| `hjemmel` (liste av LOV/FOR-refs) | `links.hjemmel` | f.eks. `LOV-2001-06-15-59-§7` |
| `overordnet_lov` (utledet fra hjemmel) | `links.eli` | Lenke til moderlov |

### Rettsavgjørelser — rettspraksis.no

| Felt (rådata) | Indeksert som | Merknad |
|---|---|---|
| `title` | `title` + `citation` | HR-2020-123-A, Rt. 2013 s. 1 |
| `court` | `court_or_body` | |
| `snippet` | `snippet` | |
| Utledet fra title | `date` | Parse dato fra HR-/RG-/Rt.-format |
| Utledet fra title | `keywords` | Rt., HR-, RG- som egne søkeord |
| Fra wikitext | `links.hjemmel` | Lovhenvisninger i teksten |
| Fra wikitext | `authors` | Dommere |

**Sitatformat-parsing:**
- `HR-2020-123-A` → dato: 2020, instans: Høyesterett
- `Rt. 2013 s. 1170` → dato: 2013, publisert: Retstidende
- `LB-2019-12345` → instans: Lagmannsrett (Borgarting)
- `RG 2010 s. 45` → Rettens Gang (underrett)

### Stortinget

| Felt (rådata) | Indeksert som | Merknad |
|---|---|---|
| `tittel` | `title` | |
| `dokumentgruppe` | `type` | Prop., Innst., NOU, Dok. 8 |
| `sesjon` | `date` (sesjon) | f.eks. "2024-2025" |
| `komite` | `court_or_body` | |
| `henvisning` | `citation` | "Prop. 57 L (2024–2025)" |
| `sist_oppdatert` | `date` | |
| Utledet fra tittel | `links.eli` | Hvilken lov gjelder saken |
| Tilknyttede saker* | `links.relaterte` | NOU→Prop.→Innst.→vedtak |

### Sivilombudet

| Felt (rådata) | Indeksert som | Merknad |
|---|---|---|
| `title` | `title` | |
| `case_number` | `citation` | f.eks. "2023/4521" |
| `published` | `date` | Allerede lagret, ikke indeksert |
| `summary` | `snippet` | |
| `url` | `url` | |

### KUDOS (DFØ)

| Felt (rådata) | Indeksert som | Merknad |
|---|---|---|
| `title` | `title` | |
| `type` | `type` | NOU, Studie, Kartlegging, osv. |
| `abstract` | `snippet` | |
| `owners` | `court_or_body` | |
| `publish_date` | `date` | Lagret, ikke indeksert |
| `authors` | `authors` | Ikke lagret ennå |
| `pdf_url` | `pdf_url` | Ikke lagret ennå |
| `language` | (filtrering) | Ikke lagret ennå |

---

## Lenkestrategi

Dokumenter lenkes via felles identifikatorer:

```
Lov (eli: /eli/lov/2001/06/15-59)
  ↕ eli-nøkkel
Forskrift (hjemmel: LOV-2001-06-15-59-§7)
  ↕ tittelmatching
Stortingssak (tittel inneholder lovnavn)
  ↕ sak-ID
Innstilling, Lovvedtak (tilknyttede saker fra API)
  ↕ lovhenvisning i tekst
Rettsavgjørelse (lovhenvisninger i wikitext/fulltekst)
```

Implementeres trinnvis i `build_index.py` etter at alle kilder er på plass.
