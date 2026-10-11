"""Consistent SQLite backup; run manually only after verifying the mounted volume.

Usage: python scripts/backup_sqlite.py /app/data/wero1.db /secure/backups/wero1-UTC.db
Never write backups into the repository or overwrite an existing backup.
"""
import hashlib
import json
import sqlite3
import sys
from pathlib import Path


def backup(source: Path, target: Path) -> dict:
    source, target = source.resolve(), target.resolve()
    if source == target or not source.is_file() or target.exists():
        raise ValueError("Source must exist; destination must be new and different")
    if not target.parent.is_dir():
        raise ValueError("Backup directory must already exist")
    source_uri = source.as_uri() + "?mode=ro"
    try:
        with sqlite3.connect(source_uri, uri=True) as src:
            with sqlite3.connect(str(target)) as dst:
                src.backup(dst)
        with sqlite3.connect(f"file:{target}?mode=ro", uri=True) as check:
            integrity = check.execute("PRAGMA integrity_check").fetchone()[0]
        if integrity != "ok":
            raise RuntimeError("Backup integrity failed")
        digest = hashlib.sha256(target.read_bytes()).hexdigest()
        return {"backup_file": str(target), "sha256": digest, "integrity": integrity}
    except Exception:
        target.unlink(missing_ok=True)
        raise


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("Usage: backup_sqlite.py SOURCE_DB NEW_BACKUP_PATH")
    print(json.dumps(backup(Path(sys.argv[1]), Path(sys.argv[2]))))
