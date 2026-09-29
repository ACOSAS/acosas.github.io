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
#By default limit is 100 => Use limit and offset to get more data.
$response = Invoke-RestMethod -Uri "$($plussApiBaseUrl)api/users/?limit=100&offset=0" -Method GET -Headers $plussRequestHeader

write-output $response
```
