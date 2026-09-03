---
title: DRAFT - SAP SuccessFactors-integrasjon
permalink: /userapi_sap_successfactors_integration.html
published: false
status: draft
---

# DRAFT – SAP SuccessFactors, Integration Suite og UserAPI

**Status: DRAFT.** Dokumentet skal fagkontrolleres før publisering eller bruk i
produksjon.

## Formål

SAP SuccessFactors Employee Central er master for avdelingsstrukturen. SAP
Integration Suite leser avdelingene gjennom OData V2, oversetter dem til
UserAPI-kontrakten og oppretter eller vedlikeholder avdelinger i ACOS WebSak.

```text
SuccessFactors Employee Central
  └─ OData V2: FODepartment
       └─ SAP Integration Suite
            ├─ mapping, rekkefølge og tilstand
            └─ REST + scope userapi
                 └─ UserAPI /api/v2/departments
                      └─ ACOS WebSak
```

SCIM-betaen oppretter ikke avdelingsstrukturen. Den kan knytte brukere til en
eksisterende avdeling ved å sende samme eksterne avdelings-ID.

## Kilde i SuccessFactors

Bruk OData V2-entiteten `FODepartment`. Den er effective-dated og har
`externalCode` og `startDate` som forretningsnøkkel. En innledende synkronisering
bør hente avdelinger som er gyldige på en eksplisitt `asOfDate`.

```http
GET /odata/v2/FODepartment
    ?$format=json
    &$select=externalCode,name,parent,headOfUnit,startDate,endDate,lastModifiedDateTime
    &asOfDate=<YYYY-MM-DD>
```

Se SAPs dokumentasjon for
[FODepartment](https://help.sap.com/docs/SAP_SUCCESSFACTORS_PLATFORM/d599f15995d348a1b45ba5603e2aba9b/35be764c2a414cd5ae39a419ba7b97fd.html)
og
[effective-dated OData-spørringer](https://help.sap.com/docs/successfactors-platform/sap-successfactors-api-reference-guide-odata-v2/effective-dated-query-in-odata).

## Feltmapping

| SuccessFactors | UserAPI | Regel |
|---|---|---|
| `externalCode` | `externalId` | én stabil, eksakt og unik verdi |
| `name` | `name` | bruk avtalt språkvariant |
| `parent` | `parentDepartmentId` | slå opp forelderens interne UserAPI-ID |
| avtalt kortkode | `abbreviation` og `code` | må være unik i WebSak |
| `headOfUnit` | `managerUserId` | sett etter oppslag mot brukerens GID-ID |
| gjeldende gyldighet | activation-rutene | aktiver eller deaktiver avdelingen |

Integrasjonen må lagre koblingen mellom SuccessFactors `externalCode` og
UserAPI `id`. En SuccessFactors-rot uten forelder må kobles til en avtalt,
eksisterende rotavdeling i WebSak.

## Synkroniseringsflyt

1. Hent og valider et komplett gjeldende avdelingssett fra `FODepartment`.
2. Avvis duplikate eksterne ID-er, ukjente foreldre og sirkler.
3. Behandle foreldre før underavdelinger.
4. Slå opp med `GET /api/v2/departments/external/{externalId}`.
5. Opprett manglende avdeling med `POST /api/v2/departments`.
6. Oppdater eksisterende avdeling med GET – endre – PUT – GET.
7. Sett leder i en ny passering når brukeren har fått en kjent GID-ID.
8. Deaktiver først etter en komplett og godkjent sammenligning.

PUT er full overskriving av skrivbare felt. Integrasjonen må derfor bevare
verdier den ikke selv forvalter. En POST med ukjent resultat skal ikke gjentas
før oppslag på `externalId` er utført.

## Integration Suite

En planlagt integration flow bør inneholde:

- SuccessFactors OData V2 receiver adapter
- validering og topologisk sortering av hierarkiet
- et tilstandslager for ID-koblinger, vannmerke og siste vellykkede kjøring
- HTTP receiver adapter mot UserAPI
- OAuth 2.0-legitimasjon lagret som Security Material
- kontrollert retry, korrelasjons-ID og feilkanal
- periodisk full avstemming i tillegg til eventuell deltasynkronisering

SAP dokumenterer
[SuccessFactors OData V2-adapteren](https://help.sap.com/docs/integration-suite/sap-integration-suite/configure-successfactors-odata-v2-receiver-adapter)
og
[støttede autentiseringsmetoder](https://help.sap.com/docs/integration-suite/sap-integration-suite/adapters-authentication-methods).

## Sikkerhet og avgrensning

- Bruk en separat, minst privilegert API-identitet mot SuccessFactors.
- Bruk en separat UserAPI-klient med bare scope `userapi`.
- Ikke lagre token, sertifikater eller secrets i mapping eller logger.
- Deaktivering flytter ikke brukere, saker eller underavdelinger automatisk.
- SCIM scope `userapi.scim` skal ikke brukes til REST-avdelingsoperasjoner.

Detaljer om UserAPI-ruter og feltregler finnes i
[avdelingsguiden](/userapi_rest_departments.html).
