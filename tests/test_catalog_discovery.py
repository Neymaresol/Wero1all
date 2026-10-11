from catalog_discovery import scan_authorized_pages

def test_two_pages_and_rejected_domain():
    pages = {
        None: {"items": [{"sku": "A", "title": "A", "affiliate_url": "https://go.hotmart.com/A"},
                         {"sku": "A", "title": "A", "affiliate_url": "https://go.hotmart.com/A"},
                         {"sku": "X", "title": "X", "affiliate_url": "https://invalid.example/X"}], "next_cursor": "p2"},
        "p2": {"items": [{"sku": "B", "title": "B", "affiliate_url": "https://go.hotmart.com/B"}]}
    }
    result = scan_authorized_pages(lambda cursor: pages[cursor], "partner", {"go.hotmart.com"})
    assert len(result["candidates"]) == 2
    assert result["rejected"] == 1
    assert all(not item["approved"] for item in result["candidates"])
    assert result["publication_enabled"] is False

def test_page_limit():
    try:
        scan_authorized_pages(lambda _: {}, "partner", set(), max_pages=0)
    except ValueError:
        pass
    else:
        raise AssertionError("expected max_pages validation")
