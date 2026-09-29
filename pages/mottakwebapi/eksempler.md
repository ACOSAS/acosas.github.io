---
title: Kodeeksempler
permalink: /mottakwebapi_examples.html
---

# Kodeeksempler

Eksemplene bruker plassholdere. Erstatt

- `<mottak-webapi-vert>` med vertsnavnet for miljøet
- `<tenant-api-key>` med GUID tildelt i Mottak+
- `arkivmelding.zip` med den lokale ZIP-filen

Alle eksempler bruker HTTPS, beregner SHA256 dynamisk og sender
`type` som matcher ruten.

## curl — POST /arkivmelding

```bash
TENANT="<tenant-api-key>"
HOST="https://<mottak-webapi-vert>"
ZIP="arkivmelding.zip"
HASH="$(sha256sum "$ZIP" | awk '{print toupper($1)}')"
BOUNDARY="$(openssl rand -hex 16)"
FILENAME="$(basename "$ZIP")"

{
  printf -- "--%s\r\n" "$BOUNDARY"
  printf "Content-Type: application/json\r\n\r\n"
  printf '{"type":"arkivmelding","files":[{"contentid":"content1","filename":"%s","hash":"%s","alg":"SHA256","metadata":false}]}\r\n' "$FILENAME" "$HASH"
  printf -- "--%s\r\n" "$BOUNDARY"
  printf "Content-Disposition: form-data; name=\"arkivmelding\"; filename=\"%s\"\r\n" "$FILENAME"
  printf "Content-Type: application/zip\r\n"
  printf "Content-Id: content1\r\n\r\n"
  cat "$ZIP"
  printf "\r\n--%s--\r\n" "$BOUNDARY"
} | curl -sS -X POST \
  -H "Accept: application/json" \
  -H "Content-Type: multipart/related; boundary=${BOUNDARY}" \
  --data-binary @- \
  "${HOST}/api/${TENANT}/arkivmelding"
```

## curl — GET /arkivmelding/test

```bash
curl -sS -H "Accept: application/json" \
  "https://<mottak-webapi-vert>/api/<tenant-api-key>/arkivmelding/test"
```

## C# — POST /arkivmelding

```csharp
using System.Net.Http.Headers;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;

public static async Task SendArkivmeldingAsync(string zipPath)
{
    var zipBytes = await File.ReadAllBytesAsync(zipPath);
    var hash = Convert.ToHexString(SHA256.HashData(zipBytes));
    var fileName = Path.GetFileName(zipPath);

    using var http = new HttpClient
    {
        BaseAddress = new Uri("https://<mottak-webapi-vert>/")
    };
    http.DefaultRequestHeaders.Accept.Add(
        new MediaTypeWithQualityHeaderValue("application/json"));

    var multipart = new MultipartContent("related", Guid.NewGuid().ToString("N"));
    var metadata = new
    {
        type = "arkivmelding",
        files = new[]
        {
            new
            {
                contentid = "content1",
                filename = fileName,
                hash,
                alg = "SHA256",
                metadata = false
            }
        }
    };
    multipart.Add(new StringContent(
        JsonSerializer.Serialize(metadata),
        Encoding.UTF8,
        "application/json"));

    var fileContent = new ByteArrayContent(zipBytes);
    fileContent.Headers.Add("Content-Disposition",
        $"form-data; name=\"arkivmelding\"; filename=\"{fileName}\"");
    fileContent.Headers.Add("Content-Type", "application/zip");
    fileContent.Headers.Add("Content-Id", "content1");
    multipart.Add(fileContent);

    using var response = await http.PostAsync(
        "api/<tenant-api-key>/arkivmelding",
        multipart);
    response.EnsureSuccessStatusCode();
}
```

For `/arkivmelding/arkiverdokument`: sett `type` til `"melding"` og
`name="melding"` i `Content-Disposition`.

## PHP — POST /arkiverdokument

```php
<?php
function sendMeldingAsync(string $meldingZip): void
{
    $client = new GuzzleHttp\Client([
        'base_uri' => 'https://<mottak-webapi-vert>'
    ]);

    $hash = strtoupper(hash_file('sha256', $meldingZip));
    $filnavn = basename($meldingZip);
    $metadata = json_encode([
        'type' => 'melding',
        'files' => [[
            'contentid' => 'content1',
            'filename' => $filnavn,
            'hash' => $hash,
            'alg' => 'SHA256',
            'metadata' => false
        ]]
    ]);

    $boundary = bin2hex(random_bytes(16));
    $multipart = new GuzzleHttp\Psr7\MultipartStream([
        [
            'name' => 'metadata',
            'contents' => $metadata,
            'headers' => ['Content-Type' => 'application/json']
        ],
        [
            'name' => 'melding',
            'contents' => fopen($meldingZip, 'r'),
            'filename' => $filnavn,
            'headers' => [
                'Content-Type' => 'application/zip',
                'Content-Id' => 'content1'
            ]
        ]
    ], $boundary);

    $client->post('/api/<tenant-api-key>/arkivmelding/arkiverdokument', [
        'headers' => [
            'Accept' => 'application/json',
            'Content-Type' => 'multipart/related; boundary=' . $boundary
        ],
        'body' => $multipart
    ]);
}
```

## Python — POST /arkiverdokument

```python
import hashlib
import os
import aiohttp
from aiohttp import MultipartWriter


def generate_hash(file_content: bytes) -> str:
    return hashlib.sha256(file_content).hexdigest().upper()


async def send_melding_async(zip_path: str) -> tuple[int, str]:
    with open(zip_path, "rb") as handle:
        zip_content = handle.read()

    filename = os.path.basename(zip_path)
    metadata = {
        "type": "melding",
        "files": [
            {
                "contentid": "content1",
                "filename": filename,
                "hash": generate_hash(zip_content),
                "alg": "SHA256",
                "metadata": False,
            }
        ],
    }

    boundary = os.urandom(16).hex()
    form = MultipartWriter("related", boundary=boundary)
    form.append_json(metadata, {"Content-Type": "application/json"})
    form.append(zip_content, {
        "Content-Type": "application/zip",
        "Content-Disposition": f'form-data; name="melding"; filename="{filename}"',
        "Content-Id": "content1",
    })

    url = "https://<mottak-webapi-vert>/api/<tenant-api-key>/arkivmelding/arkiverdokument"
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url,
            data=form,
            headers={"Accept": "application/json"},
            ssl=True,
        ) as response:
            return response.status, await response.text()
```
