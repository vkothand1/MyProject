from typing import Annotated, TypedDict

from langchain_core.documents import Document
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class RAGState(TypedDict):
    question: str
    chat_history: Annotated[list[BaseMessage], add_messages]
    retrieved_docs: list[Document]
    ranked_docs: list[Document]
    relevant_docs: list[Document]
    answer: str
    sources: list[dict]
