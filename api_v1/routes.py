# api_v1/routes.py
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import sessionmaker
from orm.models import FrPotatoApi
from potato.agwise_potato import AgWisePotato

api_v1 = Blueprint('api_v1', __name__)


@api_v1.route('/fr-potato-api-input', methods=['POST'])
def get_planting_season():
    data: object = request.get_json()

    if not data:
        return jsonify({'error': 'Missing JSON data in the request body'}), 400

    agwise = AgWisePotato()
    result = agwise.filter_data(data=data)
    return jsonify(result)
