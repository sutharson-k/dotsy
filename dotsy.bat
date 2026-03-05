@echo off
REM Dynamic Dotsy launcher - works from any location
REM This script finds its own directory and runs dotsy from there

setlocal enabledelayedexpansion

REM Get the directory where this batch file is located
set "DOTSY_DIR=%~dp0"

REM Remove trailing backslash
set "DOTSY_DIR=%DOTSY_DIR:~0,-1%"

REM Set PYTHONPATH to include dotsy directory
set "PYTHONPATH=%DOTSY_DIR%;%PYTHONPATH%"

REM Run dotsy entrypoint
py "%DOTSY_DIR%\dotsy\cli\entrypoint.py" %*

endlocal
