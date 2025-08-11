# Environment Variables

Environment variables are used to configure sensitive or environment-specific settings for your application, such as database URLs and secret keys. These values should not be hardcoded in your source code.

## .env File Location

The `.env` file should be placed in the root of the project directory (next to `pyproject.toml`).

Example `.env` file:

```env
DATABASE_URL=sqlite:///./tructrl.db
SECRET_KEY=your_secret_key
```

## Generating a Secret Key

To generate a secure secret key, run:

```sh
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copy the output and set it as your `SECRET_KEY` in the `.env` file.

## Version Control

The `.env` file contains sensitive information and should **not** be committed to version control. Make sure `.env` is listed in your `.gitignore` file.

