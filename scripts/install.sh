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

# 3. Check LM Studio availability
LM_STUDIO_URL="http://localhost:1234/v1/models"

echo "Checking LM Studio..."
if curl -sf "$LM_STUDIO_URL" > /dev/null; then
    echo "✅ LM Studio server is running"
else
    echo "⚠️  LM Studio not detected on port 1234"
    if command -v lmstudio >/dev/null 2>&1; then
        echo "➡️  Starting LM Studio in server mode"
        lmstudio --server &
        sleep 5
    elif ls LMStudio-*.AppImage >/dev/null 2>&1; then
        APPIMG=$(ls LMStudio-*.AppImage | head -n1)
        chmod +x "$APPIMG"
        "./$APPIMG" --server &
        sleep 5
    else
        echo "➡️  Downloading LM Studio AppImage..."
        curl -L -o LMStudio.AppImage "https://github.com/lmstudio-ai/LM-Studio/releases/latest/download/LMStudio-linux-x64.AppImage" || true
        if [ -f LMStudio.AppImage ]; then
            chmod +x LMStudio.AppImage
            ./LMStudio.AppImage --server &
            sleep 5
        else
            echo "❌ Automatic download failed. Please follow LM_STUDIO_SETUP.md"
        fi
    fi

    if curl -sf "$LM_STUDIO_URL" > /dev/null; then
        echo "✅ LM Studio server started"
    else
        echo "❌ LM Studio server still not running. See LM_STUDIO_SETUP.md for manual setup"
    fi
fi

echo "✅ Installation and tests complete"
