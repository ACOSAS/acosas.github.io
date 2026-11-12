---
title: Endringslogg for UserAPI
permalink: /userapi_changelog.html
---

# Endringslogg for UserAPI

Oppføringene viser vellykkede bygg fra `master`. Endringer i én eller flere PR-er samles under byggnummeret. Den første oppføringen dekker den verifiserte perioden fra 3.3.32 til 3.3.103.

<!-- BUILD_ENTRIES -->

## 3.3.119 – 2026-11-12

- Forenklet dokumentasjonens oversiktsside og flyttet endringsloggen fra Guider til samme navigasjonsnivå som Oversikt.

Commit: `38a88ca4db942783ccd625100feaf6dde0f26794`.

## 3.3.118 – 2026-11-12

- Ingen kundeorienterte endringsnotater er registrert for dette bygget.

Commit: `baadf940810281b80bc4d4026675992cb6197b91`.

## 3.3.117 – 2026-11-12

- Ingen kundeorienterte endringsnotater er registrert for dette bygget.

Commit: `7638ef4507140d41cbd77823f9369d497bdb910c`.

## 3.3.116 – 2026-11-12

- Ingen kundeorienterte endringsnotater er registrert for dette bygget.

Commit: `142e57e68a32b7c47e8853a8843a559bb20d8efe`.

## 3.3.115 – 2026-11-12

- Ingen kundeorienterte endringsnotater er registrert for dette bygget.

Commit: `6745895da57a44a75a51d74edb5cb8b56e4a2f8f`.

## 3.3.114 – 2026-11-05

- Ingen kundeorienterte endringsnotater er registrert for dette bygget.

Commit: `1d63942c4353d6d112b1c8568588a6992f10cc4a`.

## 3.3.110 – 2026-11-03

- Rettet en feil som hindret brukeroppretting uten brukernavn via det eldre bruker-API-et.
- Rettet en feil som kunne stoppe publisering av kundedokumentasjon når dokumentasjonsbranchen skulle oppdateres fra master.

Commit: `3aaa4faf8bce51fb53658aa12344b4046bf61346`.

## 3.3.106 – 2026-10-29

- Publiser en akkumulerende endringslogg for UserAPI på acosas.github.io. Hvert vellykkede master-bygg får en kort oppføring basert på PR-notatene.

Commit: `efd97b454480b3ccb566e164a6543cdf3287376f`.

## 3.3.104 – 27. oktober 2026

Observability-koden er oppdatert i tråd med Acos sine arkitekturbeslutninger. [PR 1535](https://dev.azure.com/acos-dh/Dokumenthandtering/_git/Acos.WebSak.UserApi/pullrequest/1535).

## 3.3.32–3.3.103

- SCIM 2.0 er innført som beta med provisjonering av brukere, grupper og medlemskap, eget `userapi.scim`-scope, filtrering og ETag-støtte.
- Bruker- og identitetshåndteringen støtter sekundærbrukere, delt IdentityServer-identitet mellom databaser, eksakt e-postsøk og GLM-loginmapping når IdentityServer ikke er konfigurert.
- Nye REST-ruter håndterer aktivering, tilgangsgruppemedlemskap og postfordelere. Eldre GET-ruter som endrer data er markert som utfaset.
- Kundedokumentasjon, OpenAPI-publisering, automatiske tester og avhengigheter er oppdatert.

Startpunktet er commit `404c9c00`; sluttpunktet er commit `c49b0bd8`.
