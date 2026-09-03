---
title: SCIM-provisjonering (beta)
permalink: /userapi_scim_guide.html
---

# SCIM-provisjonering fra Microsoft Entra ID (beta)

> **Beta:** SCIM-grensesnittet er tilgjengelig for kontrollert utprøving, men er
> ikke klart for full produksjon. Avtal avgrenset pilot, testdata, ansvar og
> tilbakeføringsrutine før provisjonering aktiveres. REST UserAPI er ikke beta.

SCIM 2.0-grensesnittet ligger under `/scim/v2/`, bruker media type
`application/scim+json` og krever scope `userapi.scim`. Det støtter Entra-flyter
for brukere, grupper, medlemskap, deaktivering og reaktivering.

![SCIM-provisjoneringsflyt for kunden](/pages/userapi/images/scim-provisioning-flow.svg)

## Støttede endepunkter

| Ressurs | Operasjoner |
|---|---|
| Discovery | `GET /ServiceProviderConfig`, `/ResourceTypes`, `/Schemas` og `/Schemas/{uri}` |
| Users-samling | `GET /Users` og `POST /Users` |
| Enkeltbruker | `GET`, `PUT`, `PATCH` og `DELETE /Users/{id}` |
| Groups-samling | `GET /Groups` og `POST /Groups` |
| Enkeltgruppe | `GET`, `PATCH` og `DELETE /Groups/{id}` |

`PUT /Groups/{id}` støttes ikke og returnerer `405 Method Not Allowed`.
`DELETE` er deaktivering, ikke fysisk sletting.

## Oppsett i Entra

1. Opprett en Enterprise application for provisjonering.
2. Velg automatisk provisioning mode.
3. Sett Tenant URL til kundens offentlige UserAPI-URL med `/scim/v2`.
4. Bruk en bearer credential som gir bare `userapi.scim`.
5. Kjør **Test Connection** og kontroller discovery-endepunktene.
6. Konfigurer attributtmappingene nedenfor.
7. Velg om bare tilordnede brukere og grupper eller hele valgt scope skal synkroniseres.
8. Kjør **Provision on demand** for én member og én guest før full synkronisering.

Tokenet må fornyes etter kundens avtalte levetid. Ikke bruk et personlig token.

## Brukerattributter

![Kunderelevant SCIM-feltmapping](/pages/userapi/images/scim-field-mapping.svg)

| Entra-kilde | SCIM-mål | Krav og merknad |
|---|---|---|
| `objectId` | `externalId` | Påkrevd, stabil og unik; lagres i `Gid_DIV2` |
| valgt kort brukerkode | `userName` | Påkrevd, unik, maksimalt 10 tegn |
| `accountEnabled` | `active` | Styrer deaktivering og reaktivering |
| `givenName` | `name.givenName` | Skrivbar |
| `surname` | `name.familyName` | Skrivbar |
| `displayName` | `displayName` | Brukes som formatert navn |
| `mail` | `emails[type eq "work"].value` | Primær jobb-e-post |
| jobbtelefon | `phoneNumbers[type eq "work"].value` | Primær jobbtelefon |
| sekundær telefon | `phoneNumbers[type eq "other"].value` | `work2` godtas bare som input-alias |
| mobil | `phoneNumbers[type eq "mobile"].value` | Mobiltelefon |
| `preferredLanguage` | `preferredLanguage` | Må finnes i kundens språkmapping |
| avdelingens eksterne ID | enterprise `department` | Eksakt oppslag mot ett `Gid_DIV1` |
| applikasjonsrolle | Acos `applicationRole` | Slås opp til én rettighetsmal |

Enterprise-attributtet bruker URI-en
`urn:ietf:params:scim:schemas:extension:enterprise:2.0:User:department`.
Acos-attributtet bruker
`urn:acos:params:scim:schemas:extension:user:2.0:AcosUser:applicationRole`.

Ikke map `userType`. Entra `member` og `guest` behandles likt av SCIM-adapteren;
tilgang styres av assignment, grupper, avdeling og `applicationRole`, ikke av
Entras `userType`.

## Avdelings- og rettighetsmapping

SCIM `department` skal inneholde én eksakt ekstern avdelings-ID. UserAPI slår
verdien opp mot avdelingens `Gid_DIV1`. Pipe-separerte eller kommaseparerte
verdier støttes ikke. Oppslaget må gi nøyaktig én aktiv avdeling.

`applicationRole` oversettes gjennom
`Scim:ApplicationRoleAccessTemplateIdMap`. Eksempelverdiene i
[konfigurasjonsmalen](/userapi_configuration_template.html) er plassholdere; kunden må bruke
sine reelle rettighetsmaler og dokumentere hvem som godkjenner endringer.

## Livssyklus for brukere

### Oppretting

Entra sender `POST /scim/v2/Users`. `externalId` og `userName` må være unike.
UserAPI oppretter WebSak-brukeren, setter `externalId` i `Gid_DIV2`, anvender
avdeling/rettighetsmal og synkroniserer moderne loginmapping mot IdentityServer.

### Oppdatering

Entra bruker normalt `PATCH /scim/v2/Users/{id}`. `add`, `replace` og `remove`
støttes for den avtalte profilen, blant annet navn, e-post, telefon, `active`,
`externalId`, `preferredLanguage`, `department` og `applicationRole`. `PUT` kan
brukes for full ressursoppdatering. Bruk `If-Match` når klienten har mottatt en
ETag og vil unngå å overskrive en samtidig endring.

### Deaktivering og reaktivering

![Deprovisjonering og reaktivering](/pages/userapi/images/scim-deprovisioning.svg)

`DELETE /scim/v2/Users/{id}` eller PATCH med `active=false` deaktiverer brukeren
uten fysisk sletting. Operasjonen er idempotent. Brukeren kan fortsatt hentes og
reaktiveres med PATCH eller PUT som setter `active=true`.

Saker, journalposter, dokumenter og oppgaver blir ikke automatisk omfordelt når
en bruker deaktiveres eller bytter avdeling. Denne forvaltningsoppgaven må inngå
i kundens avslutnings- og flytteprosess.

## Grupper og medlemskap

Map Entra `displayName` til SCIM `displayName` og `members` til `members`.

- `POST /scim/v2/Groups` oppretter en navngitt tilgangsgruppe.
- `PATCH /scim/v2/Groups/{id}` kan endre navn og legge til eller fjerne medlemmer.
- `DELETE /scim/v2/Groups/{id}` deaktiverer gruppen og skjuler den fra SCIM-oppslag.

Group PatchOp støtter Entras vanlige `add` og `remove`. Tjenesten aksepterer også
`replace` av hele `members`-attributtet. En eksplisitt tom
`"Operations": []` behandles som en no-op med `204` for kompatibilitet med
Microsoft SCIM Validator.

## Filter, sortering og projeksjon

Users og Groups støtter de dokumenterte `eq`, `and`, `or` og `pr`-uttrykkene.
Users kan sorteres på de tillatte standardfeltene i OpenAPI-referansen.
Paginering bruker `startIndex` og `count`.

`attributes` og `excludedAttributes` kan ikke brukes samtidig. `schemas` og `id`
returneres alltid. Den støttede profilen lover toppnivåprojeksjon og hele
extension-objekter, ikke generell projeksjon av alle subattributter.

## Retry og feilhåndtering

En retry skal sende samme ønskede tilstand med samme stabile `externalId` og SCIM
`id`; den skal ikke opprette en ny korrelasjonsnøkkel. Ved usikkert resultat:

1. les ressursen på nytt med `id` eller filter på `externalId`
2. sammenlign nåværende tilstand med ønsket tilstand
3. gjenta PATCH/PUT hvis avviket fortsatt finnes
4. eskaler ved vedvarende `409`, `412` eller `503`

UserAPI synkroniserer loginmapping også når `externalId` er uendret, slik at en
retry kan konvergere etter en midlertidig IdentityServer-feil. Oppdateringen er
ikke atomisk mellom WebSak og IdentityServer; et WebSak-steg kan være fullført
før et senere delkall feiler.

Alle eksplisitt håndterte SCIM-feil følger RFC 7644-format:

```json
{
  "schemas": ["urn:ietf:params:scim:api:messages:2.0:Error"],
  "status": "400",
  "scimType": "invalidValue",
  "detail": "Forklaring uten hemmelige verdier."
}
```

| Status | Vanlig årsak | Tiltak |
|---|---|---|
| `400` | ugyldig attributt, filter, mapping eller manglende `externalId` | korriger payload/mapping |
| `401` | token mangler eller er utløpt | hent nytt token |
| `403` | token mangler `userapi.scim` | korriger klientens scope |
| `404` | bruker, gruppe eller medlem finnes ikke | les scope/korrelasjon på nytt |
| `409` | duplikat `userName`, `externalId` eller navn | finn eksisterende ressurs og rett mapping |
| `412` | ETag samsvarer ikke | GET, flett ønsket endring og forsøk med ny ETag |
| `503` | IdentityServer/provider er ikke tilgjengelig eller konfigurert | rett konfigurasjon og retry senere |

## Pilot- og akseptansesjekkliste

- Test Connection er grønn med scope `userapi.scim`.
- Både én Entra member og én guest kan opprettes, oppdateres og deaktiveres.
- Begge kan reaktiveres uten ny WebSak-bruker.
- `objectId` finnes som SCIM `externalId`; `userType` er ikke mappet.
- Avdelingsoppslag bruker én eksakt ekstern ID.
- Alle `applicationRole`-verdier peker til godkjente rettighetsmaler.
- Gruppeoppretting og add/remove av medlem er testet.
- Provisioning logs er uten vedvarende feil etter retry.
- Eier for tokenfornyelse, mapping og hendelseshåndtering er avtalt.
- Pilotens stoppkriterier og tilbakeføringsrutine er prøvd før omfanget økes.
