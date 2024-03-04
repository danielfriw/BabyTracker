from main.blueprints.index_blueprint.index_blueprint import index_blueprint
from main.blueprints.baby_blueprint.baby_blueprint import baby_blueprint
from main.blueprints.auth_blueprint.auth_blueprint import auth_blueprint
from main.blueprints.events_blueprint.events_blueprint import events_blueprint
from main.blueprints.graphs_blueprint.graphs_blueprint import graphs_blueprint
from main.blueprints.api_baby_blueprint.api_baby_blueprint import api_baby_blueprint
from main import app, db
from main.utils.baby_context_processor_for_navbar_dropdown_list import baby_context_processor_for_navbar_dropdown_list

# Create tables (initialize the database)
with app.app_context():
    db.create_all()


# Context processors: these run before the template is rendered
# We use it here to render the users babies in the navbar dropdown list
app.context_processor(baby_context_processor_for_navbar_dropdown_list)


app.register_blueprint(index_blueprint, url_prefix='/')
app.register_blueprint(baby_blueprint, url_prefix='/baby')
app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(events_blueprint, url_prefix='/events')
app.register_blueprint(graphs_blueprint, url_prefix='/graphs')
app.register_blueprint(api_baby_blueprint, url_prefix='/api/baby')



if __name__ == '__main__':
    app.run(debug=True)
