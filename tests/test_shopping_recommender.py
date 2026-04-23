from shopping_app.agents.recommender import (
    LLMProductCandidate,
    LLMProductSearch,
    RecommendationPick,
    RecommendationPlan,
    ShoppingRecommender,
)
from shopping_app.db import ShoppingRepository
from shopping_app.models import Marketplace, ProductCandidate


class DummyEmbeddings:
    def embed_query(self, text):
        return [1.0, 0.0]

    def embed_documents(self, texts):
        vectors = []
        for text in texts:
            vectors.append([1.0, 0.0] if "Item A" in text else [0.0, 1.0])
        return vectors


class DummyStructuredLLM:
    """Return different structured outputs depending on the schema requested."""

    def invoke(self, prompt):
        # If prompt mentions "ranking" it's the final pick step
        if "ranking" in prompt.lower():
            return RecommendationPlan(
                picks=[
                    RecommendationPick(index=0, reason="best fit"),
                    RecommendationPick(index=1, reason="second best fit"),
                ]
            )
        # Otherwise it's the product search step
        return LLMProductSearch(
            candidates=[
                LLMProductCandidate(
                    platform="amazon",
                    title="Item A - Great Desk Lamp",
                    estimated_price=10.0,
                    shipping_estimate=2.0,
                    description="best desk lamp choice",
                    reason="top rated",
                ),
                LLMProductCandidate(
                    platform="walmart",
                    title="Item B - Budget Desk Lamp",
                    estimated_price=8.0,
                    shipping_estimate=1.0,
                    description="good budget desk lamp",
                    reason="affordable",
                ),
            ],
            search_summary="Found 2 desk lamps",
        )


class DummyLLM:
    def with_structured_output(self, schema):
        return DummyStructuredLLM()


def test_recommender_saves_top_item(monkeypatch, tmp_path):
    from shopping_app.agents import recommender as recommender_module

    monkeypatch.setattr(recommender_module, "OpenAIEmbeddings", lambda **kwargs: DummyEmbeddings())
    monkeypatch.setattr(recommender_module, "ChatOpenAI", lambda **kwargs: DummyLLM())
    monkeypatch.setattr(
        recommender_module,
        "_resolve_product_url",
        lambda platform, title: ("https://www.amazon.com/dp/B08TEST001", 10.0),
    )

    repo = ShoppingRepository(db_path=str(tmp_path / "shopping.db"))
    engine = ShoppingRecommender(repo)

    response = engine.recommend("desk lamp", "session-3")
    # max_recommendations defaults to 1, so only the top item is saved
    assert len(response.recommendations) == 1
    saved = repo.list_recommendations("session-3")
    assert len(saved) == 1
