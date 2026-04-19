import json
import logging

from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI

from app.config import get_settings
from app.graph.state import RAGState
from app.retrieval.reranker import rerank as rerank_documents
from app.retrieval.retriever import Retriever

logger = logging.getLogger(__name__)

FALLBACK_MESSAGE = (
    "I don't see any context for the question you asked in the knowledge base."
)

SYSTEM_PROMPT = """You are a helpful assistant. Answer the question ONLY using the provided context.
If the context does not contain relevant information, say "{fallback}".
Always cite page numbers and source documents in your answer.

Context:
{context}
""".replace("{fallback}", FALLBACK_MESSAGE)

_retriever: Retriever | None = None
_llm: ChatOpenAI | None = None


def _get_retriever() -> Retriever:
    global _retriever
    if _retriever is None:
        _retriever = Retriever()
    return _retriever


def _get_llm() -> ChatOpenAI:
    global _llm
    if _llm is None:
        settings = get_settings()
        _llm = ChatOpenAI(
            model=settings.LLM_MODEL,
            temperature=settings.LLM_TEMPERATURE,
            openai_api_key=settings.OPENAI_API_KEY,
        )
    return _llm


def retrieve(state: RAGState) -> dict:
    """Retrieve documents from ChromaDB based on the question."""
    question = state["question"]

    # Contextualize with chat history if available
    chat_history = state.get("chat_history", [])
    if chat_history:
        history_text = "\n".join(
            f"{'User' if isinstance(m, HumanMessage) else 'Assistant'}: {m.content}"
            for m in chat_history[-6:]  # last 3 exchanges
        )
        search_query = f"{history_text}\nUser: {question}"
    else:
        search_query = question

    try:
        docs = _get_retriever().retrieve(search_query)
    except Exception:
        logger.exception("Retrieval error")
        docs = []

    return {"retrieved_docs": docs}


def rerank(state: RAGState) -> dict:
    """Rerank retrieved documents using cross-encoder."""
    docs = state.get("retrieved_docs", [])
    question = state["question"]

    try:
        ranked = rerank_documents(question, docs)
    except Exception:
        logger.exception("Reranking error, using original order")
        ranked = docs[:get_settings().TOP_K_RERANK]

    return {"ranked_docs": ranked}


def grade(state: RAGState) -> dict:
    """Filter ranked documents by relevance threshold."""
    settings = get_settings()
    ranked = state.get("ranked_docs", [])

    relevant = [
        doc
        for doc in ranked
        if doc.metadata.get("rerank_score", 0) >= settings.RELEVANCE_THRESHOLD
    ]

    logger.info(
        "Grading: %d/%d docs passed threshold (%.2f)",
        len(relevant),
        len(ranked),
        settings.RELEVANCE_THRESHOLD,
    )
    return {"relevant_docs": relevant}


def should_generate(state: RAGState) -> str:
    """Conditional edge: decide whether to generate or fallback."""
    if state.get("relevant_docs"):
        return "generate"
    return "fallback"


def generate(state: RAGState) -> dict:
    """Generate answer using LLM with relevant context."""
    question = state["question"]
    docs = state["relevant_docs"]

    context_parts: list[str] = []
    sources: list[dict] = []
    for doc in docs:
        source_file = doc.metadata.get("source_file", "Unknown")
        page_num = doc.metadata.get("page_number", 0)
        headings_raw = doc.metadata.get("headings", "[]")
        if isinstance(headings_raw, str):
            try:
                headings = json.loads(headings_raw)
            except (json.JSONDecodeError, TypeError):
                headings = []
        else:
            headings = headings_raw

        context_parts.append(
            f"[Source: {source_file}, Page {page_num}]\n{doc.page_content}"
        )
        sources.append(
            {
                "source_file": source_file,
                "page_number": page_num,
                "chunk_id": doc.metadata.get("chunk_id", ""),
                "chunk_index": doc.metadata.get("chunk_index", 0),
                "headings": headings,
            }
        )

    context = "\n\n---\n\n".join(context_parts)
    system_msg = SYSTEM_PROMPT.format(context=context)

    try:
        llm = _get_llm()
        response = llm.invoke(
            [
                {"role": "system", "content": system_msg},
                {"role": "user", "content": question},
            ]
        )
        answer = response.content
    except Exception:
        logger.exception("LLM generation error")
        answer = "I encountered an error while generating the answer. Please try again."
        sources = []

    return {
        "answer": answer,
        "sources": sources,
        "chat_history": [
            HumanMessage(content=question),
            AIMessage(content=answer),
        ],
    }


def fallback(state: RAGState) -> dict:
    """Return fallback message when no relevant context is found."""
    question = state["question"]
    return {
        "answer": FALLBACK_MESSAGE,
        "sources": [],
        "chat_history": [
            HumanMessage(content=question),
            AIMessage(content=FALLBACK_MESSAGE),
        ],
    }
