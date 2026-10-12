"""Read-only tests: never call click or mutation endpoints."""
import ast
from pathlib import Path
import unittest

SOURCE = Path(__file__).resolve().parents[1] / "main.py"

class CommercialContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = SOURCE.read_text(encoding="utf-8")
        cls.tree = ast.parse(cls.source)

    def test_commercial_routes_exist(self):
        for route in ("/api/catalog", "/api/status", "/api/commercial", "/api/p0/readiness"):
            with self.subTest(route=route):
                self.assertIn(repr(route), self.source)

    def test_financial_ledger_has_confirmation_flags(self):
        for field in ("confirmed", "is_test", "reversed"):
            self.assertIn(field, self.source)

    def test_source_is_valid_python(self):
        self.assertIsInstance(self.tree, ast.Module)

if __name__ == "__main__":
    unittest.main()
