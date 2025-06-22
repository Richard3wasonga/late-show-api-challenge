import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from flask import Flask, jsonify, make_response
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, get_jwt
from jwt.exceptions import ExpiredSignatureError
from config import Config
from models import db
from models import Guest, Episode, Appearance, User, TokenBlocklist
from controllers import guest_bp, episode_bp, appearance_bp, auth_bp

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
    return make_response(jsonify({"error": "Resource not found"}), 404)

@app.errorhandler(405)
def method_not_allowed_error(e):
    return make_response(jsonify({"error": "Method not allowed"}), 405)

@app.errorhandler(400)
def bad_request_error(e):
    return make_response(jsonify({"error": "Bad request"}), 400)

@app.errorhandler(500)
def internal_server_error(e):
    return make_response(jsonify({"error": "Internal server error"}), 500)

@jwt.token_in_blocklist_loader
def token_in_blocklist(jwt_header, jwt_data):
    jti = jwt_data['jti']
    token = db.session.query(TokenBlocklist).filter_by(jti=jti).first()
    return token is not None

@jwt.expired_token_loader
def expired_jwt_token(jwt_header, jwt_data):
    return make_response(jsonify({"error": "Token has expired"}), 401)

@jwt.invalid_token_loader
def jwt_invalid_token(error):
    return make_response(jsonify({"error": "Invalid token"}), 422)

@jwt.unauthorized_loader
def jwt_missing_token(error):
    return make_response(jsonify({"error": "Missing token"}), 401)

@app.errorhandler(ExpiredSignatureError)
def handle_expired_signature(e):
    return make_response(jsonify({"error": "Token has expired. Please log in again."}), 401)


@app.route('/')
def index():
    return make_response(jsonify({"message": "Late Show API is running 🎬"}), 200)

if __name__ == '__main__':
    app.run(debug=True, port=5555)