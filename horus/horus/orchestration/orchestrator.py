from __future__ import annotations
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Any
import uuid

CORE_ROLES = ["Prime Orchestrator","Product Architect","Repo Auditor","Planner","Spec Writer","Backend Engineer","Frontend Engineer","Database Engineer","DevOps Engineer","Security Engineer","Test Engineer","QA Agent","Refactor Agent","Documentation Agent","Dependency Auditor","Performance Engineer","UX Reviewer","Accessibility Reviewer","API Integration Agent","MCP Integration Agent","Memory Curator","Skill Builder","Bug Reproducer","Patch Agent","Code Reviewer","Release Manager","Benchmark Agent","Cost Monitor","Prompt Engineer","Research Agent","Browser Automation Agent","Terminal Agent","Sandbox Agent","Migration Agent","CI/CD Agent","Observability Agent","Compliance Agent","Data Pipeline Agent","Agent Debate Panel","Final Verifier"]

class TaskState(StrEnum):
    PENDING="pending"; RUNNING="running"; BLOCKED="blocked"; DONE="done"; FAILED="failed"

@dataclass
class AgentContract:
    name: str
    role: str
    model: str
    tools: list[str]
    workspace: str
    permissions: list[str]
    memory_access: str
    budget: float
    max_runtime_minutes: int
    objective: str
    allowed_file_scope: list[str]
    exit_criteria: list[str]
    reporting_format: str = "markdown"
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

@dataclass
class TaskNode:
    id: str
    contract: AgentContract
    depends_on: list[str] = field(default_factory=list)
    state: TaskState = TaskState.PENDING
    result: str | None = None

class Blackboard:
    def __init__(self) -> None:
        self.data: dict[str, Any] = {}
    def write(self, key: str, value: Any) -> None:
        self.data[key]=value
    def read(self, key: str, default: Any=None) -> Any:
        return self.data.get(key, default)

class Orchestrator:
    def __init__(self, max_agents: int = 60) -> None:
        if max_agents > 60: raise ValueError("Horus supports max 60 concurrent agents")
        self.max_agents=max_agents
        self.tasks: dict[str, TaskNode] = {}
        self.blackboard=Blackboard()
    def add_task(self, contract: AgentContract, depends_on: list[str] | None=None) -> TaskNode:
        if len(self.tasks) >= self.max_agents: raise RuntimeError("agent limit reached")
        Path(contract.workspace).mkdir(parents=True, exist_ok=True)
        node=TaskNode(id=contract.id, contract=contract, depends_on=depends_on or [])
        self.tasks[node.id]=node
        return node
    def runnable(self) -> list[TaskNode]:
        return [t for t in self.tasks.values() if t.state==TaskState.PENDING and all(self.tasks[d].state==TaskState.DONE for d in t.depends_on)]
    def mark_done(self, task_id: str, result: str) -> None:
        self.tasks[task_id].state=TaskState.DONE; self.tasks[task_id].result=result
