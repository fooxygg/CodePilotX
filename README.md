# CodePilotX

Local AI Coding Copilot - corre en tu propio hardware, usalo desde cualquier lugar.

## Instalacion rapida

**Linux / Ubuntu (VPS):**
```bash
curl -fsSL https://raw.githubusercontent.com/fooxygg/CodePilotX/main/scripts/install.sh | bash
```

**Windows PowerShell:**
```powershell
irm https://raw.githubusercontent.com/fooxygg/CodePilotX/main/scripts/install.ps1 | iex
```

**Windows CMD:**
```cmd
curl -fsSL https://raw.githubusercontent.com/fooxygg/CodePilotX/main/scripts/install.cmd -o install.cmd && install.cmd && del install.cmd
```

**O directo con pip:**
```bash
pip install codepilotx
```

## Uso

```bash
cpx                          # chat interactivo
cpx ask "explica este error" # pregunta rapida
cpx serve --port 4444        # inicia servidor en tu PC
cpx config server <url>      # conectar a servidor remoto
cpx config api-key <clave>   # proteger con API key
cpx status                   # ver estado de conexion
```

## Arquitectura

```
VPS / cualquier maquina          TU PC (GPU local)
┌─────────────────────┐          ┌─────────────────────┐
│  pip install        │  HTTP →  │  cpx serve          │
│  codepilotx         │          │  Ollama + modelo    │
│  cpx chat           │          │  puerto 4444        │
└─────────────────────┘          └─────────────────────┘
```

El modelo corre 100% en tu hardware. Sin costos, sin restricciones, sin privacidad comprometida.

## Requisitos (servidor / tu PC)

- Python 3.9+
- [Ollama](https://ollama.com)
- Modelo: `ollama pull qwen2.5-coder:7b`

## Licencia

MIT
