#!/usr/bin/env python3
"""
AI Development Team MCP Server - Syntax Fixed
"""


from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from agents import list_default_agents
import asyncio
import os
import sys
from datetime import datetime
import json
import logging
import logging.config
import yaml
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

app = Server("ai-dev-team-server")

# Logging configuration
LOG_CONFIG = os.getenv(
    "LOG_CONFIG",
    os.path.join(os.path.dirname(__file__), "config", "logging.yaml"),
)
if os.path.exists(LOG_CONFIG):
    os.makedirs(os.path.join(os.getcwd(), "logs"), exist_ok=True)
    with open(LOG_CONFIG, "r") as f:
        logging.config.dictConfig(yaml.safe_load(f))
else:
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("ai_dev_team")

# Configuration
WORK_DIR = os.getenv("WORK_DIR", os.path.join(os.getcwd(), "projects"))
os.makedirs(WORK_DIR, exist_ok=True)

# Project file templates
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "project_templates")
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

# Simple project storage
projects = {}


@app.list_tools()
async def list_tools():
    return [
        Tool(
            name="create_simple_project",
            description="Create a simple project with basic structure",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Project name"},
                    "description": {
                        "type": "string",
                        "description": "Project description",
                    },
                },
                "required": ["name", "description"],
            },
        ),
        Tool(
            name="list_projects",
            description="List all created projects",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="list_agents",
            description="List available automated agents",
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "create_simple_project":
        project_name = arguments["name"]
        description = arguments["description"]
        project_path = os.path.join(WORK_DIR, project_name)

        logger.info("Creating project %s", project_name)

        try:
            os.makedirs(os.path.join(project_path, "src"), exist_ok=True)

            context = {
                "project_name": project_name,
                "description": description,
                "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }

            try:
                tmpl = env.get_template("README.md.j2")
                readme_content = tmpl.render(**context)
            except TemplateNotFound:
                readme_content = f"# {project_name}\n\n{description}\n\nCreated by AI Development Team on {context['created']}"

            with open(os.path.join(project_path, "README.md"), "w") as f:
                f.write(readme_content)

            try:
                tmpl = env.get_template("main.py.j2")
                main_content = tmpl.render(**context)
            except TemplateNotFound:
                main_content = (
                    f'print("Hello from {project_name}!")\n'
                    f'print("Description: {description}")\n'
                    'print("Created by AI Development Team")\n'
                )

            with open(os.path.join(project_path, "src", "main.py"), "w") as f:
                f.write(main_content)

            config_data = {
                "name": project_name,
                "description": description,
                "created": datetime.now().isoformat(),
            }
            with open(os.path.join(project_path, "project_config.json"), "w") as f:
                json.dump(config_data, f, indent=2)

            project_id = f"proj_{len(projects) + 1}"
            projects[project_id] = {
                "name": project_name,
                "description": description,
                "path": project_path,
                "created": datetime.now().isoformat(),
            }

            return [
                TextContent(
                    type="text",
                    text=f"✅ Project '{project_name}' created successfully!\n📁 Location: {project_path}",
                )
            ]

        except Exception as exc:
            logger.exception("Failed to create project %s", project_name)
            return [TextContent(type="text", text=f"❌ Error creating project: {exc}")]

    elif name == "list_projects":
        if not projects:
            return [TextContent(type="text", text="No projects created yet.")]

        logger.info("Listing %d projects", len(projects))

        project_list = "Projects:\n"
        for proj_id, proj in projects.items():
            project_list += f"• {proj['name']}: {proj['description']}\n"

        return [TextContent(type="text", text=project_list)]

    elif name == "list_agents":
        logger.info("Listing agents")
        agents = list_default_agents()
        agent_list = "Agents:\n" + "\n".join(f"• {a.name}: {a.purpose}" for a in agents)
        return [TextContent(type="text", text=agent_list)]


async def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("✅ AI Development Team MCP Server - Test Mode")
        print(f"📁 Work Directory: {WORK_DIR}")
        return

    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, initialization_options={})


if __name__ == "__main__":
    asyncio.run(main())
