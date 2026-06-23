from horus.agents import CodingAgent
from horus.core.config import HorusConfig
from horus.memory import MemoryStore

class FailingClient:
    def complete(self, req):
        raise RuntimeError("offline")

def test_agent_loop_offline(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    cfg = HorusConfig()
    cfg.memory.sqlite_path = str(tmp_path / "memory.db")
    agent = CodingAgent(cfg, MemoryStore(cfg.memory.sqlite_path), FailingClient())
    report = agent.run("audit repo", permissions=["read-only"])
    assert report.tools_used == ["git_status", "git_diff"]
    assert "Horus Run Report" in report.to_markdown()
    assert report.memory_ids
