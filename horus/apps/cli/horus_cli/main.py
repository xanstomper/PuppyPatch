from __future__ import annotations
import typer
from rich.console import Console
from rich.table import Table
from horus.core.config import HorusConfig
from horus.models import ModelRouter, ProviderRegistry
from horus.memory import MemoryStore
from horus.skills import SkillRegistry
from horus.tools import default_registry
from horus.security import PermissionGate
from horus.mcp import MCPRegistry, MCPServer
from horus.automations import Scheduler, Automation
from horus.projectgen import init_project, TEMPLATES
from horus.orchestration import AgentContract, Orchestrator, CORE_ROLES

app = typer.Typer(help="Horus by Aporia — self-improving multi-agent coding OS")
model_app = typer.Typer(); agents_app=typer.Typer(); skills_app=typer.Typer(); memory_app=typer.Typer(); mcp_app=typer.Typer(); backend_app=typer.Typer(); schedule_app=typer.Typer(); task_app=typer.Typer(); gateway_app=typer.Typer()
app.add_typer(model_app, name="model"); app.add_typer(agents_app, name="agents"); app.add_typer(skills_app, name="skills"); app.add_typer(memory_app, name="memory"); app.add_typer(mcp_app, name="mcp"); app.add_typer(backend_app, name="backend"); app.add_typer(schedule_app, name="schedule"); app.add_typer(task_app, name="task"); app.add_typer(gateway_app, name="gateway")
console=Console()

@app.callback(invoke_without_command=True)
def root(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        console.print("[bold cyan]Horus by Aporia[/] — The self-improving multi-agent coding operating system")
        console.print("Run [bold]horus --help[/] or [bold]horus doctor[/].")

@app.command()
def init(project_name: str, template: str = "coding-agent"):
    root=init_project(project_name, template)
    console.print(f"[green]Created[/] {root}")

@app.command()
def run(prompt: str, dry_run: bool = True):
    from horus.agents import CodingAgent
    report = CodingAgent().run(prompt, permissions=["read-only"], dry_run=dry_run)
    console.print(report.to_markdown())

@app.command()
def chat():
    from horus.tui import run_tui
    run_tui()

@app.command()
def doctor():
    cfg=HorusConfig.load(); reg=ProviderRegistry()
    console.print("[green]Config OK[/]")
    console.print(f"Default model: {cfg.models.default}")
    console.print(f"Providers: {', '.join(reg.list())}")

@model_app.command("list")
def model_list():
    t=Table("Provider"); [t.add_row(p) for p in ProviderRegistry().list()]; console.print(t)

@model_app.command("set")
def model_set(model: str):
    cfg=HorusConfig.load(); cfg.models.default=model; cfg.save(); console.print(f"Default model set to {model}")

@model_app.command("route")
def model_route(routes: list[str]):
    cfg=HorusConfig.load()
    for r in routes:
        role, model = r.split("=",1); cfg.models.routes[role]=model
    cfg.save(); console.print("Routes updated")

@agents_app.command("list")
def agents_list():
    t=Table("Core Role"); [t.add_row(r) for r in CORE_ROLES]; console.print(t)

@agents_app.command("spawn")
def agents_spawn(role: str, objective: str, model: str = "default"):
    cfg=HorusConfig.load(); resolved = cfg.models.default if model=="default" else model
    orch=Orchestrator(cfg.agents.max_concurrent)
    c=AgentContract(name=role.lower().replace(" ","-"), role=role, model=resolved, tools=["read_file","git_diff"], workspace=f".horus/workspaces/{role}", permissions=["read-only"], memory_access="project", budget=1.0, max_runtime_minutes=cfg.agents.default_timeout_minutes, objective=objective, allowed_file_scope=["**/*"], exit_criteria=["report completed"])
    node=orch.add_task(c); console.print(f"Spawned {node.id}: {role}")

@agents_app.command("status")
def agents_status(): console.print("No persistent orchestrator daemon running yet.")
@agents_app.command("stop")
def agents_stop(agent_id: str): console.print(f"Stop requested for {agent_id}")

@skills_app.command("list")
def skills_list():
    skills=SkillRegistry().list(); t=Table("Name","Version","Success")
    [t.add_row(s.name,s.version,str(s.success_rate)) for s in skills]; console.print(t)

@skills_app.command("create")
def skills_create(name: str, description: str):
    s=SkillRegistry().create_from_session(name, description, ["Inspect context","Execute safely","Verify"], ["read_file","run_command"]); console.print(f"Created skill {s.name}")

@skills_app.command("improve")
def skills_improve(name: str): console.print(f"Queued improvement review for {name}")

@memory_app.command("search")
def memory_search(query: str): console.print(MemoryStore().search(query))
@memory_app.command("summarize")
def memory_summarize(scope: str = "session"): console.print(MemoryStore().summarize(scope))
@memory_app.command("export")
def memory_export(path: str = "memory.jsonl"): MemoryStore().export_jsonl(path); console.print(f"Exported {path}")

@mcp_app.command("list")
def mcp_list():
    cfg=HorusConfig.load(); t=Table("Name","Command","Permissions")
    [t.add_row(k,v.command,v.permissions) for k,v in cfg.mcp.servers.items()]; console.print(t)
@mcp_app.command("add")
def mcp_add(name: str, command: str, permissions: str = "read-only"):
    cfg=HorusConfig.load(); cfg.mcp.servers[name]={"command":command,"permissions":permissions,"args":[],"env":{}}; cfg.save(); console.print(f"Added MCP server {name}")
@mcp_app.command("test")
def mcp_test(name: str): console.print({"name":name,"status":"configured/simulated"})

@backend_app.command("list")
def backend_list(): console.print(["local","docker","ssh","singularity","modal","daytona","vercel-sandbox","kubernetes","custom"])
@backend_app.command("set")
def backend_set(name: str): console.print(f"Backend set to {name} (config persistence pending)")

@task_app.command("plan")
def task_plan(prompt: str): console.print(f"Spec plan for: {prompt}")
@task_app.command("run")
def task_run(prompt: str): run(prompt)

@app.command("audit")
def audit(target: str = "repo"): console.print(f"Audit requested: {target}")
@app.command("fix")
def fix(prompt: str): console.print(f"Fix workflow queued: {prompt}")
@app.command("test")
def test(): console.print("Run project test command through configured backend.")
@app.command("deploy")
def deploy(): console.print("Deploy requires approval and deploy permission.")
@app.command("usage")
def usage(): console.print({"tokens":0,"cost":0,"note":"observability adapter ready"})
@app.command("compress")
def compress(): console.print("Memory compression queued.")
@app.command("insights")
def insights(): console.print("No insights yet. Run tasks to build telemetry.")

@schedule_app.command("create")
def schedule_create(name: str, prompt: str, schedule: str):
    job=Scheduler().create(Automation(name=name,prompt=prompt,schedule=schedule)); console.print(job)

@gateway_app.command("setup")
def gateway_setup(platform: str = "telegram"): console.print(f"Gateway setup scaffolded for {platform}")
@gateway_app.command("start")
def gateway_start(): console.print("Gateway daemon placeholder: adapters are configured via apps/gateway.")

if __name__ == "__main__": app()



