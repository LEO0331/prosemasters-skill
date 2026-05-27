#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse


APP_DIR = Path(__file__).resolve().parents[1]
API_DIR = APP_DIR / "api"

if str(API_DIR) not in sys.path:
    sys.path.insert(0, str(API_DIR))

import generate as generate_api
import health as health_api
import validate as validate_api

API_HANDLERS = {
    "/api/health": ("GET", health_api.handler.do_GET),
    "/api/validate": ("POST", validate_api.handler.do_POST),
    "/api/generate": ("POST", generate_api.handler.do_POST),
}


class LocalHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(APP_DIR), **kwargs)

    def _api_path(self) -> str:
        return urlparse(self.path).path

    def _dispatch_api(self, method: str) -> bool:
        handler_spec = API_HANDLERS.get(self._api_path())
        if not handler_spec:
            return False
        expected_method, func = handler_spec
        if expected_method != method:
            self.send_error(405, "Method not allowed")
            return True
        func(self)
        return True

    def do_OPTIONS(self) -> None:
        if self._api_path().startswith("/api/"):
            health_api.handler.do_OPTIONS(self)
            return
        self.send_response(204)
        self.end_headers()

    def do_GET(self) -> None:
        path = self._api_path()
        if path.startswith("/api/"):
            if self._dispatch_api("GET"):
                return
            self.send_error(404, "API route not found")
            return
        if path == "/":
            self.path = "/index.html"
        super().do_GET()

    def do_POST(self) -> None:
        if self._dispatch_api("POST"):
            return
        self.send_error(404, "API route not found")


def main() -> int:
    parser = argparse.ArgumentParser(description="Local test server for master-persona-builder")
    parser.add_argument("--port", type=int, default=4173)
    args = parser.parse_args()

    httpd = ThreadingHTTPServer(("127.0.0.1", args.port), LocalHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        return 0
    finally:
        httpd.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
