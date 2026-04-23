from __future__ import annotations

from typing import TypedDict

from shopping_app.models import ProductCandidate


class ShoppingState(TypedDict, total=False):
    session_id: str
    action: str
    query: str
    selected_item_ids: list[int]
    cutoff_days: int
    confirm: bool
    recommendations: list[ProductCandidate]
    message: str
    purge_count: int
    statuses: list[str]
