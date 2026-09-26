"""
Run judge_simulator against the local bot.
"""

import os
import sys
import threading
import time
from bot import ThreadedHTTPServer, VeraRequestHandler

def main():
    # Start bot server on port 8080
    server = ThreadedHTTPServer(("127.0.0.1", 8080), VeraRequestHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    time.sleep(0.5)

    os.environ["BOT_URL"] = "http://localhost:8080"
    os.environ["LLM_PROVIDER"] = "mock"
    os.environ["TEST_SCENARIO"] = "all"

    try:
        import judge_simulator
        judge_simulator.main()
    finally:
        server.shutdown()
        server.server_close()

if __name__ == "__main__":
    main()
