## Create User

```curl
    http post to /api/users
```
```cs
//user => json example
var userRequestString = JsonSerializer.Serialize(
    user
    , new JsonSerializerOptions { WriteIndented = false }
);
var usersResponse = await _httpClient.PostAsync(
    "api/users"
    , new StringContent(
        userRequestString
        , encoding: System.Text.Encoding.UTF8, "application/json"
    )
);
```
A user must be defined in WebSak and given role access and concrete permissions. The simplest way to create a user is to use a template, and give the permissions to the template. This sample shows how to create a user using the minimum amount of information: 
Use departmentCode to assing department to user. Department code is mapped against full department code **(SOA_AdmKort)**
If departmentCode is used externalDepartmentId will be disregarded

```json
{
    "username": "TESTSYS",
    "accessTemplateId": "86898",
    "departmentCode":"code", 
    "mailAddresses": ["navn@domene.no"],
    "lookupField": "Code",
    "userType": "B",
    "userAccesses": [{
        "domain": "domain.no ",
        "provider": "adfs",
        "key": "navn@domene.no"
    }],
    "code": "TESTSYS",
    "name": "Testbruker Brukeradmin",
    "title": "Testbruker",
    "postalNo": "0001",
    "contact": "string",
    "addr": "Veien 1",
    "mobile": "99889988",
    "emailAddr": "navn@domene.no"
}

```
### Important fields
**username**: If using AD the field must have the ad-user-name - ie the login-name.  

**accessTemplateID**: This field points to the WebSak ID of a template user. In Websak a user is defined, and is given roles and rights. For example one can define a template case worker, and a template document manager. A list over the actual templates must be given from a WebSak administrator to the integration developer. 

**userAcceses**: The field must contain information on the login-information that is given from the authentication provider. WebSak uses OPENID Connect, and the information given here is used to map the internal WebSak user to external autentication information. 

**departmentCode**: Code from full department code <em>(soa_admkort)</em>. User will be assigned to department having this code. 

**externalDepartmentId**: This field is mapped against misc1 on department, assigning user to department having this value. Value not found will assign user to user from accessTemplateId
