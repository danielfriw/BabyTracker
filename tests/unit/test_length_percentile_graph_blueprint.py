from unittest.mock import patch

from flask import url_for, session
from werkzeug.exceptions import NotFound

from extensions import db
from main.blueprints.length_percentile_graph_blueprint.models import LengthMeasurementsResults
from main.blueprints.length_percentile_graph_blueprint.services import calculate_results_to_db, \
    update_or_add_test_result_in_db, add_test_results_in_db, update_test_results_in_db, render_length_percentile_graph, \
    create_graph_background_data


@patch('main.blueprints.length_percentile_graph_blueprint.views.render_length_percentile_graph')
def test_get_generate_graph(mock_render_length_percentile_graph, authenticated_client, app):
    mock_render_length_percentile_graph.return_value = 'rendered template'

    with app.test_request_context():
        response = authenticated_client.get(url_for('length_percentile_graph.get_generate_graph'))

        assert response.status_code == 200
        mock_render_length_percentile_graph.assert_called_once_with(current_age_in_months=None)


@patch('main.blueprints.length_percentile_graph_blueprint.views.get_data_from_html_form')
@patch('main.blueprints.length_percentile_graph_blueprint.views.calculate_results_to_db')
@patch('main.blueprints.length_percentile_graph_blueprint.views.render_length_percentile_graph')
def test_post_generate_graph_success(mock_render_length_percentile_graph, mock_calculate_results_to_db,
                                     mock_get_data_from_html_form, authenticated_client, app):
    mock_get_data_from_html_form.age_in_months = 1
    mock_get_data_from_html_form.length = 55
    mock_calculate_results_to_db.return_value = None
    mock_render_length_percentile_graph.return_value = 'rendered template'

    with app.test_request_context():
        response = authenticated_client.post(url_for('length_percentile_graph.post_generate_graph'))

        assert response.status_code == 200
        mock_render_length_percentile_graph.assert_called_once_with(current_age_in_months=1)


@patch('main.blueprints.length_percentile_graph_blueprint.views.get_data_from_html_form')
@patch('main.blueprints.length_percentile_graph_blueprint.views.calculate_results_to_db')
@patch('main.blueprints.length_percentile_graph_blueprint.views.render_length_percentile_graph')
def test_post_generate_graph_failure(mock_render_length_percentile_graph, mock_calculate_results_to_db,
                                     mock_get_data_from_html_form, authenticated_client, app):
    mock_get_data_from_html_form.age_in_months = 1
    mock_get_data_from_html_form.length = 55
    mock_calculate_results_to_db.side_effect = ValueError('Invalid input')
    mock_render_length_percentile_graph.return_value = 'rendered template'

    with app.test_request_context():
        response = authenticated_client.post(url_for('length_percentile_graph.post_generate_graph'))

        assert response.status_code == 200
        mock_render_length_percentile_graph.assert_called_once_with(current_age_in_months=None)


@patch('main.blueprints.length_percentile_graph_blueprint.services.LengthPercentileCalculator')
@patch('main.blueprints.length_percentile_graph_blueprint.services.update_or_add_test_result_in_db')
def test_calculate_results_to_db(mock_update_or_add_test_result_in_db, mock_LengthPercentileCalculator, app):
    with app.test_request_context():
        session['baby_gender'] = 'm'
        mock_LengthPercentileCalculator.calculate_percentile.return_value = 50
        mock_update_or_add_test_result_in_db.return_value = None

        calculate_results_to_db(12, 75.0)

        assert mock_update_or_add_test_result_in_db.call_count == 1


@patch('main.blueprints.length_percentile_graph_blueprint.services.update_test_results_in_db')
@patch('main.blueprints.length_percentile_graph_blueprint.services.add_test_results_in_db')
def test_update_or_add_test_result_in_db_new_record(mock_add_test_results_in_db, mock_update_test_results_in_db, app):
    mock_update_test_results_in_db.return_value = None
    mock_add_test_results_in_db.return_value = None

    update_or_add_test_result_in_db(12, 75.0, 50)

    assert mock_update_test_results_in_db.call_count == 1
    assert mock_add_test_results_in_db.call_count == 0


#
@patch('main.blueprints.length_percentile_graph_blueprint.services.update_test_results_in_db')
@patch('main.blueprints.length_percentile_graph_blueprint.services.add_test_results_in_db')
def test_update_or_add_test_result_in_db_update_record(mock_add_test_results_in_db, mock_update_test_results_in_db,
                                                       app):
    mock_update_test_results_in_db.side_effect = NotFound
    mock_add_test_results_in_db.return_value = None

    update_or_add_test_result_in_db(12, 75.0, 50)

    assert mock_update_test_results_in_db.call_count == 1
    assert mock_add_test_results_in_db.call_count == 1


@patch('main.blueprints.length_percentile_graph_blueprint.services.current_user')
def test_update_test_results_in_db(mock_current_user, app):
    with app.test_request_context():
        mock_current_user.id = 1
        session['baby_id'] = 1
        existing_test_result = LengthMeasurementsResults(user_id=mock_current_user.id,
                                                         baby_id=session['baby_id'],
                                                         age_in_months=12,
                                                         length=60,
                                                         percentile_result=60)
        db.session.add(existing_test_result)
        db.session.commit()

        update_test_results_in_db(12, 80, 80)

        assert LengthMeasurementsResults.query.count() == 1
        assert LengthMeasurementsResults.query.first().age_in_months == 12
        assert LengthMeasurementsResults.query.first().length == 80
        assert LengthMeasurementsResults.query.first().percentile_result == 80


@patch('main.blueprints.length_percentile_graph_blueprint.services.current_user')
def test_add_test_results_in_db(mock_current_user, app):
    with app.test_request_context():
        mock_current_user.id = 1
        session['baby_id'] = 1

        add_test_results_in_db(12, 75.0, 50)

        assert LengthMeasurementsResults.query.count() == 1
        assert LengthMeasurementsResults.query.first().age_in_months == 12
        assert LengthMeasurementsResults.query.first().length == 75.0
        assert LengthMeasurementsResults.query.first().percentile_result == 50


@patch('main.blueprints.length_percentile_graph_blueprint.services.generate_all_results_dict_from_db')
@patch('main.blueprints.length_percentile_graph_blueprint.services.create_graph_background_data')
def test_render_length_percentile_graph(mock_create_graph_background_data, mock_generate_all_results_dict_from_db,
                                        captured_templates, app):
    with app.test_request_context():
        mock_create_graph_background_data.return_value = {}
        mock_generate_all_results_dict_from_db.return_value = {}

        render_length_percentile_graph(None)

        assert mock_create_graph_background_data.call_count == 1
        assert mock_generate_all_results_dict_from_db.call_count == 1
        assert captured_templates[0][0].name == 'length_percentile_graph.html'


@patch('main.blueprints.length_percentile_graph_blueprint.services.get_background_data_by_gender')
def test_create_graph_background_data(mock_get_background_data_by_gender):
    mock_get_background_data_by_gender.return_value = {'age_in_months': [1, 2, 3],
                                                       'ninty_eighth_percentile_length': [10, 20, 30],
                                                       'second_percentile_length': [5, 15, 25]}
    data = create_graph_background_data()

    assert 'x_axis_months' in data
    assert 'upper_percentile_line_values' in data
    assert 'lower_percentile_line_values' in data
