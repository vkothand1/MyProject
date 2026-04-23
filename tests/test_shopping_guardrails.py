import pytest

from shopping_app.guardrails import ensure_allowed_domain, ensure_no_purchase_intent, sanitize_query
from shopping_app.models import Marketplace


def test_sanitize_query_blocks_purchase_terms():
    with pytest.raises(ValueError):
        sanitize_query("buy now checkout this item")


def test_sanitize_query_allows_search():
    assert sanitize_query("wireless keyboard") == "wireless keyboard"


def test_domain_validation():
    ensure_allowed_domain("https://www.amazon.com/dp/test", Marketplace.AMAZON)
    with pytest.raises(ValueError):
        ensure_allowed_domain("https://evil.example.com", Marketplace.AMAZON)
