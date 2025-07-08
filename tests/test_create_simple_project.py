import asyncio
import pytest

import ai_dev_team_server as server
from tests.common import prepare_temp_env


@pytest.mark.asyncio
async def test_call_tool_creates_project(tmp_path, monkeypatch):
    # Use a temporary directory for project creation
    prepare_temp_env(tmp_path)

    result = await server.call_tool(
        "create_simple_project",
        {"name": "demo", "description": "demo project"},
    )

    assert isinstance(result, list)
    assert result and "created" in result[0].text

    project_dir = tmp_path / "demo"
    assert (project_dir / "README.md").exists()
    assert (project_dir / "src" / "main.py").exists()

    # run the generated script to ensure it works
    proc = await asyncio.create_subprocess_exec(
        "python",
        project_dir / "src" / "main.py",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    out, err = await proc.communicate()
    assert proc.returncode == 0, err.decode()
    assert "Hello from demo" in out.decode()

    # listing should include the project name
    list_result = await server.call_tool("list_projects", {})
    assert any("demo" in block.text for block in list_result)


@pytest.mark.asyncio
async def test_call_tool_delete_project(tmp_path):
    prepare_temp_env(tmp_path)

    await server.call_tool(
        "create_simple_project",
        {"name": "demo", "description": "demo project"},
    )

    del_result = await server.call_tool("delete_project", {"name": "demo"})
    assert any("deleted" in block.text for block in del_result)
    assert not (tmp_path / "demo").exists()
