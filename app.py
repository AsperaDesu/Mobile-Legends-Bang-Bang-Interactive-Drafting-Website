from datetime import datetime
import uuid
from flask import Flask, session, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
import json
from werkzeug.security import generate_password_hash, check_password_hash
import requests


json_url = "https://raw.githubusercontent.com/p3hndrx/MLBB-API/main/v1/hero-meta-final.json"

response = requests.get(json_url)
HEROES_DATA = response.json()['data'][1:]

TEMPLATE = {}
for team in ['teamA', 'teamB']:
    TEMPLATE[team] = {
        'picks' : [
            {
                'name' : '',
                'portrait' : ''
            }
            for _ in range(5)
        ],
        'bans' : [
            {
                'name' : '',
                'portrait' : ''
            }
            for _ in range(5)
        ]
    }

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Database connection
def get_db_connection():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.before_request
def assign_guest_session():
    if "guest_session" not in session:
        session["guest_session"] = str(uuid.uuid4())  # Assign unique ID to guests

@app.route("/")
def main():
    guest_session = session["guest_session"]
    user_id = session.get("user_id")
    print(TEMPLATE)
    conn = get_db_connection()
    if user_id:
        drafts = conn.execute(
            "SELECT * FROM drafts WHERE user_id = ?", (user_id,)
        ).fetchall()
    else:
        drafts = conn.execute(
            "SELECT * FROM drafts WHERE guest_session = ? ORDER BY id DESC LIMIT 5", (guest_session,)
        ).fetchall()
    conn.close()

    return render_template("main.html", drafts=drafts, user_id=user_id)


@app.route("/view_draft/<int:draft_id>")
def view_draft(draft_id):
    conn = get_db_connection()
    draft = conn.execute("SELECT draft_name, picks, bans FROM drafts WHERE id = ?", (draft_id,)).fetchone()
    conn.close()
    if not draft:
        flash("Draft not found.", "error")
        return redirect("/")

    draft_data = {'id': draft_id}
    for team in ['teamA', 'teamB']:
        draft_data[team] = {
            'picks' : [
                {
                    "name": name,
                    "portrait": [i['portrait'] for i in HEROES_DATA if i['hero_name'] == name]
                }
                for name in json.loads(draft[1])[team]
            ],
            'bans' : [
                {
                    "name": name,
                    "portrait": [i['portrait'] for i in HEROES_DATA if i['hero_name'] == name]
                }
                for name in json.loads(draft[2])[team]
            ]
        }

    return render_template("draft.html", draft_data = draft_data , draft_name = draft[0], heroes = HEROES_DATA)

@app.route('/save_draft', methods=['POST'])
def save_draft():
    if request.method == 'POST':
        # Extract data from the request
        draft_data = request.json
        draft_id = draft_data.get('id')  # Get draft_id if provided
        draft_name = draft_data.get('name', 'Untitled Draft')
        picks = draft_data.get('picks', {})
        bans = draft_data.get('bans', {})
        date_modified = datetime.now()

        user_id = session.get("user_id", None)  # None if guest session
        guest_session = session["guest_session"]

        conn = get_db_connection()

        if draft_id:  # Update existing draft
            conn.execute(
                """
                UPDATE drafts
                SET draft_name = ?, picks = ?, bans = ?, date_created = ?
                WHERE id = ? AND (user_id = ? OR guest_session = ?)
                """,
                (draft_name, json.dumps(picks), json.dumps(bans), date_modified, draft_id, user_id, guest_session),
            )
            message = "Draft updated successfully!"
        else:  # Create new draft
            conn.execute(
                """
                INSERT INTO drafts (user_id, guest_session, draft_name, picks, bans, date_created)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (user_id, guest_session, draft_name, json.dumps(picks), json.dumps(bans), date_modified),
            )
            message = "Draft saved successfully!"

        conn.commit()
        conn.close()

        return jsonify({"message": message}), 200


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect("/")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    """
    Route for signing up users.
    Handles both GET (form display) and POST (form submission) requests.
    """
    if request.method == "POST":
        username = request.form.get("username").strip().lower()
        email = request.form.get("email").strip().lower()
        password = request.form.get("password").strip()
        confirm_password = request.form.get("confirm_password").strip()

        # Basic validation
        if not username or not email or not password:
            flash("All fields are required.", "error")
            return redirect(url_for("signup"))
        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect(url_for("signup"))

        # Check if the user already exists
        conn = get_db_connection()
        user_exists = conn.execute(
            "SELECT * FROM users WHERE username = ? OR email = ?", (username, email)
        ).fetchone()

        if user_exists:
            flash("Username or email already taken. Please choose another.", "error")
            conn.close()
            return redirect(url_for("signup"))

        # Hash the password and save the user
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
        conn.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, hashed_password),
        )
        conn.commit()
        conn.close()

        flash("Account created successfully! You can now log in.", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Route for logging in users.
    Handles both GET (form display) and POST (authentication) requests.
    """
    if request.method == "POST":
        username_or_email = request.form.get("username").strip().lower()
        password = request.form.get("password")

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE username = ? OR email = ?",
            (username_or_email, username_or_email),
        ).fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session['username'] = user['username']
            flash("Logged in successfully!", "success")
            return redirect(url_for("main"))
        else:
            flash("Invalid username/email or password. Please try again.", "error")

        return redirect(url_for("login"))

    return render_template("login.html")

@app.route('/create_draft')
def create_draft():
    return render_template('draft.html', heroes=HEROES_DATA, draft_data = TEMPLATE)

if __name__ == "__main__":
    app.run(debug=True)
