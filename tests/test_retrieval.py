from unittest.mock import MagicMock, patch

import pytest
from langchain_core.documents import Document

from app.retrieval.reranker import rerank


class TestRerank:
    def test_empty_documents(self):
        result = rerank("test query", [])
        assert result == []

    @patch("app.retrieval.reranker._get_cross_encoder")
    def test_reranking_order(self, mock_encoder):
        mock_model = MagicMock()
        mock_model.predict.return_value = [0.1, 0.9, 0.5]
        mock_encoder.return_value = mock_model

        docs = [
            Document(page_content="low", metadata={}),
            Document(page_content="high", metadata={}),
            Document(page_content="mid", metadata={}),
        ]
        result = rerank("query", docs, top_k=3)
        assert result[0].page_content == "high"
        assert result[1].page_content == "mid"
        assert result[2].page_content == "low"

    @patch("app.retrieval.reranker._get_cross_encoder")
    def test_top_k_limit(self, mock_encoder):
        mock_model = MagicMock()
        mock_model.predict.return_value = [0.9, 0.8, 0.7]
        mock_encoder.return_value = mock_model

        docs = [
            Document(page_content=f"doc{i}", metadata={}) for i in range(3)
        ]
        result = rerank("query", docs, top_k=2)
        assert len(result) == 2
