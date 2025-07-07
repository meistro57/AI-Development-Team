#!/bin/bash
# AI Development Team - Setup Script
set -e

python -m venv ai-dev-env
source ai-dev-env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "Checking for Ollama or local Llama installation..."
./scripts/install_llama.sh

echo "✅ Environment ready. Activate with: source ai-dev-env/bin/activate"
