from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.BlueSkyLoginLogic import bluesky_login, UnauthorizedError

main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        try:
            client = bluesky_login(username, password)
            flash(f"Logged in as: {username}", "success")
            print(username)
            return redirect(url_for("main.home"))
        except UnauthorizedError as e:
            flash(str(e), "danger")
    return render_template("index.html")