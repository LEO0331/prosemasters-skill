from __future__ import annotations

import json
from pathlib import Path

import biography_mapper


def test_parse_txt_and_csv(tmp_path: Path) -> None:
    txt = tmp_path / "bio.txt"
    txt.write_text("803,潮州,被貶\n819,長安,召還\nbad line", encoding="utf-8")
    events_txt = biography_mapper.parse_txt(txt)
    assert len(events_txt) == 2
    assert events_txt[0]["place"] == "潮州"

    csvf = tmp_path / "bio.csv"
    csvf.write_text("date,place,event\n803,潮州,被貶\n819,長安,召還\n", encoding="utf-8")
    events_csv = biography_mapper.parse_csv(csvf)
    assert len(events_csv) == 2
    assert events_csv[1]["date"] == "819"


def test_main_outputs_sorted_timeline(tmp_path: Path, monkeypatch) -> None:
    csvf = tmp_path / "bio.csv"
    out = tmp_path / "out.json"
    csvf.write_text("date,place,event\n819,長安,召還\n803,潮州,被貶\n", encoding="utf-8")

    monkeypatch.setattr("sys.argv", ["biography_mapper.py", str(csvf), "-o", str(out)])
    rc = biography_mapper.main()
    assert rc == 0
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["timeline"][0]["date"] == "803"
    assert payload["geography_path"] == ["潮州", "長安"]


def test_main_stdout_and_missing_input(tmp_path: Path, monkeypatch, capsys) -> None:
    txt = tmp_path / "bio.txt"
    txt.write_text("803,潮州,被貶", encoding="utf-8")
    monkeypatch.setattr("sys.argv", ["biography_mapper.py", str(txt)])
    assert biography_mapper.main() == 0
    assert '"event_count": 1' in capsys.readouterr().out

    monkeypatch.setattr("sys.argv", ["biography_mapper.py", str(tmp_path / "missing.txt")])
    assert biography_mapper.main() == 1
    assert "input does not exist" in capsys.readouterr().err
