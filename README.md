<!-- Project overview and local development instructions. -->
# John Cruchon-Dupeyrat

Personal site for writing and project notes on data engineering, search, machine learning, and software architecture. The site is generated with Zola and the Linkita theme, pinned as a Git submodule on its `main` branch.

## Start locally

The repository includes a Compose based Dev Container. Open the repository in VS Code and choose **Reopen in Container**. In the container terminal, start the preview with:

```sh
python3 scripts/serve_site.py
```

VS Code forwards port 1111 and opens the preview.

To preview outside the container, install Zola **0.23.6 or newer**, Python 3, and initialize the theme:

```sh
git submodule update --init --recursive
python scripts/serve_site.py
```

The local preview runs at <http://127.0.0.1:1111/>. Zola writes the production site to `public/`.

The site uses [Linkita](https://github.com/salif/linkita), a Zola theme for personal blogs with search, dark mode, author profiles, and projects. Its `main` branch uses Tera 2 and requires Zola 0.23.6 or newer.

## Check and build

With [Just](https://just.systems/) installed, use the project recipes:

```sh
just check
just build
just preview
```

The recipes use `python` on Windows and `python3` on Unix-like systems. They require Zola **0.23.6 or newer** because Linkita uses Tera 2 components. Set `ZOLA` to a supported executable if an older version is first on `PATH`; the recipes check the version before running. For example, in PowerShell:

```powershell
$env:ZOLA = 'C:\tools\zola-0.23.6\zola.exe'
```

The equivalent commands are:

```sh
zola check
zola build
python scripts/fill_empty_feeds.py
python scripts/check_site.py
```

The generated-site check verifies required routes and assets, local links, feed XML, the web manifest, and the custom domain file.

## Publishing

`develop` is the repository's default integration branch and `main` is the release branch. GitHub Actions checks pull requests targeting either branch; pushes to `main` deploy the generated artifact to GitHub Pages, while pushes to `develop` only build and validate it. Use **GitHub Actions** as the Pages publishing source and configure the custom domain `john-cd.com` in repository settings. The site uses `https://john-cd.com` as its canonical base URL and publishes the `CNAME` file with the artifact.

The Cheatsheets documentation is maintained in the separate [john-cd/cheatsheets repository](https://github.com/john-cd/cheatsheets) and published at <https://john-cd.github.io/cheatsheets/>.

To roll back a faulty deployment, revert the source commit and publish the revert. For a wider outage, pause Pages publishing in the repository settings while repairing the source.

## Content and license

The original blog drafts remain unpublished until reviewed. The repository's first-party content is proprietary. The custom terms in [LICENSE](LICENSE) reserve reuse rights and prohibit automated extraction and AI or machine-learning training and related uses. The Linkita theme submodule and any separately identified third-party material retain their own licenses.
