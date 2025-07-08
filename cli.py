import asyncio
import logging
import typer
from ai_dev_team_server import call_tool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cli")

app = typer.Typer(help="Command line interface for AI Development Team")


@app.command()
def create(name: str, description: str):
    """Create a new project"""
    logger.info("Creating project %s", name)
    result = asyncio.run(
        call_tool("create_simple_project", {"name": name, "description": description})
    )
    if result:
        typer.echo(result[0].text)
    else:
        typer.echo("Failed to create project")


@app.command()
def list():
    """List existing projects"""
    logger.info("Listing projects")
    result = asyncio.run(call_tool("list_projects", {}))
    if result:
        typer.echo(result[0].text)
    else:
        typer.echo("No projects found")


@app.command()
def delete(name: str):
    """Delete an existing project"""
    logger.info("Deleting project %s", name)
    result = asyncio.run(call_tool("delete_project", {"name": name}))
    if result:
        typer.echo(result[0].text)
    else:
        typer.echo("Failed to delete project")


@app.command()
def agents():
    """List available agents"""
    logger.info("Listing agents")
    result = asyncio.run(call_tool("list_agents", {}))
    if result:
        typer.echo(result[0].text)
    else:
        typer.echo("No agents found")


if __name__ == "__main__":
    app()
