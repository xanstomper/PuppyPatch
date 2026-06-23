from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol

@dataclass
class GatewayMessage:
    platform: str
    user_id: str
    text: str
    attachments: list[str] | None = None

class GatewayAdapter(Protocol):
    platform: str
    def send(self, user_id: str, text: str) -> None: ...
    def verify(self, user_id: str, action: str) -> bool: ...

class InMemoryAdapter:
    def __init__(self, platform: str) -> None:
        self.platform=platform; self.sent: list[tuple[str,str]]=[]
    def send(self, user_id: str, text: str) -> None:
        self.sent.append((user_id,text))
    def verify(self, user_id: str, action: str) -> bool:
        return bool(user_id) and action not in {"deploy-prod", "delete-secrets"}

class GatewayRouter:
    def __init__(self) -> None:
        self.adapters: dict[str, GatewayAdapter] = {}
        self.home: dict[str,str] = {}
    def register(self, adapter: GatewayAdapter) -> None:
        self.adapters[adapter.platform]=adapter
    def set_home(self, user_id: str, platform: str) -> None:
        if platform not in self.adapters: raise KeyError(platform)
        self.home[user_id]=platform
    def deliver(self, user_id: str, text: str, platform: str | None=None) -> None:
        p=platform or self.home.get(user_id) or next(iter(self.adapters))
        self.adapters[p].send(user_id,text)
