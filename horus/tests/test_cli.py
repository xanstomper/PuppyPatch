from typer.testing import CliRunner
from horus_cli.main import app

runner = CliRunner()

def test_cli_doctor():
    res = runner.invoke(app, ["doctor"])
    assert res.exit_code == 0
    assert "Config OK" in res.output

def test_cli_model_list():
    res = runner.invoke(app, ["model", "list"])
    assert res.exit_code == 0
    assert "openrouter" in res.output
