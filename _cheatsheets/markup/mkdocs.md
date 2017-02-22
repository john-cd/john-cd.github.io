---
title: MkDocs Basics
category: markup
tags: python 
---

## Install and documentation generation

[mkdocs.org](http://mkdocs.org).

To install MkDocs / create a new documentation site:
```bash
$ pip install mkdocs
$ mkdocs new documentation
```

To build the documentation site:
```bash
$ cd documentation
$ mkdocs build
```

To start the live-reloading docs server - [http://localhost:8000/](http://localhost:8000/)
```bash
$ mkdocs serve
```

MkDocs can use the ghp-import tool to commit to the gh-pages branch and push the gh-pages branch to GitHub Pages:
```bash
$ mkdocs gh-deploy
```

### MkDocs project layout

    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.
