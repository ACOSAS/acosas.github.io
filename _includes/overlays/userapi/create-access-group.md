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
