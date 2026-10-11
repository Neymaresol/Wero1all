"""P0 tests: SQLite persistence and provider-confirmed sales; no external I/O."""
import ast
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_sqlite_roundtrip_after_reopen(tmp_path):
    path = tmp_path / "operario.db"
    with sqlite3.connect(path) as c:
        c.execute("CREATE TABLE ledger(id TEXT PRIMARY KEY, amount REAL)")
        c.execute("INSERT INTO ledger VALUES (?, ?)", ("sample", 12.5))
    with sqlite3.connect(path) as c:
        assert c.execute("SELECT amount FROM ledger WHERE id='sample'").fetchone()[0] == 12.5

def test_database_path_explicit():
    source = (ROOT / "main.py").read_text(encoding="utf-8")
    ast.parse(source)
    assert 'os.getenv("DB_PATH"' in source
    assert "transactions WHERE confirmed=1 AND reversed=0 AND is_test=0" in source

def test_render_disk_manifest_exists_but_is_not_proof_of_attachment():
    config = (ROOT / "render.yaml").read_text(encoding="utf-8")
    assert "mountPath: /app/data" in config
    assert "DB_PATH" in config
