from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Iterator
import json, os, urllib.request, urllib.error
from .router import ModelRef, detect_capabilities

@dataclass
class ChatMessage:
    role: str
    content: str

@dataclass
class ChatRequest:
    model: ModelRef
    messages: list[ChatMessage]
    temperature: float = 0.2
    max_tokens: int | None = None
    stream: bool = False
    extra: dict[str, Any] = field(default_factory=dict)

@dataclass
class ChatResponse:
    content: str
    model: str
    provider: str
    raw: dict[str, Any] = field(default_factory=dict)

PROVIDER_BASE_URLS = {
    "openai": "https://api.openai.com/v1",
    "openrouter": "https://openrouter.ai/api/v1",
    "nvidia": "https://integrate.api.nvidia.com/v1",
    "novita": "https://api.novita.ai/v3/openai",
    "z_ai": "https://open.bigmodel.cn/api/paas/v4",
    "kimi": "https://api.moonshot.ai/v1",
    "minimax": "https://api.minimax.io/v1",
    "huggingface": "https://api-inference.huggingface.co/v1",
    "gemini": "https://generativelanguage.googleapis.com/v1beta/openai",
    "local": "http://127.0.0.1:11434/v1",
    "custom": "",
}
PROVIDER_ENV = {
    "openai": "OPENAI_API_KEY", "openrouter": "OPENROUTER_API_KEY", "nvidia": "NVIDIA_NIM_API_KEY", "novita": "NOVITA_API_KEY", "z_ai": "Z_AI_API_KEY", "kimi": "KIMI_API_KEY", "minimax": "MINIMAX_API_KEY", "huggingface": "HUGGINGFACE_API_KEY", "gemini": "GOOGLE_API_KEY", "nous": "NOUS_API_KEY", "custom": "CUSTOM_MODEL_API_KEY"
}

class ProviderError(RuntimeError): pass

class OpenAICompatibleClient:
    def __init__(self, base_urls: dict[str, str] | None = None) -> None:
        self.base_urls = {**PROVIDER_BASE_URLS, **(base_urls or {})}
    def endpoint(self, provider: str) -> str:
        base = os.getenv(f"HORUS_{provider.upper()}_BASE_URL") or self.base_urls.get(provider)
        if not base: raise ProviderError(f"No base URL for provider {provider}")
        return base.rstrip("/") + "/chat/completions"
    def api_key(self, provider: str) -> str | None:
        env = PROVIDER_ENV.get(provider, f"{provider.upper()}_API_KEY")
        return os.getenv(env)
    def payload(self, req: ChatRequest) -> dict[str, Any]:
        data = {"model": req.model.model, "messages": [m.__dict__ for m in req.messages], "temperature": req.temperature, "stream": req.stream}
        if req.max_tokens: data["max_tokens"] = req.max_tokens
        data.update(req.extra)
        return data
    def complete(self, req: ChatRequest) -> ChatResponse:
        data = json.dumps(self.payload(req)).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        key = self.api_key(req.model.provider)
        if key: headers["Authorization"] = f"Bearer {key}"
        try:
            http_req = urllib.request.Request(self.endpoint(req.model.provider), data=data, headers=headers, method="POST")
            with urllib.request.urlopen(http_req, timeout=120) as resp:
                raw = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            raise ProviderError(e.read().decode("utf-8", errors="replace")) from e
        content = raw.get("choices", [{}])[0].get("message", {}).get("content", "")
        return ChatResponse(content=content, model=req.model.model, provider=req.model.provider, raw=raw)
    def stream_complete(self, req: ChatRequest) -> Iterator[str]:
        req.stream = True
        data = json.dumps(self.payload(req)).encode("utf-8")
        headers = {"Content-Type":"application/json", "Accept":"text/event-stream"}
        key = self.api_key(req.model.provider)
        if key: headers["Authorization"] = f"Bearer {key}"
        http_req = urllib.request.Request(self.endpoint(req.model.provider), data=data, headers=headers, method="POST")
        with urllib.request.urlopen(http_req, timeout=120) as resp:
            for raw_line in resp:
                line = raw_line.decode("utf-8", errors="replace").strip()
                if not line.startswith("data:"): continue
                chunk = line[5:].strip()
                if chunk == "[DONE]": break
                try:
                    obj = json.loads(chunk)
                    delta = obj.get("choices", [{}])[0].get("delta", {}).get("content")
                    if delta: yield delta
                except json.JSONDecodeError:
                    continue

def supports_request(ref: ModelRef, *, tools: bool=False, json_mode: bool=False, vision: bool=False) -> bool:
    caps = detect_capabilities(ref)
    return (not tools or caps.tool_calling) and (not json_mode or caps.json_mode) and (not vision or caps.vision)
