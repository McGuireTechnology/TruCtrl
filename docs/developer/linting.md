# Formatting and Linting

This project enforces consistent code style and quality using the following tools:

- **Black**: Code formatter. Run `black .` to auto-format code.
- **isort**: Import sorter. Run `isort .` to sort imports.
- **Flake8**: Linter for code style and errors. Run `flake8 .` to check for issues.
- **Ruff**: Fast linter and code quality tool. Run `ruff .` for additional checks.
- **Mypy**: Static type checker. Run `mypy .` to check type annotations.
- **Bandit**: Security linter. Run `bandit -r api` to check for security issues.

All settings are defined in `pyproject.toml`. You can run all checks and formatting with pre-commit by running:

```sh
pre-commit run --all-files
```

Please ensure your code passes all checks before submitting a pull request.
