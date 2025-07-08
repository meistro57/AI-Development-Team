import json
from tests.common import prepare_temp_env
import web_frontend
from flask import Flask


def test_api_projects(tmp_path):
    prepare_temp_env(tmp_path)
    web_frontend.app.config.update({"TESTING": True})
    with web_frontend.app.test_client() as client:
        # create a project via database through server tool
        import ai_dev_team_server as server

        client.post("/create_project", data={"name": "demo", "description": "demo"})
        resp = client.get("/api/projects")
        assert resp.status_code == 200
        data = resp.get_json()
        assert any(p["name"] == "demo" for p in data)

        resp_detail = client.get("/api/projects/demo")
        assert resp_detail.status_code == 200
        detail = resp_detail.get_json()
        assert detail["name"] == "demo"
