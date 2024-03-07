from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from flask_login import login_required, current_user
from main import db, app
from main.blueprints.height_percentile_blueprint.models import TestResults
from main.utils.percentiles_calc import percentile_calc, graph_data_boys, graph_data_girls

height_percentile_blueprint = Blueprint('height_percentile', __name__, url_prefix='/height_percentile', static_folder='static', template_folder='templates')


TEST_NAME = 'height_percentile'

@app.route('/height_percentile', methods=['GET', 'POST'])
@login_required
def height_percentile():

    if request.method == 'POST':
        age_in_months, length = get_baby_measurements_from_form()
        current_percentile_result = percentile_calc(session['baby_gender'], age_in_months, length)
        check_is_valid_result(current_percentile_result) # TODO: change to try and except


        if test_result:
            # update the test results
            test_result.length = length
            test_result.percentile_result = current_percentile_result

        else:
            # add new test results
            test_result = TestResults(user_id=current_user.id,
                                      baby_id=session['baby_id'],
                                      test_name='height_percentile',
                                      age_in_months=age_in_months,
                                      length=length,
                                      percentile_result=current_percentile_result)
            db.session.add(test_result)

        db.session.commit()

        # remove the current result from the previous results
        previous_results_dict.pop(age_in_months, None)

        return render_template('height_percentile.html',
                               labels=months_label,
                               lowest_percentile_values=lowest_percentile_values,
                               highest_percentile_values=highest_percentile_values,
                               previous_results=previous_results_dict,
                               percentile=current_percentile_result,
                               scatter_ponit_x=age_in_months,
                               scatter_ponit_y=length)

    return render_percentile_graph_with_only_previous_results()

def get_baby_measurements_from_form():
    """
    Get the baby's age and length from the form.
    :return: age_in_months, length
    """
    age_in_months = int(request.form.get('age_in_months'))
    length = float(request.form.get('length'))
    return age_in_months, length


def check_is_valid_result(current_percentile_result):
    """
    Check if the current percentile result is valid.
    If the current percentile result is invalid, flash an error message and render the percentile graph with only the previous results.
    :param current_percentile_result: the current percentile result
    """
    if is_valid_current_percentile_result(current_percentile_result):
        return
    flash_error_message_for_invalid_current_percentile_result(current_percentile_result)
    return redirect(url_for('height_percentile'))

def flash_error_message_for_invalid_current_percentile_result(current_percentile_result):
    """
    Flash an error message if the current percentile result is invalid.
    :param current_percentile_result: the current percentile result
    """
    if current_percentile_result == 0:
        error_message = 'The length is below the chart range.'
    elif current_percentile_result == 100:
        error_message = 'The length is above the chart range.'
    else:
        error_message = 'Please enter a valid age and length'

    flash(error_message)
    return

def is_valid_current_percentile_result(current_percentile_result):
    """
    Check if the current percentile result is valid.
    If the current percentile result is None or 0 or 100, it is outside of the chart range.
    :param current_percentile_result: the current percentile result
    :return: True if the current percentile result is valid, False otherwise
    """
    if current_percentile_result is None or current_percentile_result in [0, 100]:
        return False
    return True

def add_test_result_to_db(test_result, current_percentile_result):
    """
    Add the test result to the database.
    If the test result already exists, update the test result.
    :param test_result: the test result
    :param current_percentile_result: the current percentile result
    """
    test_result = (TestResults.query.filter_by(user_id=current_user.id)
                   .filter_by(baby_id=session['baby_id'])
                   .filter_by(test_name=test_name)
                   .filter_by(age_in_months=age_in_months)
                   .first())

    if test_result:
        # update the test results
        test_result.length = length
        test_result.percentile_result = current_percentile_result

    else:
        # add new test results
        test_result = TestResults(user_id=current_user.id,
                                  baby_id=session['baby_id'],
                                  test_name='height_percentile',
                                  age_in_months=age_in_months,
                                  length=length,
                                  percentile_result=current_percentile_result)
        db.session.add(test_result)

    db.session.commit()
    return

def render_percentile_graph_with_only_previous_results():
    """
    Render the percentile graph with only the previous results.
    :return: rendered template with the percentile graph and the previous results
    """
    months_label, lowest_percentile_values, highest_percentile_values = get_static_graph_background_data()
    previous_results_dict = generate_previous_results_dict()

    return render_template('height_percentile.html',
                           labels=months_label,
                           lowest_percentile_values=lowest_percentile_values,
                           highest_percentile_values=highest_percentile_values,
                           previous_results=previous_results_dict,
                           percentile=None,
                           scatter_ponit_x=None,
                           scatter_ponit_y=None)

def get_static_graph_background_data():
    """
    Get the static graph background data - which is used to plot the graph.
    - months labels - x-axis
    - lowest percentile values & highest percentile values - y-axis
    The percentile values are used to plot the percentile boundary lines on the graph.
    :return: months labels, lowest percentile values and highest percentile values
    """
    graph_static_data = graph_data_boys if session['baby_gender'] == 'm' else graph_data_girls
    months_labels = graph_static_data['Month']
    highest_percentile_values = graph_static_data['98th percentile']
    lowest_percentile_values = graph_static_data['2nd percentile']
    return months_labels, lowest_percentile_values, highest_percentile_values

def generate_previous_results_dict():
    """
    Generate the previous results dictionary.
    The key is the baby's age in months and the value is a dictionary with the length and percentile result.
    :return: dictionary in the format of {age_in_months: {'length': length, 'percentile_result': percentile_result}}
    """
    previous_results = (TestResults.query.filter_by(user_id=current_user.id)
                        .filter_by(baby_id=session['baby_id'])
                        .filter_by(test_name='height_percentile')
                        .all())
    return {result.age_in_months: {'length': result.length, 'percentile_result': result.percentile_result}
            for result in previous_results}



