PHASES = ["understand", "audit", "spec", "failure_map", "implement", "verify", "polish", "final_report"]

def workflow_prompt(task: str) -> str:
    return "\n".join([f"Phase {i+1}: {p}" for i, p in enumerate(PHASES)]) + f"\nTask: {task}"
