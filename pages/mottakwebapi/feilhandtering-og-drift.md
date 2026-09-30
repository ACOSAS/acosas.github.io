---
title: Feilhåndtering og drift
permalink: /mottakwebapi_errors.html
---

# Feilhåndtering og drift

## Statuskoder

| Kode | Når |
|---|---|
| 200 | `GET /api/{tenant}/arkivmelding/test` lyktes. Kroppen er en tekststreng med tenant-navn. |
| 201 | Pakken er lagret som importobjekt i Mottak. |
| 400 | Hash stemmer ikke (ren tekst), XSD-feil, eller metadatafil mangler i ZIP (JSON). |
| 404 | Ukjent eller inaktiv tenant-nøkkel. Ruten matcher ikke. |
| 422 | Meldingen kunne ikke behandles. JSON-feltet heter `message`. |
| 500 | Uventet feil, inkludert request som ikke er `multipart/*`. Kroppen er `ProblemDetails`. |

Tjenesten returnerer ikke 415 for feil `Content-Type`. En kropp som ikke er
multipart ender som 500.

### 400 JSON ved validering

```json
{
  "message": "Request er ikke korrekt formatert som en arkivmelding",
  "errors": ["..."],
  "warnings": ["..."],
  "fil": "arkivmelding.xml"
}
```

### 422

```json
{
  "message": "Kunne ikke håndtere innkommet melding"
}
```

### 500

```json
{
  "type": "https://tools.ietf.org/html/rfc9110#section-15.6.1",
  "title": "Server Error",
  "status": 500,
  "detail": "...",
  "instance": "POST /api/{tenant}/arkivmelding"
}
```

## Størrelsesgrenser

Grenseverdiene settes per miljø i konfigurasjonsnøkkelen `Server`:

| Nøkkel | Standard |
|---|---|
| `MaxRequestBody` | 2147483647 (ca. 2 GiB) |
| `ValueLengthLimit` | 2147483647 |
| `MultipartBodyLengthLimit` | 2147483647 |
| `MultipartHeadersLengthLimit` | 2147483647 |

Endepunktene har `DisableRequestSizeLimit` i koden, men Kestrel bruker
`MaxRequestBody`. Avklar faktisk grense med Acos for det aktuelle miljøet.

## Retry og duplikater

`messageId` i manifestet lagres på importobjektet som korrelasjon. Tjenesten
har **ingen unikhetssjekk**. Et nytt POST med samme `messageId` eller samme
ZIP kan gi et nytt importobjekt. Ved timeout eller ukjent resultat: sjekk
status i Mottak+ før du sender på nytt, eller aksepter at retry kan gi
duplikat.

## Kvittering

201 er kø-bekreftelse, ikke arkiveringsbevis. Det finnes ikke et statuskall i
dette API-et som returnerer saks- eller journalpostnummer. Følg saken i
Mottak+ og WebSak etter at mottakerjobben har kjørt.

## Tilkoblingssjekk

Bruk `GET /api/{tenant}/arkivmelding/test` for å verifisere vert, TLS og tenant-nøkkel før
integrasjonen settes i produksjon. Se
[autentisering og tenant](/mottakwebapi_auth.html).
