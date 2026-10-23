"""P0: zero-valued INT.1/INT.2 public-signal rankings are not eligible."""
from dataclasses import dataclass
import unittest
from wero1divulgacao.intent import rank_offers

@dataclass(frozen=True)
class Offer:
    id: int
    title: str
    approved: bool = True
    active: bool = True
    affiliate_authorized: bool = True

class TestIntentBothPositive(unittest.TestCase):
    def test_no_trend_signal_excludes_offer(self):
        self.assertEqual(rank_offers([Offer(1, "Notebook Gamer")], ["notebook"], []), [])

    def test_no_search_signal_excludes_offer(self):
        self.assertEqual(rank_offers([Offer(1, "Notebook Gamer")], [], ["gamer"]), [])

    def test_both_positive_includes_offer(self):
        result = rank_offers([Offer(1, "Notebook Gamer")], ["notebook"], ["gamer"])
        self.assertEqual(len(result), 1)
        self.assertGreater(result[0]["tag1_score"], 0)
        self.assertGreater(result[0]["tag2_score"], 0)

    def test_unapproved_excluded(self):
        self.assertEqual(rank_offers([Offer(1, "Notebook Gamer", approved=False)], ["notebook"], ["gamer"]), [])

    def test_unauthorized_excluded(self):
        self.assertEqual(rank_offers([Offer(1, "Notebook Gamer", affiliate_authorized=False)], ["notebook"], ["gamer"]), [])

if __name__ == "__main__":
    unittest.main()
