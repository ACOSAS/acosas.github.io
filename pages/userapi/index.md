---
title: UserAPI og SCIM
permalink: /userapi_guide.html
---

# ACOS WebSak UserAPI og SCIM

UserAPI gir kundens brukeradministrative system tilgang til å administrere brukere,
avdelinger, roller og tilgangsgrupper i ACOS WebSak. Det samme API-et eksponerer et
SCIM 2.0-grensesnitt i beta for automatisk provisjonering fra Microsoft Entra ID.
REST UserAPI er ikke omfattet av beta-statusen.

Dokumentasjonen er skrevet for identitetsforvaltere, WebSak-forvaltere,
integrasjonsutviklere og teknisk drift. Norsk Markdown i denne mappen er den
autoritative kundedokumentasjonen.

## Versjon og gyldighet

Dokumentasjonsversjon: 1.0, sist faglig oppdatert 2026-09-01. Den beskriver
UserAPI 3.3 og SCIM-kontrakten på `master`. Publiserte sider viser eksakt
UserAPI-versjon, commit SHA og genereringstidspunkt fra bygget som produserte
OpenAPI-referansen.

Ved motstrid gjelder denne prioriteten:

1. implementasjon og automatiserte tester
2. OpenAPI-dokumentet generert fra samme commit
3. Markdown i `docs/customer/`
4. historiske dokumenter i `docs/archive/`

## Komponenter og dataflyt

Kundens integrasjonsflate består av det produksjonsklare REST UserAPI-et og en
separat SCIM-beta. Leverandørens interne installasjons- og driftsaktiviteter er
ikke del av denne kundedokumentasjonen.

```text
Microsoft Entra ID                         Integrasjonsklient
  |  SCIM beta / userapi.scim                |  REST / userapi
  +----------------------+--------------------+
                         v
              ACOS WebSak UserAPI
                 |            |
                 |            +--> IdentityServer intern-API
                 |                 (loginmapping)
                 v
              ACOS WebSak
       (brukere, avdelinger, roller,
        funksjoner og tilgangsgrupper)

WebSak-klient -- OIDC --> IdentityServer -- federation --> Entra ID / annen IdP
```

UserAPI er adapteren mellom standardiserte HTTP-kontrakter og WebSaks
brukeradministrasjon. SCIM har ikke et eget datalager. Operasjoner som berører
både WebSak og IdentityServer er derfor ikke atomiske på tvers av systemene.

## Start her

- [Identitet, autentisering og tilgang](/userapi_identity_and_access.html)
- [SCIM-provisjonering fra Entra ID (beta)](/userapi_scim_guide.html)
- [REST UserAPI](/userapi_rest_guide.html)
- [Tilgangsgrupper via REST](/userapi_rest_access_groups.html)
- [Roller og tilgangsfunksjoner via REST](/userapi_rest_roles.html)
- [Avdelinger via REST](/userapi_rest_departments.html)
- [Feltmapping](/userapi_field_mapping.html)
- [Kundespesifikk konfigurasjonsmal](/userapi_configuration_template.html)
- [Legacy-endepunkter](/userapi_legacy.html)

Den genererte REST- og SCIM-referansen publiseres ved siden av disse guidene.
OpenAPI er detaljkilden for alle ruter, parametere, skjemaer og statuskoder.
