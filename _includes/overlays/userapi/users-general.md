# Users
General note on users endpoints: From version `3.1.2` it was introduced a query parameter for defining which lookup field to use then searching for users. Query parameter name is `lookupField` and is used as follow:
```curl
http get /api/users/ABUSER?lookupField=Code
``` 
The following example will return a user that has the ABUSER as Code. Default for lookup field is Id. Possible values are Id and Code.
Using lookup field other than Id must be defined using this query parameter. 

All user endpoints which requires finding a user, have this query parameter. For `POST` and `PUT` http verbs, lookup field is part of the request body. See Create User example.
