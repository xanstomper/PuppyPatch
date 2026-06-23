from __future__ import annotations
from dataclasses import dataclass
import subprocess, shlex
from horus.security import classify_command, redact

@dataclass
class ExecutionResult:
    ok: bool
    stdout: str
    stderr: str
    exit_code: int
    backend: str
    risk: str

class ExecutionBackend:
    name = "base"
    def run(self, command: str, cwd: str = ".", timeout: int = 60, dry_run: bool = False) -> ExecutionResult: raise NotImplementedError

class LocalBackend(ExecutionBackend):
    name="local"
    def run(self, command: str, cwd: str = ".", timeout: int = 60, dry_run: bool = False) -> ExecutionResult:
        risk=classify_command(command)
        if dry_run: return ExecutionResult(True, f"DRY RUN: {command}", "", 0, self.name, risk)
        p=subprocess.run(command, cwd=cwd, shell=True, capture_output=True, text=True, timeout=timeout)
        return ExecutionResult(p.returncode==0, redact(p.stdout), redact(p.stderr), p.returncode, self.name, risk)

class DockerBackend(ExecutionBackend):
    name="docker"
    def __init__(self, image: str = "python:3.11-slim", volume: str | None = None) -> None:
        self.image=image; self.volume=volume
    def run(self, command: str, cwd: str = "/workspace", timeout: int = 120, dry_run: bool = False) -> ExecutionResult:
        mount = f"-v {self.volume}:/workspace" if self.volume else ""
        docker_cmd = f"docker run --rm {mount} -w {cwd} {self.image} sh -lc {shlex.quote(command)}"
        return LocalBackend().run(docker_cmd, timeout=timeout, dry_run=dry_run)

class SSHBackend(ExecutionBackend):
    name="ssh"
    def __init__(self, host: str, user: str | None = None, port: int = 22) -> None:
        self.host=host; self.user=user; self.port=port
    def run(self, command: str, cwd: str = ".", timeout: int = 120, dry_run: bool = False) -> ExecutionResult:
        target = f"{self.user}@{self.host}" if self.user else self.host
        remote = f"cd {shlex.quote(cwd)} && {command}"
        ssh_cmd = f"ssh -p {self.port} {target} {shlex.quote(remote)}"
        return LocalBackend().run(ssh_cmd, timeout=timeout, dry_run=dry_run)

class BackendRegistry:
    def __init__(self) -> None:
        self.backends: dict[str, ExecutionBackend] = {"local": LocalBackend()}
    def register(self, backend: ExecutionBackend) -> None:
        self.backends[backend.name]=backend
    def get(self, name: str) -> ExecutionBackend:
        return self.backends[name]
    def list(self) -> list[str]:
        return sorted(self.backends)
