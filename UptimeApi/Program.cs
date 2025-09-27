var builder = WebApplication.CreateBuilder(args);

builder.WebHost.ConfigureKestrel(serverOptions =>
{
    serverOptions.ListenLocalhost(5025); // or 8000 if you prefer
});

var app = builder.Build();

app.UseDefaultFiles();
app.UseStaticFiles();

app.MapGet("/proxy-status", async context =>
{
    using var httpClient = new HttpClient();
    var json = await httpClient.GetStringAsync("https://statuspage.freshstatus.io/api/v1/summary");
    context.Response.ContentType = "application/json";
    await context.Response.WriteAsync(json);
});

app.Run();