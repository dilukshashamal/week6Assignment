# Document Processing Pipeline

This project is a comprehensive document processing pipeline that extracts text, classifies documents, extracts key-value pairs, detects tables, and validates data using checksums. The application uses various Python modules to process a bank statement PDF and can be extended to process other types of documents as well.

## Features

1. **PDF to Images Conversion**:
   - Converts PDF files to images for further processing using OCR.
   
2. **OCR (Optical Character Recognition)**:
   - Extracts text data from the images using OCR, which outputs the data in a JSON format.

3. **Document Classification**:
   - Classifies the document based on its content, determining its type (e.g., bank statement).

4. **Key-Value Extraction**:
   - Extracts key-value pairs (like dates, amounts, names, etc.) from the OCR result and the document classification.

5. **Table Extraction**:
   - Extracts tables from images (useful for documents like financial statements or reports that contain tabular data).

6. **Checksum Validation**:
   - Validates the extracted data using checksums to ensure the integrity of the processed information.

## How to Run

### Prerequisites

Before running the application, make sure you have the following dependencies installed:

1. Python 3.10
2. Required Python packages (`requirements.txt`)

To install the dependencies, run:

```bash
pip install -r requirements.txt
```
```bash
python main.py
```


