---
title: Identitet, autentisering og tilgang
permalink: /userapi_identity_and_access.html
---

# Identitet, autentisering og tilgang

SCIM-delene i denne guiden beskriver en beta for kontrollert pilot og er ikke
godkjenning for full produksjon. REST UserAPI er ikke beta.

UserAPI skiller mellom autentisering av API-klienten, WebSak-brukerens moderne
loginmapping og autorisasjonen brukeren får inne i WebSak. Disse tre nivåene må
konfigureres hver for seg.

## Token og scopes

Alle kall bruker OAuth 2.0 bearer token fra autoriteten som er konfigurert for
installasjonen.

| Grensesnitt | Påkrevd scope | Eksempel på målgruppe |
|---|---|---|
| Ordinært REST API under `/api/` | `userapi` | IAM-integrasjon eller administrasjonsklient |
| SCIM under `/scim/v2/` | `userapi.scim` | Entra provisioning service |

Et token med bare `userapi` gir ikke tilgang til SCIM. Et token med bare
`userapi.scim` gir ikke tilgang til ordinære REST-ruter. Kunden bør bruke separate
klientregistreringer og bare tildele scopet klienten trenger.

```http
Authorization: Bearer <access-token>
```

Ikke legg tokens, client secrets eller sertifikater i konfigurasjonsfiler,
dokumentasjon eller pipelinevariabler som ikke er markert som hemmelige.

## Entra, IdentityServer og WebSak

Entra ID kan ha to roller i løsningen:

- identitetstilbyder for interaktive WebSak-brukere via OIDC-federering
- provisjoneringsklient som sender SCIM-kall til UserAPI

IdentityServer formidler innlogging til WebSak. UserAPI bruker IdentityServers
intern-API når en REST- eller SCIM-operasjon skal opprette eller erstatte en
moderne loginmapping. WebSak lagrer brukerprofilen, organisatorisk tilhørighet,
roller, tilgangsfunksjoner og tilgangsgrupper.

## Identifikatorer

| Verdi | Betydning | Lagring/bruk |
|---|---|---|
| SCIM `id` | Stabil intern WebSak-bruker-ID | `Gid_GidID`, returneres av tjenesten |
| SCIM `externalId` | Entra object ID | `Gid_DIV2`, klientstyrt og unik for SCIM-brukere |
| REST `externalId` i brukerrespons | IdentityServers interne ID | `Gid_EksternID`; må ikke forveksles med SCIM `externalId` |
| SCIM `userName` | Kort WebSak-brukerkode | `Gid_GidKode`, maksimalt 10 tegn |
| REST `username` | Eldre/konfigurert loginverdi | brukes av ordinære REST-flyter |

Entra skal mappe den stabile `objectId`-verdien til SCIM `externalId`. E-post er
ikke en stabil erstatning for denne nøkkelen.

## Loginmapping

I REST er `userAccesses` en liste over loginmappinger. Hvert element inneholder:

| Felt | Betydning |
|---|---|
| `provider` | IdentityServer-scheme, for eksempel `AzureAD`; må samsvare eksakt |
| `key` | identifikator hos provideren |
| `domain` | valgfritt domene for providere som bruker dette |
| `isPrimary` | om mappingen er primær |

SCIM bygger nøyaktig én primær loginmapping fra `externalId`: konfigurert
`Scim:ModernAuthentication:Provider` brukes som `provider`, trimmet
`externalId` brukes som `key`, `isPrimary` er `true`, og `domain` er `null`.
Loginmappingen eksponeres ikke som et eget SCIM extension-felt.

## Roller, tilgangsfunksjoner og maler

En WebSak-rolle bestemmer lese- og skrivetilgang til saker, journalposter og
filer. Tilgangsfunksjoner bestemmer hvilke handlinger brukeren kan utføre på
objekter vedkommende har tilgang til. Tilgangskoder, administrative enheter,
arkivdeler og andre avgrensninger vurderes sammen med rollen.

`accessTemplateId` i REST er ID-en til en rettighetsmal (malbruker). Ved
oppretting kopierer UserAPI relevant rolle- og tilgangsoppsett fra malen. Feltet
er ikke en loginmapping og skal ikke forveksles med `userAccesses`.

SCIM bruker `applicationRole` som en kundedefinert, lesbar verdi. UserAPI slår
den opp i `Scim:ApplicationRoleAccessTemplateIdMap` og bruker resultatet som
`accessTemplateId`. Mappingen må være entydig og vedlikeholdes sammen med
rettighetsmalene i WebSak.

## Tilgangsgrupper

Navngitte tilgangsgrupper gir tilgang på tvers av linjeorganisasjonen, for
eksempel for en prosjektgruppe. De er forskjellige fra roller og
tilgangsfunksjoner. Gruppemedlemskap kan forvaltes via REST eller SCIM, men
tilgangseffekten bestemmes fortsatt av WebSaks regler og objektkoblinger.

## Feilgrense mot IdentityServer

Oppdateringer som berører både WebSak og IdentityServer er ikke én distribuert
transaksjon. UserAPI validerer før mutasjon så langt kontrakten tillater, men en
IdentityServer-feil kan komme etter at WebSak-steget er fullført. Klienten skal
derfor bruke stabile nøkler, lese tilstanden på nytt og forsøke samme ønskede
tilstand på nytt. Se [retry og feilhåndtering i SCIM-guiden](/userapi_scim_guide.html#retry-og-feilhåndtering).
