import httpx
import json
from typing import Iterator
from . import config as cfg


def _headers(api_key: str) -> dict:
    h = {"Content-Type": "application/json"}
    if api_key:
        h["Authorization"] = f"Bearer {api_key}"
    return h


def chat_stream(prompt: str, system: str = "") -> Iterator[str]:
    conf = cfg.load()
    url = conf["server_url"].rstrip("/")
    model = conf["model"]
    api_key = conf["api_key"]

    # Soporte para Ollama directo o servidor CodePilotX
    if "11434" in url or url.endswith("/api"):
        endpoint = f"{url}/api/generate"
        payload = {
            "model": model,
            "prompt": prompt,
            "system": system,
            "stream": True,
        }
    else:
        endpoint = f"{url}/chat"
        payload = {
            "model": model,
            "prompt": prompt,
            "system": system,
            "stream": True,
        }

    with httpx.stream(
        "POST", endpoint, json=payload, headers=_headers(api_key), timeout=120
    ) as r:
        r.raise_for_status()
        for line in r.iter_lines():
            if not line:
                continue
            try:
                data = json.loads(line)
                token = data.get("response") or data.get("content") or ""
                if token:
                    yield token
                if data.get("done"):
                    break
            except json.JSONDecodeError:
                continue


def ping(server_url: str = "") -> bool:
    conf = cfg.load()
    url = (server_url or conf["server_url"]).rstrip("/")
    try:
        r = httpx.get(f"{url}/api/tags" if "11434" in url else f"{url}/health", timeout=5)
        return r.status_code == 200
    except Exception:
        return False
