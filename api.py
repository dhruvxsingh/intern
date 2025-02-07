from flask import Flask, jsonify
from supabase import create_client, Client
import json

# Initialize Flask app
app = Flask(__name__)

# Supabase credentials
url = "https://orivuzqpjowmgjjxgvwh.supabase.co"  # Replace with your Supabase URL
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9yaXZ1enFwam93bWdqanhndndoIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczODg0ODA3MSwiZXhwIjoyMDU0NDI0MDcxfQ.NxgByv8fAqJuC8gSyFaAp5MZlyM-_0LCnr7GTWBLFhc"  # Replace with your Supabase API key

# Create Supabase client
supabase: Client = create_client(url, key)


@app.route("/properties", methods=["GET"])
def get_properties():
    """Get all properties from Supabase"""
    response = supabase.table("properties").select("*").execute()
    return jsonify(response.data)


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
    response = supabase.table("pdf").select("*").execute()
    print(response)
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

if __name__ == "__main__":
    # Run Flask app on the default port 5000
    app.run(host="0.0.0.0", port=8080, debug=True)
