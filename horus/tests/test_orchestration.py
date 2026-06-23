from horus.orchestration import AgentContract, Orchestrator

def contract(name="a"):
    return AgentContract(name=name, role="Planner", model="openai:gpt", tools=[], workspace=".tmp/"+name, permissions=["read-only"], memory_access="project", budget=1, max_runtime_minutes=1, objective="plan", allowed_file_scope=["**/*"], exit_criteria=["done"])

def test_task_graph_dependencies(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    o=Orchestrator(2)
    a=o.add_task(contract("a"))
    b=o.add_task(contract("b"), [a.id])
    assert [x.id for x in o.runnable()] == [a.id]
    o.mark_done(a.id,"ok")
    assert [x.id for x in o.runnable()] == [b.id]
