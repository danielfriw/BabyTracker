from typing import Optional

import pandas as pd
from flask import render_template, session
from flask_login import current_user
from werkzeug.exceptions import NotFound

from extensions import db
from main.blueprints.length_percentile_graph_blueprint.models import LengthMeasurementsResults
from main.utils.length_percentile_calculator.length_percentile_calculator import LengthPercentileCalculator
from main.utils.utils import get_static_data_file_path


def calculate_results_to_db(current_age_in_months, length):
    """
    Calculate percentile results for length measurements and update the database.
    :param current_age_in_months: Baby's current age in months.
    :param length: Baby's length in CM.
    """
    percentile_calculator = LengthPercentileCalculator(session['baby_gender'], current_age_in_months, length)
    percentile_result = percentile_calculator.calculate_percentile()
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
    existing_test_result = (LengthMeasurementsResults.query.filter_by(user_id=current_user.id,
                                                                      baby_id=session['baby_id'],
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
    new_test_result = LengthMeasurementsResults(user_id=current_user.id,
                                                baby_id=session['baby_id'],
                                                age_in_months=age_in_months,
                                                length=length,
                                                percentile_result=percentile_result)
    db.session.add(new_test_result)
    db.session.commit()


def render_length_percentile_graph(current_age_in_months: Optional[int]):
    """
    Render the percentile graph with previous results.
    :param current_age_in_months: Baby's current age in months.
    :return: Rendered template with the percentile graph and previous results.
    """
    background_data_dict = create_graph_background_data()
    all_tests_results_dict = generate_all_results_dict_from_db()

    return render_template('length_percentile_graph.html',
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
    background_data_dict = get_background_data_by_gender()

    return {'x_axis_months': background_data_dict['age_in_months'],
            'upper_percentile_line_values': background_data_dict['ninty_eighth_percentile_length'],
            'lower_percentile_line_values': background_data_dict['second_percentile_length']}


def get_background_data_by_gender():
    """
    Get percentile graph static background data based on the baby's gender.
    :return: A dictionary containing the background data (list of values) for the percentile graph.
            The dictionary contains the following keys:
            - age_in_months: list of months
            - ninty_eighth_percentile_length: list of 98th percentile values
            - second_percentile_length: list of 2nd percentile values
    """
    if session['baby_gender'] == 'm':
        csv_file = get_static_data_file_path('static_graph_background_data_male.csv', 'static_data', __file__)
    else:
        csv_file = get_static_data_file_path('static_graph_background_data_female.csv', 'static_data', __file__)

    return pd.read_csv(csv_file).to_dict(orient='list')


def generate_all_results_dict_from_db():
    """
    Generate a dictionary of previous results.
    :return: Dictionary in the format {age_in_months: {'length': length, 'percentile_result': percentile_result}}.
    """
    all_results = (LengthMeasurementsResults.query.filter_by(user_id=current_user.id
                                                             , baby_id=session['baby_id']).all())
    return {r.age_in_months: {'length': r.length, 'percentile_result': r.percentile_result} for r in all_results}
