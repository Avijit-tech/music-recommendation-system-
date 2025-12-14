from flask import Flask, render_template, request, redirect, session
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
load_dotenv()
from itsdangerous import URLSafeTimedSerializer
import pickle, os

from config import users
from spotify import get_song_details

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
bcrypt = Bcrypt(app)
serializer = URLSafeTimedSerializer(app.secret_key)

df = pickle.load(open("models/df.pkl", "rb"))
similarity = pickle.load(open("models/similarity.pkl", "rb"))

def recommend(song):
    idx = df[df["song"] == song].index[0]
    scores = sorted(list(enumerate(similarity[idx])), key=lambda x: x[1], reverse=True)
    return [df.iloc[i[0]].song for i in scores[1:5]]

@app.route("/", methods=["GET", "POST"])
def index():
    if "user" not in session:
        return redirect("/login")

    songs = df["song"].values
    recs, song_data = None, None

    if request.method == "POST":
        song = request.form["song"]
        recs = recommend(song)
        song_data = get_song_details(song)
        users.update_one({"email": session["user"]}, {"$push": {"history": song}})

    user = users.find_one({"email": session["user"]})
    history = user.get("history", [])

    return render_template("index.html", songs=songs, recs=recs, song=song_data, history=history)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        pwd = bcrypt.generate_password_hash(request.form["password"]).decode()
        users.insert_one({"email": request.form["email"], "password": pwd, "history": []})
        return redirect("/login")
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = users.find_one({"email": request.form["email"]})
        if user and bcrypt.check_password_hash(user["password"], request.form["password"]):
            session["user"] = user["email"]
            return redirect("/")
    return render_template("login.html")

@app.route("/forgot", methods=["GET", "POST"])
def forgot():
    if request.method == "POST":
        email = request.form["email"]
        token = serializer.dumps(email, salt="reset")
        return f"Reset link: /reset/{token}"
    return render_template("forgot.html")

@app.route("/reset/<token>", methods=["GET", "POST"])
def reset(token):
    email = serializer.loads(token, salt="reset", max_age=600)
    if request.method == "POST":
        pwd = bcrypt.generate_password_hash(request.form["password"]).decode()
        users.update_one({"email": email}, {"$set": {"password": pwd}})
        return redirect("/login")
    return render_template("reset.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)
