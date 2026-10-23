import unittest
from neon_readiness import neon_readiness

class FakeCursor:
    def __init__(self, tables):
        self.tables=tables
        self.sql=""
    def __enter__(self): return self
    def __exit__(self,*args): return False
    def execute(self,sql): self.sql=sql
    def fetchall(self):
        if "information_schema" in self.sql: return [(x,) for x in self.tables]
        return []
    def fetchone(self): return (0,)

class FakeConnection:
    def __init__(self,tables): self.tables=tables; self.rolled_back=False
    def __enter__(self): return self
    def __exit__(self,*args): return False
    def cursor(self): return FakeCursor(self.tables)
    def rollback(self): self.rolled_back=True

class ReadinessTests(unittest.TestCase):
    def test_no_dsn_fails_closed(self):
        r=neon_readiness(dsn="")
        self.assertFalse(r["ready_for_cutover"])
        self.assertFalse(r["configured"])
    def test_invalid_dsn_fails_closed(self):
        self.assertFalse(neon_readiness(dsn="sqlite:///tmp/db")["connected"])
    def test_missing_schema(self):
        c=FakeConnection(["offers"])
        r=neon_readiness(connect=lambda *a,**k:c,dsn="postgresql://test@localhost/db")
        self.assertTrue(r["connected"])
        self.assertIn("transactions",r["missing_tables"])
        self.assertFalse(r["ready_for_cutover"])
        self.assertTrue(c.rolled_back)
    def test_complete_schema_still_requires_migration(self):
        c=FakeConnection(["offers","catalog_products","campaign_clicks","transactions","robot_registry"])
        r=neon_readiness(connect=lambda *a,**k:c,dsn="postgresql://test@localhost/db")
        self.assertTrue(r["schema_complete"])
        self.assertEqual(r["counts"]["offers"],0)
        self.assertFalse(r["ready_for_cutover"])
    def test_no_credentials_leaked(self):
        r=neon_readiness(connect=lambda *a,**k: (_ for _ in ()).throw(RuntimeError("secret")),dsn="postgresql://user:password@localhost/db")
        self.assertNotIn("password",str(r))
if __name__=="__main__": unittest.main()
