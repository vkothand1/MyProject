"""Command-line interface for multi-format ingestion."""

import logging
import sys
from pathlib import Path

from .multiFormatIngestion import MultiFormatIngestion

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
)
logger = logging.getLogger(__name__)


def main() -> int:
    """Prompt user for file path and ingest it."""
    print("\n" + "=" * 60)
    print("  Multi-Format Document Ingestion")
    print("=" * 60)
    print("Supported formats: PNG, JPEG, GIF, WebP, PDF")
    print()

    filePath = input("Please enter the path to the file you want to ingest: ").strip()

    if not filePath:
        print("Error: No file path provided.")
        return 1

    ingestion = MultiFormatIngestion()

    try:
        job = ingestion.ingestFile(filePath)
    except FileNotFoundError as exc:
        print(f"Error: {exc}")
        return 1
    except Exception as exc:
        logger.exception("Unexpected error during ingestion")
        print(f"Error: {exc}")
        return 1

    print("\n" + "-" * 60)
    if job.success:
        print(f"✓ Extraction successful ({job.formatHandler})")
        print(f"  Source: {Path(job.sourceFilePath).name}")
        print(f"  Text length: {len(job.extractedText)} characters")
        print("\n--- Extracted Text ---\n")
        print(job.extractedText)
        print("\n" + "-" * 60)
        return 0
    else:
        print(f"✗ Extraction failed ({job.formatHandler})")
        print(f"  Error: {job.error}")
        print("\n" + "-" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
