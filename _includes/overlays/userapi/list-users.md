## List All Users

To get the stored information for all users call 
### parameters
limit=100 number of returned records<br>
offset=0 number of skipped records<br>
includeEmailAddresses=true (default false) true will cause email addresses to be populated **performance impact**<br>
includeUserAccess=true (default false) true will cause user functions to be populated **performance impact**<br>
includeRoles=true  (default false) true will cause user roles to be populated **performance impact**<br>
It is <em>recommended</em> to use /api/user/{id} to get full user profile. 


```curl
    http get to /api/users/?limit=100&offset=0&includeEmailAddresses=true&includeUserAccess=true&includeRoles=true
```
Be warned that this may return a lot of information. Future versions of this api may restrict the number of returned users. Use limit and offset to reduce number of users returned. By default 100 users will be returned. 
