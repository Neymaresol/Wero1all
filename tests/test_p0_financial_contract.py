"""Financial metrics must not imply unverified provider reconciliation."""
from pathlib import Path
s=(Path(__file__).resolve().parents[1]/"main.py").read_text()
def test_sales_filter_and_source_disclosure():
    assert "confirmed=1 AND reversed=0 AND is_test=0" in s
    assert '"financial_source":"local_sqlite"' in s
    assert '"partner_reconciliation":"not_verified_by_this_endpoint"' in s
