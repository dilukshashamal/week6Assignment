# main.py
from pdf_to_image import pdf_to_images

pdf_path = "data/bank_statement.pdf"
image_paths = pdf_to_images(pdf_path)
print("Images generated:", image_paths)
