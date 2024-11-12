import json
import re
import os
from fuzzywuzzy import fuzz

def fuzzy_match(keyword, text, threshold=80):
    """
    Check if a keyword matches any part of the text with a minimum similarity threshold.
    """
    words = text.split()
    for word in words:
        if fuzz.partial_ratio(keyword.lower(), word.lower()) >= threshold:
            return True
    return False

def extract_transaction_rows(page_text):
    """
    Extract transaction rows from page text.
    Each row contains: date, description, credit, debit, and balance.
    """
    transactions = []
    
    # Define regular expressions for extracting transaction details
    patterns = {
        "date": r"(\d{2}/\d{2}/\d{4})", 
        "description": r"([A-Za-z\s]+)", 
        "amount": r"([\d,\.]+)",  
    }
    
    # Find all transaction rows 
    rows = re.findall(
        rf"{patterns['date']}\s+{patterns['description']}\s+{patterns['amount']}?\s+{patterns['amount']}?\s+{patterns['amount']}",
        page_text, re.IGNORECASE
    )

    # Parse each transaction row
    for row in rows:
        date, description, amount1, amount2, balance = row
        credit, debit = 0.0, 0.0
        
        # Determine which amounts correspond to credit or debit
        if fuzzy_match("credit", description):
            credit = float(amount1.replace(",", ""))
        elif fuzzy_match("debit", description):
            debit = float(amount1.replace(",", ""))
        
        # Populate the transaction dictionary
        transactions.append({
            "date": date.strip(),
            "description": description.strip(),
            "credit": credit,
            "debit": debit,
            "balance": float(balance.replace(",", "")),
        })
    
    return transactions

def validate_balance(transactions, opening_balance):
    """
    Validate the running balance of each transaction row.
    """
    current_balance = opening_balance
    errors = []

    for index, transaction in enumerate(transactions):
        credit = transaction["credit"]
        debit = transaction["debit"]
        expected_balance = transaction["balance"]

        # Calculate new balance by adding credit or subtracting debit
        current_balance += credit - debit

        # Compare calculated balance with expected balance
        if round(current_balance, 2) != round(expected_balance, 2):
            errors.append({
                "row": index + 1,
                "date": transaction["date"],
                "description": transaction["description"],
                "expected_balance": expected_balance,
                "calculated_balance": current_balance,
                "error": "Balance mismatch"
            })

    return errors

def checksum_validator(ocr_json_path, classification_json_path, output_dir="data"):
    """
    Perform checksum validation on a bank statement document.
    """
    # Load OCR data and classification results
    with open(ocr_json_path, "r", encoding="utf-8") as file:
        ocr_data = json.load(file)
    
    with open(classification_json_path, "r", encoding="utf-8") as file:
        classification_data = json.load(file)

    errors_summary = {}

    # Process each page classified as a bank statement
    for page_number, page_content in ocr_data.items():
        if classification_data.get(page_number) == "bank_statement":
            page_text = " ".join(item["text"].lower() for item in page_content)

            # Extract transactions and opening balance
            transactions = extract_transaction_rows(page_text)

            # Find the opening balance from the text
            opening_balance_match = re.search(r"opening balance[:\s]*([\d,\.]+)", page_text)
            if opening_balance_match:
                opening_balance = float(opening_balance_match.group(1).replace(",", ""))
            else:
                print(f"Opening balance not found on page {page_number}")
                continue
            
            # Validate balance row-by-row
            errors = validate_balance(transactions, opening_balance)
            if errors:
                errors_summary[page_number] = errors
            else:
                print(f"No balance discrepancies found on page {page_number}")

    # Save validation errors to a JSON file
    os.makedirs(output_dir, exist_ok=True)
    checksum_result_path = os.path.join(output_dir, "checksum_validation_result.json")
    with open(checksum_result_path, "w", encoding="utf-8") as json_file:
        json.dump(errors_summary, json_file, indent=4)

    print(f"Checksum validation results saved to {checksum_result_path}")

    return checksum_result_path

