from datetime import datetime

from flask import Blueprint
from flask_restful import Api

from main.blueprints.baby_blueprint.models import Baby

api_baby_blueprint = Blueprint('api_baby', __name__, url_prefix='/api/baby')
api = Api(api_baby_blueprint)


def get_baby_from_db_by_name(user_id, baby_name):
    return Baby.query.filter_by(user_id=user_id, name=baby_name.capitalize()).first()


def validate_baby_post_gender(gender):
    if gender not in ['m', 'f']:
        return {'message': "Invalid gender. Please enter 'm' for male or 'f' for female."}, 400
    pass


def trasnfom_dob_to_date(dob):
    try:
        dob_date = datetime.strptime(dob, '%Y-%m-%d')
    except ValueError:
        return {'message': 'Invalid date of birth format. Use YYYY-MM-DD.'}, 400
    return dob_date


def validate_baby_post_name(user_id, baby_name):
    if get_baby_from_db_by_name(user_id, baby_name):
        return {'message': 'Baby already exists'}, 400
    pass