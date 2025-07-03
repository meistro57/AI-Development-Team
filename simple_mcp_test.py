#!/usr/bin/env python3
import asyncio
import json
import subprocess
import sys

async def test_mcp_server():
    print("🧪 Testing AI Development Team MCP Server...")
    
    # Start server as subprocess
    server = subprocess.Popen(
        [sys.executable, "ai_dev_team_server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=0
    )
    
    try:
        # Test 1: Initialize
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "test-client", "version": "1.0.0"}
            }
        }
        
        print("📤 Sending initialize request...")
        server.stdin.write(json.dumps(init_request) + "\n")
        server.stdin.flush()
        
        # Read response
        response = server.stdout.readline()
        if response:
            print("📥 Initialize response:", json.loads(response.strip()))
        
        # Test 2: List tools
        tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        
        print("\n📤 Requesting tools list...")
        server.stdin.write(json.dumps(tools_request) + "\n")
        server.stdin.flush()
        
        response = server.stdout.readline()
        if response:
            tools_response = json.loads(response.strip())
            print("📥 Available tools:")
            for tool in tools_response.get("result", {}).get("tools", []):
                print(f"  • {tool['name']}: {tool['description']}")
        
        # Test 3: Call a tool
        create_project_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "create_simple_project",
                "arguments": {
                    "name": "mcp-test-project",
                    "description": "Project created via MCP protocol test"
                }
            }
        }
        
        print("\n📤 Creating project via MCP...")
        server.stdin.write(json.dumps(create_project_request) + "\n")
        server.stdin.flush()
        
        response = server.stdout.readline()
        if response:
            result = json.loads(response.strip())
            print("📥 Project creation result:")
            print(json.dumps(result, indent=2))
        
        print("\n✅ MCP test completed!")
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        server.terminate()
        server.wait()

if __name__ == "__main__":
    asyncio.run(test_mcp_server())
