# routes/route.py
import json
from http import HTTPStatus

from flask import Blueprint, request, jsonify, make_response
from flask_openapi3 import Tag, Info
from flask_openapi3 import APIBlueprint, OpenAPI
from pydantic import BaseModel, Field

from app.core import limiter
from app.my_logger import MyLogger
from app.potato.agwise_potato import AgWisePotato
from app.routes.FertilizerData import FertilizerQuery, FertilizerResponse

tag = Tag(name='AgWise', description="AgWise API")
security = [{"jwt": []}]

logging = MyLogger()


class Unauthorized(BaseModel):
    code: int = Field(-1, description="Status Code")
    message: str = Field("Unauthorized!", description="Exception Information")


api_v1 = APIBlueprint(
    'api_v1',
    __name__,
    url_prefix='/api/v1',
    # abp_tags=[tag],
    # abp_security=security,
    # abp_responses={"401": Unauthorized},
    # disable openapi UI
    doc_ui=True
)

# api_v1 = Blueprint('api_v1', __name__)

potato_fr_tag = Tag(name="potato", description="Fertilizer data for potato in Rwanda")


# limiter.limit("1/minute")(api_v1)

# @api_v1.route('/fr-potato', methods=['POST'])
@api_v1.get("/fr-potato",
            summary="Fetch rwanda potato FR",
            doc_ui=False,
            tags=[potato_fr_tag],
            deprecated=True)
@limiter.limit("30/minute")
def list_all_data():
    data: object = request.get_json()

    if not data:
        return jsonify({'error': 'Missing JSON data in the request body'}), 400

    agwise = AgWisePotato()
    result = agwise.filter_data(filter_data=data, paginate=False)
    return jsonify(result)


@api_v1.get("/fertilizer-data",
            summary="Get fertilizer recommendations data in Rwanda",
            tags=[potato_fr_tag],
            responses={200: FertilizerResponse},
            )
@limiter.limit("30/minute")
def fetch_fertilizer_data(query: FertilizerQuery):
    lat, lon = None, None

    logging.info(query)

    coordinates = request.args.get('coordinates')
    region = request.args.get('region')
    province = request.args.get('province')
    season = request.args.get('season')
    district = request.args.get('district')
    limit = request.args.get('limit', 100)
    page = request.args.get('page', 1)
    paginate = request.args.get('paginate', True)

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
    result = agwise.filter_data(filter_data=data, paginate=paginate)
    return jsonify(result)
