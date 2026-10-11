"""Descoberta segura e paginada de produtos para o ecossistema PARADIGMA.

Não publica ofertas, não inventa HotLinks e não acessa parceiros sem credenciais.
"""
from urllib.parse import urlparse

def scan_authorized_pages(fetch_page, partner, allowed_hosts, max_pages=10):
    if not 1 <= max_pages <= 100:
        raise ValueError("max_pages inválido")
    cursor, seen_cursors, seen_products = None, set(), set()
    candidates, rejected = [], 0
    for _ in range(max_pages):
        result = fetch_page(cursor)
        for item in result.get("items", []):
            sku = str(item.get("sku") or "").strip()
            title = str(item.get("title") or "").strip()
            url = str(item.get("affiliate_url") or "").strip()
            parsed = urlparse(url)
            if not sku or not title or parsed.scheme != "https" or (parsed.hostname or "").lower() not in allowed_hosts:
                rejected += 1
                continue
            key = (partner, sku)
            if key not in seen_products:
                candidates.append({"partner": partner, "sku": sku, "title": title,
                                   "affiliate_url": url, "approved": False})
                seen_products.add(key)
        next_cursor = result.get("next_cursor")
        if not next_cursor or next_cursor in seen_cursors:
            break
        seen_cursors.add(next_cursor)
        cursor = next_cursor
    return {"candidates": candidates, "rejected": rejected, "publication_enabled": False}
