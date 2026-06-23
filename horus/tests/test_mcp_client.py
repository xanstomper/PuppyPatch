import json, sys, textwrap, subprocess
from pathlib import Path
from horus.mcp import MCPStdioClient

def test_mcp_stdio_client(tmp_path):
    server = tmp_path / "server.py"
    server.write_text("""
import sys,json
for line in sys.stdin:
    msg=json.loads(line)
    method=msg.get('method')
    if method=='initialize': result={'ok':True}
    elif method=='tools/list': result={'tools':[{'name':'echo'}]}
    elif method=='tools/call': result={'content':[{'type':'text','text':'ok'}]}
    else: result={}
    print(json.dumps({'jsonrpc':'2.0','id':msg.get('id'),'result':result}), flush=True)
""", encoding="utf-8")
    c=MCPStdioClient(sys.executable, [str(server)], timeout=5)
    assert c.initialize()["ok"] is True
    assert c.list_tools()["tools"][0]["name"] == "echo"
    assert c.call_tool("echo", {})["content"][0]["text"] == "ok"
    c.stop()
