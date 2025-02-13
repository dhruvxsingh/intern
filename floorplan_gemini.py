import os
import json
import base64
import requests
from io import BytesIO
from pdf2image import convert_from_path

# Configuration
API_KEY = "AIzaSyDcJykysOCIEf-HqmdC17hGczo1WdXX_Ic"
PDF_PATH = "Grandeur Floor Plan (1).pdf"
OUTPUT_JSON = "floor_plan_gemini.json"

def process_page(image):
    """Send image to Gemini API and parse response"""
    try:
        # Convert image to base64
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()

        # API request payload
        payload = {
            "contents": [{
                "parts": [
                    {
                        "text": """Analyze this architectural floor plan. List all rooms with dimensions in format:
                        - Room: [Name] | Dimensions: [Length x Width] | Area: [Area sqft]
                        Use exact measurements from the image. Skip non-essential elements."""
                    },
                    {
                        "inline_data": {
                            "mime_type": "image/png",
                            "data": img_base64
                        }
                    }
                ]
            }]
        }

        # API call
        response = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}",
            json=payload
        )
        response.raise_for_status()
        
        return response.json()
    
    except Exception as e:
        return {"error": str(e)}

# Main processing
results = {"pages": []}
try:
    images = convert_from_path(PDF_PATH)
    
    for page_num, image in enumerate(images, start=1):
        page_result = {
            "page_number": page_num,
            "status": "success",
            "rooms": []
        }
        
        try:
            # Process page with Gemini
            api_response = process_page(image)
            
            if "error" in api_response:
                page_result.update({
                    "status": "api_error",
                    "error": api_response["error"]
                })
            else:
                # Extract and parse response text
                text = api_response['candidates'][0]['content']['parts'][0]['text']
                
                # Parse rooms data
                for line in text.split('\n'):
                    line = line.strip()
                    if not line.startswith('- Room:'):
                        continue
                        
                    try:
                        parts = line.split('|')
                        room_data = {
                            "room": parts[0].split(': ')[1].strip(),
                            "dimensions": parts[1].split(': ')[1].strip(),
                            "area": parts[2].split(': ')[1].strip()
                        }
                        page_result["rooms"].append(room_data)
                    except Exception as parse_error:
                        print(f"Parse error on page {page_num}: {parse_error}")
                        continue

        except Exception as page_error:
            page_result.update({
                "status": "processing_error",
                "error": str(page_error)
            })
            
        results["pages"].append(page_result)

except Exception as main_error:
    results["error"] = str(main_error)

# Save results
with open(OUTPUT_JSON, 'w') as f:
    json.dump(results, f, indent=2)

print(f"Processing complete! Results saved to {OUTPUT_JSON}")