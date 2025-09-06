import pytest
from unittest.mock import patch, MagicMock
from src.geocoding import get_gps_coordinates
import os

@patch.dict(os.environ, {"NOMINATIM_USER_AGENT": "gpx-project"})
@patch('src.geocoding.Nominatim')
def test_get_gps_coordinates_success(mock_nominatim):
    # Arrange
    mock_location = MagicMock()
    mock_location.latitude = 48.8584
    mock_location.longitude = 2.2945
    mock_geolocator = MagicMock()
    mock_geolocator.geocode.return_value = mock_location
    mock_nominatim.return_value = mock_geolocator
    
    # Act
    coordinates = get_gps_coordinates("Eiffel Tower")
    
    # Assert
    assert coordinates == (48.8584, 2.2945)
    mock_nominatim.assert_called_once_with(user_agent="gpx-project")
    mock_geolocator.geocode.assert_called_once_with("Eiffel Tower")

@patch.dict(os.environ, {"NOMINATIM_USER_AGENT": "gpx-project"})
@patch('src.geocoding.Nominatim')
def test_get_gps_coordinates_not_found(mock_nominatim):
    # Arrange
    mock_geolocator = MagicMock()
    mock_geolocator.geocode.return_value = None
    mock_nominatim.return_value = mock_geolocator
    
    # Act
    coordinates = get_gps_coordinates("nonexistent place")
    
    # Assert
    assert coordinates is None
    mock_nominatim.assert_called_once_with(user_agent="gpx-project")
    mock_geolocator.geocode.assert_called_once_with("nonexistent place")

@patch.dict(os.environ, {"NOMINATIM_USER_AGENT": "gpx-project"})
@patch('src.geocoding.Nominatim')
def test_get_gps_coordinates_exception(mock_nominatim):
    # Arrange
    mock_geolocator = MagicMock()
    mock_geolocator.geocode.side_effect = Exception("Test exception")
    mock_nominatim.return_value = mock_geolocator
    
    # Act
    coordinates = get_gps_coordinates("any address")
    
    # Assert
    assert coordinates is None
    mock_nominatim.assert_called_once_with(user_agent="gpx-project")
    mock_geolocator.geocode.assert_called_once_with("any address")