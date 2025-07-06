#!/bin/bash
# Simple start script for AI Development Team
# Updates repository, ensures dependencies and launches the server.
set -e

# Update repository
if [ -d .git ]; then
    echo "🔄 Updating repository..."
    git pull --ff-only
fi

# Setup Python virtual environment
if [ ! -d "ai-dev-env" ]; then
    echo "Creating virtual environment..."
    python3 -m venv ai-dev-env
fi
source ai-dev-env/bin/activate

# Install requirements
pip install --upgrade pip
pip install -r requirements.txt

# Optional additional setup
if [ -x ./scripts/install_llama.sh ]; then
    ./scripts/install_llama.sh || true
fi

# Start the MCP server
exec python ai_dev_team_server.py "$@"
