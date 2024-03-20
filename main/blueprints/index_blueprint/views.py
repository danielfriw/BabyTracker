from flask import Blueprint, redirect, url_for
from flask_login import login_required, current_user

from main.blueprints.baby_blueprint.models import Baby
from main.blueprints.baby_blueprint.services import set_baby_data_in_session
from main.blueprints.index_blueprint.services import is_a_baby_assigned_to_session, does_user_have_babies, \
    render_index_page_with_all_events

index_blueprint = Blueprint('index', __name__, url_prefix='/', static_folder='static', template_folder='templates',
                            static_url_path='/main/blueprints/index_blueprint/static')


@index_blueprint.route('/')
@login_required
def index():
    if not does_user_have_babies():
        return redirect(url_for('baby.get_add_baby'))

    if not is_a_baby_assigned_to_session():
        first_user_baby = Baby.query.filter_by(user_id=current_user.id).first()
        set_baby_data_in_session(first_user_baby)

    return render_index_page_with_all_events()
