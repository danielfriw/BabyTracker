import os

from flask import request
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


def get_static_data_file_path(file_name: str, static_folder: str, current_file_path):
    """
    This function returns the path of the static data file.
    """
    script_dir = os.path.dirname(os.path.abspath(current_file_path))
    return os.path.join(script_dir, static_folder, file_name)


def get_data_from_html_form(data_name: str):
    """
    Get the comment from the form.
    :return: str
    """
    return request.form.get(data_name)
