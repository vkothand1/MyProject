import logging

from langchain_core.documents import Document
from sentence_transformers import CrossEncoder

from app.config import get_settings

logger = logging.getLogger(__name__)

_cross_encoder: CrossEncoder | None = None


def _get_cross_encoder() -> CrossEncoder:
    """Lazy-load the cross-encoder model (singleton)."""
    global _cross_encoder
    if _cross_encoder is None:
        _cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
        logger.info("Loaded cross-encoder model")
    return _cross_encoder


def rerank(
    query: str,
    documents: list[Document],
    top_k: int | None = None,
) -> list[Document]:
    """Rerank documents using cross-encoder scores."""
    if not documents:
        return []

    settings = get_settings()
    k = top_k or settings.TOP_K_RERANK

    model = _get_cross_encoder()
    pairs = [(query, doc.page_content) for doc in documents]
    scores = model.predict(pairs)

    for doc, score in zip(documents, scores):
        doc.metadata["rerank_score"] = float(score)

    ranked = sorted(documents, key=lambda d: d.metadata["rerank_score"], reverse=True)
    logger.info(
        "Reranked %d→%d docs (top score: %.3f)",
        len(documents),
        min(k, len(ranked)),
        ranked[0].metadata["rerank_score"] if ranked else 0,
    )
    return ranked[:k]
