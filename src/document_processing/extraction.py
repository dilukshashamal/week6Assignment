import re
from config import (
    OCR,
    BANK_STATEMENT_KEYS,
    CHECK_KEYS,
    SALARY_SLIP_KEYS,
    TRANSACTION_COLUMNS,
    FUZZY_MATCH_THRESHOLD
)
from fuzzywuzzy import fuzz
import pandas as pd

def extract_data(file_path, document_type):

    ocr_results = OCR.ocr(file_path, cls=True)
    extracted_text = " ".join([line[1][0] for page in ocr_results for line in page])

    extracted_data = {"key_values": {}, "tables": {}}
    if document_type == "bank_statement":
        extracted_data["key_values"] = extract_key_values(extracted_text, BANK_STATEMENT_KEYS)
        extracted_data["tables"] = extract_transaction_table(ocr_results)
    elif document_type == "check":
        extracted_data["key_values"] = extract_key_values(extracted_text, CHECK_KEYS)
    elif document_type == "salary_slip":
        extracted_data["key_values"] = extract_key_values(extracted_text, SALARY_SLIP_KEYS)
        extracted_data["tables"] = extract_salary_breakdown_table(ocr_results)

    return extracted_data

def extract_key_values(text, keys):

    extracted_values = {}
    for field, label in keys.items():
        match = re.search(f"{label}:?\\s*([\\d,\\.]+)", text, re.IGNORECASE)
        if match:
            extracted_values[field] = match.group(1)
    return extracted_values

def extract_transaction_table(ocr_results):

    transactions = []
    for page in ocr_results:
        for line in page:
            line_text = line[1][0]
            columns = line_text.split()  # Assuming each word belongs to a column

            # Check for enough columns to meet transaction row structure
            if len(columns) >= 5:
                transaction = {
                    "date": columns[0],
                    "description": " ".join(columns[1:-3]),
                    "credit": columns[-3] if is_credit(columns[-3]) else "",
                    "debit": columns[-2] if not is_credit(columns[-2]) else "",
                    "balance": columns[-1],
                }
                transactions.append(transaction)

    return transactions

def extract_salary_breakdown_table(ocr_results):

    salary_components = []
    for page in ocr_results:
        for line in page:
            line_text = line[1][0]
            columns = line_text.split()  # Assuming each word belongs to a column

            # Check for typical salary table row (e.g., "Basic Salary 5000")
            if len(columns) >= 2:
                salary_component = {
                    "component": " ".join(columns[:-1]),
                    "amount": columns[-1]
                }
                salary_components.append(salary_component)

    return salary_components

def is_credit(value):

    # Check if a value is numeric (assumed credit)
    try:
        float(value.replace(",", ""))
        return True
    except ValueError:
        return False
