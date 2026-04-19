#!/usr/bin/env python3
"""CLI script for ingesting PDFs into the ChromaDB knowledge base."""

import argparse
import logging
import sys
from pathlib import Path

# Ensure project root is on sys.path when run as a script
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.ingestion.indexer import Indexer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(description="RAG Knowledge Base Ingestion Tool")
    parser.add_argument(
        "--action",
        choices=["full", "add", "update", "delete"],
        default="full",
        help="Ingestion action to perform (default: full)",
    )
    parser.add_argument(
        "--path",
        type=str,
        default=None,
        help="Directory containing PDFs (used with 'full' action)",
    )
    parser.add_argument(
        "--file",
        type=str,
        default=None,
        help="Path to a single PDF (used with add/update/delete)",
    )
    args = parser.parse_args()

    indexer = Indexer()

    if args.action == "full":
        directory = Path(args.path) if args.path else None
        logger.info("Starting full ingestion...")
        results = indexer.index_documents(directory)
        _print_summary(results)

    elif args.action in ("add", "update"):
        if not args.file:
            logger.error("--file is required for '%s' action", args.action)
            sys.exit(1)
        pdf_path = Path(args.file)
        if not pdf_path.exists():
            logger.error("File not found: %s", pdf_path)
            sys.exit(1)
        if args.action == "add":
            result = indexer.add_document(pdf_path)
        else:
            result = indexer.update_document(pdf_path)
        logger.info("Result: %s — %s (%d chunks)", result.file_name, result.status, result.chunk_count)

    elif args.action == "delete":
        if not args.file:
            logger.error("--file is required for 'delete' action")
            sys.exit(1)
        file_name = Path(args.file).name
        result = indexer.delete_document(file_name)
        logger.info("Deleted %d chunks for %s", result.chunk_count, result.file_name)


def _print_summary(results: list) -> None:
    total_chunks = sum(r.chunk_count for r in results)
    indexed = sum(1 for r in results if r.status == "indexed")
    errors = sum(1 for r in results if r.status == "error")
    logger.info("=" * 50)
    logger.info("Ingestion Summary:")
    logger.info("  Files indexed: %d", indexed)
    logger.info("  Files errored: %d", errors)
    logger.info("  Total chunks:  %d", total_chunks)
    logger.info("=" * 50)


if __name__ == "__main__":
    main()
