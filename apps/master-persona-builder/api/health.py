import sys
from http.server import BaseHTTPRequestHandler
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import reject_forbidden_origin, repo_root_from_api_file, send_json


class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        if reject_forbidden_origin(self):
            return
        send_json(self, 200, {"ok": True})

    def do_GET(self):
        if reject_forbidden_origin(self):
            return
        repo_root = repo_root_from_api_file(Path(__file__))
        send_json(
            self,
            200,
            {
                "ok": True,
                "service": "master-persona-builder-api",
                "python_tools_available": bool(repo_root),
            },
        )
