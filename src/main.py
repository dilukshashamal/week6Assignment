# main.py

import os
from config import INPUT_DIR, OUTPUT_DIR
from document_processing.classify import classify_document
from document_processing.extraction import extract_data
from document_processing.validation import validate_document
from document_processing.utils import pdf_to_png
from paddleocr import PaddleOCR

def process_pdf(pdf_path):
    # Step 1: Convert PDF to PNG images
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    output_image_folder = os.path.join(OUTPUT_DIR, pdf_name)
    image_paths = pdf_to_png(pdf_path, output_image_folder)
    
    # Initialize OCR model
    ocr = PaddleOCR(use_angle_cls=True, lang="en")
    
    # Step 2: Perform OCR on each PNG image
    extracted_text = []
    for image_path in image_paths:
        # Process each image individually to avoid the det must be false error
        result = ocr.ocr(image_path, det=True, cls=True)  # Ensure det=True for single images
        extracted_text.append(result)
    
    return extracted_text

def main():
    # Example file to process
    pdf_path = os.path.join(INPUT_DIR, "bank_statement.pdf")
    extracted_text = process_pdf(pdf_path)
    
    # Now classify and extract data from the OCR results
    for page_text in extracted_text:
        document_type = classify_document(page_text)
        extracted_data = extract_data(document_type, page_text)
        
        # Validate the extracted data
        validation_result = validate_document(document_type, extracted_data)
        
        # Print or log the validation results
        print(validation_result)

if __name__ == "__main__":
    main()
