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
