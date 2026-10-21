import unittest
from hotmart_catalog_gate import evaluate, classify_batch

class TestHotmartGate(unittest.TestCase):
    def base(self):
        return dict(product_id="951961", affiliate_status="approved",
                    ownership_verified=True, hotlink="https://go.hotmart.com/G108129576P",
                    commission_rate_percent=38, producer_rules_checked=True,
                    destination_verified=True, market="BR", channel_authorized=True,
                    campaign_policy_checked=True)
    def test_valid_is_review_only(self):
        d=evaluate(self.base())
        self.assertTrue(d["eligible"])
        self.assertEqual(d["next_state"],"READY_FOR_REVIEW")
        self.assertFalse(d["publication_enabled"])
    def test_unknown_ownership_blocks(self):
        c=self.base(); c["ownership_verified"]=False
        self.assertIn("hotlink_ownership_unverified",evaluate(c)["reasons"])
    def test_below_20_blocks(self):
        c=self.base(); c["commission_rate_percent"]=19
        self.assertIn("commission_out_of_policy",evaluate(c)["reasons"])
    def test_unapproved_blocks(self):
        c=self.base(); c["affiliate_status"]="pending"
        self.assertFalse(evaluate(c)["eligible"])
    def test_external_url_blocks(self):
        c=self.base(); c["hotlink"]="https://example.com/path"
        self.assertIn("invalid_hotlink",evaluate(c)["reasons"])
    def test_non_br_blocks(self):
        c=self.base(); c["market"]="US"
        self.assertIn("market_not_yet_enabled",evaluate(c)["reasons"])
    def test_batch(self):
        self.assertEqual(len(classify_batch([self.base(),{}])),2)

if __name__=="__main__":
    unittest.main()
