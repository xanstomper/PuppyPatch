from __future__ import annotations
from pathlib import Path
from pydantic import BaseModel, Field
from datetime import datetime, timezone
import yaml

class Skill(BaseModel):
    name: str
    description: str
    trigger_conditions: list[str] = Field(default_factory=list)
    required_tools: list[str] = Field(default_factory=list)
    steps: list[str] = Field(default_factory=list)
    examples: list[str] = Field(default_factory=list)
    failure_modes: list[str] = Field(default_factory=list)
    verification_checks: list[str] = Field(default_factory=list)
    last_used: str | None = None
    success_rate: float = 0.0
    owner: str = "Aporia"
    version: str = "0.1.0"
    changelog: list[str] = Field(default_factory=list)

class SkillRegistry:
    def __init__(self, path: str = ".horus/skills") -> None:
        self.path = Path(path)
        self.path.mkdir(parents=True, exist_ok=True)
    def save(self, skill: Skill) -> Path:
        p = self.path / f"{skill.name.replace(' ', '_').lower()}.skill.yaml"
        p.write_text(yaml.safe_dump(skill.model_dump(), sort_keys=False), encoding="utf-8")
        return p
    def list(self) -> list[Skill]:
        skills=[]
        for p in self.path.glob("*.skill.yaml"):
            skills.append(Skill.model_validate(yaml.safe_load(p.read_text(encoding="utf-8"))))
        return skills
    def create_from_session(self, name: str, description: str, steps: list[str], tools: list[str]) -> Skill:
        skill = Skill(name=name, description=description, steps=steps, required_tools=tools, changelog=[f"created {datetime.now(timezone.utc).isoformat()}"])
        self.save(skill)
        return skill
    def record_use(self, skill: Skill, success: bool) -> Skill:
        skill.last_used = datetime.now(timezone.utc).isoformat()
        skill.success_rate = (skill.success_rate + (1.0 if success else 0.0)) / 2 if skill.success_rate else (1.0 if success else 0.0)
        skill.changelog.append(f"use success={success}")
        self.save(skill)
        return skill
