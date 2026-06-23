from horus.tools import default_registry
from horus.security import PermissionGate, classify_command, redact

def test_tool_registration():
    reg = default_registry()
    assert "read_file" in reg.specs

def test_permission_gate_blocks():
    reg = default_registry()
    res = reg.call("write_file", PermissionGate(["read-only"]), path="x", content="y", dry_run=True)
    assert not res.ok

def test_command_classifier_and_redaction():
    assert classify_command("git push origin main") == "destructive"
    assert "[REDACTED]" in redact("token ghp_abcdefghijklmnopqrstuvwxyz")
