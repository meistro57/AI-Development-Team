#!/usr/bin/env python3
"""
AI Development Team - Web Frontend
Simple web interface for creating projects
"""

from flask import Flask, render_template, request, jsonify
import asyncio
import os
from datetime import datetime
import sys
import logging

# Import our AI development team
sys.path.append(".")
from ai_dev_team_server import call_tool

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("web_frontend")

# Host and port are configurable via environment variables
HOST = os.getenv("FRONTEND_HOST", "0.0.0.0")
PORT = int(os.getenv("FRONTEND_PORT", "5000"))

# Store project history
project_history = []


@app.route("/")
def index():
    """Main page with project creation form"""
    return render_template("index.html", projects=project_history)


@app.route("/create_project", methods=["POST"])
def create_project():
    """Handle project creation"""
    try:
        # Get form data
        project_name = request.form["name"].strip()
        description = request.form["description"].strip()

        # Validate input
        if not project_name or not description:
            return jsonify({"error": "Please fill in all fields"}), 400

        # Clean project name (no spaces, special chars)
        clean_name = project_name.lower().replace(" ", "-").replace("_", "-")
        clean_name = "".join(c for c in clean_name if c.isalnum() or c == "-")

        # Call AI Development Team
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        result = loop.run_until_complete(
            call_tool(
                "create_simple_project",
                {"name": clean_name, "description": description},
            )
        )

        loop.close()

        # Parse result
        if result and len(result) > 0:
            success_message = result[0].text

            # Add to history
            project_info = {
                "name": clean_name,
                "original_name": project_name,
                "description": description,
                "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "path": f"projects/{clean_name}",
                "status": "success",
            }
            project_history.insert(0, project_info)

            return jsonify(
                {"success": True, "message": success_message, "project": project_info}
            )
        else:
            return jsonify({"error": "Failed to create project"}), 500

    except Exception as e:
        logger.exception("Failed to create project")
        return jsonify({"error": f"Error: {str(e)}"}), 500


@app.route("/projects")
def list_projects():
    """List all created projects"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        result = loop.run_until_complete(call_tool("list_projects", {}))
        loop.close()

        if result and len(result) > 0:
            projects_text = result[0].text
            return jsonify({"projects": projects_text})
        else:
            return jsonify({"projects": "No projects found"})

    except Exception as e:
        logger.exception("Failed to list projects")
        return jsonify({"error": str(e)}), 500


@app.route("/api/projects")
def api_projects():
    """Return project history as JSON"""
    return jsonify(project_history)


@app.route("/api/projects/<name>")
def api_project_detail(name):
    """Return single project details"""
    for proj in project_history:
        if proj["name"] == name:
            return jsonify(proj)
    return jsonify({"error": "Not found"}), 404


@app.route("/project/<project_name>")
def view_project(project_name):
    """View project details"""
    project_path = f"projects/{project_name}"

    if not os.path.exists(project_path):
        logger.warning("Project %s not found", project_name)
        return "Project not found", 404

    # Read project files
    files = {}

    # Read README
    readme_path = os.path.join(project_path, "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r") as f:
            files["README.md"] = f.read()

    # Read main.py
    main_path = os.path.join(project_path, "src", "main.py")
    if os.path.exists(main_path):
        with open(main_path, "r") as f:
            files["src/main.py"] = f.read()

    try:
        return render_template(
            "project_view.html", project_name=project_name, files=files
        )
    except Exception as e:
        logger.exception("Failed to render project %s", project_name)
        return f"Error: {e}", 500


if __name__ == "__main__":
    app.run(debug=True, host=HOST, port=PORT)
