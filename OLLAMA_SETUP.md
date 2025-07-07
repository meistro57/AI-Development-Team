# Ollama Integration Setup

## 1. Install Ollama

1. Visit [Ollama](https://ollama.com/) and follow the install instructions for your operating system.
2. After installation, start the server:

```bash
ollama serve &
```

## 2. Download a Model

Pull one of the recommended models:

```bash
ollama pull codellama
ollama pull llama2
ollama pull mistral
```

## 3. Configure AI Development Team

Update `config/mcp_config.json` so the server points to Ollama:

```json
{
  "llm": {
    "provider": "openai",
    "base_url": "http://localhost:11434/v1",
    "api_key": "ollama",
    "model": "codellama"
  }
}
```

## 4. Test Integration

Start the services and create a project:

```bash
ollama serve &
python ai_dev_team_server.py
```

The web interface will be available on `http://localhost:5000`.
