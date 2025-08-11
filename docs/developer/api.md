# API Subproject

## Core API Files

- **config.py**: Application configuration, environment variables, and settings.
- **crud.py**: CRUD (Create, Read, Update, Delete) operations for database models.
- **db.py**: Database connection setup and session management.
- **deps.py**: Dependency injection utilities for FastAPI routes (e.g., getting DB sessions, user auth).
- **main.py**: FastAPI application entry point; creates the app and includes routes.
- **models.py**: SQLModel or Pydantic models representing database tables and schemas.
- **routes.py**: API route definitions and endpoint logic.
- **security.py**: Security utilities, authentication, and authorization logic.
- **utils.py**: General utility functions used throughout the API.

## Domain Folders

Non-core logic and features (such as security controls, business domains, or feature modules) should be organized into subfolders within the API directory. For example, place all security control logic in `api/controls/` or similar domain-specific folders. This keeps the core API files clean and maintainable.

