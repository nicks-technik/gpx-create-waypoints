import tabula
import os
from dotenv import load_dotenv
import pandas as pd  # Import pandas

load_dotenv()


def convert_pdf_to_csv(pdf_path, csv_path):
    """Converts a PDF file containing tabular data into a CSV file."""
    try:
        # Read PDF into a list of DataFrames
        dfs = tabula.read_pdf(pdf_path, pages="all", multiple_tables=True)

        # If the CSV file already exists, remove it to ensure a clean start
        if os.path.exists(csv_path):
            os.remove(csv_path)

        # Write each DataFrame to the CSV file with semicolon delimiter
        for i, df in enumerate(dfs):
            # Write header only for the first DataFrame
            header = i == 0
            df.to_csv(
                csv_path,
                sep=";",
                index=False,
                mode="a",
                header=header,
                encoding="utf-8",
            )

        print(f"Successfully converted '{pdf_path}' to '{csv_path}'.")
    except FileNotFoundError:
        print(f"Error: The PDF file '{pdf_path}' was not found.")
    except Exception as e:
        print(f"An error occurred during PDF to CSV conversion: {e}")


if __name__ == "__main__":
    input_pdf_file = os.getenv("PDF_FILE")
    output_csv_file = os.getenv("CSV_FILE")

    if input_pdf_file and output_csv_file:
        convert_pdf_to_csv(input_pdf_file, output_csv_file)
    else:
        print("Please set INPUT_PDF_FILE and OUTPUT_CSV_FILE in your .env file.")
