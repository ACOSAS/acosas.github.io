HTTP **201 Created** betyr at importobjektet er lagret i Mottak. Kroppen er
JSON for den mottatte filen, ikke saksnummer eller journalpostnummer fra WebSak.

Tjenesten har ingen unikhetssjekk på `messageId`. Retry kan gi duplikat. Se
[feilhåndtering og drift](/mottakwebapi_errors.html).
