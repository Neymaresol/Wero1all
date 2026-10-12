import unittest
from commercial_reconciliation_gate import evaluate_commercial_gate

class CommercialReconciliationTests(unittest.TestCase):
    def test_empty_neon_blocks(self):
        result = evaluate_commercial_gate(4, 0, 0, 0)
        self.assertFalse(result.ready)
        self.assertEqual(result.reason, "PERSISTENT_CATALOG_EMPTY")
    def test_unverified_links_block(self):
        self.assertEqual(evaluate_commercial_gate(2, 2, 1, 2).reason, "UNVERIFIED_AFFILIATE_LINKS")
    def test_divergence_blocks(self):
        self.assertEqual(evaluate_commercial_gate(4, 2, 2, 2).reason, "SQLITE_NEON_DIVERGENCE")
    def test_matching_verified_inventory(self):
        self.assertTrue(evaluate_commercial_gate(2, 2, 2, 2).ready)
    def test_invalid_metrics_block(self):
        self.assertFalse(evaluate_commercial_gate(-1, 2, 2, 2).ready)

if __name__ == "__main__":
    unittest.main()
