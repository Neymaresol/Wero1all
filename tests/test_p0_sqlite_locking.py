"""P0 regression: SQLite path and busy timeout configuration, offline."""
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def test_db_directory_and_lock_timeout():
    source=(ROOT/"main.py").read_text(encoding="utf-8")
    assert "os.path.dirname(os.path.abspath(DB))" in source
    assert "sqlite3.connect(DB, timeout=15)" in source
    assert 'PRAGMA busy_timeout=15000' in source
