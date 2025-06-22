from flask import Flask, jsonify, make_response
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from .config import Config
from .models import db
from .models import Guest, Episode, Appearance, User
from .controllers import guest_bp, episode_bp, appearance_bp, auth_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

app.register_blueprint(guest_bp)
app.register_blueprint(episode_bp)
app.register_blueprint(appearance_bp)
app.register_blueprint(auth_bp)

@app.errorhandler(404)
def not_found_error(e):
    return jsonify(error="Resource not found"), 404

@app.errorhandler(405)
def method_not_allowed_error(e):
    return jsonify(error="Method not allowed"), 405

@app.errorhandler(400)
def bad_request_error(e):
    return jsonify(error="Bad request"), 400

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify(error="Internal server error"), 500

@app.route('/')
def index():
    return make_response(jsonify({"message": "Late Show API is running 🎬"}), 200)

if __name__ == '__main__':
    app.run(debug=True, port=5555)