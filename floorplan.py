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
from dotenv import load_dotenv

load_dotenv()

client = Client(os.getenv("MOLMO_KEY")) 
images = convert_from_path('Grandeur Floor Plan (1).pdf')

output = {"pages": []}

with tempfile.TemporaryDirectory() as temp_dir:
    for page_num, image in enumerate(images, start=1):
        try:
            temp_path = os.path.join(temp_dir, f"page_{page_num}.png")
            image.save(temp_path, "PNG")
            
            result = client.predict(
                input_image=handle_file(temp_path),
                caption_type="Descriptive",
                caption_length="long",
                extra_options=[],
                name_input="N/A",
                custom_prompt="""Analyze this floor plan. List ALL rooms with dimensions 
                in format: [Room Name] ([Length]X[Width]). Include ONLY numbered rooms 
                and main spaces like kitchen, bedroom, toilet.""",
                api_name="/stream_chat"
            )

            # Extract the actual response
            caption = result[1] if isinstance(result, tuple) else str(result)
            
            # Improved parsing for numbered list format
            rooms = []
            for line in caption.split('\n'):
                line = line.strip()
                
                # Handle numbered items like "1. Kitchen (4.2X3.6)"
                if line and line[0].isdigit() and '(' in line:
                    try:
                        # Remove numbering and split components
                        clean_line = line.split('.', 1)[1].strip()
                        room_part, dim_part = clean_line.split('(', 1)
                        
                        room_name = room_part.strip()
                        dimensions = dim_part.split(')')[0].strip().lower().replace('x', 'X')
                        
                        # Convert to float dimensions
                        length, width = map(float, dimensions.split('X'))
                        area = round(length * width, 2)
                        
                        rooms.append({
                            "room": room_name,
                            "dimensions": f"{length}X{width}",
                            "area": f"{area} sqm"  # Assuming meters from decimal values
                        })
                    except Exception as e:
                        print(f"Skipping line: {line} - Error: {str(e)}")
                        continue

            output["pages"].append({
                "page_number": page_num,
                "status": "success" if rooms else "empty",
                "rooms": rooms
            })
            
        except Exception as e:
            # Handle quota error specifically
            error_msg = str(e)
            if "GPU quota" in error_msg:
                error_msg += "\nSolution: Create a free Hugging Face account at https://huggingface.co/join"
                
            output["pages"].append({
                "page_number": page_num,
                "status": "error",
                "error": error_msg,
                "rooms": []
            })

with open("floor_plan_data.json", "w") as f:
    json.dump(output, f, indent=2)

print("Processing complete!")