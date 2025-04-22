from flask import Flask, render_template, redirect, url_for, session, jsonify, request
from flask_dance.contrib.google import make_google_blueprint, google
import os, json
from datetime import datetime
from flask_dance.consumer import oauth_authorized, oauth_error
from flask import redirect
from oauthlib.oauth2 import TokenExpiredError


app = Flask(__name__)
app.secret_key = "supersecret"
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"

blueprint = make_google_blueprint(
    client_id="YOUR CLIENT ID",
    client_secret="YOUR CLIENT SECRET",
    scope=["profile", "email"],
    redirect_url="https://<your-ngrok-subdomain>.ngrok-free.app/login/google/authorized"
)
app.register_blueprint(blueprint, url_prefix="/login")

USERS_FILE = "users.json"

@app.route("/")
def home():
    if not google.authorized:
        return render_template("login.html")
    return redirect(url_for("dashboard"))

@app.route("/dashboard")
def dashboard():
    if not google.authorized:
        return redirect(url_for("google.login"))

    try:
        resp = google.get("/oauth2/v2/userinfo")
        info = resp.json()
    except TokenExpiredError:
        session.clear()
        return redirect(url_for("google.login"))

    email = info["email"]
    session["email"] = email   # ✅ Save email to session here

    with open(USERS_FILE, "r") as f:
        users = json.load(f)

    if email not in users:
        session["pending_email"] = email
        return redirect(url_for("choose_username"))

    user = users[email]
    name = user.get("name", email.split("@")[0])
    total_time = sum(u.get("time_played", 0) for u in users.values())

    return render_template("dashboard.html",
        email=email,
        name=name,
        score=user.get("high_score", 0),
        games=user.get("games_played", 0),
        time=user.get("time_played", 0),
        total_time=total_time,
        history=user.get("history", [])
    )

@app.route("/choose-username", methods=["GET", "POST"])
def choose_username():
    if request.method == "POST":
        username = request.form["username"]
        email = session.get("pending_email")
        avatar = request.files.get("avatar")

        avatar_path = "/static/avatars/default.png"
        if avatar and avatar.filename != "":
            path = f"static/avatars/{email.replace('@','_')}.png"
            avatar.save(path)
            avatar_path = "/" + path

        with open(USERS_FILE, "r") as f:
            users = json.load(f)

        users[email] = {
            "name": username,
            "avatar": avatar_path,
            "high_score": 0,
            "games_played": 0,
            "time_played": 0,
            "created_at": str(datetime.now()),
            "history": []
        }

        with open(USERS_FILE, "w") as f:
            json.dump(users, f, indent=2)

        session.pop("pending_email", None)
        return redirect(url_for("dashboard"))
    return render_template("choose_username.html")


@app.route("/play")
def play():
    if not google.authorized:
        return redirect(url_for("google.login"))

    try:
        resp = google.get("/oauth2/v2/userinfo")
        info = resp.json()
    except TokenExpiredError:
        session.clear()
        return redirect(url_for("google.login"))

    email = info["email"]
    return render_template("play.html", email=email)

@app.route("/update_score", methods=["POST"])
def update_score():
    if not google.authorized:
        return "Unauthorized", 401

    email = session.get("email")
    if not email:
        return "No email in session", 400

    try:
        data = request.get_json(force=True)
        if not data or "score" not in data:
            print("🚫 JSON missing or score not found")
            return "Missing score", 400
        score = int(data["score"])
    except Exception as e:
        print("🚫 Error parsing JSON:", e)
        return "Invalid JSON", 400

    with open("users.json", "r+") as f:
        users = json.load(f)
        user = users.get(email)
        if not user:
            return "User not found", 404

        user["high_score"] = max(user.get("high_score", 0), score)
        user["games_played"] = user.get("games_played", 0) + 1
        user["time_played"] = user.get("time_played", 0) + (score * 3)

        if "history" not in user:
            user["history"] = []
        user["history"].append({
            "score": score,
            "time": datetime.now().strftime("%H:%M:%S")
        })

        f.seek(0)
        json.dump(users, f, indent=2)
        f.truncate()

    print("✅ Score updated for:", email)
    return "Score updated", 200


@app.route("/leaderboard")
def leaderboard():
    with open(USERS_FILE, "r") as f:
        users = json.load(f)
    sorted_users = sorted(users.items(), key=lambda x: x[1]["high_score"], reverse=True)
    return render_template("leaderboard.html", users=sorted_users[:100])

if __name__ == "__main__":
    app.run(debug=True)
