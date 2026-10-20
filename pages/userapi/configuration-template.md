---
title: Kundespesifikk konfigurasjonsmal
permalink: /userapi_configuration_template.html
---

# Kundespesifikk konfigurasjonsmal

Kopier tabellene til kundens sikre konfigurasjons- og driftsdokumentasjon. Fyll
bare inn identifikatorer, navn og URL-er som kan deles i den valgte kanalen.
Secrets, tokens, sertifikatinnhold og connection strings skal aldri fylles inn.

## Endepunkter og ansvar

| Verdi | Kundens verdi | Eier/godkjenner |
|---|---|---|
| Tenant-ID | `<tenant-id>` | `<identitetsansvarlig>` |
| UserAPI base-URL | `https://<host>/` | `<driftsansvarlig>` |
| SCIM base-URL | `https://<host>/scim/v2` | `<driftsansvarlig>` |
| OAuth authority | `https://<authority>/` | `<identitetsansvarlig>` |
| REST scope | `userapi` | `<sikkerhetsansvarlig>` |
| SCIM scope | `userapi.scim` | `<sikkerhetsansvarlig>` |
| IdentityServer provider/scheme | `<provider>` | `<identitetsansvarlig>` |
| Token-/sertifikatfornyelse | `<prosessreferanse>` | `<rolle>` |
| Hendelser og retry | `<prosessreferanse>` | `<rolle>` |

## Avdelingsmapping

Hver innkommende verdi skal mappe til én eksakt ekstern avdelings-ID. Ikke bruk
pipe-separerte verdier.

| Kildesystemverdi | WebSak avdeling | `externalId` (`Gid_DIV1`) | Godkjent av |
|---|---|---|---|
| `<source-department>` | `<department-name>` | `<external-id>` | `<role/date>` |

## Rolle- og rettighetsmapping

| SCIM `applicationRole` | WebSak rettighetsmal-ID | Beskrivelse | Godkjent av |
|---|---|---|---|
| `<application-role>` | `<access-template-id>` | `<rights-summary>` | `<role/date>` |

Vurder separat manuell tildeling for arkivansvarlige, systemadministratorer og
andre høye privilegier. Dokumenter hvem som kan endre mappingen.

## Språkmapping

| SCIM `preferredLanguage` | WebSak `LanguageId` | Godkjent av |
|---|---|---|
| `<bcp-47-language>` | `<language-id>` | `<role/date>` |

Mappingen må være entydig begge veier.

## Entra-attributter

| Entra-kilde | SCIM-mål | Aktiv | Kommentar |
|---|---|---|---|
| `<upn-source>` | `userName` | `ja` | loginidentifikator for konfigurert provider |
| `<short-websak-code-source>` | Acos `userCode` | `ja` | påkrevd ved POST, maks. 10 tegn; SCIM genererer ikke koden |
| `objectId` | `externalId` | `<ja/nei>` | valgfri, separat korrelasjonsverdi lagret i `Gid_DIV2` |
| `accountEnabled` | `active` | `ja` | deaktivering/reaktivering |
| `<department-source>` | enterprise `department` | `<ja/nei>` | én eksakt ekstern ID |
| `<application-role-source>` | Acos `applicationRole` | `<ja/nei>` | rettighetsmalmapping |
| `userType` | ikke mappet | `nei` | member og guest behandles likt |

## Ikke-hemmelig appsettings-mal

Verdiene nedenfor er plassholdere. Hemmelige verdier leveres gjennom godkjent
secret store eller service connection.

```json
{
  "IdentityServer": {
    "ReadOnly": false
  },
  "Tenant": {
    "Id": "<tenant-id>"
  },
  "Auth": {
    "Authority": "https://<authority>/",
    "Scopes": "userapi userapi.scim"
  },
  "Apis": {
    "IdServerInternal": "https://<identityserver-internal-base>/"
  },
  "Scim": {
    "ModernAuthentication": {
      "Provider": "<identityserver-provider-scheme>"
    },
    "ApplicationRoleAccessTemplateIdMap": {
      "<application-role>": "<access-template-id>"
    },
    "PreferredLanguageLanguageIdMap": {
      "<bcp-47-language>": "<language-id>"
    }
  }
}
```

## REST med GLM uten IdentityServer

For installasjoner som bruker `GLM_LoginMapping`, settes
`Apis:IdServerInternal` til tom streng, eller innstillingen utelates:

```json
{
  "Apis": {
    "IdServerInternal": ""
  },
  "IdentityServer": {
    "ReadOnly": false
  }
}
```

Kontroller at ingen miljøspesifikk konfigurasjon eller miljøvariabel
`Apis__IdServerInternal` fortsatt angir en URL. GLM-tabellen må finnes i
WebSak-databasen; API-et oppretter den ikke. GLM-koblinger trenger ikke
`Gid_EksternID` eller `Tenant:Id`. `IdentityServer:ReadOnly=true` sperrer
fortsatt endring av loginmappinger, også med GLM.

Autentisering av API-klienten gjennom `Auth` og scope `userapi` kreves fortsatt.
Dette oppsettet gjelder ordinært REST API. SCIM-brukeroppretting og
-oppdatering krever fortsatt konfigurert IdentityServer, tenant og provider.
Se [REST-guiden](/userapi_rest_guide.html#loginmapping-med-identityserver-eller-glm)
for GET/PUT-eksempel og erstatningsregler.

## Godkjenning før bruk

| Kontroll | Ansvarlig | Dato/resultat |
|---|---|---|
| Produktfaglig kontroll av rettighetsmaler og avdelinger | `<produktansvarlig>` | `<dato/resultat>` |
| Avgrenset SCIM-betakontroll av member, guest og grupper | `<identitetsansvarlig>` | `<dato/resultat>` |
| Scope, secret-håndtering og minste privilegium | `<sikkerhetsansvarlig>` | `<dato/resultat>` |
| Gamle kundelenker og Pages-innhold | `<dokumentasjonsansvarlig>` | `<dato/resultat>` |

Ved felles identitet i prod og historisk base settes `IdentityServer:ReadOnly`
til `true` i hist (`IdentityServer__ReadOnly=true` som miljøvariabel). Standard
er `false`. Se [felles identitet](/userapi_identity_and_access.html#felles-identitet-i-produksjon-og-historisk-base)
for opprettelsesflyt og begrensninger.
