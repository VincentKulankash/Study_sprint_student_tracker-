from flask import Flask, jsonify, request, send_from_directory, session, make_response

app = Flask(__name__, static_folder="static")

# Flask uses SECRET_KEY to sign session cookies.
# TODO: Replace this classroom value with a safer secret in a real application.
app.config["SECRET_KEY"] = "change-this-secret-key-for-class-demo"


# In-memory data for this practical.
# NOTE: Restarting the Flask server resets this list.
study_sessions = [
    {"id": 1, "topic": "Understand GET requests", "minutes": 25, "completed": False},
    {"id": 2, "topic": "Practice Flask routes", "minutes": 30, "completed": False},
]


def find_study_session(session_id):
    """Helper supplied for students: find one study sprint by its id."""
    for item in study_sessions:
        if item["id"] == session_id:
            return item
    return None


# -----------------------------------------------------------------------------
# STARTING ROUTES PROVIDED TO STUDENTS
# -----------------------------------------------------------------------------

@app.route("/")
def index():
    """Serve the supplied client-side application."""
    return send_from_directory(app.static_folder, "index.html")


@app.route("/api/study-sessions", methods=["GET"])
def get_study_sessions():
    """READ: Return all study sprints as JSON."""
    return jsonify(study_sessions), 200


# -----------------------------------------------------------------------------
# STUDENT TODO AREA
# Build the routes below yourself. Read README.md and static/js/app.js first.
# The comments intentionally give hints without giving the solutions.
# -----------------------------------------------------------------------------

# TODO 1 - SESSION + COOKIE READ
# Endpoint: GET /api/me
# Goal:
#   - Read the learner's username from Flask session storage.
#   - Keep a session-based visit counter and increase it on each request.
#   - Read the non-sensitive "focus_mode" cookie from the incoming request.
#   - Return username, visits, and focus_mode as JSON.
# Hint: session.get(...) and request.cookies.get(...) may help.

#Successfully implemented login
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json(silent=True) or {}
    username= data.get('username')

    if not isinstance(username, str):
        return jsonify({'Error': 'Username is required.'}), 400

    username = username.strip()
    if not username:
        return jsonify({'Error': 'Username is required.'}), 400

    session['username'] = username
    session['visits'] = 0

    return jsonify({
        'message' : 'Login Successful',
        'username' : username,
        }), 200


# TODO 3 - LOGOUT
# Endpoint: POST /api/logout
# Goal:
#   - Clear the current Flask session.
#   - Return a success message as JSON.
# Hint: Flask session has a method that clears all stored session values.


# TODO 4 - CREATE
# Endpoint: POST /api/study-sessions
# Goal:
#   - Read JSON containing topic and minutes.
#   - Validate the input.
#   - Create a unique integer id.
#   - Set completed to False for a new sprint.
#   - Append the new item to study_sessions.
#   - Return the created item as JSON.
# Hint: inspect the JavaScript request body in static/js/app.js.


# TODO 5 - UPDATE
# Endpoint: PATCH /api/study-sessions/<int:session_id>
# Goal:
#   - Find the requested sprint using find_study_session(...).
#   - Return a 404 JSON error when the id does not exist.
#   - Mark the sprint as completed.
#   - Return the updated sprint as JSON.


# TODO 6 - DELETE
# Endpoint: DELETE /api/study-sessions/<int:session_id>
# Goal:
#   - Find the requested sprint.
#   - Return a 404 JSON error when the id does not exist.
#   - Remove it from study_sessions.
#   - Return a useful JSON confirmation.


# TODO 7 - MANUAL COOKIE
# Endpoint: POST /api/focus-mode
# Goal:
#   - Read JSON such as {"mode": "deep"}.
#   - Accept only: standard, deep, revision, practice.
#   - Return a 400 JSON error for another value.
#   - Create a Flask response and set a cookie named "focus_mode".
#   - Make the cookie last for 7 days.
#   - Return a JSON success response.
# Hint: make_response(...) and response.set_cookie(...) may help.


if __name__ == "__main__":
    app.run(debug=True, port=5001)
