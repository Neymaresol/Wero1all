"""Read-only commercial smoke checks; set WERO_BASE_URL to opt in."""
import json
import os
import unittest
from urllib.request import urlopen

BASE = os.getenv("WERO_BASE_URL", "").rstrip("/")

@unittest.skipUnless(BASE, "WERO_BASE_URL not set: no external calls")
class CommercialReadOnly(unittest.TestCase):
    def get(self, path):
        with urlopen(BASE + path, timeout=15) as response:
            self.assertEqual(response.status, 200)
            return json.load(response)

    def test_catalog_is_json(self):
        self.assertIsInstance(self.get("/api/catalog"), (dict, list))

    def test_status_is_json(self):
        self.assertIsInstance(self.get("/api/status"), dict)

if __name__ == "__main__":
    unittest.main()
