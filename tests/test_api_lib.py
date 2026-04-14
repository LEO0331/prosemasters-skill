from __future__ import annotations

import io
import json
from pathlib import Path

import _lib


class DummyHandler:
    def __init__(self, headers: dict[str, str], body: bytes = b"") -> None:
        self.headers = headers
        self.rfile = io.BytesIO(body)
        self.wfile = io.BytesIO()
        self.status = None
        self.sent_headers: list[tuple[str, str]] = []
        self.ended = False

    def send_response(self, status: int) -> None:
        self.status = status

    def send_header(self, name: str, value: str) -> None:
        self.sent_headers.append((name, value))

    def end_headers(self) -> None:
        self.ended = True


def test_read_json_body_and_send_json() -> None:
    body = json.dumps({"a": 1}).encode("utf-8")
    h = DummyHandler({"Content-Length": str(len(body)), "Origin": "https://a.com", "Host": "a.com", "X-Forwarded-Proto": "https"}, body)
    payload = _lib.read_json_body(h)
    assert payload == {"a": 1}

    _lib.send_json(h, 200, {"ok": True})
    assert h.status == 200
    assert h.ended
    assert h.wfile.getvalue().startswith(b"{")


def test_read_json_body_errors() -> None:
    h_invalid = DummyHandler({"Content-Length": "abc"}, b"{}")
    try:
        _lib.read_json_body(h_invalid)
        assert False, "expected ValueError"
    except ValueError as exc:
        assert "Invalid Content-Length" in str(exc)

    h_empty = DummyHandler({"Content-Length": "0"}, b"")
    try:
        _lib.read_json_body(h_empty)
        assert False, "expected ValueError"
    except ValueError as exc:
        assert "Empty body" in str(exc)

    h_too_large = DummyHandler({"Content-Length": "11"}, b"{}")
    try:
        _lib.read_json_body(h_too_large, max_bytes=10)
        assert False, "expected ValueError"
    except ValueError as exc:
        assert "Payload too large" in str(exc)

    body = json.dumps(["not-object"]).encode("utf-8")
    h_list = DummyHandler({"Content-Length": str(len(body))}, body)
    try:
        _lib.read_json_body(h_list)
        assert False, "expected ValueError"
    except ValueError as exc:
        assert "must be an object" in str(exc)


def test_origin_and_auth(monkeypatch) -> None:
    monkeypatch.setenv("MPB_ALLOWED_ORIGINS", "https://allowed.com")
    h1 = DummyHandler({"Origin": "https://allowed.com", "Host": "api.com"})
    assert _lib.is_origin_allowed(h1)

    h2 = DummyHandler({"Origin": "https://x.com", "Host": "api.com"})
    assert not _lib.is_origin_allowed(h2)

    monkeypatch.setenv("MPB_API_KEY", "secret123")
    h3 = DummyHandler({"X-API-Key": "secret123"})
    assert _lib.is_authorized(h3)
    h4 = DummyHandler({"Authorization": "Bearer secret123"})
    assert _lib.is_authorized(h4)
    h5 = DummyHandler({"X-API-Key": "wrong"})
    assert not _lib.is_authorized(h5)


def test_same_origin_and_reject_helpers(monkeypatch) -> None:
    h_same = DummyHandler({"Origin": "http://localhost:3000", "Host": "localhost:3000"})
    assert _lib.is_origin_allowed(h_same)
    assert _lib._same_origin(h_same, "http://localhost:3000")

    monkeypatch.setenv("MPB_ALLOWED_ORIGINS", "")
    h_block = DummyHandler({"Origin": "https://evil.com", "Host": "api.com"})
    assert _lib.reject_forbidden_origin(h_block)
    assert h_block.status == 403

    monkeypatch.setenv("MPB_API_KEY", "k")
    h_auth = DummyHandler({"X-API-Key": "bad"})
    assert _lib.reject_unauthorized(h_auth)
    assert h_auth.status == 401


def test_validate_payload_limits(monkeypatch) -> None:
    monkeypatch.setenv("MPB_MAX_SOURCE_ITEMS", "1")
    monkeypatch.setenv("MPB_MAX_SOURCE_CHARS", "5")
    monkeypatch.setenv("MPB_MAX_TOTAL_SOURCE_CHARS", "6")
    payload = {
        "meta": {"slug": "ok", "name": "n", "description": "d"},
        "master": {"display_name": "m"},
        "source_materials": [
            {"category": "works", "content": "123456"},
            {"category": "bad", "content": "x"},
        ],
    }
    errors = _lib.validate_payload(payload)
    assert any("max items exceeded" in e for e in errors)
    assert any("must be one of" in e for e in errors)
    assert any("too large" in e for e in errors)


def test_validate_payload_required_errors() -> None:
    errors = _lib.validate_payload({"meta": {}, "master": {}, "source_materials": []})
    assert "meta.slug is required" in errors
    assert "meta.name is required" in errors
    assert "meta.description is required" in errors
    assert "master.display_name is required" in errors


def test_normalize_payload_and_helpers() -> None:
    normalized = _lib.normalize_payload(
        {
            "meta": {"slug": " Han-Yu ", "name": " n ", "description": " d "},
            "master": {"display_name": " m "},
            "source_materials": [{"category": "works", "title": " t ", "content": " c "}],
        }
    )
    assert normalized["meta"]["slug"] == "han-yu"
    assert normalized["source_materials"][0]["title"] == "t"
    assert _lib.normalize_array("a\nb") == ["a", "b"]
    assert "fallback" in _lib._bullets([], "fallback")


def test_render_helpers_and_repo_root(tmp_path: Path) -> None:
    data = _lib.normalize_payload(
        {
            "meta": {"slug": "x", "name": "N", "description": "D"},
            "master": {"display_name": "M"},
            "memory": {"core_values": ["a"]},
            "persona": {"l1_hard_rules": ["b"]},
        }
    )
    assert "Persona Skill" in _lib.render_skill_md(data)
    assert "## Memory" in _lib.render_wiki_md(data)

    api_dir = tmp_path / "a" / "b" / "api"
    api_dir.mkdir(parents=True)
    api_file = api_dir / "generate.py"
    api_file.write_text("# x\n", encoding="utf-8")
    root = tmp_path / "a"
    (root / "tools").mkdir(parents=True)
    (root / "tools" / "skill_writer.py").write_text("# x\n", encoding="utf-8")
    assert _lib.repo_root_from_api_file(api_file) == root.resolve()

