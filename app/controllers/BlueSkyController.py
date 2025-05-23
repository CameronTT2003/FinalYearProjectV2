from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask.views import MethodView
from app.models.BlueSkyUrlBuilder import get_bluesky_uri
from app.models.BlueSkyTextBuilder import extract_replies_from_thread
from app.models.BlueSkyLoginLogic import bluesky_login, UnauthorizedError
from app.models.SentimentLLM import send_prompt_with_texts
from app.models.SentimentVADER import get_average_sentiment_score
from app.models.RecordHandler import save_to_csv, get_user_records, delete_record

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
            session['username'] = username
            session['password'] = password
            return redirect(url_for("main.show_results"))
        except UnauthorizedError:
            flash("Invalid username or password.", "danger")
        except Exception as e:
            flash(str(e), "danger")
        return render_template("login.html")

class ShowResults(MethodView):

    def __init__(self, client=None):
        self.client = client

    def get(self):
        username = session.get("username")
        password = session.get("password")
        if not username or not password:
            flash("You must be logged in to view results.", "danger")
            return redirect(url_for("main.login"))
        records = get_user_records(username)
        return render_template("results.html", username=username, password=password, records=records)

    async def post(self):
        username = session.get("username")
        password = session.get("password")
        if not username or not password:
            flash("You must be logged in to view results.", "danger")
            return redirect(url_for("main.login"))
        if 'url' in request.form:
            url = request.form["url"]
            uri = get_bluesky_uri(url)
            try:
                self.client = bluesky_login(username, password)
                try: res = self.client.get_post_thread(uri)
                except Exception as e:
                    flash(f"Error fetching post thread (URL Is Invalid)", "danger")
                    return render_template("results.html", username=username, password=password)
                thread = res.thread
                initial_text, texts = extract_replies_from_thread(thread)
                sentiment_text = await send_prompt_with_texts(initial_text, texts)
                vader_sentiment_score = get_average_sentiment_score(texts)

                try:
                    print("Calling save_to_csv")
                    save_to_csv(username, url, initial_text, vader_sentiment_score, sentiment_text)
                    print("save_to_csv called successfully")
                except Exception as e:
                    print(f"Error in save_to_csv: {e}")
                    flash(f"Error in save_to_csv: {e}", "danger")

                print("Sentiment Text:", sentiment_text)
                records = get_user_records(username)

                return render_template("results.html", initial_text=initial_text, sentiment_text=sentiment_text, vader_sentiment_score=vader_sentiment_score, username=username, password=password, records=records)
            except Exception as e:
                flash(str(e), "danger")
            return render_template("results.html", username=username, password=password)

        elif 'delete' in request.form:
            record_date = request.form["date"]
            delete_record(username, record_date)
            flash("Record deleted successfully.", "success")
            records = get_user_records(username)
            return render_template("results.html", username=username, password=password, records=records)

        else:
            initial_text = request.form["initial_text"]
            vader_sentiment_score = request.form["vader_sentiment_score"]
            sentiment_text = request.form["sentiment_text"]
            records = get_user_records(username)
            return render_template("results.html", initial_text=initial_text, sentiment_text=sentiment_text, vader_sentiment_score=vader_sentiment_score, username=username, password=password, records=records)

main = Blueprint("main", __name__)
main.add_url_rule('/login', view_func=BlueSkyController.as_view('login'))
main.add_url_rule('/results', view_func=ShowResults.as_view('show_results'))
main.add_url_rule('/delete_record', view_func=ShowResults.as_view('delete_record'))

@main.route("/logout")
def logout():
    session.pop('username', None)
    session.pop('password', None)
    #flash("You have been logged out.", "success")
    return redirect(url_for("main.login"))

@main.route("/", methods=["GET"])
def home():
    return redirect(url_for("main.login"))