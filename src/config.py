import os
from paddleocr import PaddleOCR
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "../data")
INPUT_DIR = os.path.join(DATA_DIR, "input")
OUTPUT_DIR = os.path.join(DATA_DIR, "output")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
EXPECTED_VALUES_FILE = os.path.join(DATA_DIR, "config/expected_values.json")

# OCR Settings
OCR = PaddleOCR(use_angle_cls=True, lang="en")

# Classification Settings
DOCUMENT_CATEGORIES = ["bank_statement", "check", "salary_slip", "others"]
CLASSIFICATION_THRESHOLD = 0.8  # Confidence threshold for document classification

# Extraction Settings
# Define common keys for each document type to assist in field extraction
BANK_STATEMENT_KEYS = {
    "account_number": "Account Number",
    "total_balance": "Total Balance",
    "opening_balance": "Opening Balance",
    "closing_balance": "Closing Balance",
}

CHECK_KEYS = {
    "check_number": "Check Number",
    "amount": "Amount",
    "payee": "Payee",
    "date": "Date",
}

SALARY_SLIP_KEYS = {
    "employee_id": "Employee ID",
    "employee_name": "Employee Name",
    "net_salary": "Net Salary",
    "gross_salary": "Gross Salary",
    "deductions": "Deductions",
}

# Validation Settings
BALANCE_VALIDATION_TOLERANCE = 0.01  # Allowable tolerance for balance calculation (if minor discrepancies allowed)
FLAG_ERROR_ON_BALANCE_MISMATCH = True  # Flag errors if balance does not match

# Extraction Settings for Transaction Rows
TRANSACTION_COLUMNS = {
    "date": "Date",
    "description": "Description",
    "credit": "Credit",
    "debit": "Debit",
    "balance": "Balance",
}

# JSON Output Settings
JSON_INDENT = 4  # Indentation level for output JSON file
DATE_FORMAT = "%Y-%m-%d"  # Date format for output JSON file

# Logging Settings
LOGGING_LEVEL = "INFO"  # Set to DEBUG for detailed logs, INFO for general logs
LOG_FILE = os.path.join(BASE_DIR, "app.log")

# Thresholds for Fuzzy Matching
FUZZY_MATCH_THRESHOLD = 85  # Threshold for fuzzy matching in case fields vary slightly in documents

# Others
DEFAULT_CURRENCY_SYMBOL = "$"  # Currency symbol to be used, if applicable

def load_expected_values():
    """Loads expected values from a JSON configuration file."""
    try:
        with open(EXPECTED_VALUES_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Expected values file not found at {EXPECTED_VALUES_FILE}")
        return {}
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {EXPECTED_VALUES_FILE}")
        return {}

# Load expected values once and assign to a variable
EXPECTED_VALUES = load_expected_values()

