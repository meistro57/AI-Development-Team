#!/bin/bash
# Install and test Llama if LM Studio or Llama server is not detected
set -e

LM_STUDIO_URL="http://localhost:1234/v1/models"

# Check LM Studio server
if curl -sf "$LM_STUDIO_URL" > /dev/null; then
    echo "✅ LM Studio server detected"
    exit 0
fi

# Activate virtual environment if present
if [ -d "ai-dev-env" ]; then
    source ai-dev-env/bin/activate
fi

# Install llama-cpp-python if not installed
if ! python - <<'PY'
import importlib.util
raise SystemExit(0 if importlib.util.find_spec('llama_cpp') else 1)
PY
then
    echo "Installing llama-cpp-python..."
    pip install --upgrade llama-cpp-python
fi

# Test llama installation
python - <<'PY'
try:
    import llama_cpp
    print('✅ llama-cpp-python import successful')
except Exception as e:
    print('❌ Failed to import llama-cpp-python', e)
    raise
PY

# Write default llama settings
cat > config/llama_settings.json <<'CONF'
{
  "provider": "llama_cpp",
  "model_path": "/path/to/model.gguf",
  "n_ctx": 2048
}
CONF

echo "✅ Llama settings written to config/llama_settings.json"

exit 0
