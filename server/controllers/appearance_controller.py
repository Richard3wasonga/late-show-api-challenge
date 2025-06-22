from flask import Blueprint, request, jsonify, make_response
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest
from models import Appearance, db, Guest, Episode

appearance_bp = Blueprint('appearance',__name__)
api = Api(appearance_bp)

class AppearanceCreate(Resource):
    @jwt_required()
    def post(self):
        try:
            data = request.get_json()
        
            if not data:
                return make_response(jsonify({'error': 'Missing JSON data'}), 400)

            guest_id = data.get('guest_id')
            episode_id = data.get('episode_id')
            rating = data.get('rating')

            if not all([guest_id, episode_id, rating]):
                return make_response(jsonify({'error': 'guest_id, episode_id, and rating are required'}), 400)

            guest = db.session.get(Guest, guest_id)
            episode = db.session.get(Episode, episode_id)

            if not guest or not episode:
                return make_response(jsonify({'error': 'Guest or Episode not found'}), 404)

            appearance = Appearance(
                guest_id=guest_id,
                episode_id=episode_id,
                rating=rating
            )

            db.session.add(appearance)
            db.session.commit()

            return make_response(jsonify(appearance.to_dict()), 201)

        except IntegrityError:
            db.session.rollback()
            return make_response(jsonify({'error': 'Database integrity error'}), 400)

        except BadRequest:
            return make_response(jsonify({'error': 'Bad request'}), 400)

        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 500)

api.add_resource(AppearanceCreate, '/appearances')
