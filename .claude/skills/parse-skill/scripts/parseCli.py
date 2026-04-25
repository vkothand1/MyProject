"""Command-line interface for parsing extracted content into JSON."""

import json
import logging
import sys

from .contentParser import ContentParser

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
)
logger = logging.getLogger(__name__)


def main() -> int:
    """Prompt user for extracted text and parse it into JSON."""
    print("\n" + "=" * 60)
    print("  Content Parser: Text to JSON")
    print("=" * 60)
    print("Input: Raw extracted text from an ingestion skill")
    print("Output: Structured JSON in camelCase format")
    print()

    print("Enter extracted text (press Ctrl+D or Ctrl+Z on a blank line to finish):")
    print("-" * 60)

    lines = []
    try:
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        pass

    rawContent = "\n".join(lines).strip()

    if not rawContent:
        print("Error: No text provided.")
        return 1

    sourcePath = input(
        "\nOptional: Enter source file path (or leave blank): "
    ).strip()

    parser = ContentParser()

    try:
        result = parser.parseContent(
            rawContent=rawContent,
            sourcePath=sourcePath,
            saveOutput=True,
        )
    except Exception as exc:
        logger.exception("Unexpected error during parsing")
        print(f"Error: {exc}")
        return 1

    print("\n" + "-" * 60)
    if result.success:
        print("✓ Parsing successful")
        print(f"  Fields extracted: {len(result.structuredData) - 1}")
        if result.outputPath:
            print(f"  JSON saved to: {result.outputPath}")
        print("\n--- Structured JSON ---\n")
        print(json.dumps(result.structuredData, indent=2))
        print("\n" + "-" * 60)
        return 0
    else:
        print(f"✗ Parsing failed")
        print(f"  Error: {result.error}")
        print("\n" + "-" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
