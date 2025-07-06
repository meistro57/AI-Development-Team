#!/usr/bin/env python3
"""Unified launcher for the AI Development Team.

Starts the MCP server and the web frontend so the entire application
can be run with a single command.
"""

import subprocess
import sys
import signal
import web_frontend


def main() -> None:
    server_proc = subprocess.Popen([sys.executable, "ai_dev_team_server.py"])

    def shutdown(*_args):
        server_proc.terminate()
        server_proc.wait()

    try:
        signal.signal(signal.SIGINT, lambda *a: shutdown())
        signal.signal(signal.SIGTERM, lambda *a: shutdown())

        web_frontend.app.run(
            debug=True,
            host=web_frontend.HOST,
            port=web_frontend.PORT,
        )
    finally:
        shutdown()


if __name__ == "__main__":
    main()
