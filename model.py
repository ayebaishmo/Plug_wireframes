import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
genai.configure(api_key=API_KEY)

# Initialize model
model = genai.GenerativeModel("gemini-2.0-flash")

def generate_wireframe(prompt):
    structured_prompt = f"""
    Generate wireframe JSON with Excalidraw shapes for a {prompt}. Include:
    - Logo as a rectangle
    - Inputs as small rectangles with labels
    - Submit button as a rectangle
    The JSON should follow the Excalidraw data format.
    """
    
    try:
        response = model.generate_content(structured_prompt)
        
        # Log the raw response to check for issues
        print("Raw API Response:", response.text)
        
        # Try parsing the response text
        wireframe_data = json.loads(response.text)
        
        # Debugging the type of the response
        print(f"Response Type: {type(wireframe_data)}")
        
        # If the response is a list, wrap it in a dictionary
        if isinstance(wireframe_data, list):
            return {"elements": wireframe_data}
        
        # Return the response as is if it's an object
        return wireframe_data
    
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON from Gemini - {str(e)}")
        return {"error": "Invalid JSON response from Gemini"}
    except Exception as e:
        print(f"Error occurred: {e}")
        return {"error": str(e)}
