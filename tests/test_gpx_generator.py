import pytest
import pandas as pd
import os
from src.gpx_generator import create_gpx_file


def test_create_gpx_file(tmp_path):
    # Arrange
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
    output_file = tmp_path / "test.gpx"

    # Act
    create_gpx_file(hotels, output_file)

    # Assert
    assert os.path.exists(output_file)
    with open(output_file, "r") as f:
        gpx_content = f.read()
        assert "<gpx" in gpx_content
        assert '<wpt lat="48.8584" lon="2.2945">' in gpx_content
        assert "<name>Hotel 1</name>" in gpx_content
        assert (
            "<desc>Straße: Main St, Telefon: 123-456, Website: hotel1.com, Entfernung: 10km, Hm: 100m</desc>"
            in gpx_content
        )
        assert "<sym>friends-home</sym>" in gpx_content
        assert '<wpt lat="40.7128" lon="-74.006">' in gpx_content
        assert "<name>Hotel 2</name>" in gpx_content
        assert (
            "<desc>Straße: Broadway, Telefon: 789-012, Website: hotel2.com, Entfernung: 5km, Hm: 50m</desc>"
            in gpx_content
        )
        assert "<sym>friends-home</sym>" in gpx_content


def test_create_gpx_file_empty_input(tmp_path):
    # Arrange
    hotels = pd.DataFrame({"name": [], "latitude": [], "longitude": []})
    output_file = tmp_path / "test_empty.gpx"

    # Act
    create_gpx_file(hotels, output_file)

    # Assert
    assert os.path.exists(output_file)
    with open(output_file, "r") as f:
        gpx_content = f.read()
        assert "<gpx" in gpx_content
        assert "<wpt" not in gpx_content


def test_create_gpx_file_missing_coordinates(tmp_path):
    # Arrange
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
    output_file = tmp_path / "test_missing.gpx"

    # Act
    create_gpx_file(hotels, output_file)

    # Assert
    assert os.path.exists(output_file)
    with open(output_file, "r") as f:
        gpx_content = f.read()
        assert "<gpx" in gpx_content
        assert '<wpt lat="48.8584" lon="2.2945">' in gpx_content
        assert "<name>Hotel 1</name>" in gpx_content
        assert 'lon="-74.006"' not in gpx_content
