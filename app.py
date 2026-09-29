

from flask import Flask, request, render_template_string, session
from PIL import Image

from core.session_manager import init_session, set_module, get_state
import io

app = Flask(__name__)

@app.before_request
def start_session():
    init_session()
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
    "animals": {
        "beginner": {
            "proportions": "Head to body approximately 1:3",
            "steps": [
                "Draw the action line",
                "Add ribcage and pelvis",
                "Connect body masses",
                "Add legs as simple cylinders"
            ]
        },
        "intermediate": {
            "proportions": "Study the animal through gesture, anatomy, weight, and the relationship of the major body masses.",
            "steps": [
                "Establish the main gesture and weight distribution",
                "Construct the ribcage, pelvis, and major joints",
                "Observe anatomical relationships and proportion",
                "Develop the legs, head, and characteristic features",
                "Refine the drawing while preserving the original gesture"
            ]
        },
        "advanced": {
            "proportions": "Develop the animal through anatomy, structure, gesture, rhythm, weight, and individual character.",
            "steps": [
                "Analyze the gesture, balance, and weight shift",
                "Construct the anatomy beneath the visible surface",
                "Study subtle proportional and structural relationships",
                "Develop individual character, movement, and surface",
                "Refine the drawing while maintaining convincing underlying construction"
            ]
        }
    },

    "portrait_face": {
        "beginner": {
            "proportions": "Use the head as the basic unit; establish the center line and eye line before features.",
            "steps": [
                "Draw the basic head shape",
                "Establish the vertical center line",
                "Place the eye line and major facial divisions",
                "Construct the nose, mouth, and jaw",
                "Refine features while preserving the whole head structure"
            ]
        },
        "intermediate": {
            "proportions": "Relate facial features to the underlying skull structure and observe individual proportions.",
            "steps": [
                "Analyze the head planes and axis",
                "Establish individual facial proportions",
                "Construct the brow, nose, cheekbones, and jaw",
                "Develop feature relationships and asymmetry",
                "Refine form through value and edge control"
            ]
        },
        "advanced": {
            "proportions": "Control individual anatomy, perspective, expression, and subtle proportional relationships.",
            "steps": [
                "Analyze the complete anatomical structure of the head",
                "Establish perspective and individual proportions",
                "Construct planes and turning forms",
                "Develop expression and character",
                "Refine subtle value, edge, and material relationships"
            ]
        }
    },

    "figure": {
        "beginner": {
            "proportions": "Use a simple head-unit system to establish the overall figure and major body masses.",
            "steps": [
                "Draw the action line",
                "Establish the head unit",
                "Place the ribcage and pelvis",
                "Connect the major body masses",
                "Add arms and legs as simple forms"
            ]
        },
        "intermediate": {
            "proportions": "Relate body proportions to anatomy, balance, weight, and gesture.",
            "steps": [
                "Analyze gesture and line of action",
                "Construct the ribcage, pelvis, and spine",
                "Establish weight-bearing relationships",
                "Build limbs with anatomical landmarks",
                "Refine the figure through overlapping forms"
            ]
        },
        "advanced": {
            "proportions": "Control anatomy, gesture, balance, foreshortening, and individual structure.",
            "steps": [
                "Analyze the complete gesture and structural rhythm",
                "Construct anatomical masses in perspective",
                "Control balance, weight, and foreshortening",
                "Develop anatomical landmarks and surface structure",
                "Refine the figure while preserving gesture and character"
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
        },
        "intermediate": {
            "proportions": "Study the flower through botanical structure, rhythm, overlapping petals, and the relationship between flower, stem, and leaves.",
            "steps": [
                "Observe the underlying structure of the flower",
                "Establish the stem and major directional rhythms",
                "Construct overlapping petals and their perspective",
                "Relate the flower to its leaves and supporting forms",
                "Refine details while preserving the overall structure"
            ]
        },
        "advanced": {
            "proportions": "Develop the flower through botanical structure, spatial depth, rhythm, proportion, light, and individual character.",
            "steps": [
                "Analyze the botanical structure and growth pattern",
                "Establish spatial depth and overlapping forms",
                "Develop subtle variations in petal shape and rhythm",
                "Observe light, value, texture, and surface",
                "Refine the drawing while preserving the living character of the plant"
            ]
        }
    },

    "landscape": {
        "beginner": {
            "proportions": "Establish the horizon, major land masses, and depth before adding details",
            "steps": [
                "Observe the horizon and main direction of the landscape",
                "Block the largest land and sky shapes",
                "Establish foreground, middle ground, and background",
                "Add major forms such as trees, mountains, or buildings",
                "Refine details without losing the overall structure"
            ]
        },
        "intermediate": {
            "proportions": "Use spatial relationships and atmospheric depth to organize the landscape",
            "steps": [
                "Analyze the horizon and perspective structure",
                "Establish major planes and depth relationships",
                "Organize foreground, middle ground, and background",
                "Develop overlapping forms and atmospheric perspective",
                "Refine the composition while preserving depth"
            ]
        },
        "advanced": {
            "proportions": "Control complex spatial relationships, perspective, scale, and atmospheric depth",
            "steps": [
                "Analyze the complete spatial structure of the scene",
                "Establish perspective, scale, and major compositional relationships",
                "Construct complex overlapping forms",
                "Control atmospheric perspective and visual hierarchy",
                "Refine detail, edges, and tonal relationships in service of the composition"
            ]
        }
    },

    "still_life": {
        "beginner": {
            "proportions": "Arrange simple objects by observing their basic shapes, relative size, placement, and overlap.",
            "steps": [
                "Choose two or three simple objects",
                "Observe the overall arrangement and proportions",
                "Block the largest shapes",
                "Establish overlaps and placement",
                "Refine the silhouettes while preserving the whole arrangement"
            ]
        },
        "intermediate": {
            "proportions": "Develop the still life through proportion, perspective, spatial relationships, overlap, and tonal structure.",
            "steps": [
                "Analyze the relationships between all objects",
                "Establish accurate proportions and perspective",
                "Develop overlaps and negative spaces",
                "Organize the major light and shadow masses",
                "Refine individual objects without losing the unity of the arrangement"
            ]
        },
        "advanced": {
            "proportions": "Develop a convincing still life through composition, proportion, perspective, value, material, light, and spatial depth.",
            "steps": [
                "Analyze the composition and visual hierarchy",
                "Establish precise spatial and proportional relationships",
                "Develop perspective, overlap, and negative space",
                "Observe material differences through value, edge, and texture",
                "Refine the entire arrangement while maintaining compositional unity"
            ]
        }
    },

    "everyday_objects": {
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
            category = "animals"

        elif any(x in prompt for x in ["figure", "anatomy", "gesture"]):
            category = "figure"

        elif any(x in prompt for x in ["flower", "rose", "tulip"]):
            category = "flower"

        elif any(x in prompt for x in ["cup", "chair", "table", "phone", "object"]):
            category = "everyday_objects"

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




    
@app.route("/app/module/<name>")
def module_router(name):

    set_module(name)

    state = get_state()

    return f"""
    <h1>Art Mentor Studio</h1>

    <h2>Module: {name}</h2>

    <p>User Level: {state.get('user_level')}</p>

    <p>Progress:</p>

    <pre>{state.get('progress')}</pre>

    <hr>

    <a href="/app/module/warmup">Warm-Up</a><br>

    <a href="/app/module/sketch">Sketch Engine</a><br>

    <a href="/app/module/color">Color Studio</a><br>

    <a href="/app/module/review">Mentor Review</a><br>
    """
if __name__ == "__main__":
    app.run(debug=True)

    





