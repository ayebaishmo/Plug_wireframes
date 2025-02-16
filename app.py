from flask import Flask, render_template, request
import os
import google.generativeai as genai
from dotenv import load_dotenv
import requests

app = Flask(__name__)

load_dotenv()
FIGMA_FILE_ID = os.getenv("FIGMA_FILE_ID")
FIGMA_API = os.getenv("FIGMA_API")
gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)


def generate_wireframe(description):
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content(f"Generate a UI wireframe structure for {description}")
    return response.text

def send_to_figma(wireframe_data):
    url = f"https://api.figma.com/v1/files/{FIGMA_FILE_ID}/components"

    headers = {
            "X-Figma-Token": FIGMA_API,
            "Content-Type": "application/json"
        }
    data = {
            "name": "Generated Wireframe",
            "description": "Generated via AI",
            "components": wireframe_data
        }

    response = requests.post(url, headers=headers, json=data)
    print({response.content})
    print({response.status_code})
    return response.json()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        description = request.form.get("description")
        print(f"Received description: {description}")  # Debugging output
        
        wireframe_data = generate_wireframe(description)
        
        figma_response = send_to_figma(wireframe_data)
        
        return render_template("index.html", response=figma_response)
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
