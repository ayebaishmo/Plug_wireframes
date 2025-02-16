from flask import Flask, render_template, request
import os
import google.generativeai as genai
from dotenv import load_dotenv
import requests

app = Flask(__name__)

load_dotenv()

FIGMA_FILE_ID = os.getenv("FIGMA_FILE_ID", "")
FIGMA_ACCESS_TOKEN = os.getenv("FIGMA_ACCESS_TOKEN", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

if not FIGMA_FILE_ID or not FIGMA_ACCESS_TOKEN or not GEMINI_API_KEY:
    raise ValueError("Missing required API keys. Check .env file!")

genai.configure(api_key=GEMINI_API_KEY)


def generate_wireframe(description):
    """Generate wireframe structure using Gemini AI"""
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content(f"Generate a UI wireframe structure for {description}")
    return response.text


def get_figma_file():
    """Fetch Figma file data"""
    url = f"https://api.figma.com/v1/files/{FIGMA_FILE_ID}"

    headers = {
        "X-Figma-Token": FIGMA_ACCESS_TOKEN
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve file. Status code: {response.status_code}")
        print(response.content)
        return None


@app.route("/", methods=["GET", "POST"])
def index():
    """Main page to input description and retrieve wireframe"""
    if request.method == "POST":
        description = request.form.get("description")
        print(f"Received description: {description}")  
        
        wireframe_data = generate_wireframe(description)
        
        figma_data = get_figma_file()  
        
        return render_template("index.html", response=figma_data, wireframe=wireframe_data)
    
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
