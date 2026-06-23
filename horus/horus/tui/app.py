from __future__ import annotations
try:
    from textual.app import App, ComposeResult
    from textual.widgets import Header, Footer, Input, RichLog, Static, DataTable
    from textual.containers import Horizontal, Vertical
except Exception:  # pragma: no cover
    App = object  # type: ignore

class HorusTUI(App):  # type: ignore[misc]
    CSS = """
    Screen { background: #070b12; }
    #main { height: 1fr; }
    #left { width: 2fr; border: solid #334155; }
    #right { width: 1fr; border: solid #334155; }
    Input { dock: bottom; }
    """
    BINDINGS = [("ctrl+c", "quit", "Quit"), ("ctrl+l", "clear", "Clear")]
    def compose(self):
        yield Header(show_clock=True)
        with Horizontal(id="main"):
            with Vertical(id="left"):
                yield Static("Horus by Aporia — live agent console")
                yield RichLog(id="log", wrap=True, highlight=True)
                yield Input(placeholder="/model, /agents, /memory, /mcp, or describe a coding task…", id="input")
            with Vertical(id="right"):
                yield Static("Active Agents / Budget / Approvals")
                table = DataTable(id="agents")
                table.add_columns("Agent", "State", "Model")
                table.add_row("Prime", "idle", "configured")
                yield table
        yield Footer()
    def on_mount(self):
        self.query_one("#log", RichLog).write("Ready. Slash commands: /status /model /agents /skills /memory /mcp /doctor")
    def on_input_submitted(self, event):
        log = self.query_one("#log", RichLog)
        text = event.value.strip(); event.input.value=""
        log.write(f"[bold cyan]you[/]: {text}")
        if text.startswith("/"):
            log.write(f"[bold green]horus[/]: command accepted: {text}")
        else:
            log.write("[bold green]horus[/]: task queued for disciplined coding workflow.")
    def action_clear(self):
        self.query_one("#log", RichLog).clear()

def run_tui() -> None:
    if App is object:
        raise RuntimeError("Install horus-aporia[tui] to use the Textual TUI")
    HorusTUI().run()
