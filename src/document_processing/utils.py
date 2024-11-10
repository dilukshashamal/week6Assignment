import json
import logging
import os
import pandas as pd
from config import JSON_INDENT, LOGGING_LEVEL, LOG_FILE, BALANCE_VALIDATION_TOLERANCE

# Set up logging
logging.basicConfig(filename=LOG_FILE, level=LOGGING_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s')

def save_to_json(data, file_path):

    try:
        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=JSON_INDENT)
        logging.info(f"Data successfully saved to {file_path}")
    except Exception as e:
        logging.error(f"Failed to save data to JSON: {e}")

def perform_balance_validation(transactions, opening_balance):

    calculated_balance = opening_balance
    discrepancies = []

    for index, transaction in enumerate(transactions):
        credit = float(transaction.get("credit", 0).replace(",", "") or 0)
        debit = float(transaction.get("debit", 0).replace(",", "") or 0)
        expected_balance = calculated_balance + credit - debit

        # Compare expected balance to the provided balance with a tolerance
        if abs(expected_balance - float(transaction.get("balance", 0).replace(",", ""))) > BALANCE_VALIDATION_TOLERANCE:
            transaction["error"] = "Balance discrepancy"
            discrepancies.append({
                "row": index + 1,
                "expected_balance": expected_balance,
                "provided_balance": transaction.get("balance")
            })

        # Update calculated balance for the next row
        calculated_balance = expected_balance

    if discrepancies:
        logging.warning(f"Discrepancies found in balance validation: {discrepancies}")
    else:
        logging.info("Balance validation completed successfully with no discrepancies.")
    
    return transactions

def extract_transactions_as_dataframe(transactions):

    df = pd.DataFrame(transactions)
    logging.info(f"Converted transactions to DataFrame with {len(df)} rows.")
    return df

def load_json(file_path):

    try:
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
        logging.info(f"Data successfully loaded from {file_path}")
        return data
    except Exception as e:
        logging.error(f"Failed to load JSON: {e}")
        return None

def log_and_flag_discrepancies(discrepancies, output_path):
    if discrepancies:
        save_to_json(discrepancies, output_path)
        logging.warning(f"Discrepancies flagged and saved to {output_path}")
    else:
        logging.info("No discrepancies to flag.")

