#!/usr/bin/env python3
from geopy.geocoders import Nominatim
import os
import time
from dotenv import load_dotenv

load_dotenv()


def get_gps_coordinates(address):
    """Gets GPS coordinates for a given address."""
    user_agent = os.getenv("NOMINATIM_USER_AGENT", "gpx-project")
    geolocator = Nominatim(user_agent=user_agent)
    try:
        # Delay to respect Nominatim's usage policy
        delay_seconds = int(os.getenv("NOMINATIM_DELAY_SECONDS", 3))
        time.sleep(delay_seconds)
        location = geolocator.geocode(address)
        if location:
            return (location.latitude, location.longitude)
    except Exception as e:
        print(f"Error geocoding {address}: {e}")
    return None


if __name__ == "__main__":
    # This block allows the script to be run directly for testing the geocoding function.
    # It will geocode a default address and print the coordinates.
    default_address = "Eiffel Tower, Paris, France"
    print(f"Attempting to geocode address: '{default_address}'")
    coordinates = get_gps_coordinates(default_address)
    if coordinates:
        print(f"Successfully found coordinates: {coordinates}")
    else:
        print(f"Failed to find coordinates for '{default_address}'.")
