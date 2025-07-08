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
