# routes/route.py
from flask import Blueprint, request, jsonify

from app.core import limiter
from app.potato.agwise_potato import AgWisePotato

api_v1 = Blueprint('api_v1', __name__)


# limiter.limit("1/minute")(api_v1)

@api_v1.route('/fr-potato', methods=['POST'])
@limiter.limit("30/minute")
def list_all_data():
    data: object = request.get_json()

    if not data:
        return jsonify({'error': 'Missing JSON data in the request body'}), 400

    agwise = AgWisePotato()
    result = agwise.filter_data(data=data)
    return jsonify(result)


@api_v1.route('/fertilizer-data', methods=['GET'])
@limiter.limit("30/minute")
def fetch_fertilizer_data():
    lat, lon = None, None

    coordinates = request.args.get('coordinates')
    region = request.args.get('region')
    province = request.args.get('province')
    season = request.args.get('season')
    district = request.args.get('district')
    limit = request.args.get('limit', 100)
    page = request.args.get('page', 1)
    paginate = request.args.get('paginate', False)

    # Split coordinates into latitude and longitude
    if coordinates:
        try:
            lat, lon = map(float, coordinates.split(','))
        except ValueError:
            return jsonify({'error': f'Invalid coordinates format : {coordinates}'}), 400

    data = {
        'Province': province,
        'Season': season,
        'District': district,
        'AEZ': region,
        'coordinates': coordinates,
        'lat': lat,
        'lon': lon,
        'limit': limit,
        'page': page
    }
    agwise = AgWisePotato()
    result = agwise.filter_data(data=data)
    return jsonify(result)
