import sys
import uuid
from http.server import BaseHTTPRequestHandler
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import (
    normalize_payload,
    read_json_body,
    reject_forbidden_origin,
    reject_unauthorized,
    send_json,
    validate_payload,
)


class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        if reject_forbidden_origin(self):
            return
        send_json(self, 200, {"ok": True})

    def do_POST(self):
        try:
            if reject_forbidden_origin(self):
                return
            if reject_unauthorized(self):
                return
            payload = read_json_body(self)
            normalized = normalize_payload(payload)
            errors = validate_payload(normalized)
            send_json(self, 200, {"ok": len(errors) == 0, "errors": errors, "normalized": normalized})
        except Exception as exc:
            req_id = str(uuid.uuid4())
            print(f"[validate][{req_id}] {exc}", file=sys.stderr)
            send_json(self, 400, {"ok": False, "errors": ["Invalid request"], "request_id": req_id})
