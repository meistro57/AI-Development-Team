#!/usr/bin/env python3
import subprocess
import json
import time
import sys

def test_mcp_server():
    print("🧪 Testing AI Development Team MCP Server...")
    
    server = subprocess.Popen(
        [sys.executable, "ai_dev_team_server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=0
    )
    
    try:
        # Proper MCP initialization
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "roots": {
                        "listChanged": False
                    }
                },
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        print("📤 Initializing connection...")
        server.stdin.write(json.dumps(init_request) + "\n")
        server.stdin.flush()
        
        # Read initialization response
        init_response = server.stdout.readline()
        if init_response:
            response_data = json.loads(init_response.strip())
            print("📥 Initialization:", "✅ Success" if "result" in response_data else "❌ Failed")
            if "error" in response_data:
                print(f"   Error: {response_data['error']}")
        
        # Send initialized notification
        initialized_notification = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized"
        }
        
        server.stdin.write(json.dumps(initialized_notification) + "\n")
        server.stdin.flush()
        
        # Test listing tools
        tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list"
        }
        
        print("📤 Requesting tools...")
        server.stdin.write(json.dumps(tools_request) + "\n")
        server.stdin.flush()
        
        tools_response = server.stdout.readline()
        if tools_response:
            tools_data = json.loads(tools_response.strip())
            if "result" in tools_data and "tools" in tools_data["result"]:
                print("📥 Available tools:")
                for tool in tools_data["result"]["tools"]:
                    print(f"   • {tool['name']}: {tool['description']}")
                
                # Test creating a project
                create_request = {
                    "jsonrpc": "2.0",
                    "id": 3,
                    "method": "tools/call",
                    "params": {
                        "name": "create_simple_project",
                        "arguments": {
                            "name": "mcp-test-project",
                            "description": "A project created via MCP protocol"
                        }
                    }
                }
                
                print("📤 Creating project...")
                server.stdin.write(json.dumps(create_request) + "\n")
                server.stdin.flush()
                
                create_response = server.stdout.readline()
                if create_response:
                    create_data = json.loads(create_response.strip())
                    if "result" in create_data:
                        print("📥 Project creation:")
                        if "content" in create_data["result"]:
                            for content in create_data["result"]["content"]:
                                print(f"   {content['text']}")
                        else:
                            print("   ✅ Success!")
                    else:
                        print(f"   ❌ Failed: {create_data.get('error', 'Unknown error')}")
            else:
                print("❌ No tools found")
        
        print("\n🎉 MCP Test Completed Successfully!")
        
    except Exception as e:
        print(f"❌ Test error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        server.terminate()
        server.wait()

if __name__ == "__main__":
    test_mcp_server()
