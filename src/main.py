import os
import sys
import logging
from document_processing.classify import classify_document
from document_processing.extraction import extract_data
from document_processing.validation import validate_document
from document_processing.utils import save_to_json, load_json
from config import INPUT_DIR, OUTPUT_DIR, LOG_FILE, EXPECTED_VALUES_FILE

# Set up logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_document(file_path):
    """
    Processes a single document: classify, extract, validate, and save data.

    Parameters:
    - file_path (str): Path to the document file.

    Returns:
    - dict: The structured data including classification, extraction, validation status, and discrepancies if any.
    """
    logging.info(f"Starting processing for {file_path}")

    # Step 1: Classify the document type
    document_type = classify_document(file_path)
    logging.info(f"Document classified as: {document_type}")

    # Step 2: Extract data based on document type
    extracted_data = extract_data(file_path, document_type)
    logging.info(f"Data extracted for {document_type}")

    # Step 3: Load expected values for validation
    expected_values = load_json(EXPECTED_VALUES_FILE).get(document_type, {})
    logging.info(f"Loaded expected values for {document_type} from {EXPECTED_VALUES_FILE}")

    # Step 4: Validate extracted data
    validation_result = validate_document(document_type, extracted_data, expected_values)
    logging.info(f"Validation result: {'Passed' if validation_result['success'] else 'Failed'}")

    # Step 5: Prepare final output data structure
    output_data = {
        "file_path": file_path,
        "document_type": document_type,
        "extracted_data": extracted_data,
        "validation": validation_result
    }

    # Step 6: Save results to a JSON file
    output_file = os.path.join(OUTPUT_DIR, f"{os.path.basename(file_path)}_output.json")
    save_to_json(output_data, output_file)
    logging.info(f"Results saved to {output_file}")

    return output_data

def process_all_documents():
    """
    Processes all documents in the INPUT_FOLDER, classifies, extracts, validates, and saves each one.
    """
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Process each file in the input directory
    for file_name in os.listdir(INPUT_DIR):
        file_path = os.path.join(INPUT_DIR, file_name)
        try:
            process_document(file_path)
        except Exception as e:
            logging.error(f"Failed to process {file_name}: {e}")
            continue

if __name__ == "__main__":
    # Run the processing on all documents in the input folder
    process_all_documents()
    print("Processing completed. Check logs and output folder for details.")
