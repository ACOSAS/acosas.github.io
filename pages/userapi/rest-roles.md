---
title: REST roller og tilgangsfunksjoner
permalink: /userapi_rest_roles.html
---

# Roller og tilgangsfunksjoner via REST

Roller avgrenser hva brukeren kan lese og skrive innen valgte avdelinger,
arkivdeler, journalenheter og grader. Tilgangsfunksjoner er separate
funksjonskoder for handlinger brukeren kan utføre.

![Sammenheng mellom rettighetsmal, roller og tilgangsfunksjoner](/pages/userapi/images/rest-role-model.svg)

## Velg rettighetsmal når det er mulig

`accessTemplateId` er en rettighetsmal, ikke en rolle-ID. Ved brukeroppretting
kopierer malen et godkjent grunnsett av roller og tilgangsfunksjoner. Dette er
den anbefalte kundearbeidsflyten fordi tildelingen blir mer konsistent og enklere
å revidere.

Direkte rollevedlikehold brukes bare når en godkjent mal ikke dekker behovet:

| Operasjon | Rute |
|---|---|
| Les brukerens roller | `GET /api/Users/{userId}/roles?lookupField=Id` |
| Legg til rolle | `POST /api/Users/{userId}/roles` |
| Fjern rolletildeling | `DELETE /api/Users/{userId}/roles/{roleId}` |

Bruk `lookupField=Code` bare når `{userId}` inneholder brukerkode.

## Rollepayload og ID-er

```json
{
  "id": 12,
  "departmentList": "10,20",
  "archiveList": "SAK,PERSONAL",
  "journalUnitList": "1,2",
  "gradeList": "U,KO"
}
```

`id` i POST-payloaden peker på rolletypen som skal tildeles. Responsens
`roleId` identifiserer den konkrete tildelingen til brukeren. Det er `roleId`
fra GET-responsen som skal brukes i DELETE-ruten.

Listene sendes som kommaseparerte strenger. `departmentList` må inneholde
numeriske avdelings-ID-er. Utelatte avgrensningslister lagres som tomme verdier;
bruk derfor en eksplisitt, godkjent payload og kontroller resultatet med GET.

## Endring og feilkontroll

Det finnes ikke PUT for en rolletildeling. En endring må gjøres som DELETE av
eksisterende `roleId`, deretter POST av ny tildeling. Operasjonen er ikke
atomisk: hvis POST feiler, er den gamle rollen allerede fjernet. Les derfor
nåtilstanden først, bevar opprinnelig payload for eventuell gjenoppretting og
verifiser sluttresultatet.

API-et tilbyr ikke en katalog over gyldige rolletyper. Rolle-ID-er og lovlige
avgrensningsverdier må inngå i kundens godkjente konfigurasjon. Ikke anta at en
annonsert `409` alene hindrer duplikate rolletildelinger; les eksisterende roller
før POST og håndhev ønsket tilstand i integrasjonen.

## Tilgangsfunksjoner

Tilgangsfunksjoner vedlikeholdes gjennom brukerens access-code-ruter i den
genererte REST-referansen. De skal ikke blandes med `userAccesses`, som er
loginmapping mot IdentityServer. Følgende begreper er ulike:

| Begrep | Betydning |
|---|---|
| `accessTemplateId` | mal som kopierer roller og tilgangsfunksjoner |
| rolle `id` | rolletypen som tildeles |
| `roleId` | den konkrete rolletildelingen som kan slettes |
| access code | tilgangsfunksjon i WebSak |
| `userAccesses` | ekstern loginmapping, ikke en WebSak-rettighet |
