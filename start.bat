@echo off
title War Thunder 3D Scale Model Manager
echo ==========================================================
echo Starting War Thunder 3D Scale Model Manager...
echo ==========================================================

:: 1. Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not added to your PATH.
    echo Please install Python 3.10+ and make sure to check "Add Python to PATH".
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

:: 2. Install/verify requirements silently
echo Verifying python dependencies...
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo [WARNING] Failed to install python dependencies automatically.
    echo Trying to run anyway...
)

:: 3. Run the manager via PowerShell orchestrator
powershell -ExecutionPolicy Bypass -File .\run_web_manager.ps1
