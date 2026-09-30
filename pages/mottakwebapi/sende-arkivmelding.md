---
title: Sende arkivmelding
permalink: /mottakwebapi_send.html
---

# Sende arkivmelding

En innsending er én pakke: metadata som XML, og eventuelle vedlegg. Avsenderen
legger disse filene i **én ZIP** og sender ZIP-filen. Mottak pakker den ut,
finner metadatafilen og tar med vedleggene. XML-en lastes derfor ikke opp
alene. Sjekksummen i manifestet gjelder **hele ZIP-filen**.

Slik bygges pakken:

1. Legg metadatafilen og eventuelle vedlegg i ZIP-en.
2. For `/arkivmelding` heter metadatafilen som standard `arkivmelding.xml`.
   Avsenderen kan overstyre filnavnet i Mottak+ (`MetadataFilnavn`).
3. For `/arkiverdokument` er `MetadataFilnavn` påkrevd i avsenderoppsettet.
   Det navnet er metadatafilen Mottak leter etter i ZIP-en.

Begge innsendingsrutene bruker `POST` og `multipart/related`: JSON-manifest
først, deretter ZIP-filen. Forskjellen er hva som ligger i ZIP-en, og hvordan
Mottak tolker metadata.

| Rute | Når den skal brukes | `type` i manifest |
|---|---|---|
| `POST /api/{tenant}/arkivmelding` | ZIP inneholder KS/Noark-arkivmelding | `arkivmelding` |
| `POST /api/{tenant}/arkivmelding/arkiverdokument` | ZIP inneholder annen meldings-XML styrt av avsenderoppsettet | `melding` |

Hvis `type` er `arkivmelding` på `/arkiverdokument`, hoppes XSD-validering over
på den ruten.

XSD-validering på `/arkivmelding` styres av avsenderoppsettet. Når validering
er på, sjekkes XML mot avsenderens XSD-filer (standard `arkivmelding.xsd` og
`metadatakatalog.xsd`). Navnerommet avgjør om pakken tolkes som V1, V2 eller
FIKS.

## Oppbygging av multipart/related

Rekkefølgen er påkrevd: **JSON-manifest først**, deretter ZIP.

1. Sett `Content-Type` på hele forespørselen til
   `multipart/related; boundary=<unik-streng>`.
2. Første del: JSON med `Content-Type: application/json`.
3. Andre del: ZIP med
   `Content-Disposition: form-data; name="arkivmelding"` eller `name="melding"`,
   `filename` lik `files[].filename`,
   `Content-Type: application/zip` og
   `Content-Id` lik `files[].contentid`.

Parseren matcher ZIP mot manifestet på **filnavn**. `Content-Id` skal likevel
være identisk med `contentid` i JSON.

## Manifest

```json
{
  "type": "arkivmelding",
  "messageId": "<valgfri-korrelasjons-id>",
  "files": [
    {
      "contentid": "content1",
      "filename": "arkivmelding.zip",
      "hash": "<SHA256-HEX>",
      "alg": "SHA256",
      "metadata": false
    }
  ]
}
```

| Felt | Påkrevd | Gyldige verdier |
|---|---|---|
| `type` | ja | `arkivmelding` eller `melding` |
| `messageId` | nei | valgfri korrelasjons-id. Lagres på importobjektet |
| `skjemaId` | nei | brukes særlig på `/arkiverdokument` |
| `files` | ja | minst én filbeskrivelse |
| `files[].contentid` | ja | må matche `Content-Id` på ZIP-delen |
| `files[].filename` | ja | må matche `filename` i `Content-Disposition` |
| `files[].hash` | ja | sjekksum av **hele ZIP-filen** |
| `files[].alg` | ja | `SHA256` (anbefalt), `SHA512` eller `MD5` |
| `files[].metadata` | nei | `false` for ZIP-pakken |

`apikey` og `modulid` settes av tjenesten. Ikke send dem i manifestet.

## Hash

Beregn hash av ZIP-filens bytes, ikke av XML-innholdet alene. Sammenligningen
er eksakt, så bruk samme alfabet som serveren. Kundeksemplene bruker SHA256
som heksadesimal streng med store bokstaver.

Feil hash gir HTTP 400 med tekst på formen
`<filnavn> bestod ikke hash validering`.

## ZIP-innhold

ZIP-filen må inneholde metadatafilen. Vedlegg og øvrige binærfiler i pakken
følger med inn i Mottak. Mangler metadatafilen, returnerer tjenesten HTTP 400
med JSON `{ "message", "fil" }`.

Skjemaversjon leses fra XML-navnerommet når XSD-validering er på. Feil mot
XSD gir HTTP 400 med `message`, `errors`, `warnings` og `fil`.

## Svar ved suksess

HTTP **201 Created**. Kroppen er JSON for den mottatte filen:

```json
{
  "contentid": "content1",
  "filename": "arkivmelding.zip",
  "hash": "<SHA256-HEX>",
  "alg": "SHA256",
  "metadata": false
}
```

Dette er ikke saksnummer eller journalpostnummer fra WebSak. Se
[feilhåndtering og drift](/mottakwebapi_errors.html) for kvittering og retry.
