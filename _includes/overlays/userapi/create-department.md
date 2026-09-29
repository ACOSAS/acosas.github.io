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
