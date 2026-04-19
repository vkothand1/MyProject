import logging

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph

from app.graph.nodes import fallback, generate, grade, rerank, retrieve, should_generate
from app.graph.state import RAGState
from app.guardrails.validators import validate_input
from app.models import ChunkMetadata, QueryResponse

logger = logging.getLogger(__name__)

_compiled_graph = None
_checkpointer = None


def _build_graph() -> StateGraph:
    """Build the RAG LangGraph workflow."""
    graph = StateGraph(RAGState)

    graph.add_node("retrieve", retrieve)
    graph.add_node("rerank", rerank)
    graph.add_node("grade", grade)
    graph.add_node("generate", generate)
    graph.add_node("fallback", fallback)

    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "rerank")
    graph.add_edge("rerank", "grade")
    graph.add_conditional_edges(
        "grade",
        should_generate,
        {"generate": "generate", "fallback": "fallback"},
    )
    graph.add_edge("generate", END)
    graph.add_edge("fallback", END)

    return graph


def get_graph():
    """Get or create the compiled graph (singleton)."""
    global _compiled_graph, _checkpointer
    if _compiled_graph is None:
        _checkpointer = MemorySaver()
        _compiled_graph = _build_graph().compile(checkpointer=_checkpointer)
        logger.info("RAG workflow graph compiled")
    return _compiled_graph


def invoke(question: str, thread_id: str) -> QueryResponse:
    """Run the RAG pipeline for a question within a conversation thread."""
    validated_question = validate_input(question)
    graph = get_graph()

    config = {"configurable": {"thread_id": thread_id}}

    result = graph.invoke(
        {"question": validated_question},
        config=config,
    )

    sources = [
        ChunkMetadata(
            source_file=s.get("source_file", ""),
            page_number=s.get("page_number", 0),
            chunk_index=s.get("chunk_index", 0),
            chunk_id=s.get("chunk_id", ""),
            headings=s.get("headings", []),
        )
        for s in result.get("sources", [])
    ]

    return QueryResponse(
        answer=result.get("answer", ""),
        sources=sources,
    )
