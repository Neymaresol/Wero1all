"""P0 commercial source-of-truth gate; never treats SQLite-only offers as Neon-confirmed."""
from dataclasses import dataclass

@dataclass(frozen=True)
class CommercialGate:
    ready: bool
    reason: str
    verified_offers: int

def evaluate_commercial_gate(sqlite_active: int, neon_active: int, neon_https_links: int, neon_catalog: int) -> CommercialGate:
    """Fail closed when authoritative persistent catalogue is empty or inconsistent."""
    values = (sqlite_active, neon_active, neon_https_links, neon_catalog)
    if any(not isinstance(v, int) or isinstance(v, bool) or v < 0 for v in values):
        return CommercialGate(False, "INVALID_METRICS", 0)
    if neon_catalog == 0 or neon_active == 0:
        return CommercialGate(False, "PERSISTENT_CATALOG_EMPTY", 0)
    if neon_https_links != neon_active:
        return CommercialGate(False, "UNVERIFIED_AFFILIATE_LINKS", 0)
    if sqlite_active != neon_active:
        return CommercialGate(False, "SQLITE_NEON_DIVERGENCE", 0)
    return CommercialGate(True, "VERIFIED", neon_active)
