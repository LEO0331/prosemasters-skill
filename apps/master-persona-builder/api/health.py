import sys
from http.server import BaseHTTPRequestHandler
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import is_origin_allowed, repo_root_from_api_file, send_json


class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        if not is_origin_allowed(self):
            send_json(self, 403, {"ok": False, "errors": ["Forbidden origin"]})
            return
        send_json(self, 200, {"ok": True})

    def do_GET(self):
        if not is_origin_allowed(self):
            send_json(self, 403, {"ok": False, "errors": ["Forbidden origin"]})
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
