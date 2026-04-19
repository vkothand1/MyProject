import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from langchain_core.documents import Document

from app.ingestion.chunker import build_chunk_id, chunk_documents
from app.ingestion.loader import load_pdf


class TestBuildChunkId:
    def test_deterministic(self):
        id1 = build_chunk_id("test.pdf", 1, 0)
        id2 = build_chunk_id("test.pdf", 1, 0)
        assert id1 == id2

    def test_different_inputs(self):
        id1 = build_chunk_id("a.pdf", 1, 0)
        id2 = build_chunk_id("b.pdf", 1, 0)
        assert id1 != id2


class TestChunkDocuments:
    def test_basic_chunking(self):
        docs = [
            Document(
                page_content="A " * 600,
                metadata={"source_file": "test.pdf", "page_number": 1, "headings": []},
            )
        ]
        chunks = chunk_documents(docs)
        assert len(chunks) >= 2
        assert all(c.metadata["source_file"] == "test.pdf" for c in chunks)
        assert all("chunk_id" in c.metadata for c in chunks)

    def test_short_doc_single_chunk(self):
        docs = [
            Document(
                page_content="Short text.",
                metadata={"source_file": "t.pdf", "page_number": 1, "headings": []},
            )
        ]
        chunks = chunk_documents(docs)
        assert len(chunks) == 1


class TestLoadPdf:
    def test_nonexistent_file(self):
        result = load_pdf(Path("/nonexistent/file.pdf"))
        assert result == []
