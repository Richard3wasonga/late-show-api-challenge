from flask import Blueprint, jsonify, make_response
from flask_restful import Api, Resource
from models import Guest, db

guest_bp = Blueprint('guest', __name__)
api = Api(guest_bp)

class GuestList(Resource):
    def get(self):
        guests = db.session.query(Guest).all()
        if not guests:
            return make_response(jsonify({'message': 'No guests found', 'guests': []}), 200)

        guest_list = [guest.to_dict() for guest in guests]
        return make_response(jsonify(guest_list), 200)

api.add_resource(GuestList, '/guests')