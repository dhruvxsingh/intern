import fitz
import re
import json

def extract_numbers_from_text(text):
    return [float(num) for num in re.findall(r'\d+(?:,\d+)*(?:\.\d+)?', text)]

def parse_pdf(pdf_path):
    # Open the PDF file
    doc = fitz.open(pdf_path)
    
    # Get all text from the first page
    text = doc[0].get_text()
    
    # Extract property name using regex
    property_name_match = re.search(r'(.*?)\s+is\s+an\s+exclusive', text)
    property_name = property_name_match.group(1) if property_name_match else "Unknown"
    
    # Extract areas using regex
    area_pattern = r'(\d+(?:,\d+)*(?:\.\d+)?)\s*[Ss]quare\s*[Ff]eet'
    areas = [float(area.replace(',', '')) for area in re.findall(area_pattern, text)]
    
    # Extract rate per square feet
    rate_pattern = r'(\d+(?:,\d+)*(?:\.\d+)?)\s*Rupees\s+per\s+Square\s+feet'
    rate_match = re.search(rate_pattern, text)
    rate_per_sqft = float(rate_match.group(1).replace(',', '')) if rate_match else None
    
    # Calculate price range
    if areas and rate_per_sqft:
        min_price = min(areas) * rate_per_sqft / 100000  # Convert to lakhs
        max_price = max(areas) * rate_per_sqft / 100000  # Convert to lakhs
        price_range = f"₹{min_price:.2f}L - ₹{max_price:.2f}L"
    else:
        price_range = "Price not available"
    
    # Extract available units
    units_pattern = r'comprises\s+(\w+)\s+meticulously'
    units_match = re.search(units_pattern, text)
    available_units = {
        'six': 6, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10
    }.get(units_match.group(1).lower() if units_match else '', 0)
    
    # Extract only modern amenities
    amenities = []
    modern_amenities_section = False
    for line in text.split('\n'):
        if 'Modern Amenities:' in line:
            modern_amenities_section = True
            continue
        elif 'High-Quality Specifications:' in line:
            modern_amenities_section = False
            continue
            
        if modern_amenities_section and (line.strip().startswith('o') or line.strip().startswith('•')):
            amenity = line.strip().replace('o', '').replace('•', '').strip()
            if amenity:
                amenities.append(amenity)
    
    # Create the JSON structure
    output = {
        "property_name": property_name,
        "price_range": price_range,
        "available_units": available_units,
        "amenities": json.dumps(amenities)
    }
    
    # Close the PDF
    doc.close()
    
    return output

def save_to_json(data, output_path):
    data = [data]
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    pdf_path = r"E:\intern\realestate\Rohini_Grandeur (1).pdf"  # Update with your PDF path
    output_path = "property_details.json"
    
    try:
        result = parse_pdf(pdf_path)
        save_to_json(result, output_path)
        print("Successfully parsed PDF and saved to JSON:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error processing PDF: {str(e)}")