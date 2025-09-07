"""Tests for the PDF to CSV conversion module.

This module contains unit tests for the `convert_pdf_to_csv` function
defined in `src.pdf2csv`, covering successful conversion, file not found
errors, and exceptions during the conversion process.
"""

import pytest
import os
from unittest.mock import patch, MagicMock
import pandas as pd
from src.pdf2csv import convert_pdf_to_csv

@patch('src.pdf2csv.tabula.read_pdf')
def test_convert_pdf_to_csv_success(mock_read_pdf, tmp_path):
    """Tests that convert_pdf_to_csv successfully converts a PDF to CSV.

    It mocks `tabula.read_pdf` to simulate PDF content and verifies that
    the output CSV file is created with the correct content and format.
    """
    # Arrange: Set up dummy file paths and mock tabula's return value.
    pdf_path = tmp_path / "test.pdf"
    csv_path = tmp_path / "output.csv"
    
    # Create a dummy PDF file (content doesn't matter as tabula is mocked).
    pdf_path.write_text("dummy pdf content")

    # Mock tabula.read_pdf to return a list of DataFrames, simulating tables from a PDF.
    mock_df1 = pd.DataFrame({"col1": ["a", "b"], "col2": [1, 2]})
    mock_df2 = pd.DataFrame({"col3": ["c", "d"], "col4": [3, 4]})
    mock_read_pdf.return_value = [mock_df1, mock_df2]

    # Act: Call the function under test.
    convert_pdf_to_csv(str(pdf_path), str(csv_path))

    # Assert: Verify the CSV file was created and its content is correct.
    assert os.path.exists(csv_path)
    with open(csv_path, "r") as f:
        content = f.read()
        # Expected content is a concatenation of the mocked DataFrames, semicolon-separated.
        expected_content = "col1;col2\na;1\nb;2\nc;3\nd;4\n"
        assert content == expected_content
    # Verify that tabula.read_pdf was called with the correct arguments.
        mock_read_pdf.assert_called_once_with(str(pdf_path), pages="all", multiple_tables=True)

def test_convert_pdf_to_csv_file_not_found(tmp_path, capsys):
    """Tests that convert_pdf_to_csv handles FileNotFoundError correctly.

    It verifies that no CSV file is created and an error message is printed
    when the input PDF file does not exist.
    """
    # Arrange: Define paths for a non-existent PDF and an output CSV.
    pdf_path = tmp_path / "non_existent.pdf"
    csv_path = tmp_path / "output.csv"

    # Act: Call the function under test.
    convert_pdf_to_csv(str(pdf_path), str(csv_path))

    # Assert: Verify no CSV was created and the correct error message was captured.
    assert not os.path.exists(csv_path)
    captured = capsys.readouterr()
    assert f"Error: The PDF file '{pdf_path}' was not found." in captured.out

@patch('src.pdf2csv.tabula.read_pdf')
def test_convert_pdf_to_csv_tabula_exception(mock_read_pdf, tmp_path, capsys):
    """Tests that convert_pdf_to_csv handles exceptions from tabula.read_pdf.

    It verifies that no CSV file is created and an error message is printed
    when `tabula.read_pdf` raises an exception.
    """
    # Arrange: Set up dummy file paths and configure mock to raise an exception.
    pdf_path = tmp_path / "test.pdf"
    csv_path = tmp_path / "output.csv"
    pdf_path.write_text("dummy pdf content")

    mock_read_pdf.side_effect = Exception("Tabula error")

    # Act: Call the function under test.
    convert_pdf_to_csv(str(pdf_path), str(csv_path))

    # Assert: Verify no CSV was created and the correct error message was captured.
    assert not os.path.exists(csv_path)
    captured = capsys.readouterr()
    assert "An error occurred during PDF to CSV conversion: Tabula error" in captured.out

@patch('src.pdf2csv.tabula.read_pdf')
def test_convert_pdf_to_csv_overwrites_existing_file(mock_read_pdf, tmp_path):
    """Tests that convert_pdf_to_csv overwrites an existing CSV file.

    It verifies that if an output CSV file already exists, it is overwritten
    with the new conversion results.
    """
    # Arrange: Set up dummy file paths, create an existing CSV, and mock tabula.
    pdf_path = tmp_path / "test.pdf"
    csv_path = tmp_path / "output.csv"
    pdf_path.write_text("dummy pdf content")
    csv_path.write_text("old content") # Create an existing file to be overwritten.

    mock_df = pd.DataFrame({"col1": ["new"], "col2": [100]})
    mock_read_pdf.return_value = [mock_df]

    # Act: Call the function under test.
    convert_pdf_to_csv(str(pdf_path), str(csv_path))

    # Assert: Verify the CSV file exists and its content has been updated.
    assert os.path.exists(csv_path)
    with open(csv_path, "r") as f:
        content = f.read()
        assert content == "col1;col2\nnew;100\n"



def test_convert_pdf_to_csv_file_not_found(tmp_path, capsys):
    # Arrange
    pdf_path = tmp_path / "non_existent.pdf"
    csv_path = tmp_path / "output.csv"

    # Act
    convert_pdf_to_csv(str(pdf_path), str(csv_path))

    # Assert
    assert not os.path.exists(csv_path)
    captured = capsys.readouterr()
    assert f"Error: The PDF file '{pdf_path}' was not found." in captured.out

@patch('src.pdf2csv.tabula.read_pdf')
def test_convert_pdf_to_csv_tabula_exception(mock_read_pdf, tmp_path, capsys):
    # Arrange
    pdf_path = tmp_path / "test.pdf"
    csv_path = tmp_path / "output.csv"
    pdf_path.write_text("dummy pdf content")

    mock_read_pdf.side_effect = Exception("Tabula error")

    # Act
    convert_pdf_to_csv(str(pdf_path), str(csv_path))

    # Assert
    assert not os.path.exists(csv_path)
    captured = capsys.readouterr()
    assert "An error occurred during PDF to CSV conversion: Tabula error" in captured.out

@patch('src.pdf2csv.tabula.read_pdf')
def test_convert_pdf_to_csv_overwrites_existing_file(mock_read_pdf, tmp_path):
    # Arrange
    pdf_path = tmp_path / "test.pdf"
    csv_path = tmp_path / "output.csv"
    pdf_path.write_text("dummy pdf content")
    csv_path.write_text("old content") # Create an existing file

    mock_df = pd.DataFrame({"col1": ["new"], "col2": [100]})
    mock_read_pdf.return_value = [mock_df]

    # Act
    convert_pdf_to_csv(str(pdf_path), str(csv_path))

    # Assert
    assert os.path.exists(csv_path)
    with open(csv_path, "r") as f:
        content = f.read()
        assert content == "col1;col2\nnew;100\n"

