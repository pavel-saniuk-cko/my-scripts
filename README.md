# Automation Scripts
The repo contains some automation scripts which can be helpful to simplify manual work routine.

## dotnet_migration_script.py

It's a Python script which automates migration of ASP.Net Core project from 3.0 to 3.1. 
The script scans the given project directory for: _Docker_, _global.json_ and _*.csproj_ files and applies required changes as explained in this [article](https://docs.microsoft.com/en-us/aspnet/core/migration/30-to-31?view=aspnetcore-3.1&tabs=visual-studio-code). 

Obviously, you need Python runtime installed at your machine.

The usage is very simple. In you favorite shell execute the script with a valid path to your project:

```
  python3 dotnet_migration_script.py "Projects/checkout-ap-router/"
```
The script writes to the output applied modifications, for example:

```
Modified: Projects/checkout-ap-router/global.json
 -  "version": "3.0.100"
 +  "version": "3.1.102"

Modified: Projects/checkout-ap-router/test/ApmRouter.Common.UnitTests/ApmRouter.Common.UnitTests.csproj
 -  <TargetFramework>netcoreapp3.0</TargetFramework>
 +  <TargetFramework>netcoreapp3.1</TargetFramework>
 
 Modified: Projects/checkout-ap-router/src/ApmRouter.Common/ApmRouter.Common.csproj
 -  <PackageReference Include="Microsoft.AspNetCore.TestHost" Version="3.0.0" />
 +  <PackageReference Include="Microsoft.AspNetCore.TestHost" Version="3.1.1" />

Modified: Projects/checkout-ap-router/src/ApmRouter.WebApi.Internal/Dockerfile
 -  FROM mcr.microsoft.com/dotnet/core/sdk:3.0.100-alpine3.9  AS build
 +  FROM mcr.microsoft.com/dotnet/core/sdk:3.1.102-alpine3.11  AS build

Modified: Projects/checkout-ap-router/src/ApmRouter.WebApi.Internal/Dockerfile
 -  FROM mcr.microsoft.com/dotnet/core/aspnet:3.0.0-alpine3.9
 +  FROM mcr.microsoft.com/dotnet/core/aspnet:3.1.2-alpine3.11
```

Will keep silence if nothing was updated.
