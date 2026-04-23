from shopping_app.graph.workflow import ShoppingGraphService


class DummyRecommender:
    def recommend(self, query, session_id):
        from shopping_app.models import Marketplace, ProductCandidate, RecommendationResponse

        return RecommendationResponse(
            query=query,
            recommendations=[
                ProductCandidate(
                    platform=Marketplace.AMAZON,
                    title="Item A",
                    url="https://www.amazon.com/a",
                    item_price=10.0,
                    shipping_cost=2.0,
                    total_cost=12.0,
                ),
                ProductCandidate(
                    platform=Marketplace.WALMART,
                    title="Item B",
                    url="https://www.walmart.com/b",
                    item_price=8.0,
                    shipping_cost=1.0,
                    total_cost=9.0,
                ),
            ],
            message="ok",
        )


class DummyAssistant:
    def add_selected_items(self, session_id):
        return ["Added to amazon cart"]


class DummyPurgeAgent:
    def preview(self, session_id, cutoff_days):
        return 2

    def purge(self, session_id, cutoff_days, confirm):
        return 2


def test_workflow_add_and_purge(monkeypatch, tmp_path):
    service = ShoppingGraphService.__new__(ShoppingGraphService)
    service.repository = None
    service.recommender = DummyRecommender()
    service.assistant = DummyAssistant()
    service.purge_agent = DummyPurgeAgent()
    result = service._recommend_node({"query": "desk lamp", "session_id": "session-4"})
    assert len(result["recommendations"]) == 2

    add_result = service._add_node({"session_id": "session-4"})
    assert "statuses" in add_result

    purge_result = service._purge_node({"session_id": "session-4", "cutoff_days": 60, "confirm": False})
    assert purge_result["purge_count"] == 2
