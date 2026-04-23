from __future__ import annotations

from urllib.parse import urlparse

from shopping_app.models import Marketplace


DISALLOWED_PURCHASE_TERMS = {
    "checkout",
    "pay now",
    "place order",
    "purchase",
    "buy now",
    "complete order",
}

ALLOWED_DOMAINS = {
    Marketplace.AMAZON: "amazon.com",
    Marketplace.WALMART: "walmart.com",
    Marketplace.COSTCO: "costco.com",
    Marketplace.TARGET: "target.com",
}


def ensure_no_purchase_intent(text: str) -> None:
    lowered = text.lower()
    if any(term in lowered for term in DISALLOWED_PURCHASE_TERMS):
        raise ValueError("Purchase and checkout actions are not allowed.")


def ensure_allowed_domain(url: str, platform: Marketplace) -> None:
    hostname = urlparse(url).hostname or ""
    if ALLOWED_DOMAINS[platform] not in hostname:
        raise ValueError(f"Unsafe or unsupported URL for {platform.value}: {url}")


def sanitize_query(query: str) -> str:
    ensure_no_purchase_intent(query)
    cleaned = " ".join(query.split())
    if not cleaned:
        raise ValueError("Search query cannot be empty.")
    return cleaned


def ensure_safe_history_purge(confirm: bool) -> None:
    if not confirm:
        raise ValueError("History purge requires human confirmation.")
