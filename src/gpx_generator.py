# uv run python src/gpx_generator.py

import os

import pandas as pd

import gpxpy
import gpxpy.gpx

from dotenv import load_dotenv


def create_gpx_file(hotels, output_file):
    """Creates a GPX file with waypoints for the given hotels."""
    gpx = gpxpy.gpx.GPX()

    for index, hotel in hotels.iterrows():
        if pd.notna(hotel["Latitude"]) and pd.notna(hotel["Longitude"]):
            description_parts = []
            if pd.notna(hotel["Straße"]):
                description_parts.append(f"Straße: {hotel['Straße']}")
            if pd.notna(hotel["Telefon"]):
                description_parts.append(f"Telefon: {hotel['Telefon']}")
            if pd.notna(hotel["Website"]):
                description_parts.append(f"Website: {hotel['Website']}")
            if pd.notna(hotel["Entfernung"]):
                description_parts.append(f"Entfernung: {hotel['Entfernung']}")
            if pd.notna(hotel["Hm"]):
                description_parts.append(f"Hm: {hotel['Hm']}")

            description_str = ", ".join(description_parts)

            gpx.waypoints.append(
                gpxpy.gpx.GPXWaypoint(
                    latitude=hotel["Latitude"],
                    longitude=hotel["Longitude"],
                    name=hotel["Betrieb"],
                    description=description_str,
                    symbol="friends-home",
                )
            )
        else:
            print(f"Skipping hotel {hotel['Betrieb']} due to missing coordinates.")

    with open(output_file, "w") as f:
        f.write(gpx.to_xml())


if __name__ == "__main__":
    load_dotenv()
    csv_file = os.getenv("CSV_W_COOR_FILE")
    gpx_file = os.getenv("GPX_FILE")

    if csv_file:
        try:
            hotels_df = pd.read_csv(csv_file, delimiter=";")
            create_gpx_file(hotels_df, gpx_file)
            print(f"GPX file '{gpx_file}' created successfully.")
        except FileNotFoundError:
            print(f"Error: CSV file not found at {csv_file}")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("Error: CSV_W_COOR_FILE environment variable not set.")
