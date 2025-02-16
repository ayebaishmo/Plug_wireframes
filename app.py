from flask import Flask, render_template
from model import generate_wireframe

app = Flask(__name__)

@app.route("/")
def home():
    prompt = "login page with a form, logo, and submit button"
    wireframe_data = generate_wireframe(prompt)

    if not wireframe_data:
        wireframe_data = {"error": "Failed to generate wireframe."}
    
    return render_template("wireframe.html", wireframe=wireframe_data)

if __name__ == "__main__":
    app.run(debug=True)
