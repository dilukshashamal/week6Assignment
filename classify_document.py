import json
import re
import os

def classify_page_text(page_text):

    # Define keyword sets for each document type
    keywords = {
        "bank_statement": ["account number", "transaction", "balance", "deposit", "withdrawal", "statement"],
        "check": ["pay to the order", "memo", "check number", "authorized signature", "routing number"],
        "salary_slip": ["net salary", "gross salary", "deduction", "pay period", "employer", "employee", "income"],
    }

    # Count keyword matches for each category
    match_counts = {category: 0 for category in keywords}

    for category, words in keywords.items():
        for word in words:
            # Count occurrences of each keyword in the page text
            match_counts[category] += len(re.findall(r"\b" + re.escape(word) + r"\b", page_text))

    # Determine the category with the highest match count
    classified_category = max(match_counts, key=match_counts.get)

    # If no matches or very low match counts, classify as 'others'
    if all(count == 0 for count in match_counts.values()):
        classified_category = "others"
    
    return classified_category

def classify_document(ocr_json_path, output_dir="data"):
    """
    Classifies each page of a document based on extracted OCR text and saves results as JSON.

    Args:
        ocr_json_path (str): Path to the JSON file containing OCR results.
        output_dir (str): Directory where the classification result JSON will be saved.

    Returns:
        str: Path to the JSON file containing the page-wise classification results.
    """
    # Load OCR data from JSON file
    with open(ocr_json_path, "r", encoding="utf-8") as file:
        ocr_data = json.load(file)

    # Dictionary to store classification results for each page
    classification_results = {}

    # Process each page individually
    for page_number, page_content in ocr_data.items():
        # Combine all text in the page
        page_text = " ".join(item["text"].lower() for item in page_content)

        # Classify the page based on its text content
        classified_type = classify_page_text(page_text)
        classification_results[page_number] = classified_type
        print(f"Classified {page_number} as {classified_type}")

    # Save page-wise classification result as JSON
    os.makedirs(output_dir, exist_ok=True)
    classification_result_path = os.path.join(output_dir, "classification_result.json")
    with open(classification_result_path, "w", encoding="utf-8") as json_file:
        json.dump(classification_results, json_file, indent=4)
    print(f"Page-wise classification result saved to {classification_result_path}")

    return classification_result_path

if __name__ == "__main__":
    # Example usage
    ocr_json_path = "data/ocr_results.json"  # Path to OCR JSON results
    classification_json_path = classify_document(ocr_json_path)
    print("Document page-wise classification result saved to:", classification_json_path)
