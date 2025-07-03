#!/usr/bin/env python3
import subprocess
import json
import time
import sys

def test_server():
    print("🔍 Debugging MCP Server...")
    
    # Start server with error output visible
    server = subprocess.Popen(
        [sys.executable, "ai_dev_team_server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    
    try:
        # Simple initialize request
        init_msg = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "test", "version": "1.0"}
            }
        }
        
        print("📤 Sending:", json.dumps(init_msg))
        server.stdin.write(json.dumps(init_msg) + "\n")
        server.stdin.flush()
        
        # Wait and check if server is still alive
        time.sleep(2)
        
        if server.poll() is not None:
            print(f"❌ Server crashed with exit code: {server.returncode}")
            output = server.stdout.read()
            print(f"Server output: {output}")
        else:
            print("✅ Server is still running")
            
            # Try to read response
            try:
                response = server.stdout.readline()
                if response:
                    print(f"📥 Response: {response.strip()}")
                else:
                    print("📥 No response received")
            except Exception as e:
                print(f"Error reading response: {e}")
        
    except Exception as e:
        print(f"❌ Test error: {e}")
    
    finally:
        if server.poll() is None:
            server.terminate()
            server.wait()
        
        print("🏁 Test completed")

if __name__ == "__main__":
    test_server()
