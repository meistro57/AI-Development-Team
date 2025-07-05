import asyncio
import typer
from ai_dev_team_server import call_tool

app = typer.Typer(help="Command line interface for AI Development Team")


@app.command()
def create(name: str, description: str):
    """Create a new project"""
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
    result = asyncio.run(call_tool("list_projects", {}))
    if result:
        typer.echo(result[0].text)
    else:
        typer.echo("No projects found")


if __name__ == "__main__":
    app()
