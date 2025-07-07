#!/bin/bash
# AI Development Team - Full installation and test script
set -e

# 1. Setup Python virtual environment
if [ ! -d "ai-dev-env" ]; then
    echo "Creating virtual environment..."
    python3 -m venv ai-dev-env
fi
source ai-dev-env/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

# 2. Run code style and unit tests
echo "Running black..."
black .

echo "Running tests..."
pytest -q

# 3. Check Ollama availability
OLLAMA_URL="http://localhost:11434/api/tags"

echo "Checking Ollama..."
if curl -sf "$OLLAMA_URL" > /dev/null; then
    echo "✅ Ollama server is running"
else
    echo "⚠️  Ollama not detected on port 11434"
    if command -v ollama >/dev/null 2>&1; then
        echo "➡️  Starting Ollama in server mode"
        ollama serve &
        sleep 5
    else
        echo "❌ Ollama command not found. Please follow OLLAMA_SETUP.md"
    fi

    if curl -sf "$OLLAMA_URL" > /dev/null; then
        echo "✅ Ollama server started"
    else
        echo "❌ Ollama server still not running. See OLLAMA_SETUP.md for manual setup"
    fi
fi

echo "✅ Installation and tests complete"
