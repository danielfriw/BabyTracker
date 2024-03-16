from flask import Blueprint
from flask_restful import Resource, Api

from main.blueprints.api_length_percentile_calculator_blueprint.services import percentile_calc

api_length_percentile_calculator_blueprint = Blueprint('api_length_percentile_calculator', __name__, url_prefix='/api/length_percentile_calculator')
api = Api(api_length_percentile_calculator_blueprint)


class LengthPercentileCalculatorResource(Resource):
    def get(self, gender, age_in_months, length):
        try:
            result = percentile_calc(gender, int(age_in_months), float(length))
            return {'result': result}, 200
        except ValueError as e:
            return {'result': f'Error: {e}'}, 404


api.add_resource(LengthPercentileCalculatorResource, '/<gender>/<age_in_months>/<length>')