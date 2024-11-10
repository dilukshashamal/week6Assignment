import re
import os
from paddleocr import PaddleOCR
from fuzzywuzzy import fuzz
from config import OCR, DOCUMENT_CATEGORIES, CLASSIFICATION_THRESHOLD

# Keywords and patterns that commonly appear in each document type
BANK_STATEMENT_KEYWORDS = ["account number", "balance", "statement", "transaction", "credit", "debit"]
CHECK_KEYWORDS = ["check number", "payee", "amount", "memo"]
SALARY_SLIP_KEYWORDS = ["net salary", "gross salary", "deductions", "employee id", "salary slip"]

# Function to read and classify documents
def classify_document(file_path):

    # Perform OCR on the document
    ocr_results = OCR.ocr(file_path, cls=True)
    extracted_text = " ".join([line[1][0] for page in ocr_results for line in page])

    # Check if OCR results are empty
    if not extracted_text:
        return {"category": "others", "confidence": 0}

    # Score each document category based on keyword matches
    scores = {
        "bank_statement": calculate_match_score(extracted_text, BANK_STATEMENT_KEYWORDS),
        "check": calculate_match_score(extracted_text, CHECK_KEYWORDS),
        "salary_slip": calculate_match_score(extracted_text, SALARY_SLIP_KEYWORDS),
    }

    # Identify the best match
    best_category, best_score = max(scores.items(), key=lambda x: x[1])

    # Determine classification based on the threshold
    if best_score >= CLASSIFICATION_THRESHOLD:
        return {"category": best_category, "confidence": best_score}
    else:
        return {"category": "others", "confidence": best_score}


def calculate_match_score(text, keywords):

    scores = [fuzz.partial_ratio(text.lower(), keyword.lower()) for keyword in keywords]
    return sum(scores) / len(scores) if scores else 0


# Testing functionality
if __name__ == "__main__":
    test_file = os.path.join("data/input", "bank_statement.pdf")  # Example file path
    classification_result = classify_document(test_file)
    print("Document Classification:", classification_result)
