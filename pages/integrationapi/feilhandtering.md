---
title: Feilhåndtering
permalink: /integrationapi_errors.html
---

# Feilhåndtering

Felles for alle ruter i `IntegrationController`:

| Kode | Når |
|---|---|
| 401 | Access token mangler eller er ugyldig. Også når skjema-kallet fanger tilgangsfeil. |
| 403 | Tokenet har ikke tilgang til API-et eller dataene. |

Øvrige koder er knyttet til enkeltkall. OpenAPI lister ofte bare 200, 401 og
403. Tabellen under er det koden faktisk returnerer.

| Kode | Hvor |
|---|---|
| 200 | Vanlig lesing. Test-ruten returnerer tekst `foo`. Skjemasjekk returnerer `{ "resp": true/false }`. Opplasting returnerer dokument-id. |
| 201 | Ny merknad på sak eller journalpost (`Created()`). XML-kommentaren på metoden sier 204. |
| 204 | Klassering uten forhåndsdefinerte verdier. |
| 400 | Ugyldig `admEnhetId`, ugyldig klasseringsnavn, `SortOrder` mindre enn eller lik 0, usladding som ikke er lov, merknadstype som ikke finnes, opplasting uten fil. |
| 404 | Ukjent sak eller journalpost ved ny merknad, ukjent skjema, ukjent ordningsprinsipp, dokumentversjon uten fil. |
| 500 | Uventet feil. JSON Patch av kontakt og flere skjema-kall legger unntaket i kroppen. |
| 502 | Search API kan ikke nås. |
| 504 | Search API svarer ikke i tide. |

`ApiError` brukes der Swagger er annotert med den typen (klassering values
500, unredact 400/500). Feltene er `message`, `exceptionMessage`,
`exceptionType`, `stackTrace`, `innerException` og `referanseId`.

Nedlasting som ikke finner fil, bruker `ProblemDetails` med `title`,
`detail` og `status` 404.

Merknad som ikke finner sak eller journalpost, returnerer `BadRequest`
med statuskode satt til 404. Kroppen er modellfeil, ikke `ProblemDetails`.
