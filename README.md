# AI Development Team

This repository contains a simple example of an **AI-based development team**. It exposes a [MCP](https://github.com/microsoft/mcp) server that can create small projects on request and includes a minimal Flask web UI.

## Features

- **`ai_dev_team_server.py`** – MCP server exposing tools to create projects and list them.
- **`web_frontend.py`** – Flask application with a form for creating projects using the server.
- **`cli.py`** – Simple command line tool to create and list projects.
- **`templates/index.html`** – HTML template used by the web interface.
- **Tests** – Scripts such as `test_mcp.py` and `simple_mcp_test.py` show how to interact with the server.
- **Configuration** – Example systemd service and MCP configuration are located in the `config/` folder.
- **`LM_STUDIO_SETUP.md`** – Detailed guide for running the project with LM Studio as a local language model.
- **`verify_agents.py`** – Diagnostic script to confirm all AI agents respond correctly.
- **`project_templates/`** – Jinja2 templates used when generating new projects.
- **`config/docker-compose.dev.yml`** – Example Docker Compose setup with Postgres and Redis.
- **`scripts/`** – Helper scripts for environment setup, backups and updates.
- **`list_agents` tool** – Inspect available AI agents and their roles through the MCP server.

## Setup

1. Run the installation script which sets up the environment, checks for LM Studio and runs the tests:
   ```bash
   ./scripts/install.sh
   ```
   The script will create the `ai-dev-env` virtual environment if needed, install requirements, and verify that a local LM Studio server is running.
2. (Optional) set environment variables used by the server and web frontend:
   - `GITHUB_TOKEN` and `GITHUB_USERNAME` for GitHub integration.
   - `WORK_DIR` to choose where generated projects are stored (defaults to `./projects`).
   - `FRONTEND_PORT` and `FRONTEND_HOST` to configure the web UI port and host.
   - `LOG_CONFIG` to override the logging configuration file path.

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

### Command Line Interface

The `cli.py` tool provides a simple way to interact with the server without the web UI:

```bash
python cli.py create my-project "My project description"
python cli.py list
python cli.py agents
```

### Docker

You can run the entire application using Docker:

```bash
docker compose up --build
```

This exposes the web interface on `http://localhost:5000` and stores generated projects under the `projects/` directory.

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

Additional details about the underlying protocol can be found in
[docs/MCP_PROTOCOL.md](docs/MCP_PROTOCOL.md).

## License

This project is distributed under the terms of the GNU General Public License version 3. See [LICENSE](LICENSE) for details.
