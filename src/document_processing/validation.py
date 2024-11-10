import json
import logging
from .utils import perform_balance_validation, log_and_flag_discrepancies
from config import EXPECTED_VALUES_FILE, BALANCE_VALIDATION_TOLERANCE

# Load expected values once when the module is loaded
try:
    with open(EXPECTED_VALUES_FILE, 'r') as file:
        expected_values = json.load(file)
except FileNotFoundError:
    logging.error("Expected values file not found. Please check the path.")
    expected_values = {}

def validate_bank_statement(extracted_data):
    """Validate a bank statement against expected values and balance consistency."""
    discrepancies = []
    opening_balance = extracted_data.get("opening_balance")
    expected_opening_balance = expected_values.get("bank_statement", {}).get("opening_balance")

    # Validate opening balance
    if opening_balance != expected_opening_balance:
        discrepancies.append({
            "field": "opening_balance",
            "expected": expected_opening_balance,
            "found": opening_balance
        })

    # Perform balance validation on transactions
    balance_validation_result = perform_balance_validation(extracted_data["transactions"])
    discrepancies.extend(balance_validation_result["discrepancies"])

    return {"success": not discrepancies, "discrepancies": discrepancies}

def validate_salary_slip(extracted_data):
    """Validate a salary slip against expected net salary."""
    discrepancies = []
    net_salary = extracted_data.get("net_salary")
    expected_net_salary = expected_values.get("salary_slip", {}).get("expected_net_salary")

    if net_salary != expected_net_salary:
        discrepancies.append({
            "field": "net_salary",
            "expected": expected_net_salary,
            "found": net_salary
        })

    return {"success": not discrepancies, "discrepancies": discrepancies}

def validate_check(extracted_data):
    """Validate a check against expected amount."""
    discrepancies = []
    check_amount = extracted_data.get("amount")
    expected_amount = expected_values.get("check", {}).get("expected_amount")

    if check_amount != expected_amount:
        discrepancies.append({
            "field": "amount",
            "expected": expected_amount,
            "found": check_amount
        })

    return {"success": not discrepancies, "discrepancies": discrepancies}

def validate_document(document_type, extracted_data):
    """
    Validate extracted data based on document type.

    Parameters:
    - document_type (str): The type of the document ('bank_statement', 'salary_slip', or 'check')
    - extracted_data (dict): The data extracted from the document

    Returns:
    - dict: Validation result with success status and any discrepancies found
    """
    if document_type == "bank_statement":
        return validate_bank_statement(extracted_data)
    elif document_type == "salary_slip":
        return validate_salary_slip(extracted_data)
    elif document_type == "check":
        return validate_check(extracted_data)
    else:
        return {"success": True, "discrepancies": []}
