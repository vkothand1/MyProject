---
name: ingestion-skill
description: A skill for ingesting data from various sources including image and pdf files, extracting text, and storing as output file in output directory.
author: "Vinoth Kumar"
version: 1.0.0
---
### Step 1: Ask for the ingestion file location
The skill will prompt the user to provide the location of the file they wish to ingest. This can be done through a simple input prompt or a file selection dialog, depending on the user interface. The user will be asked to enter the path to the file they want to ingest. For example:
```pythonfile_path = input("Please enter the path to the file you want to ingest: ")
``` 
### Step 2: Ingest the file and extract text
Once the file path is provided, the skill will determine the file format and use appropriate libraries to extract text from the file. For image files, libraries such as Tesseract OCR can be used to extract text. For PDF files, libraries like PyPDF2 or pdfminer can be utilized. The skill will handle different file formats and ensure that the text extraction process is efficient and accurate. For example:
```python import pytesseract
from PIL import Image '''
if file_path.endswith('.pdf'):
    # Use PyPDF2 or pdfminer to extract text from PDF
    extracted_text = extract_text_from_pdf(file_path)
elif file_path.endswith(('.jpg', '.jpeg', '.png')):
    # Use Tesseract OCR to extract text from image
    image = Image.open(file_path)
    extracted_text = pytesseract.image_to_string(image)
else:
    print("Unsupported file format. Please provide a PDF or image file.")
```
### Step 3: Store the extracted text as an output file in the output directory
After successfully extracting text from the provided file, the skill will save the extracted text to an output file in a designated output directory. The skill will ensure that the output file is properly named and stored in the correct location. The user will be informed of the location of the output file once the process is complete. For example:
```python   output_directory = "output/"
output_file_path = output_directory + "extracted_text.txt"
with open(output_file_path, "w") as output_file:  output_file.write(extracted_text) print(f"Extracted text has been saved to {output_file_path}")
``` 
### Step 4 Additional Considerations
- Whereever image is blurry or has low resolution, the skill should provide have a content mentioned  to the user in the output file indicating that the text extraction may be less accurate.
- if no libraries are available for the file format, the skill should provide a clear message to the user indicating that the file format is unsupported and suggest possible alternatives or next steps. Also consider installing necessary libraries or dependencies to support a wider range of file formats in the future.
- Store the generated scripts in a scripts directory within the skill's folder location /Users/vinothkumarkothandapani/Downloads/AIProject/MyProject/.claude/skills/ingestion-skill/ for better organization and maintainability. This will allow for easier access and management of the scripts used for text extraction and file handling.
- Store the references in the references folder within the skill's /Users/vinothkumarkothandapani/Downloads/AIProject/MyProject/.claude/skills/ingestion-skill. This will help keep all relevant information and resources organized and easily accessible for future reference or updates to the skill.
- Error handling: The skill should include error handling mechanisms to manage issues such as invalid file paths, unsupported file formats, and extraction failures. This will ensure that users receive informative messages and can take  appropriate actions to resolve any issues that arise during the ingestion process.
- Performance optimization: Depending on the size and complexity of the files being ingested, the skill may need to implement performance optimizations to ensure that the text extraction process is efficient. This could include techniques such as parallel processing for large files or caching results for frequently ingested files.   