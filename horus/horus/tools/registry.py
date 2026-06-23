from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable
import subprocess
from horus.security.permissions import PermissionGate, classify_command, redact

@dataclass
class ToolSpec:
    name: str
    description: str
    schema: dict[str, Any]
    permission: str
    safety: str = "low"
    timeout: int = 30
    dry_run: bool = True

@dataclass
class ToolResult:
    ok: bool
    data: Any = None
    error: str | None = None
    safety: str = "low"

class ToolRegistry:
    def __init__(self) -> None:
        self.specs: dict[str, ToolSpec] = {}
        self.handlers: dict[str, Callable[..., ToolResult]] = {}
    def register(self, spec: ToolSpec, handler: Callable[..., ToolResult]) -> None:
        self.specs[spec.name] = spec
        self.handlers[spec.name] = handler
    def call(self, name: str, gate: PermissionGate, **kwargs: Any) -> ToolResult:
        spec = self.specs[name]
        decision = gate.check(spec.permission, spec.safety)
        if not decision.allowed:
            return ToolResult(False, error=decision.reason, safety=spec.safety)
        return self.handlers[name](**kwargs)
    def list(self) -> list[ToolSpec]:
        return list(self.specs.values())

def read_file(path: str) -> ToolResult:
    return ToolResult(True, Path(path).read_text(encoding="utf-8"))

def write_file(path: str, content: str, dry_run: bool = False) -> ToolResult:
    if dry_run:
        return ToolResult(True, {"would_write": path, "bytes": len(content)})
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(content, encoding="utf-8")
    return ToolResult(True, {"written": path})

def list_files(path: str = ".") -> ToolResult:
    return ToolResult(True, [str(p) for p in Path(path).iterdir()])

def run_command(command: str, cwd: str = ".", timeout: int = 30, dry_run: bool = False) -> ToolResult:
    risk = classify_command(command)
    if dry_run:
        return ToolResult(True, {"would_run": command, "risk": risk}, safety=risk)
    proc = subprocess.run(command, cwd=cwd, shell=True, capture_output=True, text=True, timeout=timeout)
    return ToolResult(proc.returncode == 0, {"stdout": redact(proc.stdout), "stderr": redact(proc.stderr), "exit_code": proc.returncode}, safety=risk)

def git_status(cwd: str = ".") -> ToolResult:
    return run_command("git status --short", cwd=cwd)

def git_diff(cwd: str = ".") -> ToolResult:
    return run_command("git diff", cwd=cwd)

def default_registry() -> ToolRegistry:
    reg = ToolRegistry()
    reg.register(ToolSpec("read_file", "Read a UTF-8 file", {"type":"object","properties":{"path":{"type":"string"}},"required":["path"]}, "read-only"), read_file)
    reg.register(ToolSpec("write_file", "Write a UTF-8 file", {"type":"object","properties":{"path":{"type":"string"},"content":{"type":"string"},"dry_run":{"type":"boolean"}},"required":["path","content"]}, "safe-write", "medium"), write_file)
    reg.register(ToolSpec("list_files", "List directory entries", {"type":"object","properties":{"path":{"type":"string"}}}, "read-only"), list_files)
    reg.register(ToolSpec("run_command", "Run shell command", {"type":"object","properties":{"command":{"type":"string"},"cwd":{"type":"string"},"timeout":{"type":"integer"},"dry_run":{"type":"boolean"}},"required":["command"]}, "command-exec", "high"), run_command)
    reg.register(ToolSpec("git_status", "Show git status", {"type":"object","properties":{"cwd":{"type":"string"}}}, "read-only"), git_status)
    reg.register(ToolSpec("git_diff", "Show git diff", {"type":"object","properties":{"cwd":{"type":"string"}}}, "read-only"), git_diff)
    return reg
