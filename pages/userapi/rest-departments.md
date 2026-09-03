---
title: REST avdelinger
permalink: /userapi_rest_departments.html
---

# Opprette og vedlikeholde avdelinger via REST

Bruk alltid `/api/v2/departments`. Aliaset `/api/v2/departmentsv2` og de gamle
GET-baserte mutasjonene er deprecated.

![Livssyklus for avdelinger](/pages/userapi/images/rest-departments-flow.svg)

## Lesing og nøkkelvalg

| Operasjon | Rute |
|---|---|
| Les hierarki | `GET /api/v2/departments` |
| Les flat liste | `GET /api/v2/departments/flat` |
| Hent intern ID | `GET /api/v2/departments/{id}` |
| Hent ekstern ID | `GET /api/v2/departments/external/{externalId}` |

Den hierarkiske ruten returnerer organisasjonsnoder med `department` og
`subdepartments`. Den flate ruten er best egnet for korrelasjon og kontroll.
Listene kan inneholde inaktive avdelinger; vurder `validFromDate` og
`validToDate`.

`externalId` lagres i `Gid_DIV1` og skal være én eksakt, stabil og unik verdi.
Pipe- og kommaseparerte samlinger støttes ikke.

## Oppretting

Opprett med `POST /api/v2/departments`. En forelder må finnes; oppretting av en
ny rotavdeling støttes ikke. `abbreviation` er den operative, unike
kortbetegnelsen. Hvis den mangler, brukes `code` som kortbetegnelse ved
oppretting. `unit` får standardverdien `Avd` når feltet er tomt.

```json
{
  "externalId": "ENTRA-DEPT-0042",
  "code": "HR",
  "abbreviation": "HR",
  "name": "HR og organisasjon",
  "parentDepartmentId": "10",
  "managerUserId": "501",
  "unit": "Avd",
  "emails": ["hr@example.no"]
}
```

Et vellykket kall returnerer `201` og Location for den nye avdelingen. Duplikat
kortbetegnelse eller ugyldig forelder gir `422`. Slå deretter opp avdelingen og
lagre intern `id` sammen med `externalId`.

## Oppdatering

`PUT /api/v2/departments/{id}` er en full overskriving av feltene som V2 kan
skrive. Bruk arbeidsflyten GET – endre – PUT – GET. Felter som utelates kan bli
tømt; send derfor den komplette ønskede tilstanden.

Rute-ID-en bestemmer hvilken avdeling som endres. Vedlikehold kortbetegnelsen i
`abbreviation`. `code` brukes som fallback ved oppretting, men endres ikke som et
uavhengig felt av PUT. `unit` er også bare satt ved oppretting i dagens kontrakt.

API-et validerer unik kortbetegnelse. Det validerer ikke alle mulige feil i
foreldrehierarkiet eller unik `externalId`; integrasjonen må hindre selvreferanse,
sirkler og duplikate eksterne ID-er før PUT.

## Aktivering og deaktivering

| Ønsket tilstand | Rute |
|---|---|
| Aktiv | `PUT /api/v2/departments/{departmentId}/activation` |
| Inaktiv | `DELETE /api/v2/departments/{departmentId}/activation` |

Deaktivering setter sluttdato på den valgte avdelingen. Den flytter ikke
brukere, omfordeler ikke saker og deaktiverer ikke automatisk underavdelinger
eller tilgangsgrupper. Kunden må fullføre disse aktivitetene i sin
organisasjonsendringsprosess før avdelingen tas ut av bruk.

## Postfordeler

En avdeling kan referere til en tilgangsgruppe i `mailDistributionGroup`.
Medlemskapet vedlikeholdes med eksakt ekstern avdelings-ID:

- `PUT /api/v2/departments/external/{externalId}/post-distributors/{userGidId}`
- `DELETE /api/v2/departments/external/{externalId}/post-distributors/{userGidId}`

Avdelingen, brukeren og den konfigurerte postfordelergruppen må finnes.
Kontroller medlemskapet i tilgangsgruppen etter endringen.

## Akseptansekontroll

- Hierarkisk og flat liste viser den nye eller endrede avdelingen riktig.
- `externalId` gir nøyaktig ett treff.
- Forelder, leder og kortbetegnelse er korrekte.
- Aktive datoer samsvarer med ønsket tilstand.
- Berørte brukere, saker, køer og underavdelinger er håndtert utenfor selve
  aktiveringskallet.
- Eventuell postfordelergruppe finnes og har forventede medlemmer.
