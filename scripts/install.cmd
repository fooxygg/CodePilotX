@echo off
echo.
echo   CodePilotX Installer
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo Instalando Python...
    winget install -e --id Python.Python.3.12 --accept-source-agreements --accept-package-agreements
)

echo Instalando CodePilotX...
pip install codepilotx --quiet

echo.
set /p SERVER_URL="  URL del servidor (ej: http://TU_IP:4444): "
set /p API_KEY="  API Key (dejar vacio si no tiene): "

cpx config server %SERVER_URL%
if not "%API_KEY%"=="" cpx config api-key %API_KEY%

echo.
echo   Instalacion completa.
echo   Usa: cpx chat
echo        cpx ask "tu pregunta"
echo        cpx status
echo.
pause
