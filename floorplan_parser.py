import json
import io
import re
import easyocr
from pdf2image import convert_from_path
import numpy as np

def extract_text_with_images(pdf_path):
    reader = easyocr.Reader(['en'], gpu=False)
    
    poppler_path = r"C:\Users\Dhruv_Baller\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin"
    
    try:
        # Convert PDF pages to images
        images = convert_from_path(pdf_path, poppler_path=poppler_path)
        text_content = ""
    
        for page_number, image in enumerate(images, start=1):
            # Convert PIL Image to numpy array
            image_np = np.array(image)
            
            # Perform OCR on the numpy array
            ocr_result = reader.readtext(image_np, detail=0)
            text_content += f"\n[OCR Page {page_number}]:\n" + "\n".join(ocr_result)
            # print(f"Processing page {page_number}...")
            print(f"Found text: {ocr_result}")
        
        return text_content.strip()
    
    except Exception as e:
        return f"Error processing PDF: {e}"

def parse_floor_plan(text):
    """Parse the extracted text and find rooms and dimensions."""
    # Updated pattern to catch more dimension formats
    patterns = [
        r'\((\d+)[xX](\d+)\)',  # (10x12) format
        r'(\d+)\s*[xX]\s*(\d+)',  # 10 x 12 format
        r'(\d+)\'[\s-]*(\d+)\'',  # 10'-12' format
    ]
    
    rooms = []
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    room_candidate = None
    
    for line in lines:
        dimension_found = False
        # Try all patterns
        for pattern in patterns:
            match = re.search(pattern, line)
            if match:
                dimension_found = True
                dimension = f"{match.group(1)}X{match.group(2)}"
                area = int(match.group(1)) * int(match.group(2))
                
                # Extract room name
                parts = line.split(match.group(0))
                room_part = parts[0].strip() if parts[0].strip() else room_candidate
                
                if room_part:
                    rooms.append({
                        "room": room_part,
                        "dimensions": dimension,
                        "area_sqft": area
                    })
                break
        
        if not dimension_found:
            # Store as potential room name for next line
            room_candidate = line if line else room_candidate

    # Filter out non-room entries
    filtered_rooms = [
        room for room in rooms
        if len(room["room"]) > 2 and not re.match(r'^[A-Z]+\d+$', room["room"])
    ]
    
    return filtered_rooms

def process_pdf(pdf_path):
    """Process PDF to extract and parse floor plan details."""
    try:
        # Extract text using EasyOCR for embedded images and text
        print("Starting text extraction...")
        extracted_text = extract_text_with_images(pdf_path)
        # print("Extracted text:", extracted_text)
        
        rooms = parse_floor_plan(extracted_text)
        
        # Add default entries if no rooms found
        if not rooms:
            print("No rooms detected. Adding common room types...")
            default_rooms = [
                {"room": "Master Bedroom", "dimensions": "Unknown", "area_sqft": 0},
                {"room": "Kitchen", "dimensions": "Unknown", "area_sqft": 0},
                {"room": "Living Room", "dimensions": "Unknown", "area_sqft": 0},
                {"room": "Bathroom", "dimensions": "Unknown", "area_sqft": 0}
            ]
            rooms.extend(default_rooms)
        
        # Output the result as JSON
        return json.dumps(rooms, indent=2)
    except Exception as e:
        print(f"Error details: {str(e)}")
        return f"An error occurred: {e}"

# Path to the PDF file
pdf_path = "Grandeur Floor Plan (1).pdf"
print("Starting PDF processing...")
result = process_pdf(pdf_path)
print("Final result:")
# print(result)