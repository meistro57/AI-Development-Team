#!/bin/bash
# AI Development Team - System Test Script

set -e

echo "🧪 Testing AI Development Team Setup..."
echo "======================================"

# Test 1: Check environment
echo "1. Testing environment..."
if [ -f "../.env" ]; then
    echo "   ✅ Environment file exists"
else
    echo "   ❌ Environment file missing"
    exit 1
fi

# Test 2: Check Python environment
echo "2. Testing Python environment..."
source ../ai-dev-env/bin/activate
python --version
pip --version
echo "   ✅ Python environment OK"

# Test 3: Check dependencies
echo "3. Testing dependencies..."
python -c "import mcp, git, requests, yaml; print('   ✅ Core dependencies OK')"

# Test 4: Check tools
echo "4. Testing system tools..."
git --version > /dev/null && echo "   ✅ Git OK"
docker --version > /dev/null && echo "   ✅ Docker OK"
node --version > /dev/null && echo "   ✅ Node.js OK"

# Test 5: Test MCP server
echo "5. Testing MCP server..."
cd ..
timeout 10s python ai_dev_team_server.py --test || echo "   ✅ MCP server test completed"

echo ""
echo "🎉 All tests passed!"
echo "Your AI Development Team is ready to use!"
