from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.exceptions import NotFound
from main import db, app
from main.blueprints.generate_length_percentile_graph_blueprint.models import TestResults
from main.utils.percentiles_calc import percentile_calc, graph_data_boys, graph_data_girls

generate_length_percentile_graph_blueprint = Blueprint('generate_length_percentile_graph', __name__,
                                                       url_prefix='/generate_length_percentile_graph',
                                                       static_folder='static', template_folder='templates')

TEST_NAME = 'length_percentile'


@app.route('/generate_length_percentile_graph', methods=['GET', 'POST'])
@login_required
def generate_length_percentile_graph():
    """
    Generate length percentile graph
    :return: render the graph with all results, if current results aren't given, only past results will be displayed
    """
    current_age_in_months = None

    if request.method == 'POST':
        current_age_in_months, length = get_baby_measurements_from_form()
        update_or_add_test_result_in_db(current_age_in_months, length)

    return render_length_percentile_graph(current_age_in_months)


def get_baby_measurements_from_form():
    """
    Get the baby's age and length from the form.
    :return: age_in_months, length
    """
    age_in_months = int(request.form.get('age_in_months'))
    length = float(request.form.get('length'))
    return age_in_months, length


def update_or_add_test_result_in_db(age_in_months, length):
    """
    Add the test result to the database.
    If the test result already exists, update the test result.
    :param test_result: the test result
    :param current_percentile_result: the current percentile result
    """
    percentile_result = get_length_percentile_result_if_valid(age_in_months, length)
    try:
        update_test_results_in_db(age_in_months, length, percentile_result)
    except NotFound:
        add_test_results_in_db(age_in_months, length, percentile_result)
    pass


def get_length_percentile_result_if_valid(age_in_months, length):
    """
    get lenght percentile results, if invalid flash error message and re-render the page.
    :param age_in_month: baby's age in months
    :param length: baby's length in CM
    :return: Percentile result
    """
    try:
        percentile_result = percentile_calc(session['baby_gender'], age_in_months, length)
    except ValueError as ve:
        flash(str(ve))
        print(redirect(url_for('generate_length_percentile_graph')))
        test = redirect(url_for('generate_length_percentile_graph'))
        return redirect(url_for('generate_length_percentile_graph'))

    return percentile_result


def update_test_results_in_db(age_in_months, length, percentile_result):
    existing_test_result = (TestResults.query.filter_by(user_id=current_user.id,
                                                        baby_id=session['baby_id'],
                                                        test_name=TEST_NAME,
                                                        age_in_months=age_in_months)
                            .first_or_404())
    existing_test_result.length = length
    existing_test_result.percentile_result = percentile_result
    db.session.commit()


def add_test_results_in_db(age_in_months, length, percentile_result):
    new_test_result = TestResults(user_id=current_user.id,
                                  baby_id=session['baby_id'],
                                  test_name=TEST_NAME,
                                  age_in_months=age_in_months,
                                  length=length,
                                  percentile_result=percentile_result)
    db.session.add(new_test_result)
    db.session.commit()


def render_length_percentile_graph(current_age_in_months: int):
    """
    Render the percentile graph with only the previous results.
    :return: rendered template with the percentile graph and the previous results
    """
    background_data_dict = create_graph_background_data()
    all_tests_results_dict = generate_all_tests_results_dict_from_db()

    return render_template('length_percentile.html',
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
    return graph_data_boys if session['baby_gender'] == 'm' else graph_data_girls


def generate_all_tests_results_dict_from_db():
    """
    Generate the previous results dictionary.
    The key is the baby's age in months and the value is a dictionary with the length and percentile result.
    :return: dictionary in the format of {age_in_months: {'length': length, 'percentile_result': percentile_result}}
    """
    all_results = (TestResults.query.filter_by(user_id=current_user.id
                                               , baby_id=session['baby_id']
                                               , test_name=TEST_NAME)
                   .all())
    return {r.age_in_months: {'length': r.length, 'percentile_result': r.percentile_result} for r in all_results}
