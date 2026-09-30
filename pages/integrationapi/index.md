---
title: WebSak Integration API
permalink: /integrationapi_guide.html
---

# WebSak Integration API

WebSak Integration API lar eksterne systemer lese og oppdatere saker,
journalposter, klassering, tilleggsdata, merknader, skjema og filer i ACOS
WebSak. API-et er skrevet for integrasjonsutviklere.

Dokumentasjonen er på norsk. Tekniske navn i kontrakten (`sakId`, `jpId`,
`ordnVerdi`, `stedfortreder-id`) beholdes som i OpenAPI. Norsk Markdown i
`pages/integrationapi/` er den autoritative kundedokumentasjonen for flyt,
autentisering og feilhåndtering. OpenAPI er detaljkilden for felt og typer.

## Versjon og gyldighet

Dokumentasjonsversjon: 1.0. Den beskriver HTTP-kontrakten i
`_data/swagger/integration.json` (`info.version` `v1`). Filen har ikke
publiseringsmetadata (`x-acos-publication`), så commit og genereringstidspunkt
står ikke på denne siden.

Ved motstrid gjelder denne prioriteten:

1. implementasjon i `IntegrationController`
2. OpenAPI-dokumentet
3. Markdown i `pages/integrationapi/`

## Komponenter og dataflyt

```text
Integrasjonsklient
        |
        |  HTTPS + OAuth2 access token
        |  scope-dekket token mot Integration API
        v
WebSak Integration API
        |
        +--> ACOS WebSak (sak, journalpost, filer, merknader)
        |
        +--> Search API   (kun /api/integration/search/*)
```

Kallene kjører som den autentiserte WebSak-brukeren. Stedfortreder og
sekundær brukerkonto styres med egne headere, se
[autentisering](/integrationapi_auth.html).

## Hva denne guiden dekker

Guidene under beskriver rutene i `IntegrationController`, altså stien
`/api/integration/`. OpenAPI-filen inneholder i tillegg **egendefinerte felt**
(`/api/egendefinerte/`) og **Function Library** (`/api/functionlibrary/`).
De vises i REST-referansen, men er ikke beskrevet i disse guidene.

## Start her

- [Autentisering](/integrationapi_auth.html)
- [Saker og journalposter](/integrationapi_cases.html)
- [Klassering og tilleggsdata](/integrationapi_classification.html)
- [Filer](/integrationapi_files.html)
- [Søk](/integrationapi_search.html)
- [Feilhåndtering](/integrationapi_errors.html)
- [Publiseringsmetadata](/integrationapi_build_metadata.html)

Den genererte REST-referansen publiseres ved siden av disse guidene.
Lenkene bruker `integration__*.html`.
