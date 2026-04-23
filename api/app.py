from flask import Flask, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .extensions import init_extensions
from .config import Config
from .models import User

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

    @app.route("/me")
    @jwt_required()
    def me():
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify({"id": user.id, "username": user.username})

    return app

