from typing import Literal

from pydantic import BaseModel, Field


class ChunkMetadata(BaseModel):
    source_file: str
    page_number: int
    chunk_index: int
    chunk_id: str
    headings: list[str] = Field(default_factory=list)


class QueryRequest(BaseModel):
    question: str = Field(min_length=3, max_length=1000)


class QueryResponse(BaseModel):
    answer: str
    sources: list[ChunkMetadata] = Field(default_factory=list)


class DocumentStatus(BaseModel):
    file_name: str
    status: Literal["indexed", "updated", "deleted", "error"]
    chunk_count: int = 0
    message: str = ""
