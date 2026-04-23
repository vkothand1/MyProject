from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from datetime import datetime, timedelta
from pathlib import Path
from typing import Iterable

from shopping_app.config import get_settings
from shopping_app.models import ItemStatus, ProductCandidate


class ShoppingRepository:
    def __init__(self, db_path: str | None = None) -> None:
        self.db_path = Path(db_path or get_settings().shopping_db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_db()

    @contextmanager
    def connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def init_db(self) -> None:
        with self.connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS cart_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    user_query TEXT NOT NULL,
                    platform TEXT NOT NULL,
                    title TEXT NOT NULL,
                    url TEXT NOT NULL,
                    item_price REAL NOT NULL,
                    shipping_cost REAL NOT NULL,
                    total_cost REAL NOT NULL,
                    description TEXT DEFAULT '',
                    source_query TEXT DEFAULT '',
                    list_date TEXT NOT NULL,
                    platform_added_date TEXT,
                    score REAL DEFAULT 0,
                    status TEXT NOT NULL,
                    notes TEXT DEFAULT '',
                    price_verified INTEGER DEFAULT 0,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS purge_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    cutoff_days INTEGER NOT NULL,
                    cutoff_date TEXT NOT NULL,
                    deleted_count INTEGER NOT NULL,
                    decision TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )
            # Migrate existing DBs: add price_verified column if missing
            try:
                conn.execute("ALTER TABLE cart_items ADD COLUMN price_verified INTEGER DEFAULT 0")
            except Exception:
                pass  # column already exists

    def save_recommendations(
        self, session_id: str, user_query: str, items: list[ProductCandidate]
    ) -> list[int]:
        now = datetime.utcnow().isoformat()
        ids: list[int] = []
        with self.connect() as conn:
            for item in items:
                cursor = conn.execute(
                    """
                    INSERT INTO cart_items (
                        session_id, user_query, platform, title, url, item_price,
                        shipping_cost, total_cost, description, source_query,
                        list_date, score, status, notes, price_verified,
                        created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        session_id,
                        user_query,
                        item.platform.value,
                        item.title,
                        item.url,
                        item.item_price,
                        item.shipping_cost,
                        item.total_cost,
                        item.description,
                        item.source_query,
                        item.list_date.isoformat(),
                        item.score,
                        ItemStatus.RECOMMENDED.value,
                        item.notes,
                        1 if item.price_verified else 0,
                        now,
                        now,
                    ),
                )
                ids.append(int(cursor.lastrowid))
        return ids

    def list_recommendations(self, session_id: str | None = None) -> list[dict]:
        query = "SELECT * FROM cart_items WHERE status = ?"
        params: list[object] = [ItemStatus.RECOMMENDED.value]
        if session_id:
            query += " AND session_id = ?"
            params.append(session_id)
        query += " ORDER BY score DESC, total_cost ASC, list_date DESC"
        with self.connect() as conn:
            rows = conn.execute(query, params).fetchall()
        return [dict(row) for row in rows]

    def list_active_items(self, session_id: str | None = None) -> list[dict]:
        query = "SELECT * FROM cart_items WHERE status IN (?, ?)"
        params: list[object] = [ItemStatus.RECOMMENDED.value, ItemStatus.SELECTED.value]
        if session_id:
            query += " AND session_id = ?"
            params.append(session_id)
        query += " ORDER BY created_at DESC"
        with self.connect() as conn:
            rows = conn.execute(query, params).fetchall()
        return [dict(row) for row in rows]

    def list_history(self, session_id: str | None = None) -> list[dict]:
        query = "SELECT * FROM cart_items WHERE status = ?"
        params: list[object] = [ItemStatus.ADDED_TO_PLATFORM.value]
        if session_id:
            query += " AND session_id = ?"
            params.append(session_id)
        query += " ORDER BY platform_added_date DESC, updated_at DESC"
        with self.connect() as conn:
            rows = conn.execute(query, params).fetchall()
        return [dict(row) for row in rows]

    def select_item(self, item_id: int) -> None:
        now = datetime.utcnow().isoformat()
        with self.connect() as conn:
            conn.execute(
                "UPDATE cart_items SET status = ?, updated_at = ? WHERE id = ?",
                (ItemStatus.SELECTED.value, now, item_id),
            )

    def reject_item(self, item_id: int) -> None:
        with self.connect() as conn:
            conn.execute("DELETE FROM cart_items WHERE id = ?", (item_id,))

    def get_selected_items(self, session_id: str) -> list[dict]:
        with self.connect() as conn:
            rows = conn.execute(
                "SELECT * FROM cart_items WHERE session_id = ? AND status = ?",
                (session_id, ItemStatus.SELECTED.value),
            ).fetchall()
        return [dict(row) for row in rows]

    def mark_added_to_platform(self, item_ids: Iterable[int]) -> None:
        now = datetime.utcnow().isoformat()
        with self.connect() as conn:
            for item_id in item_ids:
                conn.execute(
                    """
                    UPDATE cart_items
                    SET status = ?, platform_added_date = ?, updated_at = ?
                    WHERE id = ?
                    """,
                    (ItemStatus.ADDED_TO_PLATFORM.value, now, now, item_id),
                )

    def count_purge_candidates(self, cutoff_days: int, session_id: str | None = None) -> int:
        cutoff_date = (datetime.utcnow() - timedelta(days=cutoff_days)).isoformat()
        query = """
            SELECT COUNT(*) AS count
            FROM cart_items
            WHERE status = ? AND platform_added_date IS NOT NULL AND platform_added_date < ?
        """
        params: list[object] = [ItemStatus.ADDED_TO_PLATFORM.value, cutoff_date]
        if session_id:
            query += " AND session_id = ?"
            params.append(session_id)
        with self.connect() as conn:
            row = conn.execute(query, params).fetchone()
        return int(row["count"] if row else 0)

    def purge_history(self, session_id: str, cutoff_days: int) -> int:
        cutoff_date = (datetime.utcnow() - timedelta(days=cutoff_days)).isoformat()
        now = datetime.utcnow().isoformat()
        with self.connect() as conn:
            rows = conn.execute(
                """
                SELECT id FROM cart_items
                WHERE status = ? AND platform_added_date IS NOT NULL AND platform_added_date < ? AND session_id = ?
                """,
                (ItemStatus.ADDED_TO_PLATFORM.value, cutoff_date, session_id),
            ).fetchall()
            deleted_count = len(rows)
            conn.execute(
                "DELETE FROM cart_items WHERE status = ? AND platform_added_date IS NOT NULL AND platform_added_date < ? AND session_id = ?",
                (ItemStatus.ADDED_TO_PLATFORM.value, cutoff_date, session_id),
            )
            conn.execute(
                """
                INSERT INTO purge_events (
                    session_id, cutoff_days, cutoff_date, deleted_count, decision, created_at
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (session_id, cutoff_days, cutoff_date, deleted_count, "approved", now),
            )
        return deleted_count

    def record_purge_request(self, session_id: str, cutoff_days: int, decision: str) -> None:
        cutoff_date = (datetime.utcnow() - timedelta(days=cutoff_days)).isoformat()
        now = datetime.utcnow().isoformat()
        with self.connect() as conn:
            conn.execute(
                """
                INSERT INTO purge_events (
                    session_id, cutoff_days, cutoff_date, deleted_count, decision, created_at
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (session_id, cutoff_days, cutoff_date, 0, decision, now),
            )
