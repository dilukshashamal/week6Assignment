import json
import re
import os

def extract_key_values_from_page(page_text, document_type):
    """
    Extracts key-value pairs from a single page's text content based on document type.

    Args:
        page_text (str): Extracted text from a single page.
        document_type (str): Type of document (e.g., 'bank_statement', 'check', 'salary_slip').

    Returns:
        dict: Extracted key-value pairs for the page.
    """
    extracted_data = {}

    # Define regular expression patterns for each document type
    patterns = {
        "bank_statement": {
            "account_number": r"account number[:\s]*([\w\d]+)",
            "total_balance": r"balance[:\s]*([\d,\.]+)",
            "opening_balance": r"opening balance[:\s]*([\d,\.]+)"
        },
        "check": {
            "check_number": r"check number[:\s]*([\w\d]+)",
            "date": r"date[:\s]*([\w\d/]+)",
            "payee": r"pay to the order of[:\s]*([\w\s]+)"
        },
        "salary_slip": {
            "employee_name": r"employee[:\s]*([\w\s]+)",
            "net_salary": r"net salary[:\s]*([\d,\.]+)",
            "gross_salary": r"gross salary[:\s]*([\d,\.]+)",
            "deductions": r"deductions[:\s]*([\d,\.]+)"
        }
    }

    # Select the pattern set based on document type
    if document_type in patterns:
        for key, pattern in patterns[document_type].items():
            match = re.search(pattern, page_text, re.IGNORECASE)
            if match:
                extracted_data[key] = match.group(1)

    return extracted_data

def extract_key_values(ocr_json_path, classification_json_path, output_dir="data"):
    """
    Extracts key-value pairs from each page in a document and saves results as JSON.

    Args:
        ocr_json_path (str): Path to the JSON file containing OCR results.
        classification_json_path (str): Path to the JSON file with page-wise classification results.
        output_dir (str): Directory where the key-value extraction results will be saved.

    Returns:
        str: Path to the JSON file containing key-value extraction results.
    """
    # Load OCR data and classification results
    with open(ocr_json_path, "r", encoding="utf-8") as file:
        ocr_data = json.load(file)
    
    with open(classification_json_path, "r", encoding="utf-8") as file:
        classification_data = json.load(file)

    # Dictionary to store extracted key-value pairs for each page
    key_value_results = {}

    for page_number, page_content in ocr_data.items():
        # Combine all text in the page
        page_text = " ".join(item["text"].lower() for item in page_content)

        # Get the document type for this page from classification results
        document_type = classification_data.get(page_number, "others")

        # Extract key-value pairs based on document type
        extracted_data = extract_key_values_from_page(page_text, document_type)
        key_value_results[page_number] = extracted_data

        print(f"Extracted data for {page_number}: {extracted_data}")

    # Save key-value extraction results as JSON
    os.makedirs(output_dir, exist_ok=True)
    key_value_result_path = os.path.join(output_dir, "key_value_extraction_result.json")
    with open(key_value_result_path, "w", encoding="utf-8") as json_file:
        json.dump(key_value_results, json_file, indent=4)
    print(f"Key-value extraction result saved to {key_value_result_path}")

    return key_value_result_path

if __name__ == "__main__":
    # Example usage
    ocr_json_path = "data/ocr_results.json"  # Path to OCR JSON results
    classification_json_path = "data/classification_result.json"  # Path to page-wise classification results
    key_value_json_path = extract_key_values(ocr_json_path, classification_json_path)
    print("Key-value extraction result saved to:", key_value_json_path)
