from flask_login import current_user
from main.blueprints.baby_blueprint.models import Baby

def baby_context_processor_for_navbar_dropdown_list():
    """
    This function is used to render the users babies in the navbar dropdown list
    It runs before that the index template is rendered.
    :return: dictionary with the users babies
    """
    if current_user.is_authenticated:
        babies = Baby.query.filter_by(user_id=current_user.id).all()
        return {'babies': babies}
    return {}