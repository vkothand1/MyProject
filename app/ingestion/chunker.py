import hashlib
import logging

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import get_settings

logger = logging.getLogger(__name__)


def build_chunk_id(source_file: str, page_number: int, chunk_index: int) -> str:
    """Generate a stable, deterministic chunk ID using SHA1."""
    raw = f"{source_file}:{page_number}:{chunk_index}"
    return hashlib.sha1(raw.encode()).hexdigest()


def chunk_documents(documents: list[Document]) -> list[Document]:
    """Split page-level documents into smaller chunks with stable IDs."""
    settings = get_settings()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
        length_function=len,
    )

    chunked: list[Document] = []

    for doc in documents:
        source_file = doc.metadata["source_file"]
        page_number = doc.metadata["page_number"]
        headings = doc.metadata.get("headings", [])

        splits = splitter.split_text(doc.page_content)

        for idx, text in enumerate(splits):
            chunk_id = build_chunk_id(source_file, page_number, idx)
            chunked.append(
                Document(
                    page_content=text,
                    metadata={
                        "source_file": source_file,
                        "page_number": page_number,
                        "chunk_index": idx,
                        "chunk_id": chunk_id,
                        "headings": headings,
                    },
                )
            )

    logger.info("Created %d chunks from %d pages", len(chunked), len(documents))
    return chunked
