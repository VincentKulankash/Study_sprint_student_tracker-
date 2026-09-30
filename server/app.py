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


@app.route("/")
def index():
    """Serve the supplied client-side application."""
    return send_from_directory(app.static_folder, "index.html")


@app.route("/api/study-sessions", methods=["GET"])
def get_study_sessions():
    """READ: Return all study sprints as JSON."""
    return jsonify(study_sessions), 200


#Successfully implemented sessions and cookie read
@app.route('/api/me')
def get_current_user():
    username = session.get('username')
    visits = session.get('visits', 0) + 1
    session['visits'] = visits
    focus_mode = request.cookies.get('focus_mode')

    return jsonify({
        'username': username,
        'visits': visits,
        'focus_mode': focus_mode,
    }), 200



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


# implement logout feature 
@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200

#create study sessions
@app.route('/api/study-sessions', methods=['POST'])
def create_study_sessions():
    data = request.get_json(silent=True) or {}
    topic = data.get("topic", "").strip()
    minutes = data.get('minutes')

    if not topic:
        return jsonify({'Error':'Topic is required'}), 400

    if not isinstance(minutes, int) or minutes <= 0:
        return jsonify({'Error': 'Minutes must be a positive integer'})

    new_id = 1 if not study_sessions else max(item['id'] for item in study_sessions) + 1
    new_session = {
        'id': new_id,
        'topic': topic,
        'minutes': minutes,
        'completed': False,
    }

    study_sessions.append(new_session), 201

#create the update route using patch method and return a json 
@app.route('/api/study-sessions/<int:session_id>', methods=['PATCH'])
def update_study_sessions(session_id):
    s = find_study_session(session_id)

    if s is None:
        return jsonify({'Error': 'Study session not found'}), 404

    s['completed'] = True
    return jsonify(s), 200

#create the delete route to remove session by their id 
@app.route('/api/study-sessions/<int:session_id>', methods=['DELETE'])
def delete(session_id):
    s = find_study_session(session_id)

    if s is None:
        return jsonify({'Error': 'Study session not found'}), 404

    study_sessions.remove(s)
    return jsonify({'Message': f"Study session {session_id} deleted"}), 200

#create set_focus_mode route that gets data from frontend 
@app.route('/api/focus-mode', methods=['POST'])
def set_focus_mode():
    data = request.get_json(silent=True) or {}
    mode = data.get('mode')
    allowed_modes= {'standard', 'deep', 'revision', 'practice'}

    if mode not in allowed_modes:
        return jsonify({'Error': 'Invalid focus mode.'}), 400

    response = make_response(jsonify({
        'message': 'Focus mode updated',
        'focus-mode': mode,
    }))

    response.set_cookie('focus_mode', mode, max_age=7 * 24 * 60 * 60)
    return response

if __name__ == "__main__":
    app.run(debug=True, port=5001)
