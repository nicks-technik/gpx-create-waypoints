"""Tests for the GPX file generation module.

This module contains unit tests for the `create_gpx_file` function
defined in `src.gpx_generator`, covering successful GPX creation,
handling of empty input, and cases with missing coordinates.
"""

import pytest
import pandas as pd
import os
from src.gpx_generator import create_gpx_file


def test_create_gpx_file(tmp_path):
    """Tests that create_gpx_file correctly generates a GPX file.

    It verifies that the GPX file is created, contains the expected GPX structure,
    and includes waypoint data derived from the input DataFrame.
    """
    # Arrange: Prepare a DataFrame with hotel data including coordinates and other details.
    hotels = pd.DataFrame(
        {
            "Betrieb": ["Hotel 1", "Hotel 2"],
            "Latitude": [48.8584, 40.7128],
            "Longitude": [2.2945, -74.0060],
            "Straße": ["Main St", "Broadway"],
            "Telefon": ["123-456", "789-012"],
            "Website": ["hotel1.com", "hotel2.com"],
            "Entfernung": ["10km", "5km"],
            "Hm": ["100m", "50m"],
        }
    )
    # Define the output file path using a temporary directory.
    output_file = tmp_path / "test.gpx"

    # Act: Call the function under test to create the GPX file.
    create_gpx_file(hotels, output_file)

    # Assert: Verify the file exists and its content matches the expected GPX structure and data.
    assert os.path.exists(output_file)
    with open(output_file, "r") as f:
        gpx_content = f.read()
        # Check for basic GPX structure.
        assert "<gpx" in gpx_content
        # Verify the first waypoint's coordinates and name.
        assert '<wpt lat="48.8584" lon="2.2945">' in gpx_content
        assert "<name>Hotel 1</name>" in gpx_content
        # Verify the description content for the first waypoint.
        assert (
            "<desc>Straße: Main St, Telefon: 123-456, Website: hotel1.com, Entfernung: 10km, Hm: 100m</desc>"
            in gpx_content
        )
        # Verify the symbol for the waypoint.
        assert "<sym>friends-home</sym>" in gpx_content
        # Verify the second waypoint's coordinates and name.
        assert '<wpt lat="40.7128" lon="-74.006">' in gpx_content
        assert "<name>Hotel 2</name>" in gpx_content
        # Verify the description content for the second waypoint.
        assert (
            "<desc>Straße: Broadway, Telefon: 789-012, Website: hotel2.com, Entfernung: 5km, Hm: 50m</desc>"
            in gpx_content
        )
        # Verify the symbol for the second waypoint.
        assert "<sym>friends-home</sym>" in gpx_content


def test_create_gpx_file_empty_input(tmp_path):
    """Tests that create_gpx_file handles an empty input DataFrame.

    It verifies that a valid, but empty, GPX file is created (containing no waypoints).
    """
    # Arrange: Prepare an empty DataFrame.
    hotels = pd.DataFrame({"name": [], "latitude": [], "longitude": []})
    # Define the output file path.
    output_file = tmp_path / "test_empty.gpx"

    # Act: Call the function under test.
    create_gpx_file(hotels, output_file)

    # Assert: Verify the file exists and contains no waypoint tags.
    assert os.path.exists(output_file)
    with open(output_file, "r") as f:
        gpx_content = f.read()
        assert "<gpx" in gpx_content
        assert "<wpt" not in gpx_content


def test_create_gpx_file_missing_coordinates(tmp_path):
    """Tests that create_gpx_file correctly handles rows with missing coordinates.

    It verifies that only waypoints with valid Latitude and Longitude are included
    in the generated GPX file.
    """
    # Arrange: Prepare a DataFrame where one hotel has missing coordinates.
    hotels = pd.DataFrame(
        {
            "Betrieb": ["Hotel 1", "Hotel 2"],
            "Latitude": [48.8584, None],
            "Longitude": [2.2945, -74.0060],
            "Straße": ["Main St", None],
            "Telefon": ["123-456", None],
            "Website": ["hotel1.com", None],
            "Entfernung": ["10km", None],
            "Hm": ["100m", None],
        }
    )
    # Define the output file path.
    output_file = tmp_path / "test_missing.gpx"

    # Act: Call the function under test.
    create_gpx_file(hotels, output_file)

    # Assert: Verify the file exists and only the valid waypoint is present.
    assert os.path.exists(output_file)
    with open(output_file, "r") as f:
        gpx_content = f.read()
        assert "<gpx" in gpx_content
        # Verify the first hotel (with valid coordinates) is present.
        assert '<wpt lat="48.8584" lon="2.2945">' in gpx_content
        assert "<name>Hotel 1</name>" in gpx_content
        # Verify the second hotel (with missing coordinates) is NOT present.
        assert 'lon="-74.006"' not in gpx_content
