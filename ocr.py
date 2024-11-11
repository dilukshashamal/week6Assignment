from paddleocr import PaddleOCR
import os
import json
import glob

def perform_ocr(input_dir="data", output_dir="data", language="en"):
    # Initialize PaddleOCR for the specified language
    ocr = PaddleOCR(lang=language)
    
    # Find all PNG files in the input directory
    image_paths = sorted(glob.glob(os.path.join(input_dir, "*.png")))
    
    if not image_paths:
        print("No PNG images found in the specified directory.")
        return None

    # Dictionary to store OCR results organized by page
    ocr_results = {}

    for i, image_path in enumerate(image_paths):
        # Perform OCR on the image
        result = ocr.ocr(image_path, cls=True)
        
        # Extracted text data for the current page
        page_data = []
        
        for line in result[0]:  # Each line of the result
            text_info = {
                "text": line[1][0],      # Extracted text
                "confidence": line[1][1],  # Confidence level
                "position": line[0]       # Coordinates of the text box
            }
            page_data.append(text_info)
        
        # Store the page's OCR data in the results dictionary
        ocr_results[f"page_{i + 1}"] = page_data
        print(f"Processed OCR for {image_path}")

    # Save OCR results to a JSON file
    json_output_path = os.path.join(output_dir, "ocr_results.json")
    with open(json_output_path, "w", encoding="utf-8") as json_file:
        json.dump(ocr_results, json_file, indent=4, ensure_ascii=False)
    print(f"OCR results saved to {json_output_path}")

    return json_output_path

if __name__ == "__main__":
    # Example usage
    ocr_json_path = perform_ocr(input_dir="data")
    print("OCR output saved to:", ocr_json_path)

