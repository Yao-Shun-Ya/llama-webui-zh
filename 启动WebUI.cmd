@echo off
setlocal
cd /d "%~dp0"

set "PORT=8080"
set "URL=http://127.0.0.1:%PORT%"
set "MODELS=%~dp0models"

if not exist "%~dp0llama-server.exe" (
    echo [ERROR] llama-server.exe not found in this folder.
    pause
    exit /b 1
)

if not exist "%~dp0models.ini" (
    echo [ERROR] models.ini not found: %~dp0models.ini
    pause
    exit /b 1
)

if not exist "%~dp0webui-zh\index.html" (
    echo [WARN] webui-zh not found, using built-in English UI.
    set "UIPATH="
) else (
    set "UIPATH=%~dp0webui-zh"
)

netstat -ano | findstr /c:":%PORT% " | findstr /c:"LISTENING" >nul
if not errorlevel 1 (
    echo [INFO] Port %PORT% already in use. Opening browser...
    start "" "%URL%"
    exit /b 0
)

echo ==========================================
echo   llama.cpp WebUI
echo ------------------------------------------
echo   Models : %MODELS%  (via models.ini)
echo   URL    : %URL%
echo ==========================================
echo.

if defined UIPATH (
    start "llama.cpp server" /min "%~dp0llama-server.exe" --models-preset "%~dp0models.ini" --path "%UIPATH%" --no-models-autoload --port %PORT%
) else (
    start "llama.cpp server" /min "%~dp0llama-server.exe" --models-preset "%~dp0models.ini" --no-models-autoload --port %PORT%
)

timeout /t 5 /nobreak >nul
start "" "%URL%"

echo Server is running in the minimized window.
echo Close that window to stop the server.
echo.
timeout /t 8 /nobreak >nul
exit /b 0
