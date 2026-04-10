#!/usr/bin/env python3
"""Backup and rollback manager for distilled master versions."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import tarfile
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MASTERS = ROOT / "masters"
BACKUPS = ROOT / ".backups"


def ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def backup(slug: str) -> dict:
    src = MASTERS / slug
    if not src.exists():
        raise RuntimeError(f"master not found: {slug}")
    out_dir = BACKUPS / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    tar_path = out_dir / f"{ts()}.tar.gz"
    with tarfile.open(tar_path, "w:gz") as tar:
        tar.add(src, arcname=slug)
    return {"action": "backup", "slug": slug, "archive": str(tar_path)}


def _validate_members(members: list[tarfile.TarInfo], target_root: Path) -> None:
    base = target_root.resolve()
    for member in members:
        dest = (base / member.name).resolve()
        if not str(dest).startswith(str(base)):
            raise RuntimeError(f"unsafe archive member path: {member.name}")


def rollback(slug: str, archive: str) -> dict:
    archive_path = Path(archive)
    if not archive_path.exists():
        raise RuntimeError(f"archive not found: {archive_path}")
    target = MASTERS / slug
    if target.exists():
        shutil.rmtree(target)

    with tarfile.open(archive_path, "r:gz") as tar:
        members = tar.getmembers()
        _validate_members(members, MASTERS)
        tar.extractall(MASTERS, members=members)

    return {"action": "rollback", "slug": slug, "restored_from": str(archive_path)}


def status(slug: str) -> dict:
    d = BACKUPS / slug
    archives = sorted([str(p) for p in d.glob("*.tar.gz")]) if d.exists() else []
    return {"action": "status", "slug": slug, "backup_count": len(archives), "archives": archives}


def main() -> int:
    ap = argparse.ArgumentParser(description="Manage backups for distilled masters")
    ap.add_argument("--action", required=True, choices=["backup", "rollback", "status"])
    ap.add_argument("--slug", required=True)
    ap.add_argument("--archive", help="Archive path for rollback")
    args = ap.parse_args()

    try:
        if args.action == "backup":
            result = backup(args.slug)
        elif args.action == "rollback":
            if not args.archive:
                raise RuntimeError("--archive is required for rollback")
            result = rollback(args.slug, args.archive)
        elif args.action == "status":
            result = status(args.slug)
        else:
            raise RuntimeError(f"unsupported action: {args.action}")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
