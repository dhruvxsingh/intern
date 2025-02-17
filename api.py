from flask import request,Flask, jsonify
from supabase import create_client, Client
import json
from flask_cors import CORS
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from realestate.spiders.properties_spider import PropertiesSpider
import threading
import subprocess
import os
from dotenv import load_dotenv

# Initialize Flask app
app = Flask(__name__)
cors = CORS(app)

load_dotenv()

# Supabase credentials
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
# Create Supabase client
supabase: Client = create_client(url, key)

@app.route("/properties", methods=["GET"])
def get_properties():
    """Get all properties from Supabase"""
    response = supabase.table("properties").select("*").execute()
    return jsonify(response.data)

@app.route('/')
def home():
    return 'Home Page Route'

@app.route('/url', methods=["POST"])
def url_post():
    data = request.get_json()

    # Extract the 'url' value from the request body
    url = data.get('url')
    print(f"URL Received: {url}")

    # Optionally, process the 'url' or perform any action
    if not url:
        return jsonify({"message": "URL parameter is required"}), 400

    try:
        # Define the output file for the Scrapy spider
        output_file = 'output.json'  # You can modify the path if needed

        # Run the Scrapy process in a separate subprocess with the output file defined
        process=subprocess.Popen(['scrapy', 'crawl', 'properties', '-o', output_file, '-a', f'url={url}'])
        process.wait()
        with open(output_file, "r") as file:
            properties = json.load(file)

        # Iterate over the scraped properties and insert them into the Supabase database
        for property_data in properties:
            data = {
                "name": property_data.get("name"),
                "location": property_data.get("location"),
                "price": property_data.get("price"),
                "area": property_data.get("area"),
                "bedrooms": property_data.get("bedrooms"),
                "url": property_data.get("url"),
            }

            # Insert data into Supabase
            response = supabase.table("properties").insert(data).execute()
            print(f"Inserted property: {data['name']} into database.")
            os.remove(output_file)
            print(f"Removed {output_file} after processing.")
        return jsonify({"message": f"Scrapy spider started for {url}!"}), 200
    except Exception as e:
        return jsonify({"message": "Error running spider", "error": str(e)}), 500



@app.route("/post", methods=["GET"])
def post_properties():
    try:
        with open("output.json", "r") as file:
            properties = json.load(file)

        for property_data in properties:
            data = {
                "name": property_data.get("name"),
                "location": property_data.get("location"),
                "price": property_data.get("price"),
                "area": property_data.get("area"),
                "bedrooms": property_data.get("bedrooms"),
                "url": property_data.get("url"),
            }
            # Insert data into Supabase
            response = supabase.table("properties").insert(data).execute()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/brochure-data", methods=["GET"])
def get_propertie():
    """Get all properties from Supabase"""
    property_name = request.args.get("property")
    response = supabase.table("pdf").select("*").eq("property_name", property_name).execute()
    return jsonify(response.data)


@app.route("/brochure-fulldata", methods=["GET"])
def getfull_propertie():
    """Get all properties from Supabase"""
    response = supabase.table("pdf").select("*").execute()
    return jsonify(response.data)


@app.route("/pdf", methods=["GET"])
def post_properties_pdf():
    try:
        with open("property_details.json", "r") as file:
            properties = json.load(file)

            

        for property_data in properties:
            data = {
                "property_name": property_data.get("property_name"),
                "price_range": property_data.get("price_range"),
                "amenities": property_data.get("price"),
                "available_units": property_data.get("available_units"),
            }
            # Insert data into Supabase
            response = supabase.table("pdf").insert(data).execute()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/full-details", methods=["GET"])
def post_properties_full():
    property_name = request.args.get("property")
    pdf_response = supabase.table("pdf").select("*").eq("property_name", property_name).execute()
    properties_response = supabase.table("properties").select("*").eq("name", property_name).execute()

    if not pdf_response.data or not properties_response.data:
        return jsonify({"message": "No data available in one or both tables."}), 404

    combined_data = []
    combined_entry = {
                "property_name": pdf_response.data[0]['property_name'],
                "location": properties_response.data[0]['location'],
                "price_range": pdf_response.data[0]['price_range'],
                "available_units": pdf_response.data[0]['available_units'],
                "area": properties_response.data[0]['area'],
                "bedrooms":properties_response.data[0]['bedrooms'],
                "amenities":pdf_response.data[0]['amenities'],
                "url": properties_response.data[0]['url']  
            }
    combined_data.append(combined_entry)
    return jsonify(combined_data)


# from gradio_client import Client, handle_file

# client = Client("fancyfeast/joy-caption-alpha-two")
# result = client.predict(
# 		input_image=handle_file('https://raw.githubusercontent.com/gradio-app/gradio/main/test/test_files/bus.png'),
# 		caption_type="Descriptive",
# 		caption_length="long",
# 		extra_options=[],
# 		name_input="Hello!!",
# 		custom_prompt="Hello!!",
# 		api_name="/stream_chat"
# )
# print(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
