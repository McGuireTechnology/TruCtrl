# GitHub

## MkDocs Deployment Workflow

{!docs/snippets/mkdocs-deploy.md!}

## Dependabot

Dependabot is configured to automatically check for updates to Python dependencies (pip) and GitHub Actions workflows.

- It creates pull requests for dependency updates on a weekly schedule.
- Configuration is in `.github/dependabot.yml`.

This helps keep the project secure and up to date with minimal manual intervention.