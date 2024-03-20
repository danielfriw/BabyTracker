import os

from flask import Flask

from extensions import db, login_manager, migrate
from main.blueprints.api_baby_blueprint.baby_api import api_baby_blueprint
from main.blueprints.auth_blueprint.views import auth_blueprint
from main.blueprints.baby_blueprint.views import baby_blueprint
from main.blueprints.events_blueprint.views import events_blueprint
from main.blueprints.index_blueprint.views import index_blueprint
from main.blueprints.length_percentile_graph_blueprint.views import length_percentile_graph_blueprint
from main.utils.utils import baby_context_processor_for_navbar_dropdown_list


def create_app(test_config=None):
    app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))

    if test_config is None:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    else:
        app.config.update(test_config)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["SECRET_KEY"] = 'mysecretkey'

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    app.context_processor(baby_context_processor_for_navbar_dropdown_list)

    app.register_blueprint(index_blueprint, url_prefix='/')
    app.register_blueprint(baby_blueprint, url_prefix='/baby')
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(events_blueprint, url_prefix='/events')
    app.register_blueprint(length_percentile_graph_blueprint, url_prefix='/length_percentile_graph')
    app.register_blueprint(api_baby_blueprint, url_prefix='/api/baby')

    login_manager.login_view = 'auth.get_login'

    with app.app_context():
        db.create_all()

    return app



if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
