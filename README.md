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
CSV_FILE=data/AlpCrossHotels.csv

# Input and output files for main.py
INPUT_CSV_FILE=data/AlpCrossHotels.csv
OUTPUT_GPX_FILE=data/AlpCrossHotels.gpx

# Nominatim settings for geocoding.py
NOMINATIM_USER_AGENT=gpx-creator-tool
NOMINATIM_DELAY_SECONDS=1
```

## Usage

1. **Prepare your data:**
   Make sure the input files specified in the `.env` file exist. By default, it expects `data/AlpCrossHotels.pdf`.

2. **Convert PDF to CSV (if needed):**
   If you have a PDF file with hotel data, you can convert it to a CSV file using the `pdf2csv.py` script.
   ```bash
   python src/pdf2csv.py
   ```

3. **Run the main script:**
   Execute the main script to generate the GPX file from the CSV data.
   ```bash
   python src/main.py
   ```

4. **Find the output:**
   The generated GPX file will be saved as specified in the `OUTPUT_GPX_FILE` variable in your `.env` file (e.g., `data/AlpCrossHotels.gpx`).

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
