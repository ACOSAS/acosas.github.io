---
title: REST tilgangsgrupper
permalink: /userapi_rest_access_groups.html
---

# Tilgangsgrupper via REST

Tilgangsgrupper avgrenser tilgang til informasjon i WebSak. Denne guiden gjelder
det produksjonsklare REST-grensesnittet med scope `userapi`. Bruk gruppens
numeriske ID som stabil nøkkel når den er kjent.

![Flyt for tilgangsgrupper](/pages/userapi/images/rest-access-groups-flow.svg)

## Ruter

| Behov | Rute | Resultat |
|---|---|---|
| Liste generelle grupper | `GET /api/AccessGroups` | `AccessGroup[]` |
| Hent én gruppe | `GET /api/AccessGroups/{id}` | gruppens metadata |
| Opprett | `POST /api/AccessGroups` | `201` og opprettet gruppe |
| Liste aktive medlemmer | `GET /api/AccessGroups/members/{id}` | liste med brukerens GID-ID |
| Legg til medlem | `PUT /api/v2/accessgroups/{accessGroupId}/members/{userGidId}` | ønsket medlemskap er aktivt |
| Fjern medlem | `DELETE /api/v2/accessgroups/{accessGroupId}/members/{userGidId}` | ønsket medlemskap er avsluttet |
| Legg til etter navn | `PUT /api/v2/accessgroups/by-name/{name}/members/{userGidId}` | som over, men med navneoppslag |
| Fjern etter navn | `DELETE /api/v2/accessgroups/by-name/{name}/members/{userGidId}` | som over, men med navneoppslag |

Oppretting bruker denne payloaden:

```json
{
  "groupName": "Innsyn HR"
}
```

Medlemskapsrutene uttrykker ønsket tilstand. Et nytt PUT-kall aktiverer også et
tidligere avsluttet medlemskap. DELETE avslutter et aktivt medlemskap og kan
gjentas uten at klienten må opprette en ny korrelasjonsnøkkel. Les medlemmene på
nytt etter en retry med ukjent resultat.

## Navn, ID og gyldighet

`groupId` er den foretrukne integrasjonsnøkkelen. De navnebaserte rutene krever
at navnet treffer entydig. Kunden bør derfor ha en forvaltningsregel som hindrer
duplikate gruppenavn, selv om REST-oppretting ikke håndhever dette fullt ut.

Listen over generelle grupper kan inneholde grupper med utløpt gyldighet. Les
`fromDate` og `toDate` før gruppen tilbys som et aktivt valg. Medlemslisten viser
aktive medlemskap på forespørselstidspunktet.

## Saks- og journalgrupper

Følgende ruter viser tilgangsgrupper som er knyttet direkte til en sak eller en
journalpost:

- `GET /api/AccessGroups/cases/{caseId}`
- `GET /api/AccessGroups/journals/{journalId}`
- `DELETE /api/AccessGroups/cases/{caseId}/{groupId}`
- `DELETE /api/AccessGroups/journals/{journalId}/{groupId}`

REST-kontrakten tilbyr lesing og fjerning av disse koblingene, men ikke
oppretting av dem. Ikke bruk de generelle medlemskapsrutene som erstatning; de
endrer medlemskap i gruppen, ikke koblingen til saken eller journalposten.

## Begrensninger og anbefalt kontroll

- REST har ikke et produksjonsklart endepunkt for å endre gruppenavn eller
  deaktivere selve gruppen.
- Verifiser både gruppens gyldighet og medlemskapet når tilgang er tidskritisk.
- Logg gruppe-ID, brukerens GID-ID, ønsket tilstand og resultat, men ikke token.
- Bruk `404` til å korrigere ID-er; gjenta ikke navnebaserte kall ukritisk ved
  tvetydig eller manglende treff.
