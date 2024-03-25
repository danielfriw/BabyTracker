from unittest.mock import patch

import pytest
from flask import url_for, session
from main.blueprints.length_percentile_graph_blueprint.models import LengthMeasurementsResults
from main.blueprints.length_percentile_graph_blueprint.services import calculate_results_to_db


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
def test_post_generate_graph_success(mock_render_length_percentile_graph, mock_calculate_results_to_db, mock_get_data_from_html_form, authenticated_client, app):
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

#
# @patch('your_application.main.utils.length_percentile_calculator.length_percentile_calculator.LengthPercentileCalculator.calculate_percentile')
# def test_calculate_results_to_db(self, mock_calculate_percentile, user):
#     mock_calculate_percentile.return_value = 50
#     calculate_results_to_db(12, 75.0)
#     result = LengthMeasurementsResults.query.first()
#     assert result.percentile_result == 50
#     assert result.length == 75.0
#     assert result.age_in_months == 12
#
# def test_update_or_add_test_result_in_db_new_record(self, user):
#     assert LengthMeasurementsResults.query.count() == 0
#     update_or_add_test_result_in_db(12, 75.0, 50)
#     assert LengthMeasurementsResults.query.count() == 1
#
# def test_update_or_add_test_result_in_db_update_record(self, user):
#     new_length = 76.0
#     new_percentile = 60
#     add_test_results_in_db(12, 75.0, 50)  # Initial add
#     update_or_add_test_result_in_db(12, new_length, new_percentile)  # Update
#     result = LengthMeasurementsResults.query.first()
#     assert result.length == new_length
#     assert result.percentile_result == new_percentile
#
# @patch('flask.render_template')
# def test_render_length_percentile_graph(self, mock_render_template, user):
#     render_length_percentile_graph(12)
#     mock_render_template.assert_called_once()
#     args, kwargs = mock_render_template.call_args
#     assert kwargs['current_age'] == 12
#     assert 'graph_background_data' in kwargs
#     assert 'all_tests_results_dict' in kwargs
#
# @patch('pandas.read_csv')
# def test_create_graph_background_data(self, mock_read_csv, user):
#     mock_read_csv.return_value = MagicMock(to_dict=MagicMock(return_value={'age_in_months': [1, 2], 'ninty_eighth_percentile_length': [50, 60], 'second_percentile_length': [20, 30]}))
#     data = create_graph_background_data()
#     assert 'x_axis_months' in data
#     assert 'upper_percentile_line_values' in data
#     assert 'lower_percentile_line_values' in data
#
# def test_generate_all_results_dict_from_db(self, user):
#     add_test_results_in_db(12, 75.0, 50)
#     results_dict = generate_all_results_dict_from_db()
#     assert len(results_dict) == 1
#     assert 12 in results_dict
#     assert results_dict[12]['length'] == 75.0
#     assert results_dict[12]['percentile_result'] == 50