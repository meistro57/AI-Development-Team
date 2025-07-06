import asyncio
import os
import types
import pytest

import ai_dev_team_server as server

@pytest.mark.asyncio
async def test_call_tool_creates_project(tmp_path, monkeypatch):
    # Use a temporary directory for project creation
    server.WORK_DIR = str(tmp_path)
    server.projects.clear()

    result = await server.call_tool(
        "create_simple_project",
        {"name": "demo", "description": "demo project"},
    )

    assert isinstance(result, list)
    assert result and "created" in result[0].text

    project_dir = tmp_path / "demo"
    assert (project_dir / "README.md").exists()
    assert (project_dir / "src" / "main.py").exists()

    # listing should include the project name
    list_result = await server.call_tool("list_projects", {})
    assert any("demo" in block.text for block in list_result)
