---
title: Feltmapping
permalink: /userapi_field_mapping.html
---

# Feltmapping

Tabellene viser kunderelevant mapping, retning, krav og standarder. Fullstendige
skjemaer finnes i generert OpenAPI. `Inn` betyr at klienten kan sende feltet,
`ut` betyr at UserAPI returnerer det.

## REST bruker

| API-felt | Retning | Krav/standard | WebSak-felt eller effekt |
|---|---|---|---|
| `id` | inn ved oppdatering | intern GID-ID | `Gid_GidID` |
| `code` | inn/ut | unik brukerkode | `Gid_GidKode` |
| `name` | inn/ut | fullt navn | `Gid_Navn` |
| `username` | inn | påkrevd for ordinær bruker; ikke tillatt for sekundærbruker | loginverdi i ordinær flyt |
| `isSecondaryUser` | inn | standard `false` | oppretter sekundærrelasjon via e-post |
| `mailAddresses` | inn/ut | første adresse er primær | `Gid_EmailAdr`, `Gid_EmailAdr2` og adresseoversikt |
| `departmentCode` | inn/ut | vinner over `externalDepartmentId` | oppslag mot `Soa_AdmKort`, intern avdelings-ID lagres |
| `externalDepartmentId` | inn | én eksakt verdi | oppslag mot avdelingens `Gid_DIV1` |
| `accessTemplateId` | inn/ut | standard `-1` når utelatt ved REST-oppretting | rettighetsmal; kopierer roller og funksjoner |
| `userAccesses` | inn/ut | ikke-tom ved PUT; ikke tillatt for sekundærbruker | IdentityServer loginmapping |
| `accessToZones` | inn | tom/utelatt bruker databasens standard | sonetildeling |
| `userType` | inn | ordinær REST-standard er bruker (`B`) | WebSak brukertype; ikke et SCIM-felt |
| `title` | inn/ut | valgfritt | `Gid_Tittel` |
| `nationalNo` | inn/ut | valgfritt, behandles som sensitivt | `Gid_OffentligNr` |
| `phone`, `phone2`, `mobile` | inn/ut | valgfritt | `Gid_Tlf`, `Gid_Tlf2`, `Gid_Mobil` |
| `languageId` | inn/ut | kundens WebSak-språk-ID | `Gid_SpraakID` |
| `validFrom` | inn/ut | valgfri startdato | `Gid_FraDato` |

Andre adresse- og kontaktfelt følger navngivningen i OpenAPI. Ikke send
`misc1`–`misc5` uten en avtalt kundemapping; `Gid_DIV2` er reservert for SCIM
`externalId` når brukeren forvaltes gjennom SCIM.

## REST loginmapping

| `userAccesses`-felt | Retning | Krav/standard | Effekt |
|---|---|---|---|
| `provider` | inn/ut | standard i modellen er `AD`; bruk avtalt IdentityServer-scheme | velger provider |
| `key` | inn/ut | påkrevd identifikator hos provider | kobler ekstern identitet til bruker |
| `domain` | inn/ut | valgfritt | provider-spesifikt domene |
| `isPrimary` | inn/ut | standard `true` | markerer primær mapping |

`userAccesses` er loginmapping. `accessTemplateId` er rettighetsmal. De kan
brukes i samme ordinære brukerflyt, men løser forskjellige behov.

## SCIM User

SCIM-tabellen beskriver beta-kontrakten. Mappingene skal verifiseres i en
avgrenset pilot og må ikke tolkes som produksjonsgodkjenning.

| SCIM-felt | Retning | Krav/standard | WebSak-felt eller effekt |
|---|---|---|---|
| `id` | ut | readOnly | `Gid_GidID` |
| `externalId` | inn/ut | påkrevd, trimmes, unik | Entra object ID i `Gid_DIV2` |
| `userName` | inn/ut | påkrevd, unik, maks 10 tegn | `Gid_GidKode` |
| `active` | inn/ut | standard etter opprettingskontrakten | avledes fra gyldighetsdatoer |
| `displayName`/`name` | inn/ut | navn må kunne bygges | `Gid_Navn` |
| `emails[type eq "work"]` | inn/ut | valgfritt | primær e-post |
| `phoneNumbers` | inn/ut | typene `work`, `other`, `mobile` | `Gid_Tlf`, `Gid_Tlf2`, `Gid_Mobil` |
| `preferredLanguage` | inn/ut | må finnes i entydig konfigurasjonsmapping | `LanguageId` |
| enterprise `department` | inn/ut | én eksakt ekstern ID | oppslag `Gid_DIV1` til intern avdeling |
| enterprise `manager` | ut | readOnly | avdelingens `ManagerUserId` |
| Acos `applicationRole` | inn/ut | må finnes i rollemapping | oversettes til `accessTemplateId` |
| `roles` | ut | readOnly | WebSak-roller |
| `entitlements` | inn/ut | avtalt verdiutvalg | tilgangsfunksjoner |

SCIM mapper ikke `userType`. Entra member og guest følger samme User-mapping.

## Avdeling

| API-felt | Retning | Krav/standard | WebSak-felt |
|---|---|---|---|
| `id` | ut / inn i rute | intern ID; body-ID overstyres av ruten ved PUT | `Soa_AvdelingID` |
| `externalId` | inn/ut | én eksakt ekstern ID | `Gid_DIV1` |
| `code` | inn ved oppretting / ut | fallback når `abbreviation` mangler; endres ikke separat av PUT | `Soa_AvdelingKode` ved oppretting |
| `abbreviation` | inn/ut | operativ, unik kortbetegnelse; vinner over `code` | `Soa_AdmKort` |
| `name` | inn/ut | navn | `Soa_Navn` |
| `parentDepartmentId` | inn/ut | forelder må finnes ved oppretting; kunde validerer hierarki ved PUT | `Soa_FarAvdelingID` |
| `managerUserId` | inn/ut | intern bruker-ID | `Soa_Leder_GidID` |
| `unit` | inn ved oppretting / ut | standard `Avd`; endres ikke av PUT | `Soa_Enhet` |
| `validFromDate`, `validToDate` | ut | start genereres; sluttdato styres av activation-rutene | `Soa_FraDato`, `Soa_TilDato` |
| `journalUnitId`, `archiveUnit` | ut | readOnly gjennom V2 | `Soa_JournalEnhetID`, `Soa_ArkDel` |
| `mailDistributionGroup` | inn/ut | tilgangsgruppe-ID | `Soa_PostFordelerGruppe` |

V2 kan i tillegg skrive de dokumenterte kontakt-, adresse-, telefon-, e-post-,
leder-, mal- og konfigurasjonsfeltene i OpenAPI. Feltene `group`, `level`,
`gidId`, `intralink`, `addr3` og `addr4` er readOnly gjennom V2. Bruk
[avdelingsguiden](/userapi_rest_departments.html) for trygg GET–PUT-arbeidsflyt.

## Tilgangsgruppe

| API/SCIM-felt | Retning | Krav/standard | WebSak-effekt |
|---|---|---|---|
| REST `groupId` / SCIM `id` | ut | stabil intern gruppe-ID | identifiserer tilgangsgruppen |
| REST `groupName` / SCIM `displayName` | inn/ut | navn må være unikt i anvendt flyt | navngitt tilgangsgruppe |
| SCIM `externalId` | ut | samme verdi som gruppe-ID i støttet profil | korrelasjon |
| SCIM `members[].value` | inn/ut | brukerens SCIM/WebSak-ID | aktivt eller avsluttet medlemskap |

## Standardverdier og kildekontroll

Standardverdier kan endres mellom UserAPI-versjoner. Klienten skal derfor lese
generert OpenAPI fra samme versjon som målmiljøet og ikke basere seg på den
historiske XLSX-filen. Kundespesifikke mappinger skal fylles inn i
[konfigurasjonsmalen](/userapi_configuration_template.html) og godkjennes før produksjon.
