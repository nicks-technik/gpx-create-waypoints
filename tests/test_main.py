import pytest
import pandas as pd
import os
from unittest.mock import patch, MagicMock
import numpy as np # Import numpy
from src.main import load_hotels_from_csv, run_main

@patch('src.main.pd.read_csv')
def test_load_hotels_from_csv_success(mock_read_csv):
    # Arrange
    mock_df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
    mock_read_csv.return_value = mock_df
    file_path = "dummy.csv"

    # Act
    result_df = load_hotels_from_csv(file_path)

    # Assert
    mock_read_csv.assert_called_once_with(file_path, sep=";")
    pd.testing.assert_frame_equal(result_df, mock_df)

def test_load_hotels_from_csv_file_not_found(capsys):
    # Arrange
    file_path = "non_existent.csv"

    # Act
    result_df = load_hotels_from_csv(file_path)

    # Assert
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
    # Arrange
    # Mock environment variables
    mock_os_getenv.side_effect = lambda key: {
        "GPX_FILE": "output.gpx",
        "CSV_FILE": "input.csv",
        "CSV_W_COOR_FILE": "output_w_coor.csv",
    }.get(key)

    # Mock initial DataFrame from load_hotels_from_csv
    initial_hotels_df = pd.DataFrame({
        "Betrieb": ["Hotel A", "Hotel B", "Hotel C"],
        "Straße": ["Street A", "Street B", "Street C"],
        "Stadt": ["City A", "City B", "City C"],
        "Latitude": [np.nan, np.nan, np.nan], # Initialize with np.nan
        "Longitude": [np.nan, np.nan, np.nan], # Initialize with np.nan
    }).astype({"Latitude": "float64", "Longitude": "float64"}) # Explicitly set dtypes
    
    # Use initial_hotels_df directly as the return value
    mock_load_hotels_from_csv.return_value = initial_hotels_df

    # Mock the to_csv method of the initial_hotels_df instance
    initial_hotels_df.to_csv = MagicMock()

    # Mock geocoding responses
    # Scenario 1: Hotel A geocodes successfully
    # Scenario 2: Hotel B fails full address, succeeds street+city
    # Scenario 3: Hotel C fails full address, fails street+city, succeeds business+city
    mock_get_gps_coordinates.side_effect = [
        (10.0, 20.0),  # Hotel A: Full address success
        None,          # Hotel B: Full address fail
        (30.0, 40.0),  # Hotel B: Street+City success
        None,          # Hotel C: Full address fail
        None,          # Hotel C: Street+City fail
        (50.0, 60.0),  # Hotel C: Business+City success
    ]

    # Act
    run_main()

    # Assert
    mock_load_dotenv.assert_called_once()
    mock_os_getenv.assert_any_call("GPX_FILE")
    mock_os_getenv.assert_any_call("CSV_FILE")
    mock_os_getenv.assert_any_call("CSV_W_COOR_FILE")
    mock_load_hotels_from_csv.assert_called_once_with("input.csv")

    # Verify geocoding calls
    mock_get_gps_coordinates.assert_any_call("Hotel A, Street A, City A, Germany")
    mock_get_gps_coordinates.assert_any_call("Street B, City B, Germany")
    mock_get_gps_coordinates.assert_any_call("Hotel C, City C, Germany")

    # Verify to_csv call
    # The to_csv method is called on the initial_hotels_df directly
    initial_hotels_df.to_csv.assert_called_once()

    # Get the arguments passed to to_csv
    to_csv_args, to_csv_kwargs = initial_hotels_df.to_csv.call_args

    file_path_from_mock = to_csv_args[0]

    assert file_path_from_mock == 'output_w_coor.csv'
    assert to_csv_kwargs['sep'] == ';'
    assert to_csv_kwargs['index'] == False
    assert to_csv_kwargs['encoding'] == 'utf-8'

    # Verify the content of the DataFrame passed to to_csv
    expected_output_df = pd.DataFrame({
        "Betrieb": ["Hotel A", "Hotel B", "Hotel C"],
        "Straße": ["Street A", "Street B", "Street C"],
        "Stadt": ["City A", "City B", "City C"],
        "Latitude": [10.0, 30.0, 50.0],
        "Longitude": [20.0, 40.0, 60.0],
    })
    # Now that we are using a real DataFrame for iterrows, we can assert the content
    pd.testing.assert_frame_equal(initial_hotels_df, expected_output_df)

    # Verify create_gpx_file call
    mock_create_gpx_file.assert_called_once_with(initial_hotels_df, "output.gpx")

    # Verify print statements (basic check for key messages)
    captured = capsys.readouterr()
    assert "Hotels loaded from CSV:" in captured.out
    assert "Geocoded: Hotel A, Street A, City A, Germany (10.0, 20.0)" in captured.out
    assert "Geocoded: Street B, City B, Germany (30.0, 40.0)" in captured.out
    assert "Geocoded: Hotel C, City C, Germany (50.0, 60.0)" in captured.out
    assert "Hotels with GPS coordinates:3 out of 3" in captured.out
    assert "GPX file 'output.gpx' created successfully." in captured.out
