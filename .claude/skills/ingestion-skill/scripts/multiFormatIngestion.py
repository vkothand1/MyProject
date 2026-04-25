"""Main ingestion orchestrator supporting multiple file formats."""

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class ExtractionResult:
    """Result of text extraction from a file."""
    extractedText: str
    success: bool
    error: str = ""


@dataclass
class IngestionJob:
    """Metadata for an ingestion job."""
    sourceFilePath: str
    extractedText: str
    formatHandler: str
    success: bool
    error: str = ""


class BaseHandler:
    """Abstract base for format-specific text extractors."""

    def canHandle(self, filePath: str) -> bool:
        raise NotImplementedError

    def extract(self, filePath: str) -> ExtractionResult:
        raise NotImplementedError

    def getFormatName(self) -> str:
        raise NotImplementedError


class ImageHandler(BaseHandler):
    """Extract text from PNG, JPEG, GIF, WebP images."""

    SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"}

    def __init__(self, useClaude: bool = False) -> None:
        self.useClaude = useClaude
        self._tesseractAvailable = self._checkTesseract()

    def canHandle(self, filePath: str) -> bool:
        return Path(filePath).suffix.lower() in self.SUPPORTED_EXTENSIONS

    def getFormatName(self) -> str:
        return "Image (OCR)"

    def extract(self, filePath: str) -> ExtractionResult:
        """Extract text from an image file."""
        filePath = str(Path(filePath).resolve())

        if self.useClaude or not self._tesseractAvailable:
            return self._extractViaClaude(filePath)
        else:
            result = self._extractViaTesseract(filePath)
            if not result.success:
                logger.warning("Tesseract extraction failed; falling back to Claude vision")
                return self._extractViaClaude(filePath)
            return result

    def _checkTesseract(self) -> bool:
        """Check if pytesseract and Tesseract are available."""
        try:
            import pytesseract
            pytesseract.get_tesseract_version()
            return True
        except Exception:
            return False

    def _extractViaTesseract(self, filePath: str) -> ExtractionResult:
        """Extract text using Tesseract OCR."""
        try:
            import pytesseract
            from PIL import Image

            image = Image.open(filePath)
            text = pytesseract.image_to_string(image)

            if not text.strip():
                return ExtractionResult(
                    extractedText="",
                    success=False,
                    error="Tesseract extracted no text from image.",
                )

            logger.info("Extracted %d chars via Tesseract", len(text))
            return ExtractionResult(extractedText=text.strip(), success=True)

        except ImportError as exc:
            return ExtractionResult(
                extractedText="",
                success=False,
                error=f"Tesseract not available: {exc}",
            )
        except Exception as exc:
            logger.exception("Tesseract extraction failed")
            return ExtractionResult(
                extractedText="",
                success=False,
                error=f"Tesseract error: {exc}",
            )

    def _extractViaClaude(self, filePath: str) -> ExtractionResult:
        """Extract text using Claude vision API."""
        try:
            import base64
            import anthropic
            from dotenv import load_dotenv

            load_dotenv()
            client = anthropic.Anthropic()

            with open(filePath, "rb") as f:
                imageData = base64.standard_b64encode(f.read()).decode("utf-8")

            ext = Path(filePath).suffix.lower()
            mimeType = {
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg",
                ".png": "image/png",
                ".gif": "image/gif",
                ".webp": "image/webp",
                ".bmp": "image/bmp",
            }.get(ext, "image/jpeg")

            message = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=2048,
                system="Extract all text visible in this image. Be precise and preserve formatting.",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": mimeType,
                                    "data": imageData,
                                },
                            },
                            {
                                "type": "text",
                                "text": "Extract all visible text from this image. List each field/line.",
                            },
                        ],
                    }
                ],
            )

            text = message.content[0].text
            logger.info("Extracted %d chars via Claude vision", len(text))
            return ExtractionResult(extractedText=text.strip(), success=True)

        except ImportError as exc:
            return ExtractionResult(
                extractedText="",
                success=False,
                error=f"Anthropic SDK not available: {exc}",
            )
        except Exception as exc:
            logger.exception("Claude vision extraction failed")
            return ExtractionResult(
                extractedText="",
                success=False,
                error=f"Claude error: {exc}",
            )


class PdfHandler(BaseHandler):
    """Extract text from PDF files."""

    SUPPORTED_EXTENSIONS = {".pdf"}

    def canHandle(self, filePath: str) -> bool:
        return Path(filePath).suffix.lower() in self.SUPPORTED_EXTENSIONS

    def getFormatName(self) -> str:
        return "PDF"

    def extract(self, filePath: str) -> ExtractionResult:
        """Extract text from a PDF file."""
        filePath = str(Path(filePath).resolve())

        result = self._extractViapypdf2(filePath)
        if result.success:
            return result

        logger.info("PyPDF2 failed; trying pdfminer")
        result = self._extractViaPdfminer(filePath)
        if result.success:
            return result

        return ExtractionResult(
            extractedText="",
            success=False,
            error="All PDF extraction methods failed.",
        )

    def _extractViapypdf2(self, filePath: str) -> ExtractionResult:
        """Extract text using PyPDF2."""
        try:
            from PyPDF2 import PdfReader

            reader = PdfReader(filePath)
            text = ""

            for pageNum in range(len(reader.pages)):
                page = reader.pages[pageNum]
                text += page.extract_text()

            if not text.strip():
                return ExtractionResult(
                    extractedText="",
                    success=False,
                    error="PyPDF2 extracted no text from PDF.",
                )

            logger.info("Extracted %d chars via PyPDF2", len(text))
            return ExtractionResult(extractedText=text.strip(), success=True)

        except ImportError:
            return ExtractionResult(
                extractedText="",
                success=False,
                error="PyPDF2 not available.",
            )
        except Exception as exc:
            logger.debug("PyPDF2 extraction failed: %s", exc)
            return ExtractionResult(
                extractedText="",
                success=False,
                error=f"PyPDF2 error: {exc}",
            )

    def _extractViaPdfminer(self, filePath: str) -> ExtractionResult:
        """Extract text using pdfminer.six."""
        try:
            from io import StringIO
            from pdfminer.converter import TextConverter
            from pdfminer.layout import LAParams
            from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
            from pdfminer.pdfpage import PDFPage

            resourceManager = PDFResourceManager()
            stringBuffer = StringIO()
            laparams = LAParams()
            converter = TextConverter(resourceManager, stringBuffer, laparams=laparams)
            interpreter = PDFPageInterpreter(resourceManager, converter)

            with open(filePath, "rb") as pdfFile:
                for page in PDFPage.get_pages(
                    pdfFile, caching=True, check_extractable=True
                ):
                    interpreter.process_page(page)

            text = stringBuffer.getvalue()
            converter.close()
            stringBuffer.close()

            if not text.strip():
                return ExtractionResult(
                    extractedText="",
                    success=False,
                    error="pdfminer extracted no text from PDF.",
                )

            logger.info("Extracted %d chars via pdfminer", len(text))
            return ExtractionResult(extractedText=text.strip(), success=True)

        except ImportError:
            return ExtractionResult(
                extractedText="",
                success=False,
                error="pdfminer.six not available.",
            )
        except Exception as exc:
            logger.debug("pdfminer extraction failed: %s", exc)
            return ExtractionResult(
                extractedText="",
                success=False,
                error=f"pdfminer error: {exc}",
            )


class MultiFormatIngestion:
    """Ingest text from images, PDFs, and other file formats."""

    def __init__(
        self, useClaude: bool = False, outputDir: Optional[str] = None
    ) -> None:
        self.useClaude = useClaude
        # From: .claude/skills/ingestion-skill/scripts/multiFormatIngestion.py
        # To: .claude/output/ingestion-skill/
        self.outputDir = outputDir or str(Path(__file__).parent.parent.parent.parent / "output" / "ingestion-skill")
        self._handlers = [
            ImageHandler(useClaude=useClaude),
            PdfHandler(),
        ]

    def ingestFile(self, filePath: str) -> IngestionJob:
        """Ingest a file and extract its text content."""
        resolvedPath = Path(filePath).resolve()
        if not resolvedPath.exists():
            raise FileNotFoundError(f"File not found: {resolvedPath}")

        handler = self._findHandler(str(resolvedPath))
        if not handler:
            return IngestionJob(
                sourceFilePath=str(resolvedPath),
                extractedText="",
                formatHandler="Unknown",
                success=False,
                error=(
                    f"Unsupported file format. "
                    f"Supported: {', '.join(h.getFormatName() for h in self._handlers)}"
                ),
            )

        logger.info(
            "Ingesting %s using %s", resolvedPath.name, handler.getFormatName()
        )

        result = handler.extract(str(resolvedPath))

        job = IngestionJob(
            sourceFilePath=str(resolvedPath),
            extractedText=result.extractedText,
            formatHandler=handler.getFormatName(),
            success=result.success,
            error=result.error,
        )

        if job.success:
            outputPath = self._saveExtractedText(job)
            logger.info("Extracted text saved to %s", outputPath)

        return job

    def _findHandler(self, filePath: str) -> Optional[BaseHandler]:
        """Locate the first handler that can process filePath."""
        for handler in self._handlers:
            if handler.canHandle(filePath):
                return handler
        return None

    def _saveExtractedText(self, job: IngestionJob) -> str:
        """Write extracted text to the output directory."""
        outputDir = Path(self.outputDir)
        outputDir.mkdir(parents=True, exist_ok=True)

        stem = Path(job.sourceFilePath).stem
        outputFile = outputDir / f"{stem}_extracted.txt"

        counter = 1
        originalOutputFile = outputFile
        while outputFile.exists():
            outputFile = originalOutputFile.parent / f"{stem}_extracted_{counter}.txt"
            counter += 1

        outputFile.write_text(job.extractedText, encoding="utf-8")
        return str(outputFile)
