Write-Host ""
Write-Host "  CodePilotX Installer" -ForegroundColor Cyan
Write-Host ""

# Verificar Python
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Instalando Python..." -ForegroundColor Yellow
    winget install -e --id Python.Python.3.12 --accept-source-agreements --accept-package-agreements
    $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH","User")
}

Write-Host "Instalando CodePilotX..." -ForegroundColor Green
pip install codepilotx --quiet

Write-Host ""
Write-Host "Configurando servidor..." -ForegroundColor Yellow
$serverUrl = Read-Host "  URL del servidor CodePilotX (ej: http://TU_IP:4444)"
$apiKey    = Read-Host "  API Key (dejar vacio si no tiene)"

cpx config server $serverUrl
if ($apiKey) { cpx config api-key $apiKey }

Write-Host ""
Write-Host "  Instalacion completa." -ForegroundColor Green
Write-Host "  Usa: cpx chat           - chat interactivo"
Write-Host "       cpx ask 'pregunta' - pregunta rapida"
Write-Host "       cpx status         - ver estado"
Write-Host ""
