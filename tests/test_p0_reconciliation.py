import sqlite3
import tempfile
import unittest
from pathlib import Path
from p0_reconciliation import sqlite_inventory, compare, TABLES

class ReconciliationTests(unittest.TestCase):
    def test_missing_source_does_not_create_database(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "missing.db"
            with self.assertRaises(FileNotFoundError):
                sqlite_inventory(path)
            self.assertFalse(path.exists())

    def test_read_only_inventory_and_missing_tables(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "source.db"
            with sqlite3.connect(path) as conn:
                conn.execute("CREATE TABLE offers (id INTEGER PRIMARY KEY)")
                conn.execute("INSERT INTO offers DEFAULT VALUES")
            before = path.read_bytes()
            result = sqlite_inventory(path)
            self.assertEqual(result["offers"], 1)
            self.assertIsNone(result["catalog_products"])
            self.assertEqual(before, path.read_bytes())

    def test_missing_neon_table_is_not_a_match(self):
        local = {name: 0 for name in TABLES}
        remote = dict(local, offers=None)
        self.assertFalse(compare(local, remote)["offers"]["match"])
        self.assertTrue(compare(local, remote)["events"]["match"])

    def test_differences_are_visible(self):
        self.assertFalse(compare({"offers": 4}, {"offers": 0})["offers"]["match"])

if __name__ == "__main__":
    unittest.main()
