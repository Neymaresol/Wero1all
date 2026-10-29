"""Planejador pai-filhos de campanhas; não publica nem simula vendas."""
from dataclasses import dataclass
from urllib.parse import urlencode
from typing import Iterable

MAX_CHILDREN = 1000
ALLOWED_CHANNELS = ("facebook", "instagram", "tiktok")
ALLOWED_TAGS = ("tag1_search", "tag2_creators")

@dataclass(frozen=True)
class Offer:
    id: int
    title: str
    approved: bool
    active: bool
    affiliate_authorized: bool

def plan(offers: Iterable[Offer], *, campaign: str, channels=ALLOWED_CHANNELS,
         tags=ALLOWED_TAGS, limit: int = 10, base_url="https://wero1mercados.onrender.com"):
    """Retorna tarefas propostas; execução externa exige validação e autorização."""
    if not 1 <= limit <= MAX_CHILDREN:
        raise ValueError("limit must be between 1 and 1000")
    # Wero1Mercados safe_campaign() silently drops non-ASCII or >80-char labels.
    # Reject them here so planned links never appear attributed when they are not.
    if (not isinstance(campaign, str) or not 1 <= len(campaign) <= 80
            or not campaign.isascii()
            or not campaign.replace("-", "").replace("_", "").isalnum()):
        raise ValueError("invalid campaign")
    if any(ch not in ALLOWED_CHANNELS for ch in channels):
        raise ValueError("unsupported channel")
    if any(tag not in ALLOWED_TAGS for tag in tags):
        raise ValueError("unsupported tag")
    tasks = []
    for offer in offers:
        if not (offer.approved and offer.active and offer.affiliate_authorized and offer.id > 0):
            continue
        for tag in tags:
            for channel in channels:
                if len(tasks) >= limit:
                    return tasks
                task_id = f"{campaign}:{offer.id}:{tag}:{channel}"
                query = urlencode({"channel": channel, "campaign": campaign, "strategy": tag,
                                   "task_id": task_id})
                tasks.append({"task_id": task_id, "parent": campaign, "offer_id": offer.id,
                              "title": offer.title, "tag": tag, "channel": channel,
                              "url": f"{base_url}/go/{offer.id}?{query}",
                              "state": "proposed", "published": False,
                              "clicks": None, "sales_confirmed": None})
    return tasks
