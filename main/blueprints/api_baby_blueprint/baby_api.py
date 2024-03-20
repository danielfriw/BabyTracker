from flask import Blueprint, request
from flask_restful import Resource, Api

from extensions import db
from main.blueprints.api_baby_blueprint.services import get_baby_from_db_by_name, validate_baby_post_gender, \
    trasnfom_dob_to_date, validate_baby_post_name
from main.blueprints.baby_blueprint.models import Baby

api_baby_blueprint = Blueprint('api_baby', __name__, url_prefix='/api/baby')
api = Api(api_baby_blueprint)


class BabyResource(Resource):
    def get(self, user_id, baby_name):
        baby = get_baby_from_db_by_name(user_id, baby_name)
        if baby:
            return baby.json(), 200
        else:
            return {'message': 'Baby not found'}, 404

    def post(self, user_id, baby_name):
        data = request.json
        gender = data.get('gender')
        dob = data.get('dob')

        validate_baby_post_gender(gender)
        dob_date = trasnfom_dob_to_date(dob)
        validate_baby_post_name(user_id, baby_name)

        baby = Baby(user_id=user_id, name=baby_name.capitalize(), gender=gender, dob=dob_date)
        db.session.add(baby)
        db.session.commit()

        return baby.json(), 200

    def delete(self, user_id, baby_name):
        baby = get_baby_from_db_by_name(user_id, baby_name)
        if baby:
            db.session.delete(baby)
            db.session.commit()
            return {'message': f'{baby_name.capitalize()} deleted'}, 200
        return {'message': 'Baby not found'}, 404


api.add_resource(BabyResource, '/<user_id>/<baby_name>')
