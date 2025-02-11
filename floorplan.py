from pdf2image import convert_from_path
from gradio_client import Client, handle_file

# Convert PDF to images
images = convert_from_path('Grandeur Floor Plan (1).pdf')
images[0].save('floor_plan_page_1.png', 'PNG') 
images[1].save('floor_plan_page_2.png', 'PNG') 

client = Client("fancyfeast/joy-caption-alpha-two")

result = client.predict(
    input_image=handle_file('floor_plan_page_1.png'),
)

print(result)