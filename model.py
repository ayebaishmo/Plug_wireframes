import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("API_KEY")
genai.configure(api_key=API_KEY)

# Initialize model
model = genai.GenerativeModel("gemini-2.0-flash")

def generate_wireframe(prompt):
    structured_prompt = f"""
    Generate a wireframe description in JSON format for a {prompt}.
    The JSON should have the following structure:
    {{
        "title": "Page Title",
        "logo": "static/logo.png",
        "form": {{
            "fields": ["Username", "Password"],
            "button": "Submit"
        }}
    }}
    Return only valid JSON with no extra text.
    """

    response = model.generate_content(structured_prompt)
    
    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        print("Error: Gemini returned invalid JSON.")

if __name__ == "__main__":
    prompt = "login page with a form, a logo, and a submit button"
    design_specs = generate_wireframe(prompt)
    print(design_specs)
