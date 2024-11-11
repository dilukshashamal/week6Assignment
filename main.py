from pdf_to_image import pdf_to_images
from ocr import perform_ocr
from classify_document import classify_document

pdf_path = "data/bank_statement.pdf"
image_paths = pdf_to_images(pdf_path)
print("Images generated:", image_paths)

ocr_json_path = perform_ocr(input_dir="data")
print("OCR results saved to:", ocr_json_path)

ocr_json_path = "data/ocr_results.json"
document_type = classify_document(ocr_json_path)
print("Document classified as:", document_type)
