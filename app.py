from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import json
from pathlib import Path
import os

app = Flask(__name__)
app.secret_key = os.environ.get("KIDS_DRAWING_BUDDY_SECRET_KEY", "kids-drawing-buddy-local-secret-change-before-production")

DB_PATH = Path(__file__).with_name("kids_coloring.db")

# Original, simple SVG drawings made for this starter project.
DRAWINGS = {
    "apple": {
        "title": "Big Apple",
        "min_age": 4,
        "emoji": "🍎",
        "svg": """
        <svg class="drawing-svg" viewBox="0 0 600 520" aria-label="Big apple coloring page">
          <path class="fillable" data-region="apple"
                d="M300 145
                   C250 100 165 120 135 205
                   C100 305 160 425 285 455
                   C410 425 485 315 462 215
                   C442 125 355 98 300 145 Z"/>
          <path class="fillable" data-region="leaf"
                d="M315 112 C350 55 420 62 446 105
                   C405 132 360 133 315 112 Z"/>
          <path class="fillable" data-region="stem"
                d="M286 146 C286 108 298 77 322 52
                   L344 68 C322 91 314 117 315 148 Z"/>
          <circle cx="247" cy="270" r="11" class="eye"/>
          <circle cx="354" cy="270" r="11" class="eye"/>
          <path d="M266 326 Q301 350 337 326" class="detail-line"/>
        </svg>
        """
    },

    "flower": {
        "title": "Happy Flower",
        "min_age": 4,
        "emoji": "🌼",
        "svg": """
        <svg class="drawing-svg" viewBox="0 0 600 520" aria-label="Simple flower coloring page">
          <ellipse class="fillable" data-region="petal-top" cx="300" cy="125" rx="63" ry="88"/>
          <ellipse class="fillable" data-region="petal-right" cx="410" cy="225" rx="88" ry="63"/>
          <ellipse class="fillable" data-region="petal-bottom" cx="300" cy="325" rx="63" ry="88"/>
          <ellipse class="fillable" data-region="petal-left" cx="190" cy="225" rx="88" ry="63"/>
          <circle class="fillable" data-region="center" cx="300" cy="225" r="82"/>
          <path class="fillable" data-region="stem"
                d="M282 305 L318 305 L318 470 L282 470 Z"/>
          <path class="fillable" data-region="leaf-left"
                d="M282 390 C220 340 170 365 172 425
                   C220 445 260 430 282 400 Z"/>
          <path class="fillable" data-region="leaf-right"
                d="M318 420 C348 375 405 370 430 410
                   C402 455 350 456 318 433 Z"/>
          <circle cx="274" cy="215" r="9" class="eye"/>
          <circle cx="327" cy="215" r="9" class="eye"/>
          <path d="M277 252 Q301 269 324 252" class="detail-line"/>
        </svg>
        """
    },

    "fish": {
        "title": "Friendly Fish",
        "min_age": 5,
        "emoji": "🐟",
        "svg": """
        <svg class="drawing-svg" viewBox="0 0 600 520" aria-label="Simple fish coloring page">
          <ellipse class="fillable" data-region="body" cx="295" cy="265" rx="165" ry="112"/>
          <path class="fillable" data-region="tail"
                d="M438 215 L535 145 L515 265 L535 385 L438 315 Z"/>
          <path class="fillable" data-region="top-fin"
                d="M255 158 Q300 80 345 158 Z"/>
          <path class="fillable" data-region="bottom-fin"
                d="M260 365 Q307 435 350 365 Z"/>
          <circle cx="225" cy="240" r="13" class="eye"/>
          <path d="M225 298 Q260 325 297 299" class="detail-line"/>
          <path d="M375 185 Q402 265 375 345" class="detail-line"/>
        </svg>
        """
    },

    "icecream": {
        "title": "Ice Cream",
        "min_age": 5,
        "emoji": "🍦",
        "svg": """
        <svg class="drawing-svg" viewBox="0 0 600 520" aria-label="Simple ice cream coloring page">
          <circle class="fillable" data-region="scoop-left" cx="235" cy="180" r="92"/>
          <circle class="fillable" data-region="scoop-right" cx="365" cy="180" r="92"/>
          <circle class="fillable" data-region="scoop-top" cx="300" cy="115" r="88"/>
          <path class="fillable" data-region="cone"
                d="M205 235 L395 235 L315 475 L285 475 Z"/>
          <path d="M245 285 L345 405" class="detail-line"/>
          <path d="M355 285 L255 405" class="detail-line"/>
          <circle cx="273" cy="156" r="10" class="eye"/>
          <circle cx="327" cy="156" r="10" class="eye"/>
          <path d="M277 192 Q300 209 323 192" class="detail-line"/>
        </svg>
        """
    },

    "car": {
        "title": "Little Car",
        "min_age": 6,
        "emoji": "🚗",
        "svg": """
        <svg class="drawing-svg" viewBox="0 0 600 520" aria-label="Simple car coloring page">
          <path class="fillable" data-region="body"
                d="M105 300
                   Q115 245 180 232
                   L225 170
                   Q240 150 270 150
                   L365 150
                   Q395 150 413 174
                   L455 232
                   Q500 245 510 300
                   L510 365
                   L95 365
                   L95 315
                   Q95 302 105 300 Z"/>
          <path class="fillable" data-region="window-left"
                d="M245 180 L286 180 L286 230 L210 230 Z"/>
          <path class="fillable" data-region="window-right"
                d="M310 180 L360 180 L398 230 L310 230 Z"/>
          <circle class="fillable" data-region="wheel-left" cx="190" cy="365" r="58"/>
          <circle class="fillable" data-region="wheel-right" cx="420" cy="365" r="58"/>
          <circle cx="190" cy="365" r="23" class="detail-circle"/>
          <circle cx="420" cy="365" r="23" class="detail-circle"/>
          <circle class="fillable" data-region="light" cx="470" cy="286" r="22"/>
          <path d="M285 265 L285 335" class="detail-line"/>
        </svg>
        """
    },

    "turtle": {
        "title": "Cute Turtle",
        "min_age": 6,
        "emoji": "🐢",
        "svg": """
        <svg class="drawing-svg" viewBox="0 0 600 520" aria-label="Simple turtle coloring page">
          <ellipse class="fillable" data-region="shell" cx="300" cy="270" rx="155" ry="120"/>
          <circle class="fillable" data-region="head" cx="470" cy="270" r="72"/>
          <ellipse class="fillable" data-region="leg-front" cx="388" cy="390" rx="52" ry="32"/>
          <ellipse class="fillable" data-region="leg-back" cx="205" cy="390" rx="52" ry="32"/>
          <path class="fillable" data-region="tail" d="M145 270 L92 238 L105 300 Z"/>
          <circle cx="490" cy="247" r="10" class="eye"/>
          <path d="M486 290 Q505 305 525 288" class="detail-line"/>
          <path d="M300 153 L300 387" class="detail-line"/>
          <path d="M166 270 L434 270" class="detail-line"/>
        </svg>
        """
    },

    "rocket": {
        "title": "Space Rocket",
        "min_age": 7,
        "emoji": "🚀",
        "svg": """
        <svg class="drawing-svg" viewBox="0 0 600 520" aria-label="Simple rocket coloring page">
          <path class="fillable" data-region="rocket"
                d="M300 55
                   C365 105 390 195 365 340
                   L235 340
                   C210 195 235 105 300 55 Z"/>
          <circle class="fillable" data-region="window" cx="300" cy="190" r="52"/>
          <path class="fillable" data-region="left-fin"
                d="M240 270 Q170 305 185 390 L248 335 Z"/>
          <path class="fillable" data-region="right-fin"
                d="M360 270 Q430 305 415 390 L352 335 Z"/>
          <path class="fillable" data-region="flame"
                d="M262 340 Q300 475 338 340 Z"/>
          <path d="M270 115 Q300 96 330 115" class="detail-line"/>
        </svg>
        """
    },

    "butterfly": {
        "title": "Big Butterfly",
        "min_age": 7,
        "emoji": "🦋",
        "svg": """
        <svg class="drawing-svg" viewBox="0 0 600 520" aria-label="Simple butterfly coloring page">
          <ellipse class="fillable" data-region="body" cx="300" cy="275" rx="34" ry="125"/>
          <ellipse class="fillable" data-region="left-top-wing" cx="198" cy="190" rx="105" ry="95" transform="rotate(-20 198 190)"/>
          <ellipse class="fillable" data-region="right-top-wing" cx="402" cy="190" rx="105" ry="95" transform="rotate(20 402 190)"/>
          <ellipse class="fillable" data-region="left-bottom-wing" cx="205" cy="335" rx="92" ry="75" transform="rotate(18 205 335)"/>
          <ellipse class="fillable" data-region="right-bottom-wing" cx="395" cy="335" rx="92" ry="75" transform="rotate(-18 395 335)"/>
          <circle class="fillable" data-region="head" cx="300" cy="125" r="42"/>
          <path d="M282 92 Q250 55 226 73" class="detail-line"/>
          <path d="M318 92 Q350 55 374 73" class="detail-line"/>
          <circle cx="286" cy="121" r="6" class="eye"/>
          <circle cx="314" cy="121" r="6" class="eye"/>
        </svg>
        """
    },

    "house": {
        "title": "Cozy House",
        "min_age": 8,
        "emoji": "🏠",
        "svg": """
        <svg class="drawing-svg" viewBox="0 0 600 520" aria-label="Simple house coloring page">
          <path class="fillable" data-region="wall"
                d="M155 235 L445 235 L445 450 L155 450 Z"/>
          <path class="fillable" data-region="roof"
                d="M100 245 L300 75 L500 245 Z"/>
          <path class="fillable" data-region="door"
                d="M260 330 L340 330 L340 450 L260 450 Z"/>
          <rect class="fillable" data-region="window-left" x="185" y="285" width="72" height="72" rx="8"/>
          <rect class="fillable" data-region="window-right" x="343" y="285" width="72" height="72" rx="8"/>
          <circle class="fillable" data-region="sun" cx="500" cy="100" r="45"/>
          <path d="M221 285 L221 357 M185 321 L257 321" class="detail-line"/>
          <path d="M379 285 L379 357 M343 321 L415 321" class="detail-line"/>
          <circle cx="320" cy="390" r="7" class="eye"/>
        </svg>
        """
    },

    "castle": {
        "title": "Simple Castle",
        "min_age": 8,
        "emoji": "🏰",
        "svg": """
        <svg class="drawing-svg" viewBox="0 0 600 520" aria-label="Simple castle coloring page">
          <rect class="fillable" data-region="center" x="205" y="225" width="190" height="220"/>
          <rect class="fillable" data-region="left-tower" x="95" y="185" width="125" height="260"/>
          <rect class="fillable" data-region="right-tower" x="380" y="185" width="125" height="260"/>
          <path class="fillable" data-region="left-roof" d="M75 185 L158 90 L240 185 Z"/>
          <path class="fillable" data-region="right-roof" d="M360 185 L442 90 L525 185 Z"/>
          <path class="fillable" data-region="center-roof" d="M180 225 L300 105 L420 225 Z"/>
          <path class="fillable" data-region="door" d="M265 445 L265 350 Q300 305 335 350 L335 445 Z"/>
          <circle class="fillable" data-region="window-left" cx="158" cy="275" r="26"/>
          <circle class="fillable" data-region="window-right" cx="442" cy="275" r="26"/>
          <circle class="fillable" data-region="window-center" cx="300" cy="280" r="26"/>
        </svg>
        """
    }
}


def db():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con


def init_db():
    with db() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                child_age INTEGER
            )
        """)
        con.execute("""
            CREATE TABLE IF NOT EXISTS completed_drawings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                drawing_id TEXT NOT NULL,
                completed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, drawing_id),
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)
        con.execute("""
            CREATE TABLE IF NOT EXISTS drawing_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                drawing_id TEXT NOT NULL,
                state_json TEXT NOT NULL DEFAULT '{}',
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, drawing_id),
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)


@app.before_request
def ensure_database():
    init_db()


def logged_in_user():
    if "user_id" not in session:
        return None
    with db() as con:
        return con.execute(
            "SELECT id, username, child_age FROM users WHERE id = ?",
            (session["user_id"],)
        ).fetchone()


@app.route("/")
def index():
    user = logged_in_user()
    if not user:
        return redirect(url_for("login"))
    if not user["child_age"]:
        return redirect(url_for("age_select"))
    return redirect(url_for("gallery"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if len(username) < 3 or len(password) < 4:
            flash("Use at least 3 characters for the name and 4 for the password.")
            return render_template("register.html")

        try:
            with db() as con:
                cur = con.execute(
                    "INSERT INTO users(username, password_hash) VALUES (?, ?)",
                    (username, generate_password_hash(password))
                )
                session["user_id"] = cur.lastrowid
            return redirect(url_for("age_select"))
        except sqlite3.IntegrityError:
            flash("That name is already used. Try another one.")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        with db() as con:
            user = con.execute(
                "SELECT * FROM users WHERE username = ?",
                (username,)
            ).fetchone()

        if not user or not check_password_hash(user["password_hash"], password):
            flash("Name or password is incorrect.")
            return render_template("login.html")

        session["user_id"] = user["id"]
        return redirect(url_for("age_select") if not user["child_age"] else url_for("gallery"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/age", methods=["GET", "POST"])
def age_select():
    user = logged_in_user()
    if not user:
        return redirect(url_for("login"))

    if request.method == "POST":
        try:
            age = int(request.form.get("age", ""))
        except ValueError:
            age = 0

        if age not in range(4, 9):
            flash("Please choose an age from 4 to 8.")
            return render_template("age.html", current_age=user["child_age"])

        with db() as con:
            con.execute("UPDATE users SET child_age = ? WHERE id = ?", (age, user["id"]))
        return redirect(url_for("gallery"))

    return render_template("age.html", current_age=user["child_age"])


@app.route("/gallery")
def gallery():
    user = logged_in_user()
    if not user:
        return redirect(url_for("login"))
    if not user["child_age"]:
        return redirect(url_for("age_select"))

    with db() as con:
        completed_rows = con.execute(
            "SELECT drawing_id FROM completed_drawings WHERE user_id = ?",
            (user["id"],)
        ).fetchall()
        progress_rows = con.execute(
            "SELECT drawing_id, state_json FROM drawing_progress WHERE user_id = ?",
            (user["id"],)
        ).fetchall()

    completed = {row["drawing_id"] for row in completed_rows}
    progress = {}
    for row in progress_rows:
        try:
            progress[row["drawing_id"]] = json.loads(row["state_json"])
        except (TypeError, json.JSONDecodeError):
            progress[row["drawing_id"]] = {}

    available = {
        key: value for key, value in DRAWINGS.items()
        if value["min_age"] <= user["child_age"]
    }
    return render_template(
        "gallery.html",
        user=user,
        drawings=available,
        completed=completed,
        progress=progress
    )


@app.route("/draw/<drawing_id>")
def draw_page(drawing_id):
    user = logged_in_user()
    if not user:
        return redirect(url_for("login"))

    drawing = DRAWINGS.get(drawing_id)
    if not drawing:
        return "Drawing not found", 404

    if not user["child_age"] or drawing["min_age"] > user["child_age"]:
        flash("Choose an age that unlocks this drawing.")
        return redirect(url_for("gallery"))

    with db() as con:
        row = con.execute(
            "SELECT state_json FROM drawing_progress WHERE user_id = ? AND drawing_id = ?",
            (user["id"], drawing_id)
        ).fetchone()

    initial_state = {}
    if row:
        try:
            initial_state = json.loads(row["state_json"])
        except (TypeError, json.JSONDecodeError):
            initial_state = {}

    return render_template(
        "draw.html",
        user=user,
        drawing=drawing,
        drawing_id=drawing_id,
        initial_state=initial_state
    )


@app.route("/api/progress/<drawing_id>", methods=["GET", "POST"])
def drawing_progress(drawing_id):
    user = logged_in_user()
    if not user:
        return jsonify({"ok": False, "message": "Please log in again."}), 401
    if drawing_id not in DRAWINGS:
        return jsonify({"ok": False, "message": "Drawing not found."}), 404

    if request.method == "GET":
        with db() as con:
            row = con.execute(
                "SELECT state_json, updated_at FROM drawing_progress WHERE user_id = ? AND drawing_id = ?",
                (user["id"], drawing_id)
            ).fetchone()

        if not row:
            return jsonify({"ok": True, "state": {}, "updated_at": None})

        try:
            state = json.loads(row["state_json"])
        except (TypeError, json.JSONDecodeError):
            state = {}

        return jsonify({"ok": True, "state": state, "updated_at": row["updated_at"]})

    state = request.get_json(silent=True) or {}
    # Keep the persisted data intentionally small and predictable.
    safe_state = {
        "fills": state.get("fills", {}),
        "strokes": state.get("strokes", []),
        "last_tool": state.get("last_tool", "fill")
    }

    # Basic payload limits for this starter app.
    if not isinstance(safe_state["fills"], dict):
        safe_state["fills"] = {}
    if not isinstance(safe_state["strokes"], list):
        safe_state["strokes"] = []
    safe_state["strokes"] = safe_state["strokes"][-500:]

    state_json = json.dumps(safe_state, separators=(",", ":"))

    with db() as con:
        con.execute(
            """
            INSERT INTO drawing_progress(user_id, drawing_id, state_json, updated_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(user_id, drawing_id)
            DO UPDATE SET state_json = excluded.state_json, updated_at = CURRENT_TIMESTAMP
            """,
            (user["id"], drawing_id, state_json)
        )

    return jsonify({"ok": True, "message": "Saved"})


@app.post("/api/complete/<drawing_id>")
def complete_drawing(drawing_id):
    user = logged_in_user()
    if not user:
        return jsonify({"ok": False, "message": "Please log in again."}), 401
    if drawing_id not in DRAWINGS:
        return jsonify({"ok": False, "message": "Drawing not found."}), 404

    with db() as con:
        con.execute(
            "INSERT OR IGNORE INTO completed_drawings(user_id, drawing_id) VALUES (?, ?)",
            (user["id"], drawing_id)
        )

    return jsonify({
        "ok": True,
        "message": f"Great job! You finished {DRAWINGS[drawing_id]['title']}!"
    })


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
