from flask import Flask, render_template
from model import generate_wireframe  # Import AI function

app = Flask(__name__)

@app.route("/")
def home():
    prompt = "login page with a form, a logo, and a submit button"
    ui_components = generate_wireframe(prompt)

    if not ui_components:
        ui_components = {
            "title": "Login Page",
            "logo": "static/logo.png",
            "form": {
                "fields": ["Username", "Password"],
                "button": "Submit"
            }
        }

    return render_template("wireframe.html", ui=ui_components)

if __name__ == "__main__":
    app.run(debug=True)
