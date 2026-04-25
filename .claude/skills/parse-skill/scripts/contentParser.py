"""Parse skill: convert raw extracted text into structured JSON."""

import json
import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import anthropic
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


@dataclass
class ParseResult:
    """Result produced by ContentParser."""
    structuredData: dict[str, Any]
    outputPath: str
    success: bool
    error: str = ""


@dataclass
class ContentParser:
    """Parse raw extracted text into structured JSON."""

    model: str = "claude-haiku-4-5-20251001"
    maxTokens: int = 1024
    outputDir: str = ""

    def __post_init__(self) -> None:
        self._client = anthropic.Anthropic()
        if not self.outputDir:
            self.outputDir = str(Path(__file__).parent.parent.parent.parent / "output" / "parse-skill")

    def parseContent(
        self,
        rawContent: str,
        sourcePath: str = "",
        saveOutput: bool = True,
    ) -> ParseResult:
        """Convert rawContent to a structured dict and optionally write JSON."""
        if not rawContent.strip():
            return ParseResult(
                structuredData={},
                outputPath="",
                success=False,
                error="rawContent is empty — nothing to parse.",
            )

        logger.info("Parsing %d chars of extracted content", len(rawContent))

        try:
            structuredData = self._structureContent(rawContent)
            structuredData["_meta"] = self._buildMeta(sourcePath)

            outputPath = ""
            if saveOutput:
                outputPath = self._persistJson(structuredData, sourcePath)
                logger.info("JSON written to %s", outputPath)

            return ParseResult(
                structuredData=structuredData,
                outputPath=outputPath,
                success=True,
            )
        except anthropic.APIError as exc:
            logger.exception("Claude API error during parsing")
            return ParseResult(
                structuredData={},
                outputPath="",
                success=False,
                error=f"API error: {exc}",
            )
        except Exception as exc:
            logger.exception("Unexpected error during parsing")
            return ParseResult(
                structuredData={},
                outputPath="",
                success=False,
                error=str(exc),
            )

    def _structureContent(self, rawContent: str) -> dict[str, Any]:
        """Ask Claude to convert rawContent to a JSON object."""
        prompt = (
            "You are a structured-data extraction assistant.\n"
            "Convert the following document text into a single, flat JSON object.\n"
            "Rules:\n"
            "  - Use camelCase keys.\n"
            "  - Preserve original values exactly (dates, codes, numbers).\n"
            "  - Merge duplicated fields with a numeric suffix (_2, _3, …).\n"
            "  - Return ONLY valid JSON — no markdown fences, no explanation.\n\n"
            f"Document text:\n{rawContent}"
        )

        message = self._client.messages.create(
            model=self.model,
            max_tokens=self.maxTokens,
            messages=[{"role": "user", "content": prompt}],
        )
        responseText = message.content[0].text.strip()

        if responseText.startswith("```"):
            lines = responseText.splitlines()
            responseText = "\n".join(
                line for line in lines if not line.startswith("```")
            ).strip()

        try:
            return json.loads(responseText)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"Model did not return valid JSON.\nResponse:\n{responseText}\nError: {exc}"
            ) from exc

    def _buildMeta(self, sourcePath: str) -> dict[str, str]:
        """Return a metadata dict recording provenance and timestamp."""
        return {
            "source": sourcePath,
            "parsedAt": datetime.now(tz=timezone.utc).isoformat(),
            "parserModel": self.model,
        }

    def _persistJson(self, data: dict[str, Any], sourcePath: str) -> str:
        """Write data as formatted JSON to a file under outputDir."""
        outputDir = Path(self.outputDir)
        outputDir.mkdir(parents=True, exist_ok=True)

        stem = Path(sourcePath).stem if sourcePath else "extracted"
        timestamp = datetime.now(tz=timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        outputFile = outputDir / f"{stem}_{timestamp}.json"

        outputFile.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        return str(outputFile)
