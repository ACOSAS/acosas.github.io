---
title: Filer
permalink: /integrationapi_files.html
---

# Filer på journalpost

Filinnhold ligger på dokumentversjoner. Metadata uten bytes hentes med
`GET /api/integration/journalpost/{id}/dokumenter`.

## Liste

`GET /api/integration/journalpost/{jpId}/attachments` returnerer filene gruppert
slik:

- `attachmentType` er `MainDocument` eller `Attachment`
- `versions` er synkende versjonsnummer
- hver versjon har `variants` med `id`, `fileName`, `contentType`, `hasFile`
  og `downloadUri` når filen finnes
- `activeFile` peker på den aktive varianten

`downloadUri` er absolutt URL til nedlastingsruten, bygget fra kallets skjema
og vert.

## Laste ned

`HEAD /api/integration/journalpost/{jpId}/attachments/{verId}` returnerer
ikke kroppen. Headere er `Content-Type`, `Content-Disposition`, `ETag`
(sjekksummen) og `Last-Modified`. Bruk HEAD for å se om filen er endret.

`GET` på samme sti strømmer filen. `ETag` er den samme sjekksummen.

Begge returnerer **404** `ProblemDetails` når journalposten ikke har
versjonen, eller når versjonen ikke har fil (opplasting pågår, eller filen
er slettet).

## Laste opp

Opplasting er `multipart/form-data` med ett filfelt `file`.

| Rute | Rolle |
|---|---|
| `POST /api/integration/journalpost/{jpid}/dokument/nytthoveddokument` | Ny fil blir hoveddokument. |
| `POST /api/integration/journalpost/{jpid}/dokument/nyttvedlegg` | Ny fil blir vedlegg. |

Begge har `DisableRequestSizeLimit` i koden. Faktisk grense styres av verten
(Kestrel eller omvendt proxy), ikke av et felt i denne kontrakten.

Svaret ved suksess er **200** og dokument-id som heltall. Mangler filen, er
kroppen teksten `No file sent with request` og status **400**. Hvis lagring
ikke gir en id, er kroppen `Unknown error` og status **400**.
