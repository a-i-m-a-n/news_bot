import json
import os
import sys
from http.server import BaseHTTPRequestHandler

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import run


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            result = run()
            self._respond(200, {"status": "ok", "result": str(result)})
        except Exception as e:
            self._respond(500, {"status": "error", "message": str(e)})

    def _respond(self, status: int, payload: dict):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)