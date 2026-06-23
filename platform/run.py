#!/usr/bin/env python3
"""RedTeam Platform - Quick launcher"""

import os
import sys
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

os.chdir(str(ROOT))

def main():
    print(r"""
    ╔══════════════════════════════════════════════════════════════╗
    ║              ⚡ RedTeam Platform v1.0.0                       ║
    ║     AI Red Teaming | Cognitive Framework | Live Learning     ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

    # Initialize
    from internal.knowledge.base import init_knowledge_base
    from internal.agent.orchestrator import agent
    from internal.mcp.obsidian_bridge import get_brain

    print("[*] Initializing knowledge base...")
    init_knowledge_base()

    print("[*] Connecting tools...")
    status = agent.get_status()
    print(f"  ✓ Agent: {status['agent']}")
    print(f"  ✓ Tools: {status['tools_count']} available: {', '.join(status['tools_available'])}")
    print(f"  ✓ Skills: {len(status['skills'])} learned")
    print(f"  ✓ Learning events: {status['learning']['total_events']}")

    print("[*] Loading cognitive framework...")
    from pkg.cognitive.pipeline import cf
    pipe = cf.run_pipeline({"name": "platform_launch"})
    print(f"  ✓ OWL: {pipe['owl']['action']} | SISPIS: {pipe['sispi']['mode']}")

    print("[*] Connecting Obsidian brain...")
    brain = get_brain()
    if brain.connected:
        print("  ✓ Obsidian vault connected")
    else:
        print("  ! Obsidian vault available (file sync mode)")

    print("\n[*] Launching TUI...\n")
    from cmd.rtui.main import RedTeamTUI
    app = RedTeamTUI()
    app.run()


if __name__ == "__main__":
    main()
