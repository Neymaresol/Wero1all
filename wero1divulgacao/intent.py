"""Regras de intenção para campanhas orgânicas; sem coleta de buscas privadas."""
import re
from collections import Counter

STOPWORDS = frozenset("de da do para com uma um os as no na em por e ou".split())

def tokens(text):
    return set(t for t in re.findall(r"[a-z0-9]+", text.casefold()) if len(t)>2 and t not in STOPWORDS)

def rank_offers(offers, public_queries, trending_topics, limit=10):
    """Ordena ofertas já aprovadas; dados devem vir de fontes públicas/autorizadas."""
    if not 1 <= limit <= 1000:
        raise ValueError("limit out of range")
    search = Counter(t for q in public_queries[:100] for t in tokens(q))
    trend = Counter(t for q in trending_topics[:100] for t in tokens(q))
    ranked=[]
    for o in offers:
        if not (o.approved and o.active and o.affiliate_authorized):
            continue
        words=tokens(o.title)
        tag1=sum(search[t] for t in words)
        tag2=sum(trend[t] for t in words)
        ranked.append({"offer_id":o.id,"title":o.title,"tag1_score":tag1,
                       "tag2_score":tag2,"total_score":tag1+tag2})
    return sorted(ranked,key=lambda x:(-x["total_score"],x["offer_id"]))[:limit]
