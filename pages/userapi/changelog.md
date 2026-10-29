---
title: Endringslogg for UserAPI
permalink: /userapi_changelog.html
---

# Endringslogg for UserAPI

Oppføringene viser vellykkede bygg fra `master`. Endringer i én eller flere PR-er samles under byggnummeret. Den første oppføringen dekker den verifiserte perioden fra 3.3.32 til 3.3.103.

<!-- BUILD_ENTRIES -->

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
