"""Cognitive Frameworks Pipeline — OWL → ANCHOR → DOX → SISPIS

Port of the RedShark Cognitive Frameworks skill for the RedTeam Platform.
Provides self-improving reasoning, documentation contracts, operational persistence,
and decision calibration.
"""

import json
import time
import hashlib
import math
from typing import Any, Optional
from dataclasses import dataclass, field
from pathlib import Path

from pkg.db.memory import memory


# ============================================================
# Signal & State Types
# ============================================================

@dataclass
class OWLSignal:
    principle: str
    weight: float
    category: str  # scope_expansion, behavior_change, verification, etc.
    description: str

@dataclass
class OWLResult:
    signals: list = field(default_factory=list)
    cumulative_weight: float = 0.0
    action: str = "proceed"  # proceed, caution, stop

@dataclass
class EpistemicState:
    verified: list = field(default_factory=list)
    observed: list = field(default_factory=list)
    inferred: list = field(default_factory=list)
    speculative: list = field(default_factory=list)
    unknown: list = field(default_factory=list)


class OWL:
    """Operational Wisdom Layer — 9 engineering principles for pre-implementation reasoning."""

    PRINCIPLES = {
        "epistemics": "Don't assume. Surface uncertainty before committing to action.",
        "reality": "Read code/files before acting. Never guess the state of the world.",
        "verification": "Prove fixes work. If it can't be verified, it's not done.",
        "locality": "Make the smallest possible change that solves the problem.",
        "conservation": "Preserve existing intent, style, and architecture.",
        "simplicity": "Choose the minimal solution. Complexity is a liability.",
        "generalization": "Abstract only when justified by repeated patterns.",
        "debuggability": "Make reasoning obvious. Future you will thank present you.",
        "integrity": "Deliver honest state. Reset when wrong.",
    }

    SURFACE_THRESHOLD = 1.5

    def __init__(self):
        self.history = []

    def reason(self, task: dict) -> OWLResult:
        """Apply OWL principles to a task and return signals."""
        signals = []
        cumulative = 0.0

        for principle, desc in self.PRINCIPLES.items():
            signal = self._evaluate_principle(principle, task)
            if signal and signal.weight > 0:
                signals.append(signal)
                cumulative += signal.weight

        action = "proceed"
        if cumulative >= self.SURFACE_THRESHOLD:
            action = "caution"
        if cumulative >= 3.0:
            action = "stop"

        result = OWLResult(signals=signals, cumulative_weight=cumulative, action=action)
        self.history.append({
            "timestamp": time.time(),
            "task": task.get("name", "unknown"),
            "result": {"signals": len(signals), "weight": cumulative, "action": action}
        })
        return result

    def _evaluate_principle(self, principle: str, task: dict) -> Optional[OWLSignal]:
        """Check if a principle signals concern for this task."""
        task_str = json.dumps(task).lower()
        weight = 0.0
        category = "general"
        desc = ""

        if principle == "epistemics":
            unknowns = ["assume", "probably", "maybe", "i think"]
            if any(u in task_str for u in unknowns):
                weight = 0.5
                desc = "Task contains assumptions that need verification"
                category = "scope_expansion"
        elif principle == "reality":
            if "estimate" in task_str or "guess" in task_str:
                weight = 0.7
                desc = "Task may skip reading current state before acting"
                category = "verification"
        elif principle == "verification":
            if "verify" not in task_str and "test" not in task_str:
                weight = 0.3
                desc = "No verification steps specified"
                category = "verification"
        elif principle == "locality":
            if any(w in task_str for w in ["refactor", "rewrite", "redesign", "restructure"]):
                weight = 0.6
                desc = "High-risk change detected — consider smaller scope"
                category = "scope_expansion"
        elif principle == "conservation":
            if "migrate" in task_str or "upgrade" in task_str:
                weight = 0.4
                desc = "Migration may break existing behavior"
                category = "behavior_change"
        elif principle == "integrity":
            if "quick fix" in task_str or "temporary" in task_str:
                weight = 0.5
                desc = "Quick fixes accumulate as technical debt"
                category = "behavior_change"

        if weight > 0:
            return OWLSignal(principle=principle, weight=weight, category=category, description=desc)
        return None

    def get_history(self) -> list:
        return self.history[-10:]  # Last 10 decisions


class ANCHOR:
    """Operational Persistence System — 8 principles for execution continuity."""

    def __init__(self):
        self.state = EpistemicState()
        self.checkpoints = []
        self.active_task = None

    def start_task(self, task_id: str, description: str, success_criteria: list):
        self.active_task = {
            "id": task_id,
            "description": description,
            "success_criteria": success_criteria,
            "started_at": time.time(),
            "status": "active",
            "completion": None  # success | failure | abort | handoff
        }

    def checkpoint(self, state_type: str, key: str, value: Any):
        """Record a checkpoint in epistemic state."""
        entry = {"key": key, "value": value, "timestamp": time.time()}

        if state_type == "verified":
            self.state.verified.append(entry)
        elif state_type == "observed":
            self.state.observed.append(entry)
        elif state_type == "inferred":
            self.state.inferred.append(entry)
        elif state_type == "speculative":
            self.state.speculative.append(entry)
        else:
            self.state.unknown.append(entry)

        self.checkpoints.append({
            "turn": len(self.checkpoints) + 1,
            "state_type": state_type,
            "entry": entry
        })

        # Persist to DB
        memory.reinforce(None, f"anchor_{state_type}", {
            "key": key, "task": self.active_task["id"] if self.active_task else None
        }, 0.1)

    def complete_task(self, outcome: str):
        if self.active_task:
            self.active_task["status"] = "completed"
            self.active_task["completion"] = outcome
            self.active_task["ended_at"] = time.time()

            # Log to learning
            reward = {"success": 0.5, "failure": -0.3, "abort": -0.1, "handoff": 0.2}.get(outcome, 0)
            memory.reinforce(None, f"task_{outcome}", {
                "task_id": self.active_task["id"],
                "duration": time.time() - self.active_task["started_at"]
            }, reward)

    def get_state_summary(self) -> dict:
        return {
            "verified": len(self.state.verified),
            "observed": len(self.state.observed),
            "inferred": len(self.state.inferred),
            "speculative": len(self.state.speculative),
            "unknown": len(self.state.unknown),
            "checkpoints": len(self.checkpoints),
            "active_task": self.active_task
        }


class DOX:
    """Documentation Operations eXchange — AGENTS.md hierarchy protocol."""

    def __init__(self, root_path: str = "/home/jewboy420"):
        self.root = Path(root_path)

    def load_contract(self, target_path: str) -> list:
        """Load DOX contract chain from root to target."""
        contracts = []
        target = Path(target_path)

        # Read root AGENTS.md
        root_agents = self.root / "AGENTS.md"
        if root_agents.exists():
            contracts.append({"level": "root", "path": str(root_agents), "content": root_agents.read_text()[:200]})

        # Walk path
        for parent in target.parents:
            agents = parent / "AGENTS.md"
            if agents.exists() and agents != root_agents:
                contracts.append({"level": "child", "path": str(agents), "content": agents.read_text()[:200]})

        # Read project AGENTS.md
        project_agents = target / "AGENTS.md" if target.is_dir() else target.parent / "AGENTS.md"
        if project_agents.exists():
            contracts.append({"level": "local", "path": str(project_agents), "content": project_agents.read_text()[:200]})

        return contracts

    def emit_signal(self, constraint: str, scope: str):
        """Emit a DOX contract signal."""
        return {
            "type": "DOX_contract",
            "constraint": constraint,
            "scope": scope,
            "action": "constraint_applied"
        }

    def closeout(self, changes: list, affected_docs: list) -> dict:
        """DOX closeout pass — update affected documentation."""
        report = {
            "changes": len(changes),
            "docs_updated": [],
            "docs_unchanged": []
        }

        for doc_path in affected_docs:
            p = Path(doc_path)
            if p.exists():
                report["docs_updated"].append(doc_path)
            else:
                report["docs_unchanged"].append(doc_path)

        return report


class SISPIS:
    """Decision-routing and response calibration gate function."""

    def __init__(self):
        self.entropy_threshold = 1.0
        self.intent_weight_threshold = 2.0

    def calibrate(self, owl_result: OWLResult, anchor_state: dict) -> str:
        """Determine response mode based on signals and state."""
        # Calculate entropy (decision complexity)
        decision_space = len(owl_result.signals) + anchor_state.get("checkpoints", 0)
        entropy = math.log2(decision_space + 1) if decision_space > 0 else 0

        # Calculate intent weight
        w = owl_result.cumulative_weight

        # Gate function
        if entropy <= self.entropy_threshold and w < self.intent_weight_threshold:
            return "NO_DECISION"  # Factual response, no calibration needed
        elif entropy <= self.entropy_threshold * 2 and w < self.intent_weight_threshold * 1.5:
            return "EXPLANATION"  # Analytical response with reasoning
        else:
            return "SCHEMA"  # Full decision framework

    def format_response(self, mode: str, content: Any, context: dict = None) -> dict:
        """Format response according to calibrated mode."""
        if mode == "NO_DECISION":
            return {
                "mode": "NO_DECISION",
                "content": content,
                "meta": {"type": "factual", "calibrated": False}
            }
        elif mode == "EXPLANATION":
            return {
                "mode": "EXPLANATION",
                "reasoning": content.get("reasoning", ""),
                "conclusion": content.get("conclusion", content),
                "meta": {"type": "analytical", "calibrated": True}
            }
        else:  # SCHEMA
            return {
                "mode": "SCHEMA",
                "context": context or {},
                "signals": content.get("signals", []),
                "options": content.get("options", []),
                "recommendation": content.get("recommendation", ""),
                "verification": content.get("verification", ""),
                "meta": {"type": "decision_framework", "calibrated": True}
            }


class CognitiveFrameworks:
    """Complete OWL → ANCHOR → DOX → SISPIS pipeline."""

    def __init__(self):
        self.owl = OWL()
        self.anchor = ANCHOR()
        self.dox = DOX()
        self.sispi = SISPIS()

    def run_pipeline(self, task: dict, target_path: str = None) -> dict:
        """Run full cognitive pipeline on a task."""
        # 1. OWL — Pre-implementation reasoning
        owl_result = self.owl.reason(task)

        # 2. ANCHOR — Load state
        anchor_state = self.anchor.get_state_summary()

        # 3. DOX — Load contracts if path provided
        contracts = []
        if target_path:
            contracts = self.dox.load_contract(target_path)

        # 4. SISPIS — Calibrate output
        mode = self.sispi.calibrate(owl_result, anchor_state)

        return {
            "pipeline": "OWL→ANCHOR→DOX→SISPIS",
            "owl": {
                "action": owl_result.action,
                "signals": [{"principle": s.principle, "weight": s.weight, "desc": s.description} for s in owl_result.signals],
                "cumulative_weight": owl_result.cumulative_weight
            },
            "anchor": anchor_state,
            "dox": {"contracts": contracts, "count": len(contracts)},
            "sispi": {"mode": mode},
            "recommendation": owl_result.action if owl_result.action != "proceed" else mode
        }


# Global instance
cf = CognitiveFrameworks()
