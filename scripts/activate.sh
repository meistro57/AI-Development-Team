#!/bin/bash
# AI Development Team - Environment Activation Script

cd "/home/mark/ai-development-team"

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | xargs)
fi

# Activate Python virtual environment
source ai-dev-env/bin/activate

# Display status
echo "🤖 AI Development Team Environment Activated"
echo "📁 Working Directory: $PWD"
echo "🐍 Python: $(which python)"
echo "📦 Pip: $(which pip)"

if [ -n "$GITHUB_TOKEN" ]; then
    echo "✅ GitHub token configured"
else
    echo "⚠️  GitHub token not configured"
fi

echo ""
echo "Available commands:"
echo "  python ai_dev_team_server.py          # Start MCP server"
echo "  python ai_dev_team_server.py --test   # Test configuration"
echo "  ./scripts/test_system.sh              # Run system tests"
echo "  ./scripts/backup.sh                   # Create backup"
echo ""
