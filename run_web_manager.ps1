# PowerShell Orchestrator to launch the WT 3D Scale Model Manager web interface

$ErrorActionPreference = "Stop"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "Starting War Thunder 3D Scale Model Manager..." -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Create config.json from example if missing
$configPath = Join-Path -Path $PSScriptRoot -ChildPath "config.json"
$configExamplePath = Join-Path -Path $PSScriptRoot -ChildPath "config.json.example"

if (-not (Test-Path -Path $configPath) -and (Test-Path -Path $configExamplePath)) {
    Write-Host "Creating config.json from config.json.example..." -ForegroundColor Yellow
    Copy-Item -Path $configExamplePath -Destination $configPath
}

# 2. Check and clone dependencies if missing
$toolsGitPath = Join-Path -Path $PSScriptRoot -ChildPath "tools_git"
$dagorExplorerPath = Join-Path -Path $PSScriptRoot -ChildPath "dagor_explorer"

if (-not (Test-Path -Path $toolsGitPath)) {
    Write-Host "Dependency 'tools_git' is missing. Cloning from repository..." -ForegroundColor Yellow
    git clone https://github.com/klensy/wt-tools.git "$toolsGitPath"
}

if (-not (Test-Path -Path $dagorExplorerPath)) {
    Write-Host "Dependency 'dagor_explorer' is missing. Cloning from repository..." -ForegroundColor Yellow
    git clone https://github.com/quentin-dh/Dagor-Asset-Explorer.git "$dagorExplorerPath"
}

# 2. Start a hidden background process to launch the browser in 2 seconds
Write-Host "Scheduling browser launch..." -ForegroundColor Yellow
Start-Process powershell.exe -ArgumentList "-Command", "Start-Sleep -Seconds 2; Start-Process 'http://localhost:8000'" -WindowStyle Hidden

# 3. Run the python web server (this blocks the console and keeps the server alive)
Write-Host "Launching Python web server backend (http://localhost:8000)..." -ForegroundColor Yellow
Write-Host "Press Ctrl+C in this window to stop the server." -ForegroundColor DarkGray
python web_server.py
