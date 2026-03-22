import json
import os
from pathlib import Path

CONFIG_DIR = Path.home() / ".codepilotx"
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULTS = {
    "server_url": "http://localhost:11434",
    "model": "mi-coder",
    "api_key": "",
    "stream": True,
}

def load() -> dict:
    CONFIG_DIR.mkdir(exist_ok=True)
    if not CONFIG_FILE.exists():
        save(DEFAULTS)
        return DEFAULTS.copy()
    with open(CONFIG_FILE) as f:
        data = json.load(f)
    return {**DEFAULTS, **data}

def save(cfg: dict):
    CONFIG_DIR.mkdir(exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=2)

def set_value(key: str, value: str):
    cfg = load()
    cfg[key] = value
    save(cfg)
