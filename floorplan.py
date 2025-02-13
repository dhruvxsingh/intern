# from pdf2image import convert_from_path
# from gradio_client import Client, handle_file

# # Convert PDF to images
# images = convert_from_path('Grandeur Floor Plan (1).pdf')
# images[0].save('floor_plan_page_1.png', 'PNG') 
# images[1].save('floor_plan_page_2.png', 'PNG') 

# client = Client("fancyfeast/joy-caption-alpha-two")
# result = client.predict(
# 		input_image=handle_file('floor_plan_page_1.png'),
# 		caption_type="Descriptive",
# 		caption_length="long",
# 		extra_options=[],
# 		name_input="Hello!!",
# 		custom_prompt="""Analyze this floor plan and list all rooms with their dimensions. 
#         Output format: 
#         Room: [Name], Dimensions: [Length x Width], Area: [Area sqft]. 
#         Skip descriptions; focus only on numbers and names.""",
# 		api_name="/stream_chat"
# )
# print(result)
import os
import json
import tempfile
from pdf2image import convert_from_path
from gradio_client import Client, handle_file

# Initialize Molmo AI client
client = Client("fancyfeast/joy-caption-alpha-two")

# Convert PDF to images
images = convert_from_path('Grandeur Floor Plan (1).pdf')

# Process all pages
output = {"pages": []}

with tempfile.TemporaryDirectory() as temp_dir:
    for page_num, image in enumerate(images, start=1):
        try:
            # Save image to temp file
            temp_path = os.path.join(temp_dir, f"page_{page_num}.png")
            image.save(temp_path, "PNG")
            
            # Process with Molmo AI
            result = client.predict(
                input_image=handle_file(temp_path),
                caption_type="Descriptive",
                caption_length="long",
                extra_options=[],
                name_input="N/A",
                custom_prompt="""Analyze this floor plan and list all rooms with dimensions. 
                Output format: 
                Room: [Name], Dimensions: [Length x Width], Area: [Area sqft].
                Only include numbered room data.""",
                api_name="/stream_chat"
            )
            
            # Parse the caption into structured data
            rooms = []
            for line in result[1].split('\n'):
                if "Room:" in line:
                    parts = line.strip('- ').split(', ')
                    room_data = {
                        "room": parts[0].split(': ')[1],
                        "dimensions": parts[1].split(': ')[1],
                        "area": parts[2].split(': ')[1]
                    }
                    rooms.append(room_data)
            
            output["pages"].append({
                "page_number": page_num,
                "status": "success",
                "rooms": rooms
            })
            
        except Exception as e:
            output["pages"].append({
                "page_number": page_num,
                "status": "error",
                "error": str(e),
                "rooms": []
            })

# Save to JSON
with open("floor_plan_data.json", "w") as f:
    json.dump(output, f, indent=2)

print("Processing complete! Check floor_plan_data.json")
