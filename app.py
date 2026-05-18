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
    img = img.resize((100, 100))
    pixels = list(img.getdata())

    r = sum(p[0] for p in pixels) / len(pixels)
    g = sum(p[1] for p in pixels) / len(pixels)
    b = sum(p[2] for p in pixels) / len(pixels)

    brightness = (r + g + b) / 3

    return {
        "avg_rgb": (int(r), int(g), int(b)),
        "brightness": round(brightness, 2)
    }

def art_note():
    return ""    
@app.route("/", methods=["GET","POST"])
def home():
    colors = None
    note = ""

    if request.method == "POST":
        file = request.files.get("image")

        if file is None or file.filename == "":
            return "No file uploaded", 400

        img = Image.open(file)
        colors = extract_colors(img)
        note = art_note()
        return render_template_string(HTML, colors=colors, note=note)

if __name__ == "__main__":
    app.run(debug=True)


 
