from flask import Blueprint, request, jsonify, make_response
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required
from ..models import Episode, db

episode_bp = Blueprint('episode', __name__)
api = Api(episode_bp)

class EpisodeList(Resource):
    def get(self):
        episodes = db.session.query(Episode).all()
        if not episodes:
            return make_response(jsonify({'message': 'No episodes found', 'episodes': []}), 200)

        episode_list = [episode.to_dict() for episode in episodes]
        return make_response(jsonify(episode_list), 200)

class EpisodeDetail(Resource):
    def get(self, id):
        episode = db.session.get(Episode, id)
        if not episode:
            return make_response(jsonify({'error': 'Episode not found'}), 404)
        return make_response(jsonify(episode.to_dict()), 200)

    @jwt_required()
    def delete(self, id):
        episode = db.session.get(Episode, id)
        if not episode:
            return make_response(jsonify({"error": "Episode not found"}), 404)
            
        db.session.delete(episode)
        db.session.commit()
        return make_response(jsonify({"message": f"Episode {id} and its appearances deleted"}), 200)

api.add_resource(EpisodeList, '/episodes')
api.add_resource(EpisodeDetail, '/episodes/<int:id>')
