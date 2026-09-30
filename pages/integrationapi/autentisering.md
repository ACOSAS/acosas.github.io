---
title: Autentisering
permalink: /integrationapi_auth.html
---

# Autentisering

`IntegrationController` krever et OAuth2 access token
(`[Authorize(Startup.IntegrationAuthPolicy)]`). OpenAPI beskriver flyten
authorization code mot IdentityServer, med scope `integration` merket
«Access to external websak+ integrations». Operasjonene i dokumentet lister
ikke et påkrevd scope-array. Avklar med miljøets IdentityServer hvilke scopes
policyen faktisk krever.

Send tokenet som bearer:

```http
GET /api/integration/test HTTP/1.1
Host: <websak-pluss-api-vert>
Authorization: Bearer <access-token>
Accept: application/json
```

Manglende eller ugyldig token gir **401**. Token som ikke har tilgang til
API-et eller dataene gir **403**.

Søkerutene under `/api/integration/search/` har i tillegg
`[Authorize(Startup.SearchAuthPolicy)]`. Et token som rekker til de andre
integrasjonsrutene, rekker ikke nødvendigvis til søk.

## Stedfortreder og sekundær brukerkonto

Hvis brukeren opptrer som stedfortreder, må klienten sende én av disse:

- header `x-stedfortreder-id`
- query-parameter `stedfortreder-id`

Hvis brukeren bruker en sekundær brukerkonto:

- header `x-brukerkonto-id`
- query-parameter `brukerkonto-id`

Uten disse kjører kallet som den innloggede brukeren alene.

## Tilkoblingssjekk

`GET /api/integration/test` sjekker at klienten er autorisert. Ved suksess er
kroppen tekststrengen `foo`, ikke et JSON-objekt.
