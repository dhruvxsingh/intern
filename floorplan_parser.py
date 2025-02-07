import pdf2image
import pytesseract
import re
import json
from pytesseract import Output

# Function to extract text from PDF using OCR
def extract_text_from_pdf(pdf_path):
    # Convert PDF pages to images
    images = pdf2image.convert_from_path(pdf_path)
    extracted_text = []

    # Perform OCR on each image
    for image in images:
        text = pytesseract.image_to_string(image, config='--psm 6')  # PSM 6 for sparse text
        extracted_text.append(text)
    
    return extracted_text

# Function to parse extracted text and extract rooms and dimensions
def parse_floor_plan(text):
    pattern = re.compile(r'\((\d+)[xX](\d+)\)')  # Matches dimensions like (numberXnumber)
    rooms = []

    for page_text in text:
        lines = [line.strip() for line in page_text.split('\n') if line.strip()]
        
        room_candidate = None
        for line in lines:
            # Check for dimension pattern
            match = re.search(pattern, line)
            if match:
                dimension = f"{match.group(1)}X{match.group(2)}"
                area = int(match.group(1)) * int(match.group(2))
                # Extract room name: part before dimension or previous line
                parts = line.split(match.group(0))
                room_part = parts[0].strip() if parts[0].strip() else room_candidate
                if room_part:
                    rooms.append({
                        "room": room_part,
                        "dimensions": dimension,
                        "area_sqft": area
                    })
                room_candidate = None  # Reset candidate after capture
            else:
                # Assume current line is a potential room name for next dimension
                room_candidate = line if line else room_candidate
    
    # Filter out non-room entries (e.g., D1, D2)
    filtered_rooms = [
        room for room in rooms
        if len(room["room"]) > 2 and not re.match(r'^[A-Z]+\d+$', room["room"])
    ]
    return filtered_rooms

# Main function to process the PDF
def process_pdf(pdf_path):
    # Step 1: Extract text from PDF using OCR
    extracted_text = extract_text_from_pdf(pdf_path)
    
    # Step 2: Parse the extracted text
    rooms = parse_floor_plan(extracted_text)
    
    # Step 3: Output the result as JSON
    return json.dumps(rooms, indent=2)

# Path to the PDF file
pdf_path = "Grandeur Floor Plan (1).pdf"

# Process the PDF and print the result
result = process_pdf(pdf_path)
print(result)