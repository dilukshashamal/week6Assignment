from pdf_to_image import pdf_to_images
from ocr import perform_ocr
from classify_document import classify_document
from key_value_extractor import extract_key_values
import table_extractor
import glob
from checksum_validator import checksum_validator

pdf_path = "data/bank_statement.pdf"
image_paths = pdf_to_images(pdf_path)
print("Images generated:", image_paths)

ocr_json_path = perform_ocr(input_dir="data")
print("OCR results saved to:", ocr_json_path)

ocr_json_path = "data/ocr_results.json"
document_type = classify_document(ocr_json_path)
print("Document classified as:", document_type)

classification_json_path = "data/classification_result.json"
key_value_json_path = extract_key_values(ocr_json_path, classification_json_path)
print("Key-value extraction result saved to:", key_value_json_path)

# table_results = table_extractor.extract_tables_from_images(image_paths)

# Get all PNG and JPG files in the directory
image_paths = glob.glob("data/*.png") + glob.glob("data/*.jpg")

table_results = table_extractor.extract_tables_from_images(image_paths)
 
 
checksum_result_path = checksum_validator(ocr_json_path, classification_json_path)
print("Checksum validation result saved to:", checksum_result_path)
