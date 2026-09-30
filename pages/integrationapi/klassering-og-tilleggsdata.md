---
title: Klassering og tilleggsdata
permalink: /integrationapi_classification.html
---

# Klassering og tilleggsdata

## Klassering på sak

| Rute | Innhold |
|---|---|
| `GET /api/integration/sak/{id}/klassering` | Klasseringene på saken. |
| `GET /api/integration/sak/{id}/klasseringsett` | Klasseringssettet. |
| `POST /api/integration/sak/sok/klassering` | Saker som matcher en liste med `KlasseringKriterium`. |
| `POST /api/integration/klassering/update` | Oppdaterer klassering. Kroppen har `sakId` og `klasseringer`. |

`SortOrder` må være større enn 0 når feltet er satt. Ellers svarer
oppdateringen **400** med `ApiError` og teksten
`SortOrder must be greater than 0`.

## Lovlige ordningsverdier

`GET /api/integration/klassering/{name}/values` henter forhåndsdefinerte
verdier for et ordningsprinsipp. `name` skilles ikke på store og små
bokstaver. Valgfri query `query` filtrerer.

Noen prinsipper, for eksempel offnr og pnr, returnerer ikke treff uten
`query`. Andre filtrerer listen som ellers ville blitt returnert.

| Kode | Når |
|---|---|
| 200 | Verdier i listen `Ordningsverdi`. |
| 204 | Prinsippet har ingen forhåndsdefinerte verdier. De kan likevel valideres på annen måte. |
| 400 | `name` mangler eller er ugyldig. Kroppen er tekst. |
| 404 | Prinsippet finnes ikke, eller oppslaget kaster `ArgumentNullException`. |
| 500 | Annen feil. Kroppen er `ApiError`. |

Verdier merket sladdet har ikke den ekte `ordnVerdi`.
`POST /api/integration/klassering/unredact` fjerner sladdingen når brukeren
har lov, og logger oppslaget. Kroppen er `Ordningsverdi` fra values-kallet.
Svaret er samme objekt med usladdet `ordnVerdi` hvis tilgangen holder.
Ugyldig id, eller forsøk på å usladde en verdi som ikke er sladdet, gir
**400** med `ApiError`.

## Tilleggsdata

Katalog over feltene, uavhengig av én sak eller journalpost:

- `GET /api/integration/sak/tilleggsdata`
- `GET /api/integration/journalpost/tilleggsdata`

Verdier på ett objekt:

- `GET /api/integration/sak/{id}/tilleggsdata`
- `GET /api/integration/journalpost/{id}/tilleggsdata`

`.../tilleggsdata/list` returnerer samme data flatet ut
(`FlattenedTilleggsDataSett`), som er enklere å lese for klienter som ikke
skal traversere treet.

`POST /api/integration/tilleggsdata/update` skriver verdier inn i en
eksisterende eller ny revisjon. Kroppen har `sakId` eller `jpId`,
`nyRevisjon`, valgfri `revisjonId` og `tilleggsData`.
