---
title: Acos User Api overview
keywords: json, userapi, schemas
permalink: user_api_index.html
---
# Code Examples

## Authenticate UserAPI client
In order to use the rest enpoints available in UserApi, the consuming client needs to authenticate. Authentication is done through Acos Identity server.

The following example will authenticate a client using PowerShell script. 
```ps1
#authenticate_identity_server
#Clear-Host
$identityserverUrl = "https://identityserver/"
$tokenendpointurl = $identityserverUrl + "connect/token"
$granttype = "client_credentials" # client_credentials / password 
$client_id = "userapi"
$client_secret = "userapi"
$scope = "userapi"

$body = @{
    grant_type = $granttype
    scope = $scope
    client_id = $client_id
    client_secret = $client_secret        
}

$resp = Invoke-RestMethod -Method Post -Body $body -Uri $tokenendpointurl 
#Write-Host $resp
$token = $resp.access_token

$plussApiBaseUrl = "https://UserApi/"

$plussRequestHeader=@{
    'Authorization' = "Bearer $token"
    'Content-Type' = 'application/json'
    'Accept' = 'application/json'
}
#Gets users
#By default limit is 10000 => Use limit and offset to get more data.
$response = Invoke-RestMethod -Uri "$($plussApiBaseUrl)api/users/?limit=1000&offset=0" -Method GET -Headers $plussRequestHeader

write-output $response
```

## Create Department

```cs
POST /api/departments
```

Request body
```json
{     
    "departmentName":"Personalavdelingen",
    "departmentShortName":"PA",
    "departmentParentId":"123",
    "departmentHeadId":"1122"
}
```
Response
```json
{     
    "departmentName":"Personalavdelingen",
    "departmentShortName":"PA",
    "departmentId":124,
    "departmentParentId":"123",
    "departmentHeadId":"1122"
}
```

**departmentParentId**: The internal WebSak id of the parent department. For the initial create you need to get this information.  For sub-departments the returned value for departmentId can be used. 

**departmentHeadId**: Internal WebSak id for the department head. Can be found in the response from user creation - field **gidid**. 

## List All Users

To get the stored information for all users call 
### parameters
limit=1000 number of returned records<br>
offset=0 number of skipped records<br>
includeEmailAddresses=true (default false) true will cause email addresses to be populated **performance impact**<br>
includeUserAccess=true (default false) true will cause user functions to be populated **performance impact**<br>
includeRoles=true  (default false) true will cause user roles to be populated **performance impact**<br>
It is <em>recommended</em> to use /api/user/{id} to get full user profile. 

```curl
    http get to /api/users/?limit=1000&offset=0&includeEmailAddresses=true&includeUserAccess=true&includeRoles=true
```
Be warned that this may return a lot of information. Future versions of this api may restrict the number of returned users. Use limit and offset to reduce number of users returned. By default 10000 users will be returned. 


## Get a User

To get the stored information on a given user call 

```curl
    http get to /api/users/{id}
```

**{id}** is the value used in the field username used when creating a user, or found in the field username when getting a list of users. 

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
        "domain": " pit-test.no ",
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

## DeActivate User
To deactivate a user: 

```cs
    http post to /api/users/{id}/deactivate
```
***{id}***: replace ID with the value that was used in the username-field when creating user. 


##  Reactivate User
To reactivate a user previously deactivated: 

```cs
    http post to /api/users/{id}/activate
```
**{id}**: replace ID with the value that was used in the username-field when creating user. 

## Create Access Group

WebSak supports Access groups. An access group contains users, and can be added to cases and files. This api supports creation of access groups for future use - i.e. Create an access group for teachers for a certain class. 

```cs
    http post to /api/accessgroup 
```
Body of request

```json
{
    "GroupName": "TheGroupName"
}

```
The response contains the ID of the access group.

## Add User to Access Group
To add a user to an access group 

```cs
    http post to /api/Users/{id}/AddUserToAccessGroup/{accessGroupId}
```

**{id}** The User ID as in previous examples for user opetations
**{accessGroupId}** The ID returned when creating an access group. 
 
## Remove User from Access Group
To remove a user to an access group 

```cs
    http post to /api/Users/{id}/RemoveUserFromAccessGroup/{accessGroupId}
```

**{id}** The User ID as in previous examples for user opetations
**{accessGroupId}** The ID returned when creating an access group. 
 
