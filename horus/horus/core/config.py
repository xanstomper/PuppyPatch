from __future__ import annotations
from pathlib import Path
from typing import Any
from pydantic import BaseModel, Field
import yaml

class ModelsConfig(BaseModel):
    default: str = "openrouter:anthropic/claude-sonnet-4.5"
    routes: dict[str, str] = Field(default_factory=dict)

class AgentsConfig(BaseModel):
    max_concurrent: int = Field(default=60, ge=1, le=60)
    default_timeout_minutes: int = 45

class MemoryConfig(BaseModel):
    sqlite_path: str = ".horus/memory.db"
    fts: bool = True
    vector: bool = False
    encryption: str | bool | None = "optional"

class MCPServerConfig(BaseModel):
    command: str
    permissions: str = "read-only"
    args: list[str] = Field(default_factory=list)
    env: dict[str, str] = Field(default_factory=dict)

class MCPConfig(BaseModel):
    servers: dict[str, MCPServerConfig] = Field(default_factory=dict)

class PermissionsConfig(BaseModel):
    default: list[str] = Field(default_factory=lambda: ["read-only"])
    require_approval: list[str] = Field(default_factory=lambda: ["destructive", "deploy", "secrets", "admin"])

class HorusConfig(BaseModel):
    models: ModelsConfig = Field(default_factory=ModelsConfig)
    agents: AgentsConfig = Field(default_factory=AgentsConfig)
    memory: MemoryConfig = Field(default_factory=MemoryConfig)
    mcp: MCPConfig = Field(default_factory=MCPConfig)
    permissions: PermissionsConfig = Field(default_factory=PermissionsConfig)

    @classmethod
    def load(cls, path: str | Path = "horus.yaml") -> "HorusConfig":
        p = Path(path)
        if not p.exists():
            return cls()
        data: dict[str, Any] = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        return cls.model_validate(data)

    def save(self, path: str | Path = "horus.yaml") -> None:
        Path(path).write_text(yaml.safe_dump(self.model_dump(), sort_keys=False), encoding="utf-8")
