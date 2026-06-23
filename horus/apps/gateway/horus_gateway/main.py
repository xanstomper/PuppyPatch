from __future__ import annotations
try:
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel
except Exception:  # pragma: no cover
    FastAPI = None
from .adapters import GatewayRouter, InMemoryAdapter

if FastAPI:
    app = FastAPI(title="Horus Gateway", version="0.1.0")
    router = GatewayRouter()
    for p in ["cli","telegram","discord","slack","whatsapp","signal","email"]:
        router.register(InMemoryAdapter(p))
    class Incoming(BaseModel):
        platform: str = "cli"
        user_id: str
        text: str
    @app.get("/health")
    def health(): return {"ok": True, "platforms": list(router.adapters)}
    @app.post("/message")
    def message(msg: Incoming):
        if msg.platform not in router.adapters: raise HTTPException(404, "platform not configured")
        if msg.text.startswith("/sethome"):
            router.set_home(msg.user_id, msg.platform); return {"ok": True, "home": msg.platform}
        return {"ok": True, "queued": True, "reply": f"Horus received: {msg.text}"}
else:
    app = None
