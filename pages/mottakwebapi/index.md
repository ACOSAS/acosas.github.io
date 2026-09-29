---
title: Acos Mottak WebApi
permalink: /mottakwebapi_guide.html
---

# Acos Mottak WebApi

Mottak WebApi tar imot arkivmeldinger og andre meldingspakker fra eksterne
systemer og legger dem i Acos Mottak. Deretter journalfører Mottak innholdet i
ACOS WebSak via mottakermodulen. API-et er skrevet for integrasjonsutviklere
som skal sende pakker, og for teknisk drift som skal verifisere tilkobling.

Dokumentasjonen er på norsk. Tekniske navn i kontrakten (`tenant`, `type`,
`hash`, `alg`, `contentid`) beholdes som i OpenAPI. Norsk Markdown i
`pages/mottakwebapi/` er den autoritative kundedokumentasjonen.

## Versjon og gyldighet

Dokumentasjonsversjon: 1.0. Den beskriver HTTP-kontrakten for Mottak WebApi
på samme commit som OpenAPI-filen. Publiserte sider viser versjon, commit SHA
og genereringstidspunkt fra bygget som produserte REST-referansen.

Ved motstrid gjelder denne prioriteten:

1. implementasjon og automatiserte tester
2. OpenAPI-dokumentet generert fra samme commit
3. Markdown i `pages/mottakwebapi/`
4. historiske kodeeksempler under `pages/swagger/`

## Komponenter og dataflyt

```text
Integrasjonsklient
        |
        |  HTTPS + tenant-GUID i URL
        |  multipart/related (JSON-manifest + ZIP)
        v
Acos Mottak WebApi
        |
        |  201 når importobjekt er lagret i Mottak
        v
Mottak (regler og importjobb)
        |
        v
MottakerWebsak  -->  ACOS WebSak
```

![Dataflyt fra avsender til WebSak](/pages/mottakwebapi/images/dataflyt.svg)

HTTP 201 betyr at pakken er mottatt og lagret i Mottak. Det er ikke kvittering
på at saken eller journalposten er opprettet i WebSak.

## Start her

- [Autentisering og tenant](/mottakwebapi_auth.html)
- [Sende arkivmelding](/mottakwebapi_send.html)
- [Feilhåndtering og drift](/mottakwebapi_errors.html)
- [Kodeeksempler](/mottakwebapi_examples.html)
- [Publiseringsmetadata](/mottakwebapi_build_metadata.html)

Den genererte REST-referansen publiseres ved siden av disse guidene. OpenAPI
er detaljkilden for ruter, parametere, skjemaer og statuskoder. Multipart-kropp
og feltbeskrivelser er dokumentert i guidene fordi den genererte modelsiden
bare viser navn, type og format.
