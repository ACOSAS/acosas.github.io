---
title: Acos User Api overview
keywords: json, userapi, schemas
permalink: user_api_index.html
---
# Code Examples

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

```cs
    http get to /api/users/
```
Be warned that this may return a lot of information. Future versions of this api may restrict the number of returned users. 


## Get a User

To get the stored information on a given user call 

```cs
    http get to /api/users/{id}
```

**{id}** is the value used in the field username used when creating a user, or found in the field username when getting a list of users. 

## Create User

```cs
    http post to /api/users
```
A user must be defined in WebSak and given role access and concrete permissions. The simplest way to create a user is to use a template, and give the permissions to the template. This sample shows how to create a user using the minimum amount of information: 

```json
{
    "username": "TESTSYS",
    "accessTemplateId": "86898",
    "mailAddresses": ["navn@domene.no"],
    "lookupField": "Code",
    "userType": "B",
    "userAccesses": [{
        "domain": " pit-test.no ",
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


## Update User
To update a user use http put to /api/users/{id}. Send a complete user object. The changed values will be replaced. Username and code should not be changed: 

```json
{
    "username": "TESTSYS",
    "accessTemplateId": "86898",
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
 
