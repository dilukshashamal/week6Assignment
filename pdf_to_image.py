import fitz  
from PIL import Image
import os

def pdf_to_images(pdf_path, output_dir="data", zoom=2):

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    image_paths = []

    # Iterate through each page
    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        
        # Set the zoom factor for higher resolution
        mat = fitz.Matrix(zoom, zoom)
        
        # Render the page to a pixmap
        pix = page.get_pixmap(matrix=mat, alpha=False)
        
        # Save the page as a PNG image
        image_path = os.path.join(output_dir, f"page_{page_num + 1}.png")
        pix.save(image_path)
        image_paths.append(image_path)
        print(f"Saved {image_path}")

    pdf_document.close()
    return image_paths

if __name__ == "__main__":
    # Example usage
    pdf_path = "data/bank_statement.pdf"  # Path to your PDF file
    images = pdf_to_images(pdf_path)
    print("Generated images:", images)
