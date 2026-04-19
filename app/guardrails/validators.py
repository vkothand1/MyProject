import re


class RAGError(Exception):
    """Base exception for RAG application."""


class IngestionError(RAGError):
    """Error during document ingestion."""


class RetrievalError(RAGError):
    """Error during document retrieval."""


class GenerationError(RAGError):
    """Error during answer generation."""


def validate_input(question: str) -> str:
    """Validate and sanitize user input."""
    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    question = question.strip()

    if len(question) < 3:
        raise ValueError("Question must be at least 3 characters long.")

    if len(question) > 1000:
        raise ValueError("Question must be at most 1000 characters long.")

    # Strip potential prompt injection patterns
    question = re.sub(
        r"(ignore|forget|disregard)\s+(all\s+)?(previous|above|prior)\s+(instructions|prompts|context)",
        "",
        question,
        flags=re.IGNORECASE,
    )

    return question.strip() or "?"
