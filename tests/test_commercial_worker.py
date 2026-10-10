import unittest
from scripts.commercial_worker import plan_campaigns, report

class CommercialWorkerTests(unittest.TestCase):
    def test_deduplicates_and_ignores_inactive(self):
        tasks=plan_campaigns([{"id":3,"active":True},{"id":3,"active":True},{"id":4,"active":False}])
        self.assertEqual(len(tasks),1)
        self.assertEqual(tasks[0].offer_id,3)
        self.assertEqual(report(tasks)["published"],0)
    def test_does_not_publish_unapproved_channel(self):
        self.assertEqual(plan_campaigns([{"id":1,"active":True}],channels=("kwai",)),[])
    def test_bounded(self):
        self.assertEqual(len(plan_campaigns([{"id":i,"active":True} for i in range(1,50)],max_tasks=5)),5)

if __name__=="__main__":
    unittest.main()
