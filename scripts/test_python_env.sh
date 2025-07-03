#!/bin/bash
# Test Python Environment

cd "$(dirname "$0")/.."
source ai-dev-env/bin/activate

echo "🧪 Testing Python Environment..."
echo "================================="

echo "1. Python version:"
python --version

echo "2. Virtual environment:"
echo "   $VIRTUAL_ENV"

echo "3. Pip version:"
pip --version

echo "4. Testing core imports:"
python -c "
try:
    import mcp
    print('   ✅ MCP available')
except ImportError as e:
    print(f'   ❌ MCP not available: {e}')

try:
    import git
    print('   ✅ GitPython available')
except ImportError as e:
    print(f'   ❌ GitPython not available: {e}')

try:
    import requests
    print('   ✅ Requests available')
except ImportError as e:
    print(f'   ❌ Requests not available: {e}')

try:
    import yaml
    print('   ✅ PyYAML available')
except ImportError as e:
    print(f'   ❌ PyYAML not available: {e}')

try:
    import pytest
    print('   ✅ Pytest available')
except ImportError as e:
    print(f'   ❌ Pytest not available: {e}')
"

echo ""
echo "5. Package list:"
pip list | head -10
echo "   ... and $(pip list | wc -l) total packages"

echo ""
echo "✅ Python environment test completed!"
