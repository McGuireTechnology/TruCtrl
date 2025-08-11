# Python

## Python Environment Setup

It is recommended to use a [virtual environment](https://docs.python.org/3/library/venv.html) for Python development. To create a `.venv` in the project root:

```sh
python3 -m venv .venv
source .venv/bin/activate
```

This will isolate your Python dependencies from the system Python.

## Managing Dependencies with `pyproject.toml`

All Python dependencies for the project and its subprojects are managed in the root `pyproject.toml` file. This file defines required packages, optional documentation and development dependencies, and project metadata. To install all dependencies:

```sh
pip install .[dev,docs]
```

You can also install only the main dependencies:

```sh
pip install .
```

## Python Subprojects

The following subprojects use Python:

- `api/` – FastAPI application and CLI
- `tests/` – Test suite for the API and other Python code
- `docs/` – Documentation build scripts and macros (for MkDocs)

