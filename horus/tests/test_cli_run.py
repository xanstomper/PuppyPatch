from typer.testing import CliRunner
from horus_cli.main import app

runner = CliRunner()

def test_cli_run_outputs_report(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("HORUS_OFFLINE", "1")
    res = runner.invoke(app, ["run", "audit repo"])
    assert res.exit_code == 0
    assert "Horus Run Report" in res.output
