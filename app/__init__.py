from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_object("config")
    app.config["SESSION_TYPE"] = "filesystem"

    from app.controllers.BlueSkyController import main  # Import the main blueprint

    app.register_blueprint(main)  # Register the main blueprint

    return app