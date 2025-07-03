# LM Studio Integration Setup

## 1. Install LM Studio

### Download and Install
1. Go to [LM Studio website](https://lmstudio.ai/)
2. Download the appropriate version for your system
3. Install following the standard installation process

### For Linux (if AppImage)
```bash
# Make executable and run
chmod +x LMStudio-*.AppImage
./LMStudio-*.AppImage
```

## 2. Download a Model

### Recommended Models for AI Development Team

**For Coding Tasks:**
- `TheBloke/CodeLlama-7B-Instruct-GGUF` (7GB) - Good balance
- `TheBloke/CodeLlama-13B-Instruct-GGUF` (13GB) - Better performance
- `TheBloke/WizardCoder-Python-7B-V1.0-GGUF` (7GB) - Python focused

**For General Development:**
- `TheBloke/Llama-2-7B-Chat-GGUF` (7GB) - Reliable
- `TheBloke/Mistral-7B-Instruct-v0.1-GGUF` (7GB) - Fast
- `TheBloke/Neural-Chat-7B-v3-1-GGUF` (7GB) - Good conversation

**For Advanced Tasks (if you have enough RAM):**
- `TheBloke/Llama-2-13B-Chat-GGUF` (13GB)
- `TheBloke/CodeLlama-34B-Instruct-GGUF` (34GB)

### Download Process
1. Open LM Studio
2. Go to "Discover" tab
3. Search for your chosen model
4. Click "Download"
5. Wait for download to complete

## 3. Start Local Server

### In LM Studio:
1. Go to "Local Server" tab
2. Select your downloaded model
3. Configure settings:
   - **Context Length**: 4096 or higher
   - **GPU Offload**: Enable if you have a compatible GPU
   - **Temperature**: 0.7 (good for coding)
4. Click "Start Server"
5. Note the server URL (usually `http://localhost:1234`)

### Verify Server is Running:
```bash
curl http://localhost:1234/v1/models
```

## 4. Configure AI Development Team

### Update MCP Configuration
Edit `config/mcp_config.json` to use LM Studio:

```json
{
  "mcpServers": {
    "ai-dev-team": {
      "command": "python",
      "args": ["ai_dev_team_server.py"],
      "cwd": "/path/to/ai-development-team",
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}",
        "GITHUB_USERNAME": "${GITHUB_USERNAME}",
        "WORK_DIR": "/path/to/ai-development-team/projects"
      }
    }
  },
  "llm": {
    "provider": "openai",
    "base_url": "http://localhost:1234/v1",
    "api_key": "lm-studio",
    "model": "local-model"
  }
}
```

## 5. Test Integration

### Start Both Services:
```bash
# Terminal 1: Start LM Studio server (or use GUI)
# Terminal 2: Start AI Development Team
cd /path/to/ai-development-team
source ai-dev-env/bin/activate
python ai_dev_team_server.py
```

### Test with Simple Request:
```bash
# Test the system
./scripts/test_system.sh
```

## 6. Usage Examples

### Create Your First AI Project:
```python
# In your MCP client or direct interaction
project_spec = {
    "name": "my-awesome-app",
    "description": "A task management application",
    "type": "web_app",
    "tech_stack": ["React", "FastAPI", "PostgreSQL"],
    "features": ["user_auth", "real_time", "responsive"]
}

# The AI team will create a complete project!
```

## 7. Performance Tips

### Model Selection:
- **7B models**: Good for most tasks, faster response
- **13B models**: Better quality, slower response  
- **34B+ models**: Best quality, requires significant RAM

### System Requirements:
- **7B model**: 8GB RAM minimum
- **13B model**: 16GB RAM minimum
- **34B model**: 32GB RAM minimum

### Optimization:
- Use GPU acceleration if available
- Adjust context length based on your needs
- Lower temperature (0.3-0.5) for more focused code generation
- Higher temperature (0.7-0.9) for more creative solutions

## 8. Troubleshooting

### Common Issues:

**Model Won't Load:**
- Check available RAM
- Try a smaller model
- Close other applications

**Server Won't Start:**
- Check port 1234 isn't in use: `lsof -i :1234`
- Try a different port in LM Studio settings

**Slow Responses:**
- Use GPU acceleration if available
- Try a smaller model
- Reduce context length

**Connection Errors:**
- Verify LM Studio server is running
- Check firewall settings
- Ensure correct URL in configuration

## 9. Advanced Configuration

### Custom Model Parameters:
```json
{
  "model_settings": {
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 40,
    "repeat_penalty": 1.1,
    "max_tokens": 2048
  }
}
```

### Multiple Models:
You can switch between models in LM Studio for different tasks:
- Coding model for development tasks
- General model for planning and documentation
- Specialized models for specific domains

## 10. Integration with Development Workflow

### Typical Workflow:
1. Start LM Studio with appropriate model
2. Start AI Development Team MCP server
3. Request project creation through your MCP client
4. AI team creates complete project with:
   - GitHub repository
   - Full project structure
   - Comprehensive tests
   - CI/CD pipeline
   - Deployment configuration
   - Documentation

### Example Commands:
```bash
# Quick project creation
./scripts/activate.sh
# Then use your MCP client to request:
# "Create a REST API for user management with authentication"
```

The AI Development Team will handle everything automatically!
