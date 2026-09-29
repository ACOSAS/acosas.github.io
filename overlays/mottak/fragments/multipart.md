Forespørselen er `multipart/related`, ikke JSON. Jekyll-REST-tabellen viser bare
`application/json`, så den er tom her.

Rekkefølgen er påkrevd: **JSON-manifest først**, deretter ZIP.

1. `Content-Type` på hele forespørselen: `multipart/related; boundary=<unik-streng>`.
2. Første del: JSON med `Content-Type: application/json`.
3. Andre del: ZIP med `Content-Disposition: form-data; name="arkivmelding"` eller
   `name="melding"`, `filename` lik `files[].filename`,
   `Content-Type: application/zip` og `Content-Id` lik `files[].contentid`.

Parseren matcher ZIP mot manifestet på **filnavn**. Se
[Sende arkivmelding](/mottakwebapi_send.html) for feltliste og eksempler.
