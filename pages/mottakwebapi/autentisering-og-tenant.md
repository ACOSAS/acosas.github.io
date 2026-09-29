---
title: Autentisering og tenant
permalink: /mottakwebapi_auth.html
---

# Autentisering og tenant

Integrasjonspartnere autentiserer med en **API-nøkkel i URL-stien**, ikke med
OAuth bearer token. Nøkkelen er en GUID og erstatter `{tenant}` i alle ruter:

```http
GET /api/{tenant}/arkivmelding/test
POST /api/{tenant}/arkivmelding
POST /api/{tenant}/arkivmelding/arkiverdokument
```

Eksempel med plassholder:

```http
GET /api/00000000-0000-0000-0000-000000000000/arkivmelding/test HTTP/1.1
Host: <mottak-webapi-vert>
Accept: application/json
```

Ugyldig, inaktiv eller ukjent nøkkel treffer ikke ruten. Klienten får **HTTP
404**, ikke 401 eller 403.

## Tildeling per miljø

Nøkkelen tildeles i **Mottak+** på en aktiv avsendermodul av typen
arkivmelding. Test og produksjon har hver sine nøkler. En ny nøkkel tildeles
ved oppsett mot produksjon. Ikke gjenbruk testnøkkelen i produksjon.

Rotasjon skjer ved at Acos eller kundens Mottak-forvalter oppretter eller
bytter `ApiKey` på avsenderen. Det finnes ikke et eget API-kall for rotasjon.
Etter bytte må integrasjonen bruke den nye GUID-en. Den gamle slutter å
treffe ruten (404).

## Behandle nøkkelen som hemmelighet

- Ikke legg ekte nøkler i dokumentasjon, kildestyring, logger eller
  feilmeldinger som sendes videre.
- Bruk miljøvariabler eller hemmelighetslager i pipeline og runtime.
- Begrens hvem som kan lese nøkkelen i Mottak+.

OpenAPI kan vise intern OAuth for tjenestens egne kall mot fillager. Det er
**ikke** avsenderautentisering. Integrasjonspartnere skal ikke hente token
for å sende arkivmelding.

## Tilkoblingssjekk

Kall `GET /api/{tenant}/arkivmelding/test` før første produksjonsutsending. Ved suksess
returnerer tjenesten HTTP 200 og en tekststreng med tenant-navn, for
eksempel `Arkivmelding test: OK, testet Tenant: <navn>`.
