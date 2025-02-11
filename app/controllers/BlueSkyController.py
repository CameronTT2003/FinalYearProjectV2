import os, asyncio
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask.views import MethodView
from app.models.BlueSkyUrlBuilder import get_bluesky_uri
from app.models.BlueSkyTextBuilder import extract_replies_from_thread
from app.models.BlueSkyLoginLogic import bluesky_login, UnauthorizedError
from app.models.SentimentLLM import send_prompt_with_texts
from app.models.sentimentVADER  import get_average_sentiment_score
from app.models.DataSaver import save_to_csv
 

class BlueSkyController(MethodView):

    def __init__(self):
        self.client = None

    def get(self):
        return render_template("login.html")

    def post(self):
        username = request.form["username"]
        password = request.form["password"]
        try:
            self.client = bluesky_login(username, password)
            print("User ID and password set:", username, password) 
            flash("Login successful!", "success")
            return redirect(url_for("main.show_results", username=username, password=password))
        except UnauthorizedError:
            flash("Invalid username or password.", "danger")
        except Exception as e:
            flash(str(e), "danger")
        return render_template("login.html")

class ShowResults(MethodView):

    def __init__(self, client=None):
        self.client = client

    def get(self):
        username = request.args.get("username")
        password = request.args.get("password")
        return render_template("results.html", username=username, password=password)

    async def post(self):
        username = request.form["username"]
        password = request.form["password"]
        url = request.form["url"]
        uri = get_bluesky_uri(url)
        if not username or not password:
            flash("You must be logged in to view results.", "danger")
            print("error1")
            return redirect(url_for("main.login"))
        try:
            self.client = bluesky_login(username, password) 
            res = self.client.get_post_thread(uri)
            thread = res.thread
            initial_text, texts = extract_replies_from_thread(thread)
            vader_sentiment_score = get_average_sentiment_score(texts)
            sentiment_text  = await  send_prompt_with_texts(initial_text, texts)

            try:
                print("Calling save_to_csv")
                save_to_csv(username, url, initial_text, vader_sentiment_score, sentiment_text)
                print("save_to_csv called successfully")
            except Exception as e:
                print(f"Error in save_to_csv: {e}")

            print("Sentiment Text:", sentiment_text)
            return render_template("results.html", initial_text=initial_text, sentiment_text=sentiment_text, vader_sentiment_score = vader_sentiment_score, username=username, password=password)
        except Exception as e:
            flash(str(e), "danger")
        return render_template("results.html", username=username, password=password)

main = Blueprint("main", __name__)
main.add_url_rule('/login', view_func=BlueSkyController.as_view('login'))
main.add_url_rule('/results', view_func=ShowResults.as_view('show_results'))

@main.route("/logout")
def logout():
    flash("You have been logged out.", "success")
    return redirect(url_for("main.login"))

@main.route("/", methods=["GET"])
def home():
    return redirect(url_for("main.login"))