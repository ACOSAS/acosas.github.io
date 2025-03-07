---
title: Acos Mottak WebApi overview
keywords: json, mottak, schemas
permalink: acos_mottak_webapi_index.html
---
# Code Examples

## POST /arkivmelding
```cs
public async Task Post(){
  await SendArkivmeldingAsync(@"c:\temp\arkivmelding.zip");
}

public async Task SendArkivmeldingAsync(string arkivmeldingZip)
{
    using (var http = new HttpClient()
    {
        BaseAddress = new Uri("http://arkivmeldingapi.azurewebsites.net"),
    })
    {
        http.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));
        
        var mulitipart = new MultipartContent("related", Guid.NewGuid().ToString("N"));

        var filnavn = Path.GetFileName(arkivmeldingZip);
        var metadata = new {type = "arkivmelding", files = new[] {new
        {
            contentid="content1",
            filename=filnavn,
            hash="F7F1C95DC61E52995A15FA2155403AC6752EC390D4743ACD35DACEA68680A536",
            alg="SHA256",
            metadata=false
        }}};

        var metaContent= new StringContent(JsonConvert.SerializeObject(metadata), Encoding.UTF8, "application/json");

        mulitipart.Add(metaContent);
        var fileBytesContent = new ByteArrayContent(File.ReadAllBytes(arkivmeldingZip));

        fileBytesContent.Headers.Add("Content-Disposition", $"form-data; name=\"arkivmelding\"; filename=\"{filnavn}\"");
        fileBytesContent.Headers.Add("Content-Type", "application/zip");
        fileBytesContent.Headers.Add("Content-Id", "content1");
        mulitipart.Add(fileBytesContent);

        try
        {

            var response = await http.PostAsync("api/6CF63C7F-B738-4B0E-BB50-08080B0360F1/arkivmelding/",
                mulitipart);

            response.EnsureSuccessStatusCode();
        }
        catch (Exception ex)
        {
            Console.WriteLine("error: {0}", ex.Message);
        }
    }
}
```

## POST /arkivmelding/arkiverdokument
```cs
public async Task Post(){
  await SendMeldingAsync(@"c:\temp\melding.zip");
}

public async Task SendMeldingAsync(string meldingZip)
{
    using (var http = new HttpClient()
    {
        BaseAddress = new Uri("http://arkivmeldingapi.azurewebsites.net"),
    })
    {
        http.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));
        
        
        var mulitipart = new MultipartContent("related", Guid.NewGuid().ToString("N"));

        var filnavn = Path.GetFileName(meldingZip);
        var metadata = new {type = "melding", files = new[] {new
        {
            contentid="content1",
            filename=filnavn,
            hash="F7F1C95DC61E52995A15FA2155403AC6752EC390D4743ACD35DACEA68680A536", //må være korrekt hash av meldingZip
            alg="SHA256",
            metadata=false
        }}};

        var metaContent= new StringContent(JsonConvert.SerializeObject(metadata), Encoding.UTF8, "application/json");

        mulitipart.Add(metaContent);
        var fileBytesContent = new ByteArrayContent(File.ReadAllBytes(meldingZip));

        fileBytesContent.Headers.Add("Content-Disposition", $"form-data; name=\"melding\"; filename=\"{filnavn}\"");
        fileBytesContent.Headers.Add("Content-Type", "application/zip");
        fileBytesContent.Headers.Add("Content-Id", "content1");
        mulitipart.Add(fileBytesContent);

        try
        {

            var response = await http.PostAsync("api/6CF63C7F-B738-4B0E-BB50-08080B0360F1/arkivmelding/arkiverdokument",
                mulitipart);


            response.EnsureSuccessStatusCode();
        }
        catch (Exception ex)
        {
            Console.WriteLine("error: {0}", ex.Message);
        }
    }
}
```

```php
<?php
public function sendMeldingAsync($meldingZip)
{
    $client = new Client(['base_uri' => 'https://arkivmelding-api-test.azurewebsites.net']);

    // calculate SHA256 hash from $meldingZip
    $hash = strtoupper(hash_file('sha256', $meldingZip));

    $filnavn = basename($meldingZip);
    $metadata = [
        'type' => 'arkivmelding',
        'files' => [
            [
                'contentid' => 'content1',
                'filename' => $filnavn,
                'hash' => $hash,
                'alg' => 'SHA256',
                'metadata' => false
            ]
        ]
    ];

    $metaContent = json_encode($metadata);

    // Create a boundary
    $boundary = bin2hex(random_bytes(20));

    $multipart = new MultipartStream([
        [
            'name'     => 'metadata',
            'contents' => $metaContent,
            'headers'  => ['Content-Type' => 'application/json']
        ],
        [
            'name'     => 'melding',
            'contents' => fopen($meldingZip, 'r'),
            'filename' => $filnavn,
            'headers'  => [
                'Content-Type' => 'application/zip',
                'Content-Id'   => 'content1',
                'Content-Disposition' => 'form-data; name="arkivmelding" filename="' . $filnavn . '"'
            ]
        ]
    ], $boundary);

    try {
        $response = $client->post('/api/6CF63C7F-B738-4B0E-BB50-08080B0360F1/arkivmelding/arkiverdokument', [
            'headers' => [
                'Accept' => 'application/json',
                'Content-Type' => 'multipart/related; boundary=' . $boundary
            ],
            'body' => $multipart
        ]);
    } catch (Exception $e) {

        echo "error: " . $e->getMessage();       
    }
}
```

```python
#imports
import hashlib
import base64
import os
import json
from io import BytesIO
import aiohttp
from aiohttp import MultipartWriter

...

def generate_hash(file_content):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(file_content)
    return sha256_hash.hexdigest().upper()

async def send_melding_async(zip_content):
    url = "https://arkivmelding-api-test.azurewebsites.net/api/6CF63C7F-B738-4B0E-BB50-08080B0360F1/arkivmelding/arkiverdokument"
    # Beregn SHA-256 hash av innholdet i zip-filen
    hash_value = generate_hash(zip_content)

    # Forbered metadata
    metadata = {
        "type": "melding",
        "files": [
            {
                "contentid": "content1",
                "filename": "arkivmelding.zip",
                "hash": hash_value,
                "alg": "SHA256",
                "metadata": False
            }
        ]
    }

    # Opprett en unik boundary
    boundary = os.urandom(16).hex()
    # Opprett MultipartWriter for multipart data med spesifikk boundary
    # Legg til metadata i multipart-forespørselen
    form_data = MultipartWriter('related', boundary=boundary)
    metadata_part = form_data.append_json(metadata, {
        'Content-Type': 'application/json',
    })

    # Legg til filinnholdet (ZIP-filen) i multipart-forespørselen med korrekt Content-Id
    file_part = form_data.append(zip_content, {
        'Content-Type': 'application/zip',
        'Content-Disposition': f'form-data; name="melding"; filename="arkivmelding.zip"',
        'Content-Id': 'content1'
    })

    # Send forespørselen
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=form_data, headers={
            'Accept': 'application/json',
            'Content-Type': f'multipart/related; boundary={boundary}'
        }, ssl=True) as response:
            response_text = await response.text()
            return response.status, response_text  # Returner status og respons-innhold
```
{%include links.html %}
