---
title: Acos Mottak WebApi overview
keywords: json, mottak, schemas
permalink: arkivmelding_index.html
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

            var response = await http.PostAsync("api/6CF63C7F-B738-4B0E-BB50-08080B0360F1/arkiverdokument",
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
{%include links.html %}
