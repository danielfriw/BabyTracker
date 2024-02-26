from flask import Blueprint, request
from flask_restful import Resource, Api
from datetime import datetime
from main import db
from main.blueprints.baby_blueprint.models import Baby

api_baby_blueprint = Blueprint('api_baby', __name__, url_prefix='/api/baby', static_folder='static', template_folder='templates')
api = Api(api_baby_blueprint)


class BabyResource(Resource):
    def get(self, user_id, baby_name):
        baby = Baby.query.filter_by(user_id=user_id).filter_by(name=baby_name.capitalize()).first()
        if baby:
            return baby.json(), 200
        else:
            return {'message': 'Baby not found'}, 404

    def post(self, user_id, baby_name):
        gender = request.json.get('gender')
        dob = request.json.get('dob')
        if gender not in ['m', 'f']:
            return {'message': "enter correct gender as 'm' or 'f'"}, 400

        try:
            dob_date = datetime.strptime(dob, '%Y-%m-%d')
        except ValueError:
            return {'message': 'Invalid date of birth format. Use YYYY-MM-DD.'}, 400

        if Baby.query.filter_by(user_id=user_id, name=baby_name.capitalize()).first():
            return {'message': 'Baby already exists'}, 400

        baby = Baby(user_id=user_id, name=baby_name.capitalize(), gender=gender, dob=dob_date)
        db.session.add(baby)
        db.session.commit()
        return baby.json(), 200

    def delete(self, user_id, baby_name):
        if Baby.query.filter_by(user_id=user_id).filter_by(name=baby_name.capitalize()).first():
            Baby.query.filter_by(user_id=user_id).filter_by(name=baby_name.capitalize()).delete()
            db.session.commit()
            return {'message': f'{baby_name} deleted'}, 200
        else:
            return {'message': f'{baby_name} not found'}, 404


api.add_resource(BabyResource, '/<user_id>/<baby_name>')
