"""Safe, pure admission gate for Hotmart catalog candidates (no network or publishing)."""
from urllib.parse import urlparse
from decimal import Decimal, InvalidOperation

def evaluate(candidate):
    """Return an explainable decision; fail closed on missing evidence."""
    reasons = []
    if candidate.get("affiliate_status") != "approved":
        reasons.append("affiliate_not_verified")
    if candidate.get("ownership_verified") is not True:
        reasons.append("hotlink_ownership_unverified")
    url = str(candidate.get("hotlink") or "")
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.hostname not in {"go.hotmart.com", "hotm.art"} or not parsed.path.strip("/"):
        reasons.append("invalid_hotlink")
    try:
        commission = Decimal(str(candidate["commission_rate_percent"]))
        if not commission.is_finite() or commission < 20 or commission > 100:
            reasons.append("commission_out_of_policy")
    except (KeyError, TypeError, InvalidOperation):
        reasons.append("commission_unknown")
    if candidate.get("producer_rules_checked") is not True:
        reasons.append("producer_rules_unchecked")
    if candidate.get("destination_verified") is not True:
        reasons.append("destination_unverified")
    if candidate.get("market") != "BR":
        reasons.append("market_not_yet_enabled")
    if candidate.get("channel_authorized") is not True:
        reasons.append("channel_not_authorized")
    if candidate.get("campaign_policy_checked") is not True:
        reasons.append("campaign_policy_unchecked")
    return {"eligible": not reasons, "reasons": reasons, "publication_enabled": False,
            "next_state": "READY_FOR_REVIEW" if not reasons else "BLOCKED"}

def classify_batch(candidates):
    return [dict(product_id=c.get("product_id"), **evaluate(c)) for c in candidates]
