---
title: REST UserAPI
permalink: /userapi_rest_guide.html
---

# REST UserAPI

Det ordinære REST-grensesnittet ligger under `/api/` og krever OAuth 2.0-scope
`userapi`. Bruk JSON med `Content-Type: application/json`. OpenAPI-referansen er
den komplette kontrakten; tabellene her beskriver anbefalte kundearbeidsflyter.
REST UserAPI er produksjonsgrensesnittet og er ikke omfattet av SCIMs
beta-status.

## Brukere

| Operasjon | Anbefalt rute | Merknad |
|---|---|---|
| Liste | `GET /api/Users` | paginering med `limit` og `offset` |
| Hent | `GET /api/Users/{id}` | `lookupField=Id` er standard; `Code` støttes |
| Opprett | `POST /api/Users` | kan inkludere første `userAccesses`-mapping; returnerer `409` når bruker finnes og `feilVedEksisterende=true` |
| Oppdater profil | `PUT /api/Users/{id}` | full profilpayload; endrer ikke loginmapping, roller eller tilgangskoder direkte |
| Aktiver | `PUT /api/v2/users/{userGidId}/activation` | riktig V2-mutasjon |
| Deaktiver | `DELETE /api/v2/users/{userGidId}/activation` | setter sluttdato; sletter ikke fysisk |
| Les loginmapping | `GET /api/Users/{id}/useraccesses` | `id` er numerisk GID-ID |
| Erstatt loginmapping | `PUT /api/Users/{id}/useraccesses` | payload er en ikke-tom `userAccesses`-liste |

Ved oppretting anbefales en godkjent `accessTemplateId`. Hvis både
`departmentCode` og `externalDepartmentId` sendes, har `departmentCode`
prioritet. `externalDepartmentId` skal være én eksakt verdi.

### Brukerprofil og loginmapping

Brukerprofil og loginmapping er separate ressurser. Ved oppretting av en
ordinær primærbruker kan `userAccesses` sendes i samme
`POST /api/Users`. UserAPI oppretter da mappingen etter at WebSak-brukeren er
opprettet. REST-responsens `externalId` er IdentityServers interne ID
(`Gid_EksternID`); verdien genereres av tjenesten og skal ikke sendes av
klienten.

`PUT /api/Users/{id}` oppdaterer brukerprofilen. Den oppdaterer ikke
`userAccesses`, selv om feltet vises i den delte `UserRequest`-modellen i
OpenAPI. For en eksisterende bruker skal loginmappingen leses og erstattes via
henholdsvis `GET` og `PUT /api/Users/{id}/useraccesses`. Det separate PUT-kallet
er bare nødvendig når mappingen skal opprettes eller endres.

`userAccessFunctions`, `userAccessCodes` og `userRoles` er heller ikke direkte
skrivefelter i brukerprofil-PUT. Bruk en godkjent `accessTemplateId` eller de
dedikerte rutene for tilgangskoder og roller. Ikke send en komplett GET-respons
tilbake som POST/PUT-payload; bygg en operasjonsspesifikk request.

Hvis en eksisterende bruker mangler `externalId`, skal klienten ikke opprette
en ny WebSak-bruker. Les nåtilstanden, erstatt loginmappingen via
`PUT /api/Users/{id}/useraccesses`, og kontroller deretter både mappingen og
`externalId` på nytt.

### Sekundærbruker

Sekundærbrukere støttes via `POST /api/Users`. De kobles til én aktiv
primærbruker ved å matche normalisert primær e-postadresse.

```json
{
  "isSecondaryUser": true,
  "code": "SEK123",
  "name": "Eksempel Sekundær",
  "mailAddresses": ["person@example.no"],
  "departmentCode": "ADM-ENHET",
  "accessTemplateId": "<rettighetsmal-id>"
}
```

En sekundærbruker må ha minst én e-postadresse og kan ikke inneholde `username`
eller `userAccesses`. Nøyaktig én aktiv primærbruker må ha samme e-post. Ingen
treff gir `400`; flere treff gir `409`. Kunden må derfor rydde duplikate
e-postadresser før provisjonering.

## Avdelinger

Bruk V2-ruten `/api/v2/departments`. Aliaset `/api/v2/departmentsv2` er
deprecated.

| Operasjon | Rute |
|---|---|
| Hierarkisk liste | `GET /api/v2/departments` |
| Flat liste | `GET /api/v2/departments/flat` |
| Hent på intern ID | `GET /api/v2/departments/{id}` |
| Hent på ekstern ID | `GET /api/v2/departments/external/{externalId}` |
| Opprett | `POST /api/v2/departments` |
| Oppdater | `PUT /api/v2/departments/{id}` |
| Aktiver | `PUT /api/v2/departments/{departmentId}/activation` |
| Deaktiver | `DELETE /api/v2/departments/{departmentId}/activation` |
| Legg til postfordeler | `PUT /api/v2/departments/external/{externalId}/post-distributors/{userGidId}` |
| Fjern postfordeler | `DELETE /api/v2/departments/external/{externalId}/post-distributors/{userGidId}` |

Avdelingens `externalId` lagres i `Gid_DIV1` og må være én eksakt ekstern ID.
Ikke bruk pipe-separerte ID-er. Hvis flere eksterne organisasjonsenheter skal
samles til én WebSak-avdeling, må mappingen gjøres i kildesystemet eller i et
eksplisitt integrasjonslag før kallet til UserAPI.

Oppretting og vedlikehold har viktige regler for forelder, kortbetegnelse,
fullstendig PUT og deaktivering. Følg den egne
[avdelingsguiden](/userapi_rest_departments.html) før integrasjonen settes i drift.

## Roller og tilgangsfunksjoner

Roller beskriver lese-/skrivetilgang og organisatoriske avgrensninger.
Tilgangsfunksjoner beskriver handlingene brukeren kan utføre. Bruk helst
`accessTemplateId` ved oppretting og oppdatering, slik at et godkjent sett av
roller og funksjoner tildeles samlet.

REST-referansen inneholder også ruter for å lese og vedlikeholde roller og
tilgangskoder direkte. Direkte endringer krever mer kundespesifikk kontroll og
bør bare brukes når malbasert tildeling ikke dekker behovet.

Se [guiden for roller og tilgangsfunksjoner](/userapi_rest_roles.html) for forskjellen
mellom rolle-ID, konkret `roleId`, access codes, rettighetsmal og loginmapping.

## Tilgangsgrupper

| Operasjon | Rute |
|---|---|
| Liste | `GET /api/AccessGroups` |
| Hent | `GET /api/AccessGroups/{id}` |
| Opprett | `POST /api/AccessGroups` med `groupName` |
| Liste medlemmer | `GET /api/AccessGroups/members/{id}` |
| Legg til medlem | `PUT /api/v2/accessgroups/{accessGroupId}/members/{userGidId}` |
| Fjern medlem | `DELETE /api/v2/accessgroups/{accessGroupId}/members/{userGidId}` |
| Legg til etter navn | `PUT /api/v2/accessgroups/by-name/{name}/members/{userGidId}` |
| Fjern etter navn | `DELETE /api/v2/accessgroups/by-name/{name}/members/{userGidId}` |

Foretrekk ID-baserte ruter når klienten har gruppe-ID. Navn kan endres og er
derfor en svakere korrelasjonsnøkkel.

Se [guiden for tilgangsgrupper](/userapi_rest_access_groups.html) for gyldighet,
idempotente medlemskapsendringer og begrensningene for saks- og journalgrupper.

## Identiteter og soner

`/api/Identities` gjelder identitetskategorier 2 og 3, som kontakt- og
organisasjonsidentiteter. Endepunktet oppretter ikke en WebSak-bruker og
registrerer ikke loginmapping i IdentityServer. `/api/Zones` viser sonene som kan
brukes i `accessToZones`.

## Feil og idempotens

- Behandle `400`/`422` som valideringsfeil og rett payloaden.
- Behandle `409` fra brukeroppretting som signal om å hente eksisterende bruker.
- Gjenta ikke en POST ukritisk etter ukjent resultat; slå først opp med stabil nøkkel.
- Aktivering, deaktivering og medlemskapsendringer bør uttrykke ønsket tilstand.
- IdentityServer-operasjoner kan feile etter at WebSak er oppdatert. Les begge
  relevante visninger på nytt før retry.

Se [legacy-oversikten](/userapi_legacy.html) for gamle GET-baserte mutasjoner som ikke skal
tas i bruk av nye integrasjoner.
