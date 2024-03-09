from typing import Optional

from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.exceptions import NotFound
from main import db, app
from main.blueprints.generate_length_percentile_graph_blueprint.models import TestResults
from main.utils.percentiles_calc import percentile_calc, graph_data_boys, graph_data_girls

generate_length_percentile_graph_blueprint = Blueprint('generate_length_percentile_graph', __name__,
                                                       url_prefix='/generate_length_percentile_graph',
                                                       static_folder='static', template_folder='templates')


@app.route('/generate_length_percentile_graph', methods=['GET', 'POST'])
@login_required
def generate_length_percentile_graph():
    """
    Generate and render the length percentile graph.
    :return: Rendered template with the percentile graph and previous results.
    """
    if request.method == 'POST':

        current_age_in_months, length = get_baby_measurements_from_form()

        try:
            calculate_results_to_db(current_age_in_months, length)
            return render_length_percentile_graph(current_age_in_months)

        except ValueError as ve:
            flash(str(ve))

    return render_length_percentile_graph(current_age_in_months=None)


def get_baby_measurements_from_form():
    """
    Extract baby's age and length from the form.
    :return: age_in_months, length.
    """
    age_in_months = int(request.form.get('age_in_months'))
    length = float(request.form.get('length'))
    return age_in_months, length


def calculate_results_to_db(current_age_in_months, length):
    """
    Calculate percentile results for length measurements and update the database.
    :param current_age_in_months: Baby's current age in months.
    :param length: Baby's length in CM.
    """
    percentile_result = percentile_calc(session['baby_gender'], current_age_in_months, length)
    update_or_add_test_result_in_db(current_age_in_months, length, percentile_result)


def update_or_add_test_result_in_db(age_in_months, length, percentile_result):
    """
    Update or add test results to the database.
    :param age_in_months: Baby's age in months.
    :param length: Baby's length in CM.
    :param percentile_result: Calculated percentile result.
    """
    try:
        update_test_results_in_db(age_in_months, length, percentile_result)
    except NotFound:
        add_test_results_in_db(age_in_months, length, percentile_result)


def update_test_results_in_db(age_in_months, length, percentile_result):
    """
    Update test results in the database.
    :param age_in_months: Baby's age in months.
    :param length: Baby's length in CM.
    :param percentile_result: Calculated percentile result.
    """
    existing_test_result = (TestResults.query.filter_by(user_id=current_user.id,
                                                        baby_id=session['baby_id'],
                                                        test_name=get_test_name(),
                                                        age_in_months=age_in_months).first_or_404())
    existing_test_result.length = length
    existing_test_result.percentile_result = percentile_result
    db.session.commit()


def add_test_results_in_db(age_in_months, length, percentile_result):
    """
    Add test results to the database.
    :param age_in_months: Baby's age in months.
    :param length: Baby's length in CM.
    :param percentile_result: Calculated percentile result.
    """
    new_test_result = TestResults(user_id=current_user.id,
                                  baby_id=session['baby_id'],
                                  test_name=get_test_name(),
                                  age_in_months=age_in_months,
                                  length=length,
                                  percentile_result=percentile_result)
    db.session.add(new_test_result)
    db.session.commit()

def get_test_name():
    return 'length_percentile'

def render_length_percentile_graph(current_age_in_months: Optional[int]):
    """
    Render the percentile graph with previous results.
    :param current_age_in_months: Baby's current age in months.
    :return: Rendered template with the percentile graph and previous results.
    """
    background_data_dict = create_graph_background_data()
    all_tests_results_dict = generate_all_tests_results_dict_from_db()

    return render_template('generate_length_percentile_graph.html',
                           graph_background_data=background_data_dict,
                           all_tests_results_dict=all_tests_results_dict,
                           current_age=current_age_in_months)


def create_graph_background_data():
    """
    Get the static graph background data - which is used to plot the graph.
    - months labels - x-axis
    - lowest percentile values & highest percentile values - y-axis
    The percentile values are used to plot the percentile boundary lines on the graph.
    :return: months labels, lowest percentile values and highest percentile values
    """
    background_data_dict = get_data_by_gender()

    return {'x_axis_months': background_data_dict['Month'],
            'upper_percentile_line_values': background_data_dict['98th percentile'],
            'lower_percentile_line_values': background_data_dict['2nd percentile']}


def get_data_by_gender():
    """
    Get percentile graph static background data based on the baby's gender.
    :return: Graph data for boys or girls.
    """
    return graph_data_boys if session['baby_gender'] == 'm' else graph_data_girls


def generate_all_tests_results_dict_from_db():
    """
    Generate a dictionary of previous results.
    :return: Dictionary in the format {age_in_months: {'length': length, 'percentile_result': percentile_result}}.
    """
    all_results = (TestResults.query.filter_by(user_id=current_user.id
                                               , baby_id=session['baby_id']
                                               , test_name=get_test_name()).all())
    return {r.age_in_months: {'length': r.length, 'percentile_result': r.percentile_result} for r in all_results}
