# PowerShell Orchestrator for Messerschmitt Bf 109 3D Mesh Extraction

$ErrorActionPreference = "Stop"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "Starting Messerschmitt Bf 109 3D Extraction Pipeline" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Execute the Python extraction script
Write-Host "Executing Python extraction script..." -ForegroundColor Yellow
python extract_bf109.py

# 2. Local cleanup
Write-Host "Cleaning up temporary files and cache directories..." -ForegroundColor Yellow

$tempDirs = @(
    "temp_aces",
    "temp_char",
    "temp_game",
    "temp_grp",
    "temp_grp_hdr",
    "temp_mis",
    "temp_export"
)

foreach ($dir in $tempDirs) {
    $path = Join-Path -Path "." -ChildPath $dir
    if (Test-Path -Path $path) {
        Write-Host "Removing directory: $path" -ForegroundColor DarkGray
        Remove-Item -Path $path -Recurse -Force
    }
}

# Clean up any other .py files except the main extraction script
Get-ChildItem -Path "." -Filter "*.py" | Where-Object { $_.Name -ne "extract_bf109.py" } | ForEach-Object {
    Write-Host "Removing temporary script: $($_.Name)" -ForegroundColor DarkGray
    Remove-Item -Path $_.FullName -Force
}

Write-Host "`nPipeline execution completed successfully!" -ForegroundColor Green
Write-Host "The final assets are located in .\Bf109_Raw_Asset" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan
