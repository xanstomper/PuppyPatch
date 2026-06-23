from horus.memory import MemoryStore

def test_memory_search(tmp_path):
    m = MemoryStore(str(tmp_path / "m.db"))
    m.add("decision", "Use FastAPI for gateway", "project")
    assert m.search("FastAPI")[0]["type"] == "decision"
