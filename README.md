# AI Development Team

This repository contains a simple example of an **AI-based development team**. It exposes a [MCP](https://github.com/microsoft/mcp) server that can create small projects on request and includes a minimal Flask web UI.

## Features

- **`ai_dev_team_server.py`** – MCP server exposing tools to create projects and list them.
- **`web_frontend.py`** – Flask application with a form for creating projects using the server.
- **`cli.py`** – Simple command line tool to create and list projects.
- **`templates/index.html`** – HTML template used by the web interface.
- **Persistent storage** – Projects are saved to a SQLite database.
- **Authentication** – Basic auth can protect the web UI when enabled.
- **GitHub integration** – New projects may be pushed to GitHub automatically.
- **Tests** – Scripts such as `test_mcp.py` and `simple_mcp_test.py` show how to interact with the server.
- **Configuration** – Example systemd service and MCP configuration are located in the `config/` folder.
- **`OLLAMA_SETUP.md`** – Detailed guide for running the project with Ollama as a local language model.
- **`verify_agents.py`** – Diagnostic script to confirm all AI agents respond correctly.
- **`project_templates/`** – Jinja2 templates used when generating new projects.
- **`config/docker-compose.dev.yml`** – Example Docker Compose setup with Postgres and Redis.
- **`scripts/`** – Helper scripts for environment setup, backups and updates.
- **`list_agents` tool** – Inspect available AI agents and their roles through the MCP server.
- **REST API endpoints** – `/api/projects` and `/api/projects/<name>` expose project data.
- **Code formatted with Black** – Consistent style enforced via `black`.
- **Security checks** – CI runs `bandit` and `safety` to detect issues.

## Setup

1. Run the installation script which sets up the environment, checks for Ollama and runs the tests. If Ollama is not running a helper script will install a local Llama backend automatically:
   ```bash
   ./scripts/install.sh
   ```
   The script will create the `ai-dev-env` virtual environment if needed, install requirements, run `black` and the tests, and verify that a local Ollama server is running.
2. (Optional) set environment variables used by the server and web frontend:
   - `GITHUB_TOKEN` and `GITHUB_USERNAME` for GitHub integration.
   - `WORK_DIR` to choose where generated projects are stored (defaults to `./projects`).
   - `DB_PATH` to set the SQLite database file for persistent project storage.
   - `WEB_USERNAME` and `WEB_PASSWORD` to enable basic authentication for the web UI.
   - `FRONTEND_PORT` and `FRONTEND_HOST` to configure the web UI port and host.
   - `LOG_CONFIG` to override the logging configuration file path.

## Running

Launch both the MCP server and the web interface with a single command:
```bash
python run_app.py
```
This will start the backend server and Flask frontend together. Then open
`http://localhost:5000` in your browser to create projects via the web UI.

If you prefer, the server (`ai_dev_team_server.py`) and the web frontend
(`web_frontend.py`) can still be run independently.

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

### Running as a service

If you want the team to run continuously and pull new updates automatically, install the provided systemd service:

```bash
sudo ./scripts/setup_service.sh
```

The service launches `start.sh` on boot which updates the repository before starting the server and restarts it on failure.

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

### Code Formatting

Use the `black` formatter to keep the style consistent:

```bash
black .
```

## License

This project is distributed under the terms of the GNU General Public License version 3. See [LICENSE](LICENSE) for details.
