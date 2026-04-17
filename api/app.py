from flask import Flask
from .extensions import init_extensions
from .config import Config

# Lazy blueprint registration after init


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    init_extensions(app)

    # Register blueprints after extensions init
    from .auth import auth_bp
    from .notes import notes_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(notes_bp, url_prefix="/api/notes")

    @app.route("/")
    def index():
        return {"message": "Notes API Backend ready. See README for endpoints."}

    return app
