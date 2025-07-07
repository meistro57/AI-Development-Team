from typer.testing import CliRunner
import cli
import ai_dev_team_server as server

runner = CliRunner()


def test_cli_create_and_list(tmp_path, monkeypatch):
    server.WORK_DIR = str(tmp_path)
    server.projects.clear()

    result = runner.invoke(cli.app, ["create", "demo", "demo project"])
    assert result.exit_code == 0
    assert "created" in result.output

    result_list = runner.invoke(cli.app, ["list"])
    assert result_list.exit_code == 0
    assert "demo" in result_list.output
