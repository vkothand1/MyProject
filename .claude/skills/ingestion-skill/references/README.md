# Ingestion Skill Reference

## Overview
Multi-format document ingestion with intelligent text extraction from images and PDFs.

## Supported Formats

### Images
- **Extensions**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`, `.bmp`
- **Primary**: Tesseract OCR
- **Fallback**: Claude vision API (automatic if Tesseract unavailable)
- **Quality Warnings**: Model reports image quality during extraction

### PDFs
- **Extensions**: `.pdf`
- **Primary**: PyPDF2 (simple, fast)
- **Fallback**: pdfminer.six (complex/encrypted PDFs)

## Dependencies

- `anthropic` - Claude vision API
- `pytesseract` - OCR wrapper
- `Pillow` - Image processing
- `PyPDF2` - PDF extraction
- `pdfminer.six` - Advanced PDF parsing
- `python-dotenv` - Environment configuration

Install via: `pip install -r requirements.txt`

**System requirement for Tesseract OCR**:
- macOS: `brew install tesseract`
- Ubuntu: `apt-get install tesseract-ocr`
- Windows: https://github.com/UB-Mannheim/tesseract/wiki

## Usage

### Command Line
```bash
cd .claude/skills/ingestion-skill/scripts
python -m cli
```
Prompts for file path → extracts text → saves to `output/`

### Programmatic
```python
from multiFormatIngestion import MultiFormatIngestion

ingestion = MultiFormatIngestion(useClaude=True)
job = ingestion.ingestFile("/path/to/document.pdf")

if job.success:
    print(job.extractedText)
    print(f"Handler: {job.formatHandler}")
else:
    print(f"Error: {job.error}")
```

## Architecture

- **MultiFormatIngestion**: Orchestrator that routes files to appropriate handler
- **ImageHandler**: Tesseract OCR → Claude vision fallback
- **PdfHandler**: PyPDF2 → pdfminer.six fallback
- **ExtractionResult**: Success/error dataclass
- **IngestionJob**: Metadata about ingestion with extracted content

## Error Handling

| Scenario | Handling |
|---|---|
| File not found | FileNotFoundError raised |
| Unsupported format | Returns IngestionJob with error description |
| Extraction failure | Tries fallback handler if available |
| API/library unavailable | Clear error message with suggestions |

## Output Format

- **Location**: `.claude/skills/ingestion-skill/output/`
- **Filename**: `{original_name}_extracted.txt`
- **Content**: Raw extracted text, newline-delimited
- **Idempotency**: Multiple extractions append counter (_1, _2, etc.)

## Performance Notes

- **Small images** (<5MB): <5 seconds
- **Large images** (>10MB): 10-30 seconds (CPU-bound OCR)
- **Simple PDFs**: <2 seconds
- **Complex PDFs**: 5-30 seconds (fallback extraction)
- **Optimization**: Tesseract faster than Claude vision, but less accurate

## Quality Assessment

When using Claude vision, the model notes image quality:
- Clear/high-res: "High confidence extraction"
- Blurry/low-res: "Quality warning: Low resolution detected — extraction may be inaccurate"
- Handwritten: "Complex handwriting — manual review recommended"

These quality notes are included in the extracted output for user awareness.
