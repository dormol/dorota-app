from flask import session

def init_session():
    if "art_mentor" not in session:
        session["art_mentor"] = {
            "user_level": "beginner",
            "current_module": "warmup",
            "completed_sessions": [],
            "progress": {
                "drawing": 1,
                "color": 1,
                "composition": 1
            },
            "last_exercise": None,
            "mentor_notes": []
        }

def get_state():
    return session.get("art_mentor", {})

def update_state(key, value):
    state = get_state()
    state[key] = value
    session["art_mentor"] = state

def add_progress(area, value=1):
    state = get_state()
    state["progress"][area] = state["progress"].get(area, 0) + value
    session["art_mentor"] = state

def set_module(module_name):
    state = get_state()
    state["current_module"] = module_name
    session["art_mentor"] = state

def save_mentor_note(note):
    state = get_state()
    state["mentor_notes"].append(note)
    session["art_mentor"] = state

