import pytest
import os
from unittest.mock import patch, MagicMock
import pandas as pd
from src.pdf2csv import convert_pdf_to_csv

@patch('src.pdf2csv.tabula.read_pdf')
def test_convert_pdf_to_csv_success(mock_read_pdf, tmp_path):
    # Arrange
    pdf_path = tmp_path / "test.pdf"
    csv_path = tmp_path / "output.csv"
    
    # Create a dummy PDF file (content doesn't matter as tabula is mocked)
    pdf_path.write_text("dummy pdf content")

    # Mock tabula.read_pdf to return a list of DataFrames
    mock_df1 = pd.DataFrame({"col1": ["a", "b"], "col2": [1, 2]})
    mock_df2 = pd.DataFrame({"col3": ["c", "d"], "col4": [3, 4]})
    mock_read_pdf.return_value = [mock_df1, mock_df2]

    # Act
    convert_pdf_to_csv(str(pdf_path), str(csv_path))

    # Assert
    assert os.path.exists(csv_path)
    with open(csv_path, "r") as f:
        content = f.read()
        expected_content = "col1;col2\na;1\nb;2\nc;3\nd;4\n"
        assert content == expected_content
    mock_read_pdf.assert_called_once_with(str(pdf_path), pages="all", multiple_tables=True)

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

