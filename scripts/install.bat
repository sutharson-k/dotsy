@echo off
REM Dotsy Installation Script for Windows
REM This script installs dotsy using pip

setlocal enabledelayedexpansion

echo.
echo ██████████████████░░
echo ██████████████████░░
echo ████  ██████  ████░░
echo ████    ██    ████░░
echo ████          ████░░
echo ████  ██  ██  ████░░
echo ██      ██      ██░░
echo ██████████████████░░
echo ██████████████████░░
echo.
echo Starting Dotsy installation...
echo.

REM Check if Python is available
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python from https://python.org and try again
    exit /b 1
)

echo [INFO] Found Python:
python --version

REM Get the script directory (Dotsy root)
set "SCRIPT_DIR=%~dp0.."
echo [INFO] Installing from: %SCRIPT_DIR%

REM Install dotsy in editable mode
echo [INFO] Installing dotsy...
cd /d "%SCRIPT_DIR%"
py -m pip install -e .

if %errorlevel% neq 0 (
    echo [ERROR] Installation failed
    exit /b 1
)

echo.
echo [SUCCESS] Dotsy installed successfully!
echo.
echo You can now run dotsy with:
echo   dotsy
echo.
echo Or for ACP mode:
echo   dotsy-acp
echo.

endlocal
