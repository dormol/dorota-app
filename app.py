

from flask import Flask, request, render_template_string
from PIL import Image
import io

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Color Generator</title>
</head>
<body>
    <h1>Upload an image to extract colors</h1>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="image" required>
        <button type="submit">Submit</button>
    </form>
    
    {% if colors %}
    <h2>Detected Colors:</h2>

    <div style="display:flex; gap:10px; flex-wrap:wrap;">
        {% for c in colors %}
            <div style="
                width:60px;
                height:60px;
                background-color:{{ c }};
                border-radius:8px;
                border:1px solid #333;
                box-shadow:0 2px 6px rgba(0,0,0,0.2);
            "></div>
        {% endfor %}
    </div>

    <p style="margin-top:10px;">{{ colors }}</p>
{% endif %}    
    {% if note %}
        <h3>Note:</h3>
        <p>{{ note }}</p>
    {% endif %}
</body>
</html>
"""

def extract_colors(img):
    img = img.convert("RGB")
    img = img.resize((100, 100))

    pixels = list(img.getdata())

    color_count = {}

    for pixel in pixels:
        if pixel in color_count:
            color_count[pixel] += 1
        else:
            color_count[pixel] = 1

    sorted_colors = sorted(
        color_count.items(),
        key=lambda x: x[1],
        reverse=True
    )

    top_colors = []

    for color, count in sorted_colors[:5]:
        hex_color = '#%02x%02x%02x' % color
        top_colors.append(hex_color)

    return top_colors

def art_note():
    return "This is an automatic art note."    
@app.route("/", methods=["GET", "POST"])
def home():
    colors = None
    note = art_note()
    
    if request.method == "POST":
        print("FILES:", request.files)
        print("FORM:", request.form)
        file = request.files.get("image")
        
        if file is None or file.filename == "":
            return "No file uploaded", 400

        img = Image.open(file)
        colors = extract_colors(img)

    return render_template_string(HTML, colors=colors, note=note)

if __name__ == "__main__":
    app.run(debug=True) 




