"""RedTeam Platform - Terminal UI with Textual."""

import os
import sys
import json
import time
import threading
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.widgets import Header, Footer, Static, Tree, DataTable, Input, Button, Label, Tabs, Tab, RichLog
from textual.binding import Binding
from textual.screen import Screen
from textual.reactive import reactive
from rich.text import Text
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax

from internal.agent.orchestrator import agent
from internal.knowledge.base import init_knowledge_base, get_attack_library, search_technique
from pkg.db.memory import memory


class DashboardScreen(Screen):
    def compose(self) -> ComposeResult:
        with Container():
            yield Static("", id="banner")
            with Horizontal():
                with Vertical(id="stats-panel"):
                    yield Static("", id="stats")
                with Vertical(id="tools-panel"):
                    yield Static("", id="tools")
            with Horizontal():
                with Vertical(id="activity-panel"):
                    yield Static("", id="activity")
                with Vertical(id="learning-panel"):
                    yield Static("", id="learning")

    def on_mount(self):
        self.refresh_data()
        self.set_interval(5, self.refresh_data)

    def refresh_data(self):
        status = agent.get_status()
        stats = f"""[bold cyan]⚡ RedTeam Agent[/bold cyan]
[green]● Online[/green]

[bold]Agent:[/bold] {status['agent']}
[bold]Tools:[/bold] {status['tools_count']} loaded
[bold]Skills:[/bold] {len(status['skills'])}
[bold]Learning Events:[/bold] {status['learning']['total_events']}

[bold yellow]Tools Available:[/bold yellow]
""" + "\n".join(f"  {t}" for t in status['tools_available'])

        self.query_one("#stats", Static).update(stats)

        tools = "\n".join([
            "[bold magenta]╔══ Available Tools ══╗[/bold magenta]",
            f"  [green]✅[/green] AI-Infra-Guard v4.1.14 - AI Security Scanner",
            f"  [green]✅[/green] Agentic-Security - LLM Vulnerability Scanner",
            f"  [green]✅[/green] PentestAgent - Pentest Framework",
            f"  [green]✅[/green] PyRIT - MS Red Teaming Framework",
            f"  [green]✅[/green] Garak - LLM Vulnerability Scanner",
            f"  [green]✅[/green] RedTeamerAgent - Code Security Auditor",
            "",
            "[bold magenta]╚══ Capabilities ══╝[/bold magenta]",
            "  • Full CWE-1000 Taxonomy",
            "  • OWASP LLM Top 10",
            "  • 50+ Jailbreak Techniques",
            "  • Multi-turn Attack Chains",
            "  • Live Learning & Skill Acquisition",
            "  • SQLite Memory Core",
        ])
        self.query_one("#tools", Static).update(tools)

        recent = memory.conn.execute(
            "SELECT event_type, outcome, reward, created_at FROM learning_log ORDER BY created_at DESC LIMIT 5"
        ).fetchall()
        activity = "[bold cyan]Recent Activity:[/bold cyan]\n"
        for r in recent:
            ts = datetime.fromtimestamp(r["created_at"]).strftime("%H:%M:%S")
            icon = "🟢" if r["reward"] > 0 else "🔴"
            activity += f"  {icon} [{ts}] {r['event_type']} ({r['outcome']})\n"
        self.query_one("#activity", Static).update(activity)

        skills = agent.get_status()["skills"][:5]
        learn = "[bold cyan]Skill Progress:[/bold cyan]\n"
        for s in skills:
            bar = "█" * int(s["proficiency"] * 20) + "░" * (20 - int(s["proficiency"] * 20))
            learn += f"  {s['name']}: [{bar}] {s['proficiency']:.0%}\n"
        if not skills:
            learn += "  No skills learned yet. Run attacks to build skills.\n"
        self.query_one("#learning", Static).update(learn)


class AttackScreen(Screen):
    def compose(self) -> ComposeResult:
        with Container():
            yield Static("[bold red]╔══════════════════ ATTACK CONSOLE ══════════════════╗[/bold red]", id="attack-title")
            with Horizontal():
                with Vertical(id="attack-list-panel"):
                    yield Static("[bold]Attack Library[/bold]", id="attack-lib-title")
                    yield Tree("Categories", id="attack-tree")
                with Vertical(id="attack-controls"):
                    yield Label("Target (URL/model):")
                    yield Input(placeholder="http://target:8080 or model-name", id="target-input")
                    yield Label("Technique:")
                    yield Input(placeholder="DAN, Grandma, Injection...", id="technique-input")
                    with Horizontal():
                        yield Button("🚀 Run Attack", variant="error", id="run-attack")
                        yield Button("📋 Scan Target", variant="primary", id="run-scan")
                        yield Button("🧪 Pentest", variant="warning", id="run-pentest")
                    yield Static("", id="attack-output", classes="output-box")

    def on_mount(self):
        tree = self.query_one("#attack-tree", Tree)
        attacks = get_attack_library()
        for cat, patterns in attacks.items():
            node = tree.root.add(f"[bold yellow]{cat}[/bold yellow] ({len(patterns)})")
            for p in patterns:
                node.add_leaf(f"{p['name']} [dim]eff: {p['effectiveness']:.0%}[/dim]")

    def on_button_pressed(self, event: Button.Pressed):
        target = self.query_one("#target-input", Input).value
        technique = self.query_one("#technique-input", Input).value or "DAN"
        output = self.query_one("#attack-output", Static)

        if event.button.id == "run-attack":
            output.update("[yellow]🚀 Launching attack...[/yellow]")
            def run():
                result = agent.run_jailbreak(target, technique)
                self.call_from_thread(lambda: output.update(
                    f"[bold]Technique:[/bold] {result.get('technique', 'N/A')}\n"
                    f"[bold]Success:[/bold] {'✅' if result.get('success') else '❌'}\n"
                    f"[bold]Output:[/bold] {result.get('output', 'N/A')[:500]}"
                ))
            threading.Thread(target=run, daemon=True).start()

        elif event.button.id == "run-scan":
            output.update(f"[cyan]🔍 Scanning {target}...[/cyan]")
            def run():
                result = agent.run_scan(target)
                self.call_from_thread(lambda: output.update(
                    f"[bold]Scan Results for:[/bold] {target}\n"
                    f"[bold]Session:[/bold] {result.get('session', 'N/A')}\n"
                    f"[bold]Output:[/bold] {result.get('output', str(result.get('errors', 'No output')))[:500]}"
                ))
            threading.Thread(target=run, daemon=True).start()

        elif event.button.id == "run-pentest":
            result = agent.run_pentest(target)
            output.update(f"[bold]Pentest Session:[/bold] {result.get('session', 'Failed')}")


class KnowledgeScreen(Screen):
    def compose(self) -> ComposeResult:
        with Container():
            yield Static("[bold cyan]╔══════════════════ KNOWLEDGE BASE ══════════════════╗[/bold cyan]", id="kb-title")
            yield Input(placeholder="Search knowledge base...", id="kb-search")
            yield RichLog(id="kb-results", highlight=True, markup=True)

    def on_input_submitted(self, event: Input.Submitted):
        if event.input.id == "kb-search" and event.value:
            results = search_technique(event.value)
            log = self.query_one("#kb-results", RichLog)
            log.clear()
            log.write(f"[bold]Search results for: '{event.value}'[/bold]\n")
            for r in results:
                log.write(f"[bold cyan]{r['title']}[/bold cyan]")
                log.write(f"  {r['content'][:200]}")
                log.write(f"  [dim]Category: {r.get('category', 'N/A')} | Accessed: {r['access_count']} times[/dim]\n")


class SessionScreen(Screen):
    def compose(self) -> ComposeResult:
        with Container():
            yield Static("[bold magenta]╔══════════════════ SESSION LOG ══════════════════╗[/bold magenta]", id="session-title")
            yield DataTable(id="sessions-table")
            yield RichLog(id="session-detail", highlight=True, markup=True)

    def on_mount(self):
        table = self.query_one("#sessions-table", DataTable)
        table.add_columns("ID", "Target", "Status", "Findings", "Started")
        sessions = memory.conn.execute(
            "SELECT id, target, status, findings, started_at FROM redteam_sessions ORDER BY started_at DESC LIMIT 20"
        ).fetchall()
        for s in sessions:
            ts = datetime.fromtimestamp(s["started_at"]).strftime("%m/%d %H:%M")
            table.add_row(s["id"][:8], s["target"], s["status"], str(s["findings"]), ts)

    def on_data_table_row_selected(self, event):
        sid = event.row_key.value
        log = self.query_one("#session-detail", RichLog)
        log.clear()
        findings = memory.get_session_findings(sid)
        if findings:
            log.write(f"[bold red]Findings for session {sid[:8]}:[/bold red]")
            for f in findings:
                sev_color = {"critical": "red", "high": "yellow", "medium": "cyan", "low": "green"}.get(f["severity"], "white")
                log.write(f"[{sev_color}][{f['severity'].upper()}][/] {f['title']}")
                log.write(f"  [dim]{f['description'][:200] if f['description'] else ''}[/dim]")
        else:
            log.write("[yellow]No findings in this session[/yellow]")


class RedTeamTUI(App):
    TITLE = "⚡ RedTeam Platform - AI Red Teaming System"
    SUB_TITLE = "v1.0.0 | DOX/Cognitive Framework | Live Learning"

    SCREENS = {
        "dashboard": DashboardScreen(),
        "attack": AttackScreen(),
        "knowledge": KnowledgeScreen(),
        "sessions": SessionScreen(),
    }

    BINDINGS = [
        Binding("d", "switch_screen('dashboard')", "Dashboard"),
        Binding("a", "switch_screen('attack')", "Attack"),
        Binding("k", "switch_screen('knowledge')", "KB"),
        Binding("s", "switch_screen('sessions')", "Sessions"),
        Binding("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        with Tabs(classes="tabs"):
            yield Tab("📊 Dashboard", id="dashboard")
            yield Tab("⚔️ Attack", id="attack")
            yield Tab("📚 Knowledge", id="knowledge")
            yield Tab("📋 Sessions", id="sessions")
        yield Container(id="screen-container")
        yield Footer()

    def on_mount(self):
        self.push_screen("dashboard")

    def on_tabs_tab_clicked(self, event: Tabs.TabClicked):
        self.switch_screen(event.tab.id)

    def action_switch_screen(self, screen_name: str):
        screen = self.SCREENS.get(screen_name)
        if screen:
            self.switch_screen(screen)
            tabs = self.query_one(Tabs)
            for tab in tabs:
                if tab.id == screen_name:
                    tabs.active = tab.id
                    break

    def action_quit(self):
        self.exit()


def main():
    print("[*] Initializing RedTeam Platform...")
    init_knowledge_base()
    status = agent.get_status()
    print(f"[*] Agent '{status['agent']}' ready with {status['tools_count']} tools")
    print(f"[*] Starting TUI...")
    app = RedTeamTUI()
    app.run()


if __name__ == "__main__":
    main()
