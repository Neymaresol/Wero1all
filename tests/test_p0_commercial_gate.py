import unittest
from datetime import datetime, timezone
from p0_commercial_gate import readiness

class CommercialGateTests(unittest.TestCase):
    def test_empty_catalog_is_not_ready(self):
        counts = dict(offers=0, catalog_products=0, campaign_clicks=0, transactions=0)
        self.assertFalse(readiness(counts, counts)["ready"])
    def test_sqlite_neon_divergence_blocks_go(self):
        a = dict(offers=4, catalog_products=2, campaign_clicks=0, transactions=0)
        b = dict(offers=0, catalog_products=0, campaign_clicks=0, transactions=0)
        result = readiness(a, b)
        self.assertFalse(result["ready"])
        self.assertIn("offers", result["differences"])
    def test_missing_heartbeat_blocks_go(self):
        counts = dict(offers=1, catalog_products=1, campaign_clicks=0, transactions=0)
        self.assertFalse(readiness(counts, counts)["heartbeat_fresh"])
    def test_no_synthetic_financial_confirmation(self):
        counts = dict(offers=1, catalog_products=1, campaign_clicks=0, transactions=0)
        result = readiness(counts, counts, datetime.now(timezone.utc).isoformat())
        self.assertIsNone(result["sales_confirmed"])
        self.assertIsNone(result["commission_confirmed"])
if __name__ == "__main__":
    unittest.main()
