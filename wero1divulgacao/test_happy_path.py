from wero1divulgacao.happy_path import simulate_happy_path

def test_happy_path_is_simulation_only():
    result = simulate_happy_path()
    assert result["simulation"] is True
    assert result["real_sales_created"] == 0
    assert result["real_transfers_created"] == 0
    assert result["example_commission_brl"] == 5.0
    assert [e["stage"] for e in result["events"]][:2] == ["INT.1", "INT.2"]
    assert result["events"][-1]["status"] == "simulation_only"
