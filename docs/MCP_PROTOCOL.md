# MCP Protocol Usage

The AI Development Team exposes its functionality through the [MCP](https://github.com/microsoft/mcp) protocol.

## Initialization

Clients must send an `initialize` request before using any tools. The server currently implements the `list_tools` and `call_tool` methods.

Example initialization request:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {},
    "clientInfo": {"name": "example-client", "version": "1.0"}
  }
}
```

## Tool Usage

Use `tools/list` to discover available tools and `tools/call` to invoke them. The `create_simple_project` tool accepts a project `name` and `description`.

For more details see the example tests in `test_mcp.py`.
