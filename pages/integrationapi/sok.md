---
title: Søk
permalink: /integrationapi_search.html
---

# Søk

Tre ruter er proxy mot Search API. De krever søke-policyen i tillegg til
integrasjonstokenet, se [autentisering](/integrationapi_auth.html).

| Rute | Indeks |
|---|---|
| `GET /api/integration/search/saker` | `saker` |
| `GET /api/integration/search/journalposter` | `journalposter` |
| `GET /api/integration/search/dokumenter` | `dokumenter` |

Felles query-parametre:

| Parameter | Betydning |
|---|---|
| `q` | Søkestreng. Tom streng sendes videre hvis parameteren mangler. |
| `skip` | Antall treff som hoppes over. |
| `take` | Antall treff som hentes. |
| `save` | Om spørringen skal lagres. |
| `settingsId` | Innstillings-id. Standard 0. |

Andre query-parametre på kallet videresendes. Slik filtreres for eksempel
klassering: `&saksakKlassifikasjoner=<verdi>`.

Proxyen kaller `api/search/{indeks}` på Search API med brukerens bearer-token.
Vellykket svar returneres med Search API sin `Content-Type`. Feilstatus fra
Search API sendes videre med samme kode og kropp.

| Kode fra proxyen | Når |
|---|---|
| 502 | Search API kan ikke nås (`HttpRequestException`). Kroppen er `Bad Gateway - Unable to reach SearchApi`. |
| 504 | Kallet timer ut. Kroppen er `Gateway Timeout - SearchApi request timed out`. |
| 500 | Annen feil i proxyen. Kroppen er `Internal Server Error`. |
