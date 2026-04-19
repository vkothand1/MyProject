import json
import logging
from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

from app.config import get_settings
from app.ingestion.chunker import chunk_documents
from app.ingestion.loader import load_pdf, load_pdfs_from_directory
from app.models import DocumentStatus

logger = logging.getLogger(__name__)


class Indexer:
    """Manages ChromaDB indexing with manifest-based tracking."""

    def __init__(self) -> None:
        self._settings = get_settings()
        self._embeddings = OpenAIEmbeddings(
            model=self._settings.EMBEDDING_MODEL,
            openai_api_key=self._settings.OPENAI_API_KEY,
        )
        self._vector_store = Chroma(
            collection_name=self._settings.CHROMA_COLLECTION_NAME,
            embedding_function=self._embeddings,
            persist_directory=self._settings.CHROMA_DB_PATH,
        )
        self._manifest_path = Path(self._settings.MANIFEST_PATH)
        self._manifest = self._load_manifest()

    # ── Public API ──────────────────────────────────────────────

    def index_documents(self, directory: Path | None = None) -> list[DocumentStatus]:
        """Full ingestion: load all PDFs, chunk, embed, and store."""
        kb_path = directory or Path(self._settings.KNOWLEDGE_BASE_PATH)
        documents = load_pdfs_from_directory(kb_path)
        if not documents:
            logger.warning("No documents to index from %s", kb_path)
            return []

        chunks = chunk_documents(documents)
        return self._upsert_chunks(chunks)

    def add_document(self, pdf_path: Path) -> DocumentStatus:
        """Add a single PDF to the index."""
        file_name = pdf_path.name
        if file_name in self._manifest:
            logger.info("%s already indexed — use update instead", file_name)
            return DocumentStatus(
                file_name=file_name,
                status="error",
                message="Already indexed. Use update to re-index.",
            )

        documents = load_pdf(pdf_path)
        if not documents:
            return DocumentStatus(
                file_name=file_name, status="error", message="Failed to load PDF"
            )

        chunks = chunk_documents(documents)
        self._store_chunks(chunks)
        self._update_manifest(file_name, chunks)
        return DocumentStatus(
            file_name=file_name, status="indexed", chunk_count=len(chunks)
        )

    def update_document(self, pdf_path: Path) -> DocumentStatus:
        """Delete old chunks for a file, then re-index it."""
        file_name = pdf_path.name
        self._delete_file_chunks(file_name)

        documents = load_pdf(pdf_path)
        if not documents:
            return DocumentStatus(
                file_name=file_name, status="error", message="Failed to load PDF"
            )

        chunks = chunk_documents(documents)
        self._store_chunks(chunks)
        self._update_manifest(file_name, chunks)
        return DocumentStatus(
            file_name=file_name, status="updated", chunk_count=len(chunks)
        )

    def delete_document(self, file_name: str) -> DocumentStatus:
        """Remove all chunks for a file from ChromaDB and manifest."""
        count = self._delete_file_chunks(file_name)
        return DocumentStatus(
            file_name=file_name, status="deleted", chunk_count=count
        )

    def get_indexed_files(self) -> list[DocumentStatus]:
        """Return status of all indexed files."""
        return [
            DocumentStatus(
                file_name=name,
                status="indexed",
                chunk_count=len(chunk_ids),
            )
            for name, chunk_ids in self._manifest.items()
        ]

    def get_vector_store(self) -> Chroma:
        """Return the underlying Chroma vector store."""
        return self._vector_store

    # ── Private helpers ─────────────────────────────────────────

    def _upsert_chunks(self, chunks: list[Document]) -> list[DocumentStatus]:
        """Group chunks by file, upsert each file's chunks."""
        files: dict[str, list[Document]] = {}
        for chunk in chunks:
            fname = chunk.metadata["source_file"]
            files.setdefault(fname, []).append(chunk)

        results: list[DocumentStatus] = []
        for file_name, file_chunks in files.items():
            try:
                self._delete_file_chunks(file_name)
                self._store_chunks(file_chunks)
                self._update_manifest(file_name, file_chunks)
                results.append(
                    DocumentStatus(
                        file_name=file_name,
                        status="indexed",
                        chunk_count=len(file_chunks),
                    )
                )
            except Exception:
                logger.exception("Failed to index %s", file_name)
                results.append(
                    DocumentStatus(
                        file_name=file_name,
                        status="error",
                        message="Indexing failed",
                    )
                )

        self._save_manifest()
        return results

    def _store_chunks(self, chunks: list[Document]) -> None:
        """Add chunks to ChromaDB with their stable IDs."""
        ids = [c.metadata["chunk_id"] for c in chunks]
        # Serialize list fields to strings for ChromaDB compatibility
        for chunk in chunks:
            chunk.metadata["headings"] = json.dumps(
                chunk.metadata.get("headings", [])
            )
        self._vector_store.add_documents(documents=chunks, ids=ids)

    def _delete_file_chunks(self, file_name: str) -> int:
        """Delete all chunks for a file from ChromaDB and manifest."""
        chunk_ids = self._manifest.pop(file_name, [])
        if chunk_ids:
            try:
                self._vector_store.delete(ids=chunk_ids)
            except Exception:
                logger.exception("Failed to delete chunks for %s", file_name)
            self._save_manifest()
        return len(chunk_ids)

    def _update_manifest(
        self, file_name: str, chunks: list[Document]
    ) -> None:
        """Update in-memory manifest with new chunk IDs for a file."""
        self._manifest[file_name] = [c.metadata["chunk_id"] for c in chunks]

    def _load_manifest(self) -> dict[str, list[str]]:
        """Load manifest from disk."""
        if self._manifest_path.exists():
            try:
                return json.loads(self._manifest_path.read_text())
            except Exception:
                logger.exception("Failed to load manifest, starting fresh")
        return {}

    def _save_manifest(self) -> None:
        """Persist manifest to disk."""
        self._manifest_path.write_text(
            json.dumps(self._manifest, indent=2)
        )
