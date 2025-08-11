
# Alembic Database Migrations

Alembic is used for managing database schema migrations in this project.

## Migration Directory

- All migration scripts and Alembic environment files are located in the `api/migrations` folder.

## Initializing Alembic

If you need to re-initialize Alembic (not usually necessary):

```sh
alembic init api/migrations
```

## Creating a Migration

To generate a new migration after changing your models:

```sh
alembic revision --autogenerate -m "Describe your change"
```


## Applying Migrations

To apply all pending migrations to the database:

```sh
alembic upgrade head
```

## Downgrading Migrations

To revert the last migration (downgrade one step):

```sh
alembic downgrade -1
```

You can also specify a specific revision to downgrade to:

```sh
alembic downgrade <revision>
```

## Configuration

- The Alembic configuration file is `alembic.ini` in the project root.
- Edit `api/migrations/env.py` to set up your database connection and model imports.

For more details, see the [Alembic documentation](https://alembic.sqlalchemy.org/).
