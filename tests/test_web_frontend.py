import pytest

import web_frontend
from flask import Flask

class FakeContent:
    def __init__(self, text):
        self.text = text

class FakeResult:
    def __init__(self, text):
        self.content = [FakeContent(text)]

@pytest.fixture
def client():
    web_frontend.app.config.update({'TESTING': True})
    with web_frontend.app.test_client() as client:
        yield client

@pytest.mark.parametrize("mock_result", [
    [FakeContent("ok")],
    FakeResult("ok"),
    {"success": True, "message": "ok"}
])
def test_create_project_parsing(monkeypatch, client, mock_result):
    async def fake_call_tool(name, args):
        return mock_result
    monkeypatch.setattr(web_frontend, "call_tool", fake_call_tool)

    resp = client.post('/create_project', data={'name': 'demo', 'description': 'test'})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['success'] is True
    assert 'project' in data
