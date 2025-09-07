"""Tests for the main module of the GPX project.

This module contains unit tests for the functions defined in `src.main`,
including CSV loading and the main execution flow.
"""

import pytest
import pandas as pd
import os
from unittest.mock import patch, MagicMock
import numpy as np # Import numpy
from src.main import load_hotels_from_csv, run_main

@patch('src.main.pd.read_csv')
def test_load_hotels_from_csv_success(mock_read_csv):
    """Tests that load_hotels_from_csv successfully loads a CSV file.

    It mocks pandas.read_csv to control its return value and verifies
    that the function calls read_csv with the correct arguments and returns
    the expected DataFrame.
    """
    # Arrange: Set up the mock DataFrame and the mock's return value.
    mock_df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
    mock_read_csv.return_value = mock_df
    file_path = "dummy.csv"

    # Act: Call the function under test.
    result_df = load_hotels_from_csv(file_path)

    # Assert: Verify the mock was called correctly and the result is as expected.
    mock_read_csv.assert_called_once_with(file_path, sep=";")
    pd.testing.assert_frame_equal(result_df, mock_df)

def test_load_hotels_from_csv_file_not_found(capsys):
    """Tests that load_hotels_from_csv handles FileNotFoundError correctly.

    It verifies that the function returns None and prints an error message
    when the specified CSV file does not exist.
    """
    # Arrange: Define a non-existent file path.
    file_path = "non_existent.csv"

    # Act: Call the function under test.
    result_df = load_hotels_from_csv(file_path)

    # Assert: Verify the function returns None and the correct error message is printed.
    assert result_df is None
    captured = capsys.readouterr()
    assert f"Error: The file {file_path} was not found." in captured.out

@patch('src.main.load_dotenv')
@patch('src.main.os.getenv')
@patch('src.main.load_hotels_from_csv')
@patch('src.main.get_gps_coordinates')
@patch('src.main.create_gpx_file')
def test_main_execution_flow(
    mock_create_gpx_file,
    mock_get_gps_coordinates,
    mock_load_hotels_from_csv,
    mock_os_getenv,
    mock_load_dotenv,
    capsys
):
    """Tests the complete execution flow of the run_main function.

    This test mocks all external dependencies (environment variables, CSV loading,
    geocoding, and GPX file creation) to ensure that `run_main` orchestrates
    these components correctly, processes data as expected, and produces
    the correct outputs and console messages.
    """
    # Arrange: Set up mock return values and side effects for all external dependencies.
    # Mock environment variables that run_main will try to retrieve.
    mock_os_getenv.side_effect = lambda key: {
        "GPX_FILE": "output.gpx",
        "CSV_FILE": "input.csv",
        "CSV_W_COOR_FILE": "output_w_coor.csv",
    }.get(key)

    # Mock the initial DataFrame that load_hotels_from_csv would return.
    # It includes NaN values for Latitude and Longitude, explicitly typed as float64
    # to match the expected output after geocoding.
    initial_hotels_df = pd.DataFrame({
        "Betrieb": ["Hotel A", "Hotel B", "Hotel C"],
        "Straße": ["Street A", "Street B", "Street C"],
        "Stadt": ["City A", "City B", "City C"],
        "Latitude": [np.nan, np.nan, np.nan], # Initialize with np.nan
        "Longitude": [np.nan, np.nan, np.nan], # Initialize with np.nan
    }).astype({"Latitude": "float64", "Longitude": "float64"}) # Explicitly set dtypes
    
    # Configure the mock for load_hotels_from_csv to return our prepared DataFrame.
    mock_load_hotels_from_csv.return_value = initial_hotels_df

    # Mock the to_csv method of the DataFrame instance that run_main will operate on.
    # This allows us to verify that to_csv is called with the correct arguments.
    initial_hotels_df.to_csv = MagicMock()

    # Mock geocoding responses for get_gps_coordinates.
    # The side_effect list simulates different geocoding scenarios for each hotel:
    # - Hotel A: Full address geocodes successfully.
    # - Hotel B: Full address fails, but street+city geocodes successfully.
    # - Hotel C: Full address fails, street+city fails, but business+city geocodes successfully.
    mock_get_gps_coordinates.side_effect = [
        (10.0, 20.0),  # Hotel A: Full address success
        None,          # Hotel B: Full address fail
        (30.0, 40.0),  # Hotel B: Street+City success
        None,          # Hotel C: Full address fail
        None,          # Hotel C: Street+City fail
        (50.0, 60.0),  # Hotel C: Business+City success
    ]

    # Act: Execute the main function.
    run_main()

    # Assert: Verify that all mocked functions were called correctly and the outputs are as expected.
    # Verify that dotenv was loaded.
    mock_load_dotenv.assert_called_once()
    # Verify environment variables were queried.
    mock_os_getenv.assert_any_call("GPX_FILE")
    mock_os_getenv.assert_any_call("CSV_FILE")
    mock_os_getenv.assert_any_call("CSV_W_COOR_FILE")
    # Verify that hotels were loaded from the correct CSV file.
    mock_load_hotels_from_csv.assert_called_once_with("input.csv")

    # Verify geocoding calls for each address variation.
    mock_get_gps_coordinates.assert_any_call("Hotel A, Street A, City A, Germany")
    mock_get_gps_coordinates.assert_any_call("Street B, City B, Germany")
    mock_get_gps_coordinates.assert_any_call("Hotel C, City C, Germany")

    # Verify that the to_csv method on the DataFrame was called exactly once.
    initial_hotels_df.to_csv.assert_called_once()

    # Extract arguments passed to the to_csv call.
    to_csv_args, to_csv_kwargs = initial_hotels_df.to_csv.call_args

    # Verify the file path and other parameters passed to to_csv.
    file_path_from_mock = to_csv_args[0]
    assert file_path_from_mock == 'output_w_coor.csv'
    assert to_csv_kwargs['sep'] == ';'
    assert to_csv_kwargs['index'] == False
    assert to_csv_kwargs['encoding'] == 'utf-8'

    # Define the expected state of the DataFrame after run_main has processed it.
    expected_output_df = pd.DataFrame({
        "Betrieb": ["Hotel A", "Hotel B", "Hotel C"],
        "Straße": ["Street A", "Street B", "Street C"],
        "Stadt": ["City A", "City B", "City C"],
        "Latitude": [10.0, 30.0, 50.0],
        "Longitude": [20.0, 40.0, 60.0],
    })
    # Assert that the DataFrame modified in-place by run_main matches the expected output.
    pd.testing.assert_frame_equal(initial_hotels_df, expected_output_df)

    # Verify that the GPX file creation function was called with the final DataFrame and correct filename.
    mock_create_gpx_file.assert_called_once_with(initial_hotels_df, "output.gpx")

    # Verify key messages printed to the console using capsys.
    captured = capsys.readouterr()
    assert "Hotels loaded from CSV:" in captured.out
    assert "Geocoded: Hotel A, Street A, City A, Germany (10.0, 20.0)" in captured.out
    assert "Geocoded: Street B, City B, Germany (30.0, 40.0)" in captured.out
    assert "Geocoded: Hotel C, City C, Germany (50.0, 60.0)" in captured.out
    assert "Hotels with GPS coordinates:3 out of 3" in captured.out
    assert "GPX file 'output.gpx' created successfully." in captured.out
