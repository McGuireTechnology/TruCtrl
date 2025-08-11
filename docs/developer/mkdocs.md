
# MkDocs Documentation

## Theme

This project uses the **Material for MkDocs** theme, which provides a modern, responsive design and many advanced features.

Theme settings (such as colors and navigation) are configured in `mkdocs.yml`.

## Extensions

Common Markdown extensions enabled in `mkdocs.yml` may include:

- `admonition` — for notes, warnings, and tips
- `codehilite` — syntax highlighting for code blocks
- `toc` — table of contents generation
- `footnotes` — support for footnotes
- `attr_list` — add HTML attributes to Markdown elements

Check your `mkdocs.yml` for the full list of enabled extensions and their configuration.

## Running the Development Server

To preview documentation locally with live reload:

```sh
mkdocs serve -a 127.0.0.1:8001
```

This will start the dev server at [http://127.0.0.1:8001](http://127.0.0.1:8001).

## Building the Documentation

To build the static site for deployment:

```sh
mkdocs build
```

The generated site will be in the `site/` directory.

## Additional Tips

- Edit Markdown files in the `docs/` directory.
- Update `mkdocs.yml` to change navigation or theme settings.

## Deployment Workflow

{!docs/snippets/mkdocs-deploy.md!}
