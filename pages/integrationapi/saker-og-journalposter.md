---
title: Saker og journalposter
permalink: /integrationapi_cases.html
---

# Saker og journalposter

Identifikatorer i stien (`id`, `sakId`, `jpId`) er WebSak sine heltallige
nøkler.

## Opprette

| Rute | Hva koden gjør |
|---|---|
| `POST /api/integration/sak/ny` | Oppretter sak fra mal. Kroppen er `NySakRequest` med `tittel1` og `tittel2`. Svaret er full saksmodell. |
| `POST /api/integration/sak/nyframal` | Oppretter sak fra mal og mapper resultatet til integrasjonsmodellen `Sak`. |
| `POST /api/integration/journalpost/ny` | Oppretter journalpost fra mal på en sak. Svaret er journalpostens id (heltall). |

`nyframal` tar `malSakId`, `tittel1`, `tittel2`, valgfri `sakstype`,
`parentSakId`, `admEnhetId` og `klasseringer`. `journalpost/ny` tar `sakId`,
`malJpId`, `tittel` og valgfri `admEnhetId`.

`admEnhetId` slås opp i avdelingsregisteret. Ukjent id gir **400** med teksten
`Invalid AdmEnhetId`. Annen `AcosException` ved ny journalpost gir også 400
med unntaksteksten. Uventet feil gir **500**.

## Lese

| Rute | Innhold |
|---|---|
| `GET /api/integration/sak/{id}` | Saksdetaljer. |
| `GET /api/integration/sak/{id}/journalposter` | Journalposter på saken. Hver post får sakens visnings-id. |
| `GET /api/integration/journalpost/{id}` | Enkel journalpost. |
| `GET /api/integration/journalpost/{id}/full` | Journalpost med utvidet informasjon. |
| `GET /api/integration/journalpost/{id}/dokumenter` | Metadata for hoveddokument og vedlegg, ikke filbytes. |
| `GET /api/integration/kontaker/aktivbruker` | Kontakten for brukeren kallet kjører som. Stien er stavet `kontaker`. |

## Parter, mottakere og merknader

`GET /api/integration/sak/{sakId}/parter` lister parter.
`POST` på samme sti legger til parter. Kroppen har feltet `parter`.

`GET /api/integration/journalpost/{id}/mottakere` henter mottakere. Koden
henter person-id, og oppslaget logges i WebSak.
`POST /api/integration/journalpost/{jpId}/avsmottakere` legger til avsender
eller mottaker. `erKopiMottaker` styrer om kontakten er kopimottaker.

`PATCH /api/integration/journalpost/{jpId}/kontakter/{id}` oppdaterer en
kontakt med JSON Patch (`application/json` eller
`application/json-patch+json`). Svaret er `{ "resp": ... }`. Feil i kallet
returneres som **500** med unntaket i kroppen.

Merknader leses med GET på `/sak/{id}/merknader` og
`/journalpost/{id}/merknader`. Nye merknader postes som en **JSON-streng**
(ikke et objekt) til `.../merknader/{type}`:

```json
"Teksten i merknaden"
```

`type` er merknadstypen slik den står i klientens nedtrekksliste. Koden
returnerer `Created()` ved suksess, som er HTTP **201**. XML-kommentaren på
metoden sier 204. Ukjent sak eller journalpost gir **404**. Ugyldig type gir
**400** med modellfeil på `type`.

## Skjema

`POST /api/integration/skjema/lagreskjema` lagrer et skjema. Ukjent skjema
(`AcosException` med teksten `Not found`) gir **404**. Manglende tilgang gir
**401**. Annen feil gir **500**.

`GET /api/integration/skjema/kanlese/{skjemaref}` og
`.../kanskrive/{skjemaref}` svarer **200** med `{ "resp": <bool> }`. Ukjent
skjemareferanse gir **404**.

## Skjerming

`POST /api/integration/sak/{id}/screening` setter tilgangskode, avskjerming
og paragraf. `accessCode`, `screeningCode` og `section` kan være koden fra
registeret eller en numerisk id. `updateChildren`:

| Verdi | Virkning |
|---|---|
| `NoUpdate` | Underliggende oppdateres ikke. |
| `SetIfEmpty` | Underliggende oppdateres der verdien er tom. |
| `Overwrite` | Underliggende overskrives. |

Tom kropp kaster `ArgumentNullException` («Invalid format on post data»).
