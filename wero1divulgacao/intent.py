"""Classificação de intenção pública para campanhas orgânicas."""
import re
import unicodedata
from collections import Counter

STOPWORDS = frozenset("de da do para com uma um os as no na em por e ou".split())

def tokens(text):
    normalized = unicodedata.normalize("NFKD", text.casefold())
    normalized = "".join(c for c in normalized if not unicodedata.combining(c))
    return set(t for t in re.findall(r"[a-z0-9]+", normalized)
               if len(t) > 2 and t not in STOPWORDS)

def rank_offers(offers, public_queries, trending_topics, limit=10):
    """Ranking consultivo: exige sinais positivos nas duas fontes; não autentica INT.1/INT.2."""
    if not 1 <= limit <= 1000:
        raise ValueError("limit out of range")
    search = Counter(t for q in public_queries[:100] for t in tokens(q))
    trend = Counter(t for q in trending_topics[:100] for t in tokens(q))
    ranked = []
    for offer in offers:
        if not (offer.approved and offer.active and offer.affiliate_authorized and offer.id > 0):
            continue
        words = tokens(offer.title)
        tag1 = sum(search[t] for t in words)
        tag2 = sum(trend[t] for t in words)
        # A soma positiva sozinha permite INT.1 ou INT.2 zerado: fail closed.
        if tag1 <= 0 or tag2 <= 0:
            continue
        ranked.append({"offer_id": offer.id, "title": offer.title,
                       "tag1_score": tag1, "tag2_score": tag2,
                       "total_score": tag1 + tag2})
    return sorted(ranked, key=lambda x: (-x["total_score"], x["offer_id"]))[:limit]
