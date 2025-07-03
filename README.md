# AI Development Team

This repository contains a simple example of an **AI-based development team**. It exposes a [MCP](https://github.com/microsoft/mcp) server that can create small projects on request and includes a minimal Flask web UI.

## Features

- **`ai_dev_team_server.py`** – MCP server exposing tools to create projects and list them.
- **`web_frontend.py`** – Flask application with a form for creating projects using the server.
- **`templates/index.html`** – HTML template used by the web interface.
- **Tests** – Scripts such as `test_mcp.py` and `simple_mcp_test.py` show how to interact with the server.
- **Configuration** – Example systemd service and MCP configuration are located in the `config/` folder.
- **`LM_STUDIO_SETUP.md`** – Detailed guide for running the project with LM Studio as a local language model.

## Setup

1. Create a virtual environment and install the required packages:
   ```bash
   python -m venv ai-dev-env
   source ai-dev-env/bin/activate
   pip install -r requirements.txt
   ```
2. (Optional) set environment variables used by the server:
   - `GITHUB_TOKEN` and `GITHUB_USERNAME` for GitHub integration.
   - `WORK_DIR` to choose where generated projects are stored (defaults to `./projects`).

## Running

Launch the MCP server:
```bash
python ai_dev_team_server.py
```

The web frontend can be started separately:
```bash
python web_frontend.py
```
Then open `http://localhost:5000` in your browser to create projects via the web UI.

## Testing

Basic interaction tests are provided. After installing the requirements you can run:
```bash
python test_mcp.py
```
or
```bash
python simple_mcp_test.py
```
These scripts start the server and exercise its MCP API.

## License

This project is distributed under the terms of the GNU General Public License version 3. See [LICENSE](LICENSE) for details.
