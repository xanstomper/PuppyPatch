from __future__ import annotations
from enum import StrEnum
from dataclasses import dataclass
import re

class Permission(StrEnum):
    READ_ONLY = "read-only"
    SAFE_WRITE = "safe-write"
    REPO_WRITE = "repo-write"
    COMMAND_EXEC = "command-exec"
    NETWORK = "network"
    BROWSER = "browser"
    DEPLOY = "deploy"
    SECRETS = "secrets"
    DESTRUCTIVE = "destructive"
    ADMIN = "admin"

@dataclass
class ApprovalDecision:
    allowed: bool
    reason: str
    requires_approval: bool = False

class PermissionGate:
    def __init__(self, granted: set[str] | list[str]) -> None:
        self.granted = set(granted)
    def check(self, required: str, safety: str = "low") -> ApprovalDecision:
        if required not in self.granted and Permission.ADMIN not in self.granted:
            return ApprovalDecision(False, f"missing permission: {required}")
        if safety in {"high", "destructive", "deploy", "secrets"}:
            return ApprovalDecision(False, f"approval required for {safety}", True)
        return ApprovalDecision(True, "allowed")

DANGEROUS = [r"rm\s+-rf", r"Remove-Item.+-Recurse", r"del\s+/s", r"format\s+", r"git\s+push", r"terraform\s+apply", r"kubectl\s+delete", r"drop\s+database"]
SECRET_PATTERNS = [r"sk-[A-Za-z0-9_-]{16,}", r"gh[pousr]_[A-Za-z0-9_]{20,}", r"AKIA[0-9A-Z]{16}"]

def classify_command(command: str) -> str:
    lower = command.lower()
    if any(re.search(p, command, re.I) for p in DANGEROUS):
        return "destructive"
    if any(x in lower for x in ["npm install", "pip install", "uv add", "poetry add"]):
        return "network"
    return "low"

def redact(text: str) -> str:
    out = text
    for pat in SECRET_PATTERNS:
        out = re.sub(pat, "[REDACTED]", out)
    return out
