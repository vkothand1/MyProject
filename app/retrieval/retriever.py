import logging

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

from app.config import get_settings

logger = logging.getLogger(__name__)


class Retriever:
    """ChromaDB similarity search retriever."""

    def __init__(self, vector_store: Chroma | None = None) -> None:
        self._settings = get_settings()
        if vector_store is not None:
            self._store = vector_store
        else:
            embeddings = OpenAIEmbeddings(
                model=self._settings.EMBEDDING_MODEL,
                openai_api_key=self._settings.OPENAI_API_KEY,
            )
            self._store = Chroma(
                collection_name=self._settings.CHROMA_COLLECTION_NAME,
                embedding_function=embeddings,
                persist_directory=self._settings.CHROMA_DB_PATH,
            )

    def retrieve(
        self, query: str, top_k: int | None = None
    ) -> list[Document]:
        """Return top_k documents most similar to the query."""
        k = top_k or self._settings.TOP_K_RETRIEVAL
        try:
            results = self._store.similarity_search_with_relevance_scores(
                query, k=k
            )
        except Exception:
            logger.exception("Retrieval failed for query: %s", query[:100])
            return []

        documents: list[Document] = []
        for doc, score in results:
            doc.metadata["similarity_score"] = score
            documents.append(doc)

        logger.info("Retrieved %d documents for query", len(documents))
        return documents
