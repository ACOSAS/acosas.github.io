---
title: Legacy-endepunkter
permalink: /userapi_legacy.html
---

# Legacy-endepunkter

Eldre UserAPI-versjoner brukte GET for flere mutasjoner. Rutene beholdes
midlertidig for bakoverkompatibilitet, men er deprecated og skal ikke brukes i
nye integrasjoner. De returnerer `Deprecation`, `Sunset` og `Link`-headere som
peker til erstatningen. Oppgitt sunset-dato i API-et er 2028-01-01.

## Anbefalte erstatninger

| Deprecated rute | Bruk i stedet |
|---|---|
| `GET /api/Users/{id}/Activate` | `PUT /api/v2/users/{id}/activation` |
| `GET /api/Users/{id}/Deactivate` | `DELETE /api/v2/users/{id}/activation` |
| `GET /api/Departments/{id}/activate` | `PUT /api/v2/departments/{id}/activation` |
| `GET /api/Departments/{id}/deactivate` | `DELETE /api/v2/departments/{id}/activation` |
| `GET /api/v2/departments/{id}/activate` | `PUT /api/v2/departments/{id}/activation` |
| `GET /api/v2/departments/{id}/deactivate` | `DELETE /api/v2/departments/{id}/activation` |
| `GET /api/Users/{id}/AddUserToAccessGroup/{groupId}` | `PUT /api/v2/accessgroups/{groupId}/members/{id}` |
| `GET /api/Users/{id}/RemoveUserFromAccessGroup/{groupId}` | `DELETE /api/v2/accessgroups/{groupId}/members/{id}` |
| `GET /api/Users/{id}/AddUserToAccessGroupByGroupName/{name}` | `PUT /api/v2/accessgroups/by-name/{name}/members/{id}` |
| `GET /api/Users/{id}/RemoveUserFromAccessGroupName/{name}` | `DELETE /api/v2/accessgroups/by-name/{name}/members/{id}` |
| `GET /api/Users/{id}/AddUserAsPostDistributor/{externalId}` | `PUT /api/v2/departments/external/{externalId}/post-distributors/{id}` |
| `GET /api/Users/{id}/RemoveUserAsPostDistributor/{externalId}` | `DELETE /api/v2/departments/external/{externalId}/post-distributors/{id}` |

Aliaset `/api/v2/departmentsv2` er også deprecated. Bruk
`/api/v2/departments` med samme resterende path.

## Migreringsråd

1. Finn alle kall til rutene i tabellen, også i skript og overvåking.
2. Bytt både HTTP-metode og path; ikke bare path.
3. Oppdater klientens forventede statuskoder og retry-policy.
4. Test aktivering/deaktivering og gruppemedlemskap i et ikke-produksjonsmiljø.
5. Overvåk `Deprecation`-headere til legacy-trafikken er borte.

Legacy-rutene vises fortsatt i REST OpenAPI så lenge de finnes i runtime. Denne
siden er den normative migreringsoversikten.
