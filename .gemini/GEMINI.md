# Garmin GPX Project Best Practices

This document outlines best practices for a Python project that loads hotel addresses from a CSV file, retrieves their GPS coordinates, and generates a GPX file for use with Garmin devices.

## 1. Project Structure

A well-organized project structure is crucial for maintainability. Here's a recommended layout:

```
gpx-project/
├── data/
│   ├── hotels.csv
│   └── hotels.gpx
├── src/
│   ├── __init__.py
│   ├── geocoding.py
│   ├── gpx_generator.py
│   └── main.py
├── tests/
│   ├── __init__.py
│   ├── test_geocoding.py
│   └── test_gpx_generator.py
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

- **`data/`**: Store input (CSV) and output (GPX) files.
- **`src/`**: Contains the main Python source code.
- **`tests/`**: Contains unit tests for your code.
- **`.gitignore`**: Specifies files and directories to be ignored by Git.
- **`LICENSE`**: The project's license file.
- **`README.md`**: A detailed description of the project.
- **`requirements.txt`**: A list of Python dependencies.

## 2. Dependency Management with uv and pyproject.toml

Use a `pyproject.toml` file to manage project dependencies and the `uv` tool to install them. `uv` is a fast, modern Python package installer.

To install the dependencies, use `uv`:

```bash
uv pip install .
```

## 6. Code Style and Linting

Follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide for Python code. Use tools like `flake8` or `black` to automatically check and format your code.

## 6.1 Code

The symbols of the gpx_waypoints in the gpx_generator.py file is friends-home

## 7. Testing

Write unit tests for your geocoding and GPX generation logic. This helps ensure that your code works as expected and prevents regressions. The `unittest` or `pytest` frameworks are good choices.

## 8. Error Handling

Your code should gracefully handle potential errors, such as:

- The input CSV file not being found.
- Network errors during geocoding.
- Invalid or un-geocodable addresses.
- Errors while writing the output GPX file.

## 9. README.md

A good `README.md` file should include:

- A clear description of the project.
- Instructions on how to install and run the project.
- Information about the required input data format.
- Any known limitations or issues.
