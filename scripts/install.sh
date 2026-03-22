#!/bin/bash
set -e

echo ""
echo "  ██████╗ ██████╗ ██╗  ██╗"
echo "  ██╔════╝██╔══██╗╚██╗██╔╝"
echo "  ██║     ██████╔╝ ╚███╔╝ "
echo "  ██║     ██╔═══╝  ██╔██╗ "
echo "  ╚██████╗██║     ██╔╝ ██╗"
echo "   ╚═════╝╚═╝     ╚═╝  ╚═╝"
echo "  CodePilotX Installer"
echo ""

# Verificar Python
if ! command -v python3 &>/dev/null; then
    echo "Instalando Python..."
    if command -v apt &>/dev/null; then
        sudo apt install -y python3 python3-pip
    elif command -v yum &>/dev/null; then
        sudo yum install -y python3 python3-pip
    fi
fi

echo "Instalando CodePilotX..."
pip3 install --quiet codepilotx

echo ""
echo "Configurando servidor..."
read -p "  URL del servidor CodePilotX (ej: http://TU_IP:4444): " SERVER_URL
read -p "  API Key (dejar vacio si no tiene): " API_KEY

cpx config server "$SERVER_URL"
[ -n "$API_KEY" ] && cpx config api-key "$API_KEY"

echo ""
echo "  Instalacion completa."
echo "  Usa: cpx chat          - chat interactivo"
echo "       cpx ask 'pregunta' - pregunta rapida"
echo "       cpx status         - ver estado"
echo ""
