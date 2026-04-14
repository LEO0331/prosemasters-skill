from __future__ import annotations

import json
import tarfile
from pathlib import Path

import version_manager


def _set_paths(base: Path) -> tuple[Path, Path]:
    masters = base / "masters"
    backups = base / ".backups"
    masters.mkdir(parents=True, exist_ok=True)
    backups.mkdir(parents=True, exist_ok=True)
    version_manager.MASTERS = masters
    version_manager.BACKUPS = backups
    return masters, backups


def test_validate_slug_and_safe_child(tmp_path: Path) -> None:
    _set_paths(tmp_path)
    assert version_manager.validate_slug("su-shi") == "su-shi"
    try:
        version_manager.validate_slug("../bad")
        assert False, "expected RuntimeError"
    except RuntimeError as exc:
        assert "invalid slug" in str(exc)

    good = version_manager.safe_child(tmp_path, "a")
    assert good == (tmp_path / "a").resolve()
    try:
        version_manager.safe_child(tmp_path, "../escape")
        assert False, "expected RuntimeError"
    except RuntimeError as exc:
        assert "unsafe path escape attempt" in str(exc)


def test_validate_members_rejects_unsafe(tmp_path: Path) -> None:
    members: list[tarfile.TarInfo] = []
    file_member = tarfile.TarInfo("ok/file.txt")
    file_member.size = 1
    members.append(file_member)
    dir_member = tarfile.TarInfo("ok")
    dir_member.type = tarfile.DIRTYPE
    members.append(dir_member)
    version_manager._validate_members(members, tmp_path)

    bad_link = tarfile.TarInfo("bad")
    bad_link.type = tarfile.SYMTYPE
    try:
        version_manager._validate_members([bad_link], tmp_path)
        assert False, "expected RuntimeError"
    except RuntimeError as exc:
        assert "disallowed link member" in str(exc)

    bad_escape = tarfile.TarInfo("../escape.txt")
    try:
        version_manager._validate_members([bad_escape], tmp_path)
        assert False, "expected RuntimeError"
    except RuntimeError as exc:
        assert "unsafe archive member path" in str(exc)


def test_backup_status_and_rollback_flow(tmp_path: Path) -> None:
    masters, _ = _set_paths(tmp_path)
    master = masters / "han-yu"
    master.mkdir(parents=True)
    (master / "self.md").write_text("v1", encoding="utf-8")

    b = version_manager.backup("han-yu")
    assert b["action"] == "backup"
    archive = Path(b["archive"])
    assert archive.exists()

    st = version_manager.status("han-yu")
    assert st["backup_count"] == 1

    (master / "self.md").write_text("mutated", encoding="utf-8")
    rb = version_manager.rollback("han-yu", str(archive))
    assert rb["action"] == "rollback"
    assert (master / "self.md").read_text(encoding="utf-8") == "v1"


def test_backup_and_rollback_errors(tmp_path: Path) -> None:
    masters, backups = _set_paths(tmp_path)
    try:
        version_manager.backup("missing")
        assert False, "expected RuntimeError"
    except RuntimeError as exc:
        assert "master not found" in str(exc)

    external = tmp_path / "external.tar.gz"
    with tarfile.open(external, "w:gz") as tar:
        f = tmp_path / "x.txt"
        f.write_text("x", encoding="utf-8")
        tar.add(f, arcname="han-yu/x.txt")

    (masters / "han-yu").mkdir(parents=True)
    try:
        version_manager.rollback("han-yu", str(external))
        assert False, "expected RuntimeError"
    except RuntimeError as exc:
        assert "untrusted archive path" in str(exc)

    r = version_manager.rollback("han-yu", str(external), allow_external_archive=True)
    assert r["action"] == "rollback"


def test_main_actions(monkeypatch, capsys, tmp_path: Path) -> None:
    masters, _ = _set_paths(tmp_path)
    (masters / "su-shi").mkdir(parents=True)
    (masters / "su-shi" / "self.md").write_text("x", encoding="utf-8")

    monkeypatch.setattr("sys.argv", ["version_manager.py", "--action", "backup", "--slug", "su-shi"])
    assert version_manager.main() == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["action"] == "backup"

    monkeypatch.setattr("sys.argv", ["version_manager.py", "--action", "rollback", "--slug", "su-shi"])
    assert version_manager.main() == 1
    assert "--archive is required" in capsys.readouterr().err

