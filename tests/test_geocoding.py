"""Tests for the geocoding module.

This module contains unit tests for the `get_gps_coordinates` function
defined in `src.geocoding`, covering successful geocoding, handling of
not-found addresses, and exceptions during the geocoding process.
"""

import pytest
from unittest.mock import patch, MagicMock
from src.geocoding import get_gps_coordinates
import os

@patch.dict(os.environ, {"NOMINATIM_USER_AGENT": "gpx-project"})
@patch('src.geocoding.Nominatim')
def test_get_gps_coordinates_success(mock_nominatim):
    """Tests that get_gps_coordinates successfully retrieves GPS coordinates.

    It mocks the Nominatim geocoding service to simulate a successful API call
    and verifies that the function returns the correct latitude and longitude.
    """
    # Arrange: Set up mock objects for Nominatim and its geocode method.
    # Create a mock Location object with latitude and longitude attributes.
    mock_location = MagicMock()
    mock_location.latitude = 48.8584
    mock_location.longitude = 2.2945
    # Create a mock geolocator and configure its geocode method to return the mock location.
    mock_geolocator = MagicMock()
    mock_geolocator.geocode.return_value = mock_location
    # Configure the Nominatim constructor to return the mock geolocator.
    mock_nominatim.return_value = mock_geolocator
    
    # Act: Call the function under test with a dummy address.
    coordinates = get_gps_coordinates("Eiffel Tower")
    
    # Assert: Verify the returned coordinates and that mocks were called correctly.
    assert coordinates == (48.8584, 2.2945)
    # Verify Nominatim was initialized with the correct user agent.
    mock_nominatim.assert_called_once_with(user_agent="gpx-project")
    # Verify the geocode method was called with the correct address.
    mock_geolocator.geocode.assert_called_once_with("Eiffel Tower")

@patch.dict(os.environ, {"NOMINATIM_USER_AGENT": "gpx-project"})
@patch('src.geocoding.Nominatim')
def test_get_gps_coordinates_not_found(mock_nominatim):
    """Tests that get_gps_coordinates returns None when an address is not found.

    It mocks the Nominatim geocoding service to simulate a failed API call
    (no location found) and verifies that the function correctly returns None.
    """
    # Arrange: Set up mock objects to simulate no location being found.
    mock_geolocator = MagicMock()
    mock_geolocator.geocode.return_value = None # Simulate address not found.
    mock_nominatim.return_value = mock_geolocator
    
    # Act: Call the function under test with a non-existent address.
    coordinates = get_gps_coordinates("nonexistent place")
    
    # Assert: Verify that the function returns None and mocks were called correctly.
    assert coordinates is None
    mock_nominatim.assert_called_once_with(user_agent="gpx-project")
    mock_geolocator.geocode.assert_called_once_with("nonexistent place")

@patch.dict(os.environ, {"NOMINATIM_USER_AGENT": "gpx-project"})
@patch('src.geocoding.Nominatim')
def test_get_gps_coordinates_exception(mock_nominatim):
    """Tests that get_gps_coordinates handles exceptions during geocoding.

    It mocks the Nominatim geocoding service to simulate an exception during
    the API call and verifies that the function gracefully returns None.
    """
    # Arrange: Set up mock objects to simulate an exception during geocoding.
    mock_geolocator = MagicMock()
    mock_geolocator.geocode.side_effect = Exception("Test exception") # Simulate an error.
    mock_nominatim.return_value = mock_geolocator
    
    # Act: Call the function under test with any address.
    coordinates = get_gps_coordinates("any address")
    
    # Assert: Verify that the function returns None and mocks were called correctly.
    assert coordinates is None
    mock_nominatim.assert_called_once_with(user_agent="gpx-project")
    mock_geolocator.geocode.assert_called_once_with("any address")