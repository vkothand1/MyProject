from __future__ import annotations

from dataclasses import dataclass

from shopping_app.db import ShoppingRepository
from shopping_app.guardrails import ensure_no_purchase_intent


@dataclass
class ShoppingAssistant:
    repository: ShoppingRepository

    def add_selected_items(self, session_id: str) -> list[str]:
        selected_rows = self.repository.get_selected_items(session_id)
        if not selected_rows:
            return []

        statuses: list[str] = []
        for row in selected_rows:
            ensure_no_purchase_intent(row["title"])
            self.repository.mark_added_to_platform([int(row["id"])])
            statuses.append(
                f"Marked '{row['title']}' as added to {row['platform']} cart"
            )
        return statuses
