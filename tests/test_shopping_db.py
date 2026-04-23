from datetime import datetime, timedelta

from shopping_app.db import ShoppingRepository
from shopping_app.models import Marketplace, ProductCandidate


def test_recommend_select_reject_and_history(tmp_path):
    repo = ShoppingRepository(db_path=str(tmp_path / "shopping.db"))
    session_id = "session-1"
    items = [
        ProductCandidate(
            platform=Marketplace.AMAZON,
            title="Item A",
            url="https://www.amazon.com/a",
            item_price=10.0,
            shipping_cost=2.0,
            total_cost=12.0,
            source_query="desk lamp",
        ),
        ProductCandidate(
            platform=Marketplace.WALMART,
            title="Item B",
            url="https://www.walmart.com/b",
            item_price=8.0,
            shipping_cost=3.0,
            total_cost=11.0,
            source_query="desk lamp",
        ),
    ]

    repo.save_recommendations(session_id, "desk lamp", items)
    recommendations = repo.list_recommendations(session_id)
    assert len(recommendations) == 2

    repo.select_item(int(recommendations[0]["id"]))
    selected = repo.get_selected_items(session_id)
    assert len(selected) == 1

    repo.reject_item(int(recommendations[1]["id"]))
    active = repo.list_active_items(session_id)
    assert len(active) == 1

    repo.mark_added_to_platform([int(selected[0]["id"])])
    history = repo.list_history(session_id)
    assert len(history) == 1
    assert history[0]["status"] == "added_to_platform"


def test_purge_candidates_scoped_to_session(tmp_path):
    repo = ShoppingRepository(db_path=str(tmp_path / "shopping.db"))
    session_id = "session-2"
    item = ProductCandidate(
        platform=Marketplace.TARGET,
        title="Item C",
        url="https://www.target.com/p/c",
        item_price=5.0,
        shipping_cost=0.0,
        total_cost=5.0,
        source_query="snack",
    )
    repo.save_recommendations(session_id, "snack", [item])
    rec = repo.list_recommendations(session_id)[0]
    repo.select_item(int(rec["id"]))
    repo.mark_added_to_platform([int(rec["id"])])

    with repo.connect() as conn:
        conn.execute(
            "UPDATE cart_items SET platform_added_date = ? WHERE id = ?",
            ((datetime.utcnow() - timedelta(days=90)).isoformat(), rec["id"]),
        )

    assert repo.count_purge_candidates(60, session_id=session_id) == 1
    deleted = repo.purge_history(session_id, 60)
    assert deleted == 1
    assert repo.list_history(session_id) == []
