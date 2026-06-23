from horus.mcp import MCPRegistry, MCPServer, MCPToolCall

def test_mcp_bridge():
    r=MCPRegistry(); r.add(MCPServer("fs","mcp-filesystem"))
    assert r.health("fs")["configured"]
    assert r.simulate_call(MCPToolCall("fs","read",{"path":"."}))["status"] == "simulated"
