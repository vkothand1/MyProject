import logging
from pathlib import Path

import fitz
from langchain_core.documents import Document

logger = logging.getLogger(__name__)


def load_pdf(pdf_path: Path) -> list[Document]:
    """Load a single PDF and return a list of Documents, one per page."""
    documents: list[Document] = []
    file_name = pdf_path.name

    try:
        doc = fitz.open(str(pdf_path))
    except Exception:
        logger.exception("Failed to open PDF: %s", file_name)
        return documents

    try:
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text("text")
            if not text or not text.strip():
                continue

            headings = _extract_headings(page)

            documents.append(
                Document(
                    page_content=text.strip(),
                    metadata={
                        "source_file": file_name,
                        "page_number": page_num + 1,
                        "headings": headings,
                    },
                )
            )
    finally:
        doc.close()

    logger.info("Loaded %d pages from %s", len(documents), file_name)
    return documents


def load_pdfs_from_directory(directory: Path) -> list[Document]:
    """Load all PDFs from a directory."""
    all_documents: list[Document] = []
    pdf_files = sorted(directory.glob("*.pdf"))

    if not pdf_files:
        logger.warning("No PDF files found in %s", directory)
        return all_documents

    for pdf_path in pdf_files:
        docs = load_pdf(pdf_path)
        all_documents.extend(docs)

    logger.info(
        "Loaded %d total pages from %d PDFs",
        len(all_documents),
        len(pdf_files),
    )
    return all_documents


def _extract_headings(page: fitz.Page) -> list[str]:
    """Extract likely headings from a page using font size heuristics."""
    headings: list[str] = []
    blocks = page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE)["blocks"]

    for block in blocks:
        if block.get("type") != 0:
            continue
        for line in block.get("lines", []):
            text = "".join(span["text"] for span in line["spans"]).strip()
            if not text or len(text) > 200:
                continue

            max_font_size = max(
                (span["size"] for span in line["spans"]), default=0
            )
            is_bold = any(
                "bold" in span.get("font", "").lower() for span in line["spans"]
            )

            if max_font_size >= 14 or (is_bold and max_font_size >= 12):
                headings.append(text)

    return headings
