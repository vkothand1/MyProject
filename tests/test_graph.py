from unittest.mock import MagicMock, patch

import pytest
from langchain_core.documents import Document

from app.graph.nodes import FALLBACK_MESSAGE, fallback, grade, should_generate


class TestGrade:
    @patch("app.graph.nodes.get_settings")
    def test_filters_below_threshold(self, mock_settings):
        mock_settings.return_value = MagicMock(RELEVANCE_THRESHOLD=0.5)
        state = {
            "ranked_docs": [
                Document(page_content="low", metadata={"rerank_score": 0.2}),
                Document(page_content="high", metadata={"rerank_score": 0.8}),
            ]
        }
        result = grade(state)
        assert len(result["relevant_docs"]) == 1
        assert result["relevant_docs"][0].page_content == "high"


class TestShouldGenerate:
    def test_generate_when_docs(self):
        state = {"relevant_docs": [Document(page_content="x", metadata={})]}
        assert should_generate(state) == "generate"

    def test_fallback_when_empty(self):
        state = {"relevant_docs": []}
        assert should_generate(state) == "fallback"

    def test_fallback_when_missing(self):
        state = {}
        assert should_generate(state) == "fallback"


class TestFallback:
    def test_returns_fallback_message(self):
        state = {"question": "What is the weather?"}
        result = fallback(state)
        assert result["answer"] == FALLBACK_MESSAGE
        assert result["sources"] == []
