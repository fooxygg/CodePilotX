"""
Servidor FastAPI que corre en TU PC y expone Ollama al exterior.
Se autentica con API key para que solo tu VPS/CLI pueda usarlo.
"""
import httpx
import json
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from . import config as cfg

app = FastAPI(title="CodePilotX Server", version="0.1.0")

OLLAMA_URL = "http://localhost:11434"


class ChatRequest(BaseModel):
    prompt: str
    model: str = ""
    system: str = ""
    stream: bool = True


def verify_key(authorization: str = Header(default="")):
    conf = cfg.load()
    api_key = conf.get("api_key", "")
    if api_key and authorization != f"Bearer {api_key}":
        raise HTTPException(status_code=401, detail="Invalid API key")


@app.get("/health")
def health():
    return {"status": "ok", "service": "CodePilotX"}


@app.post("/chat")
def chat(req: ChatRequest, authorization: str = Header(default="")):
    verify_key(authorization)
    conf = cfg.load()
    model = req.model or conf["model"]

    payload = {
        "model": model,
        "prompt": req.prompt,
        "system": req.system,
        "stream": True,
    }

    def stream_response():
        with httpx.stream("POST", f"{OLLAMA_URL}/api/generate", json=payload, timeout=120) as r:
            for line in r.iter_lines():
                if line:
                    yield line + "\n"

    return StreamingResponse(stream_response(), media_type="application/x-ndjson")


def start(host: str = "0.0.0.0", port: int = 4444):
    import uvicorn
    print(f"\n  CodePilotX Server corriendo en http://{host}:{port}")
    print(f"  Comparte esta URL con tu VPS para conectarte\n")
    uvicorn.run(app, host=host, port=port)
