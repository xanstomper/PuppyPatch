from __future__ import annotations
from dataclasses import dataclass
from typing import Any
import json, subprocess, itertools, threading, queue, time

@dataclass
class JSONRPCError(Exception):
    code: int
    message: str
    data: Any = None

class MCPStdioClient:
    def __init__(self, command: str, args: list[str] | None = None, env: dict[str,str] | None = None, timeout: float = 30.0) -> None:
        self.command=command; self.args=args or []; self.env=env; self.timeout=timeout; self.proc: subprocess.Popen[str] | None=None; self.ids=itertools.count(1); self._responses: queue.Queue[dict[str,Any]] = queue.Queue(); self._reader: threading.Thread | None=None
    def start(self) -> None:
        if self.proc: return
        self.proc = subprocess.Popen([self.command, *self.args], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", env=self.env)
        self._reader = threading.Thread(target=self._read_loop, daemon=True); self._reader.start()
    def _read_loop(self) -> None:
        assert self.proc and self.proc.stdout
        for line in self.proc.stdout:
            line=line.strip()
            if not line: continue
            try: self._responses.put(json.loads(line))
            except json.JSONDecodeError: continue
    def stop(self) -> None:
        if self.proc:
            self.proc.terminate(); self.proc=None
    def request(self, method: str, params: dict[str,Any] | None=None) -> Any:
        self.start(); assert self.proc and self.proc.stdin
        rid = next(self.ids)
        msg = {"jsonrpc":"2.0", "id": rid, "method": method, "params": params or {}}
        self.proc.stdin.write(json.dumps(msg)+"\n"); self.proc.stdin.flush()
        deadline=time.time()+self.timeout
        while time.time()<deadline:
            try: resp=self._responses.get(timeout=0.05)
            except queue.Empty: continue
            if resp.get("id") != rid: continue
            if "error" in resp:
                e=resp["error"]; raise JSONRPCError(e.get("code",-1), e.get("message","MCP error"), e.get("data"))
            return resp.get("result")
        raise TimeoutError(f"MCP request timed out: {method}")
    def initialize(self, client_name: str = "horus") -> Any:
        return self.request("initialize", {"protocolVersion":"2024-11-05", "capabilities":{}, "clientInfo":{"name":client_name,"version":"0.1.0"}})
    def list_tools(self) -> Any:
        return self.request("tools/list", {})
    def call_tool(self, name: str, arguments: dict[str,Any]) -> Any:
        return self.request("tools/call", {"name": name, "arguments": arguments})
