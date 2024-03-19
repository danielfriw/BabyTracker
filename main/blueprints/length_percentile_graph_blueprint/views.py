from flask import Blueprint, request, flash
from flask_login import login_required

from main.blueprints.length_percentile_graph_blueprint.services import render_length_percentile_graph, \
    calculate_results_to_db

length_percentile_graph_blueprint = Blueprint('length_percentile_graph', __name__,
                                              url_prefix='/length_percentile_graph',
                                              static_folder='static', template_folder='templates')


@length_percentile_graph_blueprint.route('/generate_graph', methods=['GET'])
@login_required
def get_generate_graph():
    return render_length_percentile_graph(current_age_in_months=None)


@length_percentile_graph_blueprint.route('/generate_graph', methods=['POST'])
@login_required
def post_generate_graph():
    current_age_in_months = int(request.form.get('age_in_months'))
    length = float(request.form.get('length'))

    try:
        calculate_results_to_db(current_age_in_months, length)
        return render_length_percentile_graph(current_age_in_months=current_age_in_months)

    except ValueError as ve:
        flash(str(ve))
        return render_length_percentile_graph(current_age_in_months=None)
