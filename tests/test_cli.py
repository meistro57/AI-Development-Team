from typer.testing import CliRunner
import cli
from tests.common import prepare_temp_env

runner = CliRunner()


def test_cli_create_and_list(tmp_path, monkeypatch):
    prepare_temp_env(tmp_path)

    result = runner.invoke(cli.app, ["create", "demo", "demo project"])
    assert result.exit_code == 0
    assert "created" in result.output

    result_list = runner.invoke(cli.app, ["list"])
    assert result_list.exit_code == 0
    assert "demo" in result_list.output


def test_cli_delete_and_agents(tmp_path):
    prepare_temp_env(tmp_path)

    runner.invoke(cli.app, ["create", "demo", "demo project"])
    del_result = runner.invoke(cli.app, ["delete", "demo"])
    assert del_result.exit_code == 0
    assert "deleted" in del_result.output

    list_result = runner.invoke(cli.app, ["list"])
    assert "demo" not in list_result.output

    agents_result = runner.invoke(cli.app, ["agents"])
    assert agents_result.exit_code == 0
    assert "ProjectManager" in agents_result.output
