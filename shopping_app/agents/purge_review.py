from __future__ import annotations

from dataclasses import dataclass

from shopping_app.db import ShoppingRepository
from shopping_app.guardrails import ensure_safe_history_purge


@dataclass
class PurgeReviewAgent:
    repository: ShoppingRepository

    def preview(self, session_id: str, cutoff_days: int) -> int:
        return self.repository.count_purge_candidates(cutoff_days, session_id=session_id)

    def purge(self, session_id: str, cutoff_days: int, confirm: bool) -> int:
        ensure_safe_history_purge(confirm)
        return self.repository.purge_history(session_id, cutoff_days)
