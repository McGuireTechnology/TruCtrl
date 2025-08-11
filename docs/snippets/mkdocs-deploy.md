The documentation is automatically deployed to GitHub Pages using a GitHub Actions workflow:

- On every push to the `main` branch, the workflow:
  - Installs Python and all documentation dependencies (including MkDocs, Material for MkDocs, and mike) via `pip install .[docs]`.
  - Uses `mike` to deploy the latest docs version and set it as the default.
  - Publishes the built site to GitHub Pages using the `peaceiris/actions-gh-pages` action.

You can find the workflow file at `.github/workflows/deploy-docs.yml`.