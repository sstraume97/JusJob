"""Henter uttalelser fra Sivilombudet (sivilombudet.no).

Ingen offentlig API funnet -- krever skraping av HTML-listesider og
enkeltuttalelser. Vær skånsom: respekter robots.txt og bruk
REQUEST_DELAY_SECONDS mellom forespørsler.

TODO: kartlegg listesidenes URL-struktur og paginering, og implementer
henting + parsing av enkeltuttalelser (saksnummer, dato, tema, konklusjon).
"""
from __future__ import annotations

BASE_URL = "https://www.sivilombudet.no"
REQUEST_DELAY_SECONDS = 1.0


def main() -> None:
    raise NotImplementedError("Sivilombudet-henting er ikke implementert ennå")


if __name__ == "__main__":
    main()
