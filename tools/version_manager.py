#!/usr/bin/env python3
"""Backup and rollback manager for distilled master versions."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import tarfile
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MASTERS = ROOT / "masters"
BACKUPS = ROOT / ".backups"
SLUG_RE = re.compile(r"^[a-z0-9-]+$")


def ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def validate_slug(slug: str) -> str:
    if not SLUG_RE.fullmatch(slug):
        raise RuntimeError("invalid slug: use lowercase letters, digits, and hyphens only")
    return slug


def safe_child(base: Path, name: str) -> Path:
    candidate = (base / name).resolve()
    base_resolved = base.resolve()
    try:
        candidate.relative_to(base_resolved)
    except ValueError:
        raise RuntimeError(f"unsafe path escape attempt: {name}")
    return candidate


def master_dir(slug: str) -> Path:
    return safe_child(MASTERS, slug)


def backup_dir(slug: str) -> Path:
    return safe_child(BACKUPS, slug)


def backup(slug: str) -> dict:
    slug = validate_slug(slug)
    src = master_dir(slug)
    if not src.exists():
        raise RuntimeError(f"master not found: {slug}")
    out_dir = backup_dir(slug)
    out_dir.mkdir(parents=True, exist_ok=True)
    tar_path = out_dir / f"{ts()}.tar.gz"
    with tarfile.open(tar_path, "w:gz") as tar:
        tar.add(src, arcname=slug)
    return {"action": "backup", "slug": slug, "archive": str(tar_path)}


def _validate_members(members: list[tarfile.TarInfo], target_root: Path) -> None:
    base = target_root.resolve()
    for member in members:
        if member.issym() or member.islnk():
            raise RuntimeError(f"archive contains disallowed link member: {member.name}")
        if not (member.isfile() or member.isdir()):
            raise RuntimeError(f"archive contains disallowed member type: {member.name}")
        dest = (base / member.name).resolve()
        try:
            dest.relative_to(base)
        except ValueError:
            raise RuntimeError(f"unsafe archive member path: {member.name}")


def rollback(slug: str, archive: str, allow_external_archive: bool = False) -> dict:
    slug = validate_slug(slug)
    archive_path = Path(archive)
    if not archive_path.exists():
        raise RuntimeError(f"archive not found: {archive_path}")
    if not allow_external_archive:
        trusted_root = backup_dir(slug)
        archive_resolved = archive_path.resolve()
        try:
            archive_resolved.relative_to(trusted_root)
        except ValueError:
            raise RuntimeError(
                "untrusted archive path: only .backups/{slug}/ is allowed "
                "(use --allow-external-archive to override)"
            )

    target = master_dir(slug)
    if target.exists():
        shutil.rmtree(target)

    with tarfile.open(archive_path, "r:gz") as tar:
        members = tar.getmembers()
        _validate_members(members, MASTERS)
        tar.extractall(MASTERS, members=members)

    return {"action": "rollback", "slug": slug, "restored_from": str(archive_path)}


def status(slug: str) -> dict:
    slug = validate_slug(slug)
    d = backup_dir(slug)
    archives = sorted([str(p) for p in d.glob("*.tar.gz")]) if d.exists() else []
    return {"action": "status", "slug": slug, "backup_count": len(archives), "archives": archives}


def main() -> int:
    ap = argparse.ArgumentParser(description="Manage backups for distilled masters")
    ap.add_argument("--action", required=True, choices=["backup", "rollback", "status"])
    ap.add_argument("--slug", required=True)
    ap.add_argument("--archive", help="Archive path for rollback")
    ap.add_argument(
        "--allow-external-archive",
        action="store_true",
        help="Allow rollback from archive paths outside .backups/{slug}/",
    )
    args = ap.parse_args()

    try:
        if args.action == "backup":
            result = backup(args.slug)
        elif args.action == "rollback":
            if not args.archive:
                raise RuntimeError("--archive is required for rollback")
            result = rollback(args.slug, args.archive, allow_external_archive=args.allow_external_archive)
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
