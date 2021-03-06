"""
   The script scans the given project directory for: _Docker_, _global.json_ and _*.csproj_ files and 
   applies required changes as explained in this [article](https://docs.microsoft.com/en-us/aspnet/core/migration/30-to-31?view=aspnetcore-3.1&tabs=visual-studio-code). 
"""

import os
import sys
import queue
import re

dockerLambda = lambda entry: os.path.basename(entry) == "Dockerfile"
globalJsonLambda = lambda entry: os.path.basename(entry) == "global.json"
csprojLambda = lambda entry: os.path.splitext(entry)[1] == ".csproj"

targetFramework = os.environ.get('DOTNET_MIGRATION_TARGET_FRAMEWORK') or "3.1"
packageVersion = os.environ.get('DOTNET_MIGRATION_PACKAGE_VERSION') or "3.1.11"
sdkVersion = os.environ.get('DOTNET_MIGRATION_SDK_VERSION') or "3.1.405"

fileProcessorMappings = {
    dockerLambda: lambda line: replace(line, dockerFileRegexReplacementMappings),
    globalJsonLambda: lambda line: replace(line, globalJsonRegexReplacementMappings),
    csprojLambda: lambda line: migrateProjFile(line)
}

dockerFileRegexReplacementMappings = [
    (re.compile(r"\S*mcr\.microsoft\.com\/dotnet\/core\/sdk:\S+"), "mcr.microsoft.com/dotnet/sdk:" + targetFramework),
    (re.compile(r"\S*mcr\.microsoft\.com\/dotnet\/core\/aspnet:\S+"), "mcr.microsoft.com/dotnet/aspnet:" + targetFramework),
    (re.compile(r"\S*mcr\.microsoft\.com\/dotnet\/core\/runtime:\S+"), "mcr.microsoft.com/dotnet/runtime:" + targetFramework)
]

globalJsonRegexReplacementMappings = [
    (re.compile(r"\"version\":\s?\"\d\.\d\.\d+\""), "\"version\": \"" + sdkVersion + "\"")
]   

projFileRegexReplacementMappings = [
    (re.compile(r"<TargetFramework>netcoreapp\S+<\/TargetFramework>"), "<TargetFramework>netcoreapp" + targetFramework + "</TargetFramework>")
]

def replace(line, mappings):
    for (regex, replacement) in mappings: 
        if regex.search(line):
            return regex.sub(replacement, line)
    return line

packageReferenceRegex = re.compile(r"<PackageReference Include=\"Microsoft\.AspNetCore.\S+\" Version=\"\d\.\d\.\d\".*\/>")
versionRegex = re.compile(r"Version=\"\d.\d.\d\"")

def migrateProjFile(line):
    if packageReferenceRegex.search(line):
        return versionRegex.sub("Version=\"" + packageVersion + "\"", line)
    return replace(line, projFileRegexReplacementMappings)

def printDiff(entry, originalLine, modifedLine):
    print("Modified: " + entry)
    print(" -  " + originalLine.strip())
    print(" +  " + modifedLine.strip() + "\r\n")

def processFile(entry):
    for targetFileLambda in fileProcessorMappings:
        if targetFileLambda(entry):
            stringContent = modify(entry, fileProcessorMappings.get(targetFileLambda))
            save(entry, stringContent)

def modify(entry, modifyLineLambda):
    stringContent = list()
    file = open(entry, "r")
    while True:
        line = file.readline()
        if not line:
            break

        modified = modifyLineLambda(line)
        if line != modified:
            printDiff(entry, line, modified)
        stringContent.append(modified)

    file.close()
    return stringContent

def save(entry, stringContent):
    file = open(entry, "w")
    file.writelines(stringContent)
    file.close

def main(projPath):
    ioQueue = queue.Queue()
    ioQueue.put(projPath)
    while ioQueue.empty() == False:
        observingPath = ioQueue.get()
        for entry in os.listdir(observingPath):
            entryPath = os.path.join(observingPath, entry)
            if os.path.isfile(entryPath):
                processFile(entryPath)
            elif os.path.isdir(entryPath):
                ioQueue.put(entryPath)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Error: try again with a path to your project root folder.")
    elif len(sys.argv) > 1:
        main(sys.argv[1])
