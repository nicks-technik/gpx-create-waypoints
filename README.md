# GPX Generator for Hotel Addresses

This project provides a set of Python scripts to read hotel addresses from a CSV file, fetch their GPS coordinates, and generate a GPX file compatible with Garmin devices and other GPS software.

## Features

- **CSV Input**: Reads hotel data from a CSV file.
- **Geocoding**: Uses Nominatim to convert addresses to GPS coordinates.
- **GPX Output**: Creates a standard GPX file with waypoints for each hotel.

## Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repository-url>
   cd gpx-project
   ```

2. **Install dependencies using uv:**
   Make sure you have `uv` installed. You can find installation instructions [here](https://github.com/astral-sh/uv).
   ```bash
   uv pip install .
   ```

## Configuration

Before running the scripts, create a `.env` file in the root of the project. This file will hold the configuration variables for the project.

```
# .env for gpx-create-waypoints

# Input and output files for pdf2csv.py
PDF_FILE=data/AlpCrossHotels.pdf
CSV_FILE=data/hotels.csv
CSV_W_COOR_FILE=data/hotelswithcoor.csv
GPX_FILE=data/AlpCrossHotels.gpx

# Nominatim settings for geocoding.py
NOMINATIM_USER_AGENT=gpx-creator-tool
NOMINATIM_DELAY_SECONDS=1
```

## Usage

This project consists of several scripts that work together to generate a GPX file from hotel data.

1.  **`src/pdf2csv.py` (Optional: Convert PDF to CSV):**
    If your hotel data is in a PDF file, this script can convert it into a CSV format.
    *   **Description:** Reads hotel data from the PDF file specified by `PDF_FILE` in `.env` and converts it to a CSV file, saved as `CSV_FILE` in `.env`.
    *   **How to run:**
        ```bash
        uv run python src/pdf2csv.py
        ```

2.  **`src/main.py` (Main GPX Generation Script):**
    This is the primary script that orchestrates the geocoding and GPX file generation.
    *   **Description:** Reads hotel data from the input CSV file (`CSV_FILE` in `.env`), uses the geocoding service to get coordinates, and then generates the GPX file (`GPX_FILE` in `.env`).
    *   **How to run:**
        ```bash
        uv run python src/main.py
        ```

3.  **Internal Modules:**
    The following scripts are internal modules used by `src/main.py` and are not typically run directly by the user:

    *   **`src/geocoding.py`:**
        *   **Description:** Handles the conversion of addresses to geographical coordinates (latitude and longitude) using the Nominatim service. It includes logic for rate limiting and error handling during API calls.
    *   **`src/gpx_generator.py`:**
        *   **Description:** This module is called by `src/main.py` to generate the GPX file from the geocoded hotel data, creating waypoints with names, descriptions, and symbols (e.g., SYM="friends-home" icon).

4.  **Output:**
    The generated GPX file will be saved as specified in the `GPX_FILE` variable in your `.env` file (e.g., `data/AlpCrossHotels.gpx`).

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
