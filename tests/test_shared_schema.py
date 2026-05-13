from __future__ import annotations

import json
from pathlib import Path


def test_shared_schema_matches_runtime_shape() -> None:
    schema_path = Path(__file__).resolve().parents[1] / "apps" / "master-persona-builder" / "shared" / "schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))

    assert schema["properties"]["meta"]["required"] == ["slug", "name", "description"]
    assert "memory" in schema["properties"]
    assert "persona" in schema["properties"]
    categories = schema["properties"]["source_materials"]["items"]["properties"]["category"]["enum"]
    assert categories == ["works", "criticism", "letters", "biography", "citation"]
