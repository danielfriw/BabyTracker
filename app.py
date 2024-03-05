from main.blueprints.index_blueprint.views import index_blueprint
from main.blueprints.baby_blueprint.views import baby_blueprint
from main.blueprints.auth_blueprint.views import auth_blueprint
from main.blueprints.events_blueprint.views import events_blueprint
from main.blueprints.height_percentile_blueprint.views import height_percentile_blueprint
from main.blueprints.api_baby_blueprint.views import api_baby_blueprint
from main import app, db
from main.utils.baby_context_processor_for_navbar_dropdown_list import baby_context_processor_for_navbar_dropdown_list

with app.app_context():
    db.create_all()

app.context_processor(baby_context_processor_for_navbar_dropdown_list)

app.register_blueprint(index_blueprint, url_prefix='/')
app.register_blueprint(baby_blueprint, url_prefix='/baby')
app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(events_blueprint, url_prefix='/events')
app.register_blueprint(height_percentile_blueprint, url_prefix='/graphs')
app.register_blueprint(api_baby_blueprint, url_prefix='/api/baby')

if __name__ == '__main__':
    app.run(debug=True)
