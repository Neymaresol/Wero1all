"""P0 read-only regression contracts for catalog reconciliation and heartbeat."""
import unittest

def reconcile_counts(sqlite_count, neon_count):
    if sqlite_count < 0 or neon_count < 0:
        raise ValueError("negative count")
    return {"consistent": sqlite_count == neon_count, "publish_allowed": sqlite_count == neon_count and neon_count > 0}

def heartbeat_ok(last_heartbeat, status):
    return bool(last_heartbeat) and status == "ACTIVE"

class P0Contracts(unittest.TestCase):
    def test_empty_catalog_fails_closed(self):
        self.assertFalse(reconcile_counts(0, 0)["publish_allowed"])
    def test_divergence_fails_closed(self):
        self.assertFalse(reconcile_counts(3, 0)["publish_allowed"])
    def test_reconciled_catalog(self):
        self.assertTrue(reconcile_counts(3, 3)["publish_allowed"])
    def test_missing_heartbeat_fails_closed(self):
        self.assertFalse(heartbeat_ok(None, "UNVERIFIED"))
    def test_valid_heartbeat(self):
        self.assertTrue(heartbeat_ok("2026-10-12T12:00:00Z", "ACTIVE"))

if __name__ == "__main__":
    unittest.main()
