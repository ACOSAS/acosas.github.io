`files[].hash` er sjekksum av **hele ZIP-filen**, ikke av XML-innholdet alene.
Sammenligningen er eksakt. Kundeksemplene bruker SHA256 som heksadesimal streng
med store bokstaver. Feil hash gir HTTP 400 med tekst på formen
`<filnavn> bestod ikke hash validering`.
