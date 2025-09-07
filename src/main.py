# uv run python -m src.main

import os

import pandas as pd
import numpy as np
from dotenv import load_dotenv

from src.geocoding import get_gps_coordinates
from src.gpx_generator import create_gpx_file


def load_hotels_from_csv(file_path):
    """Loads hotel addresses from a CSV file."""
    try:
        return pd.read_csv(file_path, sep=";")
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None


def run_main():
    load_dotenv()

    gpx_file = os.getenv("GPX_FILE")
    csv_file = os.getenv("CSV_FILE")
    csv_w_coor_file = os.getenv("CSV_W_COOR_FILE")

    hotels_df = load_hotels_from_csv(csv_file)
    if hotels_df is not None:
        print("Hotels loaded from CSV:")
        pd.set_option("display.max_rows", None)
        print(hotels_df)

        # Add Latitude and Longitude columns
        hotels_df["Latitude"] = np.nan
        hotels_df["Longitude"] = np.nan
        hotels_df["Latitude"] = hotels_df["Latitude"].astype(float)
        hotels_df["Longitude"] = hotels_df["Longitude"].astype(float)

        counter_Betrieb_Strasse_Stadt_geocodes = 0
        counter_Strasse_Stadt_geocodes = 0
        counter_Betrieb_Stadt_geocodes = 0
        counter_geocodes = 0
        counter_not_geocodes = 0

        hotels_not_found = ""

        for index, row in hotels_df.iterrows():
            address = f"{row['Betrieb']}, {row['Straße']}, {row['Stadt']}, Germany"
            full_address = address

            coordinates = get_gps_coordinates(address)

            if coordinates:
                hotels_df.loc[index, "Latitude"] = coordinates[0]
                hotels_df.loc[index, "Longitude"] = coordinates[1]

                counter_geocodes += 1
                counter_Betrieb_Strasse_Stadt_geocodes += 1

                print(
                    str(counter_geocodes)
                    + ") Geocoded: "
                    + address
                    + " "
                    + str(coordinates)
                )
            else:
                print(f"Could not geocode: {address}")

                address = f"{row['Straße']}, {row['Stadt']}, Germany"
                coordinates = get_gps_coordinates(address)

                if coordinates:
                    hotels_df.loc[index, "Latitude"] = coordinates[0]
                    hotels_df.loc[index, "Longitude"] = coordinates[1]

                    counter_geocodes += 1
                    counter_Strasse_Stadt_geocodes += 1

                    print(
                        str(counter_geocodes)
                        + ") Geocoded: "
                        + address
                        + " "
                        + str(coordinates)
                    )
                else:
                    print(f"Could not geocode: {address}")

                    address = f"{row['Betrieb']}, {row['Stadt']}, Germany"
                    coordinates = get_gps_coordinates(address)

                    if coordinates:
                        hotels_df.loc[index, "Latitude"] = coordinates[0]
                        hotels_df.loc[index, "Longitude"] = coordinates[1]

                        counter_geocodes += 1
                        counter_Betrieb_Stadt_geocodes += 1

                        print(
                            str(counter_geocodes)
                            + ") Geocoded: "
                            + address
                            + " "
                            + str(coordinates)
                        )
                    else:
                        counter_not_geocodes += 1
                        print(
                            str(counter_not_geocodes)
                            + ") Could absolutely not geocode: "
                            + full_address
                        )
                        hotels_not_found += address + "\n"

        total_geocodes = (
            counter_Betrieb_Strasse_Stadt_geocodes
            + counter_Strasse_Stadt_geocodes
            + counter_Betrieb_Stadt_geocodes
        )

        pd.set_option("display.max_rows", None)
        print(hotels_df)
        print(
            "Hotels with GPS coordinates:"
            + str(total_geocodes)
            + " out of "
            + str(len(hotels_df))
        )

        hotels_df.to_csv(csv_w_coor_file, sep=";", index=False, encoding="utf-8")

        print(f"Hotels not found:\n{hotels_not_found}")

        # Create GPX file
        create_gpx_file(hotels_df, gpx_file)
        print(f"GPX file '{gpx_file}' created successfully.")

if __name__ == "__main__":
    run_main()