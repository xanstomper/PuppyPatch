from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ModelCapabilities:
    context_window: int = 128000
    tool_calling: bool = True
    json_mode: bool = True
    vision: bool = False
    embeddings: bool = False
    reranking: bool = False

@dataclass(frozen=True)
class ModelRef:
    provider: str
    model: str

    @classmethod
    def parse(cls, value: str) -> "ModelRef":
        if ":" not in value:
            raise ValueError("model ref must be provider:model")
        provider, model = value.split(":", 1)
        return cls(provider=provider, model=model)

class ProviderRegistry:
    DEFAULT_PROVIDERS = {
        "nous", "openrouter", "novita", "nvidia", "mimo", "z_ai", "kimi", "minimax", "huggingface", "openai", "anthropic", "gemini", "local", "custom"
    }
    def __init__(self) -> None:
        self.providers = set(self.DEFAULT_PROVIDERS)
    def supports(self, provider: str) -> bool:
        return provider in self.providers
    def list(self) -> list[str]:
        return sorted(self.providers)

class ModelRouter:
    def __init__(self, default: str, routes: dict[str, str] | None = None, fallbacks: list[str] | None = None) -> None:
        self.default = ModelRef.parse(default)
        self.routes = {role: ModelRef.parse(model) for role, model in (routes or {}).items()}
        self.fallbacks = [ModelRef.parse(x) for x in (fallbacks or [])]
    def set_default(self, model: str) -> None:
        self.default = ModelRef.parse(model)
    def set_route(self, role: str, model: str) -> None:
        self.routes[role] = ModelRef.parse(model)
    def route(self, role: str | None = None, *, min_context: int = 0, need_tools: bool = False, need_json: bool = False, need_vision: bool = False) -> ModelRef:
        ref = self.routes.get(role or "", self.default)
        caps = detect_capabilities(ref)
        if min_context and caps.context_window < min_context:
            return self.fallbacks[0] if self.fallbacks else ref
        if need_tools and not caps.tool_calling:
            return self.fallbacks[0] if self.fallbacks else ref
        if need_json and not caps.json_mode:
            return self.fallbacks[0] if self.fallbacks else ref
        if need_vision and not caps.vision:
            return self.fallbacks[0] if self.fallbacks else ref
        return ref

def detect_capabilities(ref: ModelRef) -> ModelCapabilities:
    name = ref.model.lower()
    vision = any(x in name for x in ["vision", "vl", "gpt-4o", "gemini"])
    context = 1000000 if "gemini" in name else 200000 if any(x in name for x in ["claude", "kimi", "k2"]) else 128000
    embeddings = "embed" in name
    reranking = "rerank" in name
    return ModelCapabilities(context_window=context, vision=vision, embeddings=embeddings, reranking=reranking)
