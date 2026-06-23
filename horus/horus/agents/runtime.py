from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
import json, os
from horus.core.config import HorusConfig
from horus.core.workflow import PHASES, workflow_prompt
from horus.memory import MemoryStore
from horus.models import ModelRouter, OpenAICompatibleClient, ChatMessage, ChatRequest, ProviderError
from horus.security import PermissionGate
from horus.tools import default_registry, ToolResult

@dataclass
class AgentStep:
    phase: str
    action: str
    result: str
    ok: bool = True

@dataclass
class AgentRunReport:
    prompt: str
    model: str
    steps: list[AgentStep] = field(default_factory=list)
    final: str = ""
    tools_used: list[str] = field(default_factory=list)
    approvals_required: list[str] = field(default_factory=list)
    memory_ids: list[int] = field(default_factory=list)

    def to_markdown(self) -> str:
        lines = ["# Horus Run Report", "", f"**Prompt:** {self.prompt}", f"**Model:** {self.model}", "", "## Steps"]
        for s in self.steps:
            status = "✅" if s.ok else "⚠️"
            lines.append(f"- {status} **{s.phase}** — {s.action}: {s.result}")
        if self.tools_used:
            lines += ["", "## Tools Used", *[f"- `{t}`" for t in self.tools_used]]
        if self.approvals_required:
            lines += ["", "## Approvals Required", *[f"- {a}" for a in self.approvals_required]]
        lines += ["", "## Final", self.final]
        return "\n".join(lines)

class CodingAgent:
    def __init__(self, config: HorusConfig | None = None, memory: MemoryStore | None = None, client: OpenAICompatibleClient | None = None) -> None:
        self.config = config or HorusConfig.load()
        self.memory = memory or MemoryStore(self.config.memory.sqlite_path)
        self.router = ModelRouter(self.config.models.default, self.config.models.routes)
        self.client = client or OpenAICompatibleClient()
        self.tools = default_registry()

    def run(self, prompt: str, role: str = "coder", permissions: list[str] | None = None, dry_run: bool = True) -> AgentRunReport:
        model_ref = self.router.route(role, need_tools=True, need_json=True)
        report = AgentRunReport(prompt=prompt, model=f"{model_ref.provider}:{model_ref.model}")
        report.memory_ids.append(self.memory.add("task", prompt, "session", {"role": role}))
        plan = self._plan(prompt, model_ref)
        report.memory_ids.append(self.memory.add("plan", plan, "session"))
        for phase in PHASES:
            report.steps.append(AgentStep(phase, "phase-enter", "ok"))
        tool_plan = self._extract_tool_plan(plan, prompt)
        gate = PermissionGate(permissions or self.config.permissions.default)
        for call in tool_plan:
            name = call.get("tool")
            args = call.get("args", {})
            if name not in self.tools.specs:
                report.steps.append(AgentStep("implement", f"unknown tool {name}", "skipped", False)); continue
            spec = self.tools.specs[name]
            result = self.tools.call(name, gate, **args)
            report.tools_used.append(name)
            if not result.ok and result.error and "approval required" in result.error:
                report.approvals_required.append(f"{name}: {result.error}")
            report.steps.append(AgentStep("implement", f"tool:{name}", self._result_summary(result), result.ok))
            self.memory.add("tool_call", json.dumps({"tool": name, "args": args, "ok": result.ok, "error": result.error}), "event")
        report.final = self._finalize(prompt, plan, report)
        report.memory_ids.append(self.memory.add("final_report", report.to_markdown(), "session"))
        return report

    def _plan(self, prompt: str, model_ref: Any) -> str:
        system = "You are Horus by Aporia. Return a concise software-engineering plan and optional JSON tool calls under a TOOL_PLAN fenced block."
        request = workflow_prompt(prompt) + "\nIf useful, include TOOL_PLAN as JSON list: [{\"tool\":\"git_status\",\"args\":{}}]."
        if os.getenv("HORUS_OFFLINE", "0") == "1":
            return self._offline_plan(prompt)
        try:
            resp = self.client.complete(ChatRequest(model_ref, [ChatMessage("system", system), ChatMessage("user", request)], temperature=0.1))
            return resp.content or self._offline_plan(prompt)
        except (ProviderError, OSError, TimeoutError, Exception):
            return self._offline_plan(prompt)

    def _offline_plan(self, prompt: str) -> str:
        return """Plan: inspect repository, gather git status/diff, create implementation spec, apply safe changes only after approval, verify tests, write final report.
TOOL_PLAN
[{"tool":"git_status","args":{"cwd":"."}},{"tool":"git_diff","args":{"cwd":"."}}]
END_TOOL_PLAN
"""

    def _extract_tool_plan(self, plan: str, prompt: str) -> list[dict[str, Any]]:
        if "TOOL_PLAN" in plan:
            body = plan.split("TOOL_PLAN",1)[1].split("END_TOOL_PLAN",1)[0].strip().strip("`")
            try:
                parsed = json.loads(body)
                if isinstance(parsed, list): return parsed
            except json.JSONDecodeError:
                pass
        lowered = prompt.lower()
        calls: list[dict[str, Any]] = []
        if any(x in lowered for x in ["audit", "repo", "status", "diff", "refactor", "fix"]):
            calls += [{"tool":"git_status","args":{"cwd":"."}}, {"tool":"git_diff","args":{"cwd":"."}}]
        return calls

    def _result_summary(self, result: ToolResult) -> str:
        if result.error: return result.error
        text = json.dumps(result.data, ensure_ascii=False) if not isinstance(result.data, str) else result.data
        return text[:500]

    def _finalize(self, prompt: str, plan: str, report: AgentRunReport) -> str:
        blocked = len(report.approvals_required)
        if blocked:
            return f"Task analyzed and tool execution partially blocked by {blocked} approval gate(s). Review approvals, then rerun with explicit permissions."
        return "Task analyzed, relevant safe tools executed, memory updated, and final engineering report generated."
