from flask import Blueprint, request, make_response, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from models import User, db
from werkzeug.exceptions import BadRequest
from sqlalchemy.exc import IntegrityError

auth_bp = Blueprint('auth', __name__)
api = Api(auth_bp)

class Register(Resource):
    def post(self):
        try:
            data = request.get_json()

            if not data:
                return make_response(jsonify({'error': 'Missing JSON data'}), 400)

            username = data.get('username', '').strip().lower()
            password = data.get('password')

            if User.query.filter_by(username=username).first():
                return make_response(jsonify({'error': 'Username already exists'}), 400)

            new_user = User(
                username = username
            )
            new_user.set_password(password)

            db.session.add(new_user)
            db.session.commit()

            return make_response(jsonify({'message': 'User registered successfully'}), 201)

        except IntegrityError:
            db.session.rollback()
            return make_response(jsonify({'error': 'Database integrity error (likely duplicate or null value)'}), 400)

        except BadRequest:
            return make_response(jsonify({'error': 'Invalid request data'}), 400)

        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 500)

class Login(Resource):
     def post(self):
        try:
            data = request.get_json()

            if not data:
                return make_response(jsonify({"error": "Missing request data"}), 400)

            username = data.get('username', '').strip().lower()
            password = data.get('password')

            user = User.query.filter_by(username=username).first()

            if user and user.check_password(password):
                token = create_access_token(identity=str(user.id))
                refresh_token = create_refresh_token(identity=str(user.id))
                return make_response(jsonify({
                    "access_token": token,
                    "refresh_token": refresh_token
                }), 200)

            return make_response(jsonify({"error": "Invalid username or password"}), 401)

        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)

class RefreshToken(Resource):
    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()
        new_token = create_access_token(identity=identity)
        return make_response(jsonify({"access_token": new_token}), 200)

api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(RefreshToken, '/refresh')