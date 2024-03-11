from flask import Blueprint, request, flash
from flask_login import login_required

from main import app
from main.blueprints.length_percentile_graph_blueprint.services import render_length_percentile_graph, \
    calculate_results_to_db

length_percentile_graph_blueprint = Blueprint('length_percentile_graph', __name__,
                                              url_prefix='/length_percentile_graph',
                                              static_folder='static', template_folder='templates')


@app.route('/generate_length_percentile_graph', methods=['GET'])
@login_required
def get_generate_length_percentile_graph():
    return render_length_percentile_graph(current_age_in_months=None)


@app.route('/generate_length_percentile_graph', methods=['POST'])
@login_required
def post_generate_length_percentile_graph():
    current_age_in_months = int(request.form.get('age_in_months'))
    length = float(request.form.get('length'))

    try:
        calculate_results_to_db(current_age_in_months, length)
        return render_length_percentile_graph(current_age_in_months=current_age_in_months)

    except ValueError as ve:
        flash(str(ve))
        return render_length_percentile_graph(current_age_in_months=None)
