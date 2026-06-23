from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass
class MCPServer:
    name: str
    command: str
    args: list[str] = field(default_factory=list)
    permissions: str = "read-only"
    env: dict[str,str] = field(default_factory=dict)

@dataclass
class MCPToolCall:
    server: str
    tool: str
    arguments: dict[str, Any]
    dry_run: bool = True

class MCPRegistry:
    def __init__(self) -> None:
        self.servers: dict[str, MCPServer] = {}
    def add(self, server: MCPServer) -> None:
        self.servers[server.name]=server
    def list(self) -> list[MCPServer]:
        return list(self.servers.values())
    def health(self, name: str) -> dict[str, Any]:
        s=self.servers[name]
        return {"name": s.name, "configured": bool(s.command), "permissions": s.permissions}
    def simulate_call(self, call: MCPToolCall) -> dict[str, Any]:
        if call.server not in self.servers: raise KeyError(call.server)
        return {"server": call.server, "tool": call.tool, "arguments": call.arguments, "dry_run": call.dry_run, "status": "simulated"}
