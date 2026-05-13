from flask import Flask, request, render_template_string
from PIL import Image

app = Flask(__name__)

HTML = """
<h2>ART Dorota Studio Assistant</h2>

<form method="POST" enctype="multipart/form-data">
  <input type="file" name="image">
  <button type="submit">Analyze</button>
</form>
"""

def extract_colors(img):
    return []

def art_note():
    return "analysis"

@app.route("/", methods=["GET","POST"])
def home():
    colors = None
    note = ""

    if request.method == "POST":
        file = request.files["image"]
        img = Image.open(file)
        colors = extract_colors(img)
        note = art_note()

    return render_template_string(HTML, colors=colors, note=note)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
