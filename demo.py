# from gradio_client import Client, handle_file
# from pdf2image import convert_from_path

# # Convert PDF to images
# images = convert_from_path("Grandeur Floor Plan (1).pdf")
# images[0].save("floor_plan_page_1.png", "PNG")

# # Ensure the file is saved before using handle_file
# img_file = "floor_plan_page_1.png"
# import os
# print(os.path.exists("floor_plan_page_1.png"))  # Should print True

# # Load the image using handle_file
# client = Client("fancyfeast/joy-caption-alpha-two")
# result = client.predict(
#     input_image=handle_file(img_file),  # Use local file
#     caption_type="Descriptive",
#     caption_length="long",
#     extra_options=[],
#     name_input="Hello!!",
#     custom_prompt="Hello!!",
#     api_name="/stream_chat",
# )

# print(result)
import re
from gradio_client import Client, handle_file
from pdf2image import convert_from_path

# Convert PDF to images
images = convert_from_path("Grandeur Floor Plan (1).pdf")
images[0].save("floor_plan_page_1.png", "PNG")

# Load the image using handle_file
img_file = "floor_plan_page_1.png"

client = Client("fancyfeast/joy-caption-alpha-two")
result = client.predict(
    input_image=handle_file(img_file),  # Use local file
    caption_type="Descriptive",
    caption_length="long",
    extra_options=[],
    name_input="Hello!!",
    custom_prompt="Hello!!",
    api_name="/stream_chat",
)

# Extract Room Names and Their Areas
text = result[1]  # Extracting the caption text
pattern = r"([A-Z\s]+) \((\d+)\)\" with dimensions (\d+)' x (\d+)'"  # Regex pattern
matches = re.findall(pattern, text)

# Format the extracted data
room_areas = {match[0].strip(): f"{int(match[2]) * int(match[3])} sq. ft" for match in matches}

# Print the extracted information
print("Extracted Room Areas:")
for room, area in room_areas.items():
    print(f"{room}: {area}")
