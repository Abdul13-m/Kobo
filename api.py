from flask import Flask, request, redirect, jsonify
from datetime import datetime
import requests
import base64

app = Flask(__name__)

# Function to generate Kobo editable link
def get_enketo_edit_url(_id):
    print(f"Processing _id: {_id}")
    
    # Step 1: Construct the base URL
    base_url = f"https://kf.kobo.iom.int/api/v2/assets/awSuNUXMitvmg5cNoCcLDj/data/{_id}/enketo/edit/?return_url=false"
    
    # Step 2: Generate the refresh token
    refresh_token = datetime.now().strftime("%Y%m%d%H%M%S")
    full_url_with_token = f"{base_url}&refreshToken={refresh_token}"
    print(f"Generated URL: {full_url_with_token}")

    # Step 3: Encode credentials using Base64
    credentials = "pak_dtm_admin:Ros9Pencil99"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded_credentials}"
    }

    # Step 4: Make the API request
    try:
        response = requests.get(full_url_with_token, headers=headers)
        response.raise_for_status()
        parsed_response = response.json()
        print(f"API Response: {parsed_response}")
        return parsed_response.get("url", "No URL Found")
    except Exception as e:
        print(f"Error for _id {_id}: {e}")
        return None

# Root route
@app.route('/')
def home():
    return "Welcome to the Kobo API! Use the /generate_link endpoint with an _id parameter to generate a link."

# API endpoint
@app.route("/generate_link", methods=["GET"])
def generate_link():
    _id = request.args.get("_id")
    print(f"Received _id: {_id}")  # Debug: Log received _id
    if not _id:
        return jsonify({"error": "Missing _id parameter"}), 400

    # Get the Kobo edit link
    link = get_enketo_edit_url(_id)
    if link:
        # Redirect directly to the Kobo link
        return redirect(link)
    else:
        return jsonify({"error": "Failed to generate the link"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8000)
