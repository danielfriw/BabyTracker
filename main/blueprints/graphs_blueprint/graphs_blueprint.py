from flask import Blueprint, render_template, request, flash, session
from flask_login import login_required, current_user
from main import db, app
from main.blueprints.graphs_blueprint.models import TestResults
from main.utils.percentiles_calc import percentile_calc, graph_data_boys, graph_data_girls


graphs_blueprint = Blueprint('graphs', __name__, url_prefix='/graphs', static_folder='static', template_folder='templates')

@app.route('/height_percentile', methods=['GET', 'POST'])
@login_required
def height_percentile():
    test_name = 'length_percentile'

    # graph creation data
    graph_data = graph_data_boys if session['baby_gender'] == 'm' else graph_data_girls
    months_label, lowest_percentile_values, highest_percentile_values = (
        graph_data['Month'],
        graph_data['2nd percentile'],
        graph_data['98th percentile']
    )

    previous_results = (TestResults.query.filter_by(user_id=current_user.id)
                        .filter_by(baby_id=session['baby_id'])
                        .filter_by(test_name='length_percentile')
                        .all())
    previous_results_dict = {
        result.age_in_months: {'length': result.length, 'percentile_result': result.percentile_result}
        for result in previous_results}

    if request.method == 'POST':
        age_in_months = int(request.form.get('age_in_months'))
        length = float(request.form.get('length'))

        current_percentile_result = percentile_calc(session['baby_gender'], age_in_months, length)

        if current_percentile_result is None or current_percentile_result in [0, 100]:
            error_message = ('Please enter a valid age and length' if current_percentile_result is None
                             else f'The length is {"below" if current_percentile_result == 0 else "above"} the chart range.')
            flash(error_message)

            return render_template('height_percentile.html',
                                   labels=months_label,
                                   lowest_percentile_values=lowest_percentile_values,
                                   highest_percentile_values=highest_percentile_values,
                                   previous_results=previous_results_dict,
                                   percentile=None,
                                   scatter_ponit_x=None,
                                   scatter_ponit_y=None)

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
                                      test_name='length_percentile',
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

    return render_template('height_percentile.html',
                           labels=months_label,
                           lowest_percentile_values=lowest_percentile_values,
                           highest_percentile_values=highest_percentile_values,
                           previous_results=previous_results_dict,
                           percentile=None,
                           scatter_ponit_x=None,
                           scatter_ponit_y=None)
