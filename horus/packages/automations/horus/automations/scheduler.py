from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Automation:
    name: str
    prompt: str
    schedule: str
    delivery_platform: str = "cli"
    model_route: str = "default"
    tools_allowed: list[str] | None = None
    max_budget: float = 1.0
    timeout_minutes: int = 30
    approval_policy: str = "manual"
    recurrence: str = "cron"
    enabled: bool = True

class Scheduler:
    def __init__(self) -> None:
        self.jobs: dict[str, Automation] = {}
    def create(self, job: Automation) -> Automation:
        self.jobs[job.name]=job
        return job
    def list(self) -> list[Automation]:
        return list(self.jobs.values())
