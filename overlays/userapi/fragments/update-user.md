## Update User
To update a user use http put to /api/users/{id}. Send a complete user object. The changed values will be replaced. Username and code should not be changed: 

```json
{
    "username": "TESTSYS",
    "accessTemplateId": "86898",
    "departmentCode":"code",
    "mailAddresses": ["navn2@domene.no"],
    "lookupField": "Code",
    "userType": "B",
    "userAccesses": [{
        "domain": " domene.no ",
        "provider": "adfs",
        "key": "navn@domene.no"
    }],
    "code": "TESTSYS",
    "name": "Testbruker Brukeradmin nyttnavn",
    "title": "Testbruker",
    "postalNo": "0001",
    "contact": "string",
    "addr": "Veien 2",
    "mobile": "99889988",
    "emailAddr": "navn2@domene.no"
}

```
