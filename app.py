

from flask import Flask, request, render_template_string, session
from PIL import Image
import io

app = Flask(__name__)
app.secret_key = "art-mentor-dev-key"
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Color Generator</title>
</head>
<body>
    <h1>Upload an image to extract colors</h1>
    <form method="POST" enctype="multipart/form-data">
    <input type="file" name="image">
    <input type="submit" value="Upload Image">
    </form>
    
    {% if colors %}
  

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
    img = img.resize((150, 150))

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

    for color, count in sorted_colors[:12]:
        hex_color = '#%02x%02x%02x' % color
        top_colors.append(hex_color)

    return top_colors
MENTOR_RULES = {

    "horse": {
        "beginner": {
            "proportions": "Head to body approximately 1:3",
            "steps": [
                "Draw the action line",
                "Add ribcage and pelvis",
                "Connect body masses",
                "Add legs as simple cylinders"
            ]
        }
    },

    "face": {
        "beginner": {
            "proportions": "Eyes placed at the middle of the head",
            "steps": [
                "Draw an oval",
                "Add center line",
                "Place eye line",
                "Add nose and mouth"
            ]
        }
    },

    "figure": {
        "beginner": {
            "proportions": "Body approximately 7 heads tall",
            "steps": [
                "Draw vertical axis",
                "Add head unit",
                "Place ribcage and pelvis",
                "Add arms and legs"
            ]
        }
    },

    "flower": {
        "beginner": {
            "proportions": "Flowers structured around radial symmetry",
            "steps": [
                "Draw central stem line",
                "Block basic flower shape",
                "Divide into petals",
                "Refine overlaps",
                "Add leaves"
            ]
        }
    },

    "object": {
        "beginner": {
            "proportions": "Simple geometric construction: box/cylinder-based structure",
            "steps": [
                "Block basic form",
                "Construct perspective box",
                "Define proportions",
                "Refine silhouette"
            ]
        },
        "intermediate": {
            "proportions": "Add spatial depth and structural accuracy",
            "steps": [
                "Establish perspective lines",
                "Build 3D form",
                "Refine overlaps"
            ]
        },
        "advanced": {
            "proportions": "Full structural and perspective control",
            "steps": [
                "Analyze real object proportions",
                "Apply multi-point perspective",
                "Refine material and edge control"
            ]
        }
    }

}
    

def art_note():

    return "This is an automatic art note."
@app.route("/warmup", methods=["GET"])
def warmup():
    return """
    <h1>Art Mentor — Module 1: Warm-Up Engine</h1>

    <p>15-minute focus session</p>

    <button onclick="startWarmup()">Start Warm-Up</button>

    <h2 id="timer">15:00</h2>

    <script>
        let duration = 15 * 60;
        let interval;

        function startWarmup() {
            if (interval) return;

            interval = setInterval(() => {
                let minutes = Math.floor(duration / 60);
                let seconds = duration % 60;

                document.getElementById("timer").innerText =
                    String(minutes).padStart(2,'0') + ":" + String(seconds).padStart(2,'0');

                duration--;

                if (duration < 0) {
                    clearInterval(interval);
                    document.getElementById("timer").innerText = "DONE";
                }
            }, 1000);
        }
    </script>
    """

@app.route("/sketch", methods=["GET", "POST"])
def sketch():

    feedback = None
    prompt = ""
    level = "beginner"

    if request.method == "POST":

        level = request.form.get("level", "Beginner").lower()
        prompt = request.form.get("prompt", "").lower()

        category = None

        if any(x in prompt for x in ["face", "portrait"]):
            category = "face"

        elif "horse" in prompt:
            category = "horse"

        elif any(x in prompt for x in ["figure", "anatomy", "gesture"]):
            category = "figure"

        elif any(x in prompt for x in ["flower", "rose", "tulip"]):
            category = "flower"

        elif any(x in prompt for x in ["cup", "chair", "table", "phone", "object"]):
            category = "object"

        elif any(x in prompt for x in ["landscape", "tree", "mountain"]):
            category = "landscape"

        if category:
            feedback = MENTOR_RULES[category].get(
                level,
                MENTOR_RULES[category]["beginner"]
            )

    feedback_html = ""

    if feedback:
        feedback_html += "<h3>Proportions</h3>"
        feedback_html += f"<p>{feedback['proportions']}</p>"

        feedback_html += "<h3>Construction Steps</h3><ol>"

        for step in feedback["steps"]:
            feedback_html += f"<li>{step}</li>"

        feedback_html += "</ol>"

    else:
        feedback_html = """
        <p>
        Enter a classical drawing subject such as:
        face, figure, flower, horse, object, or landscape.
        </p>
        """

    return f"""
    <h1>Art Mentor — Sketch Engine v2</h1>

    <form method="POST">

        <h2>Select Level</h2>

        <input type="radio" name="level" value="Beginner" checked> Beginner<br>
        <input type="radio" name="level" value="Intermediate"> Intermediate<br>
        <input type="radio" name="level" value="Advanced"> Advanced<br>

        <h2>What would you like to draw?</h2>

        <input type="text" name="prompt" style="width:320px;">

        <br><br>

        <button type="submit">Generate Mentor Guidance</button>

    </form>

    <hr>

    <h2>Mentor Guidance</h2>

    {feedback_html}
    """

        
    
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
@app.route("/app", methods=["GET", "POST"])
def app_controller():

    if "module" not in session:
        session["module"] = 1
        session["level"] = "Beginner"

    action = request.args.get("go")

    if action:
        session["module"] = int(action)

    module = session["module"]

    if module == 1:
        return warmup()

    elif module == 2:
        return sketch()

    elif module == 3:
        return render_template_string("<h1>Module 3 - Composition</h1>")

    elif module == 4:
        return render_template_string("<h1>Module 4 - Color Studio</h1>")

    elif module == 5:
        return render_template_string("<h1>Module 5 - Medium Studio</h1>")

    elif module == 6:
        return render_template_string("<h1>Module 6 - Painting Session</h1>")

    elif module == 7:
        return render_template_string("<h1>Module 7 - Mentor Review</h1>")

    else:
        session["module"] = 1
        return warmup()


if __name__ == "__main__":
    app.run(debug=True)

    
















