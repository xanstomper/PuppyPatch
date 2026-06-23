"""Red team agent orchestrator - coordinates tools, attacks, and learning."""

import json
import os
import subprocess
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

from pkg.db.memory import memory
from internal.knowledge.base import get_attack_library, search_technique


class RedTeamAgent:
    def __init__(self, name: str = "RedShark", model: str = None):
        self.agent_id = memory.register_agent(name, model=model, provider="local")
        self.name = name
        self.session_id = None
        self.tools = self._discover_tools()

    def _discover_tools(self) -> dict:
        """Discover all available red teaming tools."""
        tools = {}

        # AI-Infra-Guard
        aig_paths = [
            "/home/jewboy420/AI-Infra-Guard/ai-infra-guard",
            "/home/jewboy420/AI-Infra-Guard/ai-infra-guard"
        ]
        for p in aig_paths:
            if os.path.exists(p):
                tools["aig"] = {"path": p, "type": "scanning", "name": "AI-Infra-Guard"}
                break

        # Garak
        garak_path = "/home/jewboy420/garak"
        if os.path.exists(garak_path):
            tools["garak"] = {"path": garak_path, "type": "llm_scanner", "name": "Garak"}

        # PyRIT
        pyrit_path = "/home/jewboy420/PyRIT"
        if os.path.exists(pyrit_path):
            tools["pyrit"] = {"path": pyrit_path, "type": "redteam_framework", "name": "PyRIT"}

        # PentestAgent
        pentest_path = "/home/jewboy420/pentestagent"
        if os.path.exists(pentest_path):
            tools["pentestagent"] = {"path": pentest_path, "type": "pentest", "name": "PentestAgent"}

        # Agentic Security
        try:
            import agentic_security
            tools["agentic_security"] = {"path": "agentic_security", "type": "llm_scanner", "name": "Agentic Security"}
        except ImportError:
            pass

        # RedTeamerAgent
        rta_path = "/home/jewboy420/xanstomper-repos/RedTeamerAgent"
        if os.path.exists(rta_path):
            tools["redteamer"] = {"path": rta_path, "type": "code_auditor", "name": "RedTeamerAgent"}

        return tools

    def create_session(self, target: str, config: dict = None) -> str:
        self.session_id = memory.create_session(target, self.agent_id, config)
        return self.session_id

    def run_scan(self, target: str, scan_type: str = "full") -> dict:
        """Run AI-Infra-Guard scan."""
        results = {"findings": [], "errors": []}

        if "aig" not in self.tools:
            results["errors"].append("AI-Infra-Guard not found")
            return results

        aig = self.tools["aig"]["path"]
        sid = self.create_session(target, {"scan_type": scan_type})

        try:
            cmd = [aig, "scan"]
            if target.startswith("http"):
                cmd.extend(["--url", target])
            else:
                cmd.extend(["--path", target])

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            output = result.stdout + result.stderr

            # Parse findings from output
            findings_found = "VULNERABILITY" in output or "CRITICAL" in output or "HIGH" in output
            if findings_found:
                memory.add_finding(sid, "scan", f"Vulnerabilities found in {target}",
                                  output[:1000], severity="high", cvss=7.5)

            results["output"] = output[:2000]
            results["session"] = sid

            # Learning reinforcement
            outcome = {"success": result.returncode == 0, "findings": findings_found}
            memory.live_learn(self.agent_id, f"scan_{scan_type}", outcome)

        except Exception as e:
            results["errors"].append(str(e))

        return results

    def run_jailbreak(self, target_model: str, technique: str = "DAN") -> dict:
        """Run jailbreak attack against target model."""
        attacks = memory.get_attacks_by_type("jailbreak")
        attack = next((a for a in attacks if technique.lower() in a["name"].lower()), attacks[0] if attacks else None)

        if not attack:
            return {"error": "No jailbreak attack found"}

        result = {
            "technique": attack["name"],
            "template": attack["prompt_template"],
            "success": False,
            "output": None
        }

        # Route to available tool
        if "garak" in self.tools:
            try:
                cmd = ["python3", "-m", "garak", "--model_type", "rest",
                       "--model_name", target_model, "--probes", "jailbreak"]
                r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
                result["output"] = r.stdout[:1500]
                result["success"] = r.returncode == 0
            except Exception as e:
                result["error"] = str(e)

        # Log learning
        memory.live_learn(self.agent_id, "jailbreak", {
            "success": result["success"],
            "technique": technique,
            "novelty": True
        })

        return result

    def run_pentest(self, target: str, test_type: str = "full") -> dict:
        """Run penetration testing using PentestAgent."""
        if "pentestagent" not in self.tools:
            return {"error": "PentestAgent not installed"}

        sid = self.create_session(target, {"type": "pentest", "test_type": test_type})
        return {"session": sid, "status": "prepared", "target": target}

    def audit_code(self, path: str) -> dict:
        """Run code audit with RedTeamerAgent."""
        if "redteamer" not in self.tools:
            return {"error": "RedTeamerAgent not found"}

        return {
            "agent": "RedTeamerAgent",
            "path": path,
            "status": "ready",
            "capabilities": [
                "Full CWE-1000 taxonomy coverage",
                "16+ language SAST",
                "Secrets detection",
                "Supply chain analysis",
                "CVSS 3.1 scoring"
            ]
        }

    def get_status(self) -> dict:
        """Get agent status and capabilities."""
        skills = memory.get_agent_skills(self.agent_id)
        summary = memory.get_learning_summary(self.agent_id, days=30)

        return {
            "agent": self.name,
            "id": self.agent_id,
            "tools_available": list(self.tools.keys()),
            "tools_count": len(self.tools),
            "skills": skills,
            "learning": summary,
            "status": "operational"
        }

    def learn_from_outcome(self, action: str, outcome: dict):
        """Real-time learning from action outcomes."""
        return memory.live_learn(self.agent_id, action, outcome)


agent = RedTeamAgent()
