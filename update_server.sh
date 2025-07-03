#!/bin/bash
# Update the MCP server with fixed version

cd ~/ai-development-team

# Back up current server
cp ai_dev_team_server.py ai_dev_team_server.py.backup

# Create the fixed server
cat > ai_dev_team_server.py << 'EOF'
#!/usr/bin/env python3
"""
AI Development Team MCP Server - Fixed Version
A comprehensive MCP server that acts as a full development team
"""

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Resource, Tool, TextContent
import asyncio
import os
import json
import subprocess
import sys
from pathlib import Path
import tempfile
import shutil
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/ai_dev_team.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

app = Server("ai-dev-team-server")

# Configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
WORK_DIR = os.getenv("WORK_DIR", os.path.join(os.getcwd(), "projects"))

# Ensure work directory exists
os.makedirs(WORK_DIR, exist_ok=True)

class DevTeamAgent:
    """Base class for development team agents"""
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.tasks = []
        self.status = "idle"
    
    async def execute_task(self, task):
        self.status = "working"
        self.tasks.append(task)
        logger.info(f"{self.name} executing task: {task}")

class ProjectManagerAgent(DevTeamAgent):
    """Manages project lifecycle and coordination"""
    def __init__(self):
        super().__init__("ProjectManager", "Project Management")
        self.projects = {}
    
    async def create_project_plan(self, project_spec):
        """Create comprehensive project plan"""
        plan = {
            "project_id": f"proj_{int(datetime.now().timestamp())}",
            "name": project_spec.get("name", "New Project"),
            "description": project_spec.get("description", ""),
            "tech_stack": project_spec.get("tech_stack", []),
            "phases": [
                {
                    "name": "Setup & Architecture",
                    "tasks": ["repo_creation", "project_structure", "ci_cd_setup"],
                    "agent": "ArchitectAgent"
                },
                {
                    "name": "Core Development", 
                    "tasks": ["core_implementation", "feature_development"],
                    "agent": "DeveloperAgent"
                },
                {
                    "name": "Testing & QA",
                    "tasks": ["unit_tests", "integration_tests", "e2e_tests"],
                    "agent": "QAAgent"
                },
                {
                    "name": "DevOps & Deployment",
                    "tasks": ["containerization", "deployment_setup", "monitoring"],
                    "agent": "DevOpsAgent"
                },
                {
                    "name": "Final Review",
                    "tasks": ["code_review", "security_audit", "performance_test"],
                    "agent": "ReviewAgent"
                }
            ],
            "created_at": datetime.now().isoformat(),
            "status": "planning"
        }
        
        self.projects[plan["project_id"]] = plan
        return plan

# Global agent instances
project_manager = ProjectManagerAgent()

@app.list_resources()
async def list_resources():
    """List available team resources"""
    return [
        Resource(
            uri="team://status",
            name="Development Team Status", 
            description="Current status of all team agents"
        ),
        Resource(
            uri="team://projects",
            name="Active Projects",
            description="List of all active projects"
        ),
        Resource(
            uri="team://capabilities",
            name="Team Capabilities",
            description="Overview of what the team can do"
        )
    ]

@app.read_resource()
async def read_resource(uri: str):
    """Read team resource content"""
    
    if uri == "team://status":
        status = {
            "project_manager": {"name": project_manager.name, "status": project_manager.status},
            "system": {
                "work_dir": WORK_DIR,
                "github_configured": bool(GITHUB_TOKEN),
                "projects_count": len(project_manager.projects)
            }
        }
        return TextContent(type="text", text=json.dumps(status, indent=2))
    
    elif uri == "team://projects":
        return TextContent(
            type="text",
            text=json.dumps(project_manager.projects, indent=2)
        )
    
    elif uri == "team://capabilities":
        capabilities = {
            "project_management": ["Project planning", "Task coordination", "Timeline management"],
            "architecture": ["System design", "GitHub repo creation", "Technology selection"],
            "development": ["Code generation", "Project structure", "Implementation"],
            "qa": ["Test generation", "Quality assurance", "Performance testing"],
            "devops": ["CI/CD setup", "Containerization", "Deployment configuration"],
            "review": ["Code review", "Security audit", "Final approval"]
        }
        return TextContent(type="text", text=json.dumps(capabilities, indent=2))

@app.list_tools()
async def list_tools():
    """List available development team tools"""
    return [
        Tool(
            name="create_simple_project",
            description="Create a simple project to test the system",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Project name"},
                    "description": {"type": "string", "description": "Project description"},
                    "type": {"type": "string", "enum": ["web_app", "api", "simple"], "default": "simple"},
                },
                "required": ["name", "description"]
            }
        ),
        Tool(
            name="get_system_status",
            description="Get system and configuration status",
            inputSchema={
                "type": "object",
                "properties": {},
            }
        ),
        Tool(
            name="test_github_connection",
            description="Test GitHub API connection and authentication",
            inputSchema={
                "type": "object",
                "properties": {},
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    """Execute development team tools"""
    
    if name == "create_simple_project":
        # Create a basic project structure for testing
        project_name = arguments["name"]
        project_path = os.path.join(WORK_DIR, project_name)
        
        try:
            os.makedirs(project_path, exist_ok=True)
            
            # Create basic README
            readme_content = f"""# {project_name}

{arguments.get("description", "A project created by AI Development Team")}

## Getting Started

This is a simple project created to test the AI Development Team MCP Server.

## Project Structure

```
{project_name}/
├── README.md          # This file
├── src/              # Source code
└── tests/            # Test files
```

## Next Steps

1. Add your code to the `src/` directory
2. Add tests to the `tests/` directory  
3. Update this README with more details

## Created by

AI Development Team MCP Server
- Created: {datetime.now().isoformat()}
- Type: {arguments.get("type", "simple")}
"""
            
            with open(os.path.join(project_path, "README.md"), "w") as f:
                f.write(readme_content)
            
            # Create basic directories
            os.makedirs(os.path.join(project_path, "src"), exist_ok=True)
            os.makedirs(os.path.join(project_path, "tests"), exist_ok=True)
            
            # Create a simple Python file
            python_content = f'''"""
{project_name} - Main module
Generated by AI Development Team
"""

def main():
    """Main function"""
    print("Hello from {project_name}!")
    print("AI Development Team is working!")
    print("Project type: {arguments.get('type', 'simple')}")
    print("Created: {datetime.now().isoformat()}")

if __name__ == "__main__":
    main()
'''
            
            with open(os.path.join(project_path, "src", "main.py"), "w") as f:
                f.write(python_content)
            
            # Create a simple test
            test_content = f'''"""
Tests for {project_name}
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import main

def test_main():
    """Test main function runs without error"""
    try:
        main()
        assert True, "Main function executed successfully"
    except Exception as e:
        assert False, f"main() failed: {e}"

def test_project_structure():
    """Test project structure exists"""
    project_root = os.path.join(os.path.dirname(__file__), '..')
    assert os.path.exists(os.path.join(project_root, 'README.md'))
    assert os.path.exists(os.path.join(project_root, 'src'))
    assert os.path.exists(os.path.join(project_root, 'tests'))
    assert os.path.exists(os.path.join(project_root, 'src', 'main.py'))

if __name__ == "__main__":
    test_main()
    test_project_structure()
    print("All tests passed!")
'''
            
            with open(os.path.join(project_path, "tests", "test_main.py"), "w") as f:
                f.write(test_content)
            
            return {
                "success": True,
                "project_name": project_name,
                "project_path": project_path,
                "files_created": [
                    "README.md",
                    "src/main.py", 
                    "tests/test_main.py"
                ],
                "message": f"Simple project '{project_name}' created successfully!",
                "next_steps": [
                    f"cd {project_path}",
                    "python src/main.py",
                    "python tests/test_main.py"
                ]
            }
            
        except Exception as e:
            logger.error(f"Failed to create project: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    elif name == "get_system_status":
        # Check system dependencies
        dependencies = {}
        for cmd in ["git", "python3", "docker", "node", "npm"]:
            try:
                result = subprocess.run([cmd, "--version"], capture_output=True, text=True, timeout=5)
                dependencies[cmd] = {
                    "available": result.returncode == 0,
                    "version": result.stdout.strip().split('\n')[0] if result.returncode == 0 else None
                }
            except:
                dependencies[cmd] = {"available": False, "version": None}
        
        status = {
            "system": {
                "work_directory": WORK_DIR,
                "work_dir_exists": os.path.exists(WORK_DIR),
                "work_dir_writable": os.access(WORK_DIR, os.W_OK),
                "python_version": sys.version.split()[0],
                "virtual_env": os.getenv("VIRTUAL_ENV", "Not activated")
            },
            "configuration": {
                "github_token_set": bool(GITHUB_TOKEN),
                "github_username_set": bool(GITHUB_USERNAME),
            },
            "dependencies": dependencies,
            "projects": {
                "total_projects": len(project_manager.projects),
                "active_projects": [p for p in project_manager.projects.values() if p["status"] != "completed"]
            }
        }
        
        return status
    
    elif name == "test_github_connection":
        if not GITHUB_TOKEN:
            return {
                "success": False,
                "error": "GitHub token not configured. Set GITHUB_TOKEN environment variable."
            }
        
        try:
            import requests
            
            headers = {
                "Authorization": f"token {GITHUB_TOKEN}",
                "Accept": "application/vnd.github.v3+json"
            }
            
            response = requests.get("https://api.github.com/user", headers=headers, timeout=10)
            
            if response.status_code == 200:
                user_data = response.json()
                return {
                    "success": True,
                    "user": user_data.get("login"),
                    "name": user_data.get("name"),
                    "public_repos": user_data.get("public_repos"),
                    "private_repos": user_data.get("total_private_repos"),
                    "api_rate_limit": response.headers.get("X-RateLimit-Remaining")
                }
            else:
                return {
                    "success": False,
                    "error": f"GitHub API error: {response.status_code} - {response.text}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Connection error: {str(e)}"
            }

async def main():
    """Main server entry point"""
    logger.info("Starting AI Development Team MCP Server...")
    
    # Ensure work directory exists
    os.makedirs(WORK_DIR, exist_ok=True)
    
    # Check if running in test mode
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        logger.info("Running in test mode...")
        
        # Test system status
        status = await call_tool("get_system_status", {})
        print(json.dumps(status, indent=2))
        
        # Test GitHub connection if configured
        if GITHUB_TOKEN:
            github_status = await call_tool("test_github_connection", {})
            print("\nGitHub Connection Test:")
            print(json.dumps(github_status, indent=2))
        
        return
    
    try:
        # Updated to work with newer MCP versions
        async with stdio_server() as (read_stream, write_stream):
            await app.run(
                read_stream, 
                write_stream, 
                initialization_options={}
            )
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
EOF

chmod +x ai_dev_team_server.py

echo "✅ MCP server updated successfully!"
echo "🧪 Testing the fixed server..."

# Test the server
python ai_dev_team_server.py --test
