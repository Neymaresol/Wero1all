"""Offline Double Check of SQLite backup and restoration."""
import importlib.util
import sqlite3
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "backup_sqlite.py"
spec = importlib.util.spec_from_file_location("backup_sqlite", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_backup_integrity_and_restore(tmp_path):
    src, out = tmp_path / "source.db", tmp_path / "backup.db"
    with sqlite3.connect(src) as c:
        c.execute("CREATE TABLE sales (id TEXT PRIMARY KEY, confirmed INTEGER)")
        c.execute("INSERT INTO sales VALUES ('test-only', 0)")
    result = module.backup(src, out)
    assert result["integrity"] == "ok"
    assert len(result["sha256"]) == 64
    with sqlite3.connect(out) as c:
        assert c.execute("SELECT confirmed FROM sales").fetchone()[0] == 0

def test_backup_never_overwrites(tmp_path):
    src, out = tmp_path / "source.db", tmp_path / "backup.db"
    sqlite3.connect(src).close()
    out.write_text("existing", encoding="utf-8")
    try:
        module.backup(src, out)
    except ValueError:
        pass
    else:
        assert False, "Existing backup must not be overwritten"
    assert out.read_text(encoding="utf-8") == "existing"
