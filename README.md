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

The generated-site check verifies required pages and assets, local HTML and CSS references (including anchors), feed and sitemap XML, manifest icons, the homepage title, and the custom domain file.

## Maintenance scripts and CI

The scripts in `scripts/` support the local preview and production build:

- `check_zola_version.py` selects the configured Zola executable and rejects versions older than 0.23.6.
- `fill_empty_feeds.py` copies valid empty RSS and Atom feeds only when Zola did not emit those files. This keeps the public feed routes available while all blog posts remain drafts.
- `check_site.py` validates the generated files, internal HTML/CSS references, anchors, XML feeds, manifest icons, and CNAME.
- `serve_site.py` starts Zola's preview server and periodically restores missing empty feed routes while Zola rebuilds.

GitHub Actions uses the same build steps as the local build:

- `.github/workflows/site.yml` runs for pull requests and pushes on `develop` and `main`. Its build job checks out the theme submodule, installs Zola 0.23.6, checks content, builds the site, fills empty feeds, validates the output, and uploads the Pages artifact. A separate job deploys that artifact only for a push to `main`.
- `.github/workflows/codeql.yml` runs CodeQL's JavaScript and Python analyzers on pull requests, pushes, and a weekly schedule. The current first-party source is Python; the Linkita JavaScript remains in its upstream submodule.
- `.github/dependabot.yml` checks for updates to Actions, the theme submodule, the container image, and Dev Container configuration.

The tracked `.devcontainer/.env` contains only the Compose project name and public Zola version/checksum pins. Keep credentials in the ignored `.devcontainer/.env.local`, never in the tracked file.

## Publishing

`develop` is the integration branch and `main` is the release branch. Keep release history linear by advancing `main` from a validated `develop` commit. Pull requests to either branch and pushes to both branches build and validate the site; only a push to `main` deploys the generated artifact to GitHub Pages. GitHub Pages must use **GitHub Actions** as its publishing source and the custom domain `john-cd.com`. The site uses `https://john-cd.com` as its canonical base URL. GitHub Pages is configured in repository settings to use the custom domain; it ignores a `CNAME` file in custom Actions artifacts. The `github-pages` environment's deployment branch policy must allow `main`. If the build passes but the deploy job is rejected before starting a runner, check that policy first.

The Cheatsheets documentation is maintained in the separate [john-cd/cheatsheets repository](https://github.com/john-cd/cheatsheets) and published at <https://john-cd.github.io/cheatsheets/>.

To roll back a faulty deployment, revert the source commit and publish the revert. For a wider outage, pause Pages publishing in the repository settings while repairing the source.

## Content and license

The original blog drafts remain unpublished until reviewed. The repository's first-party content is proprietary. The custom terms in [LICENSE](LICENSE) reserve reuse rights and prohibit automated extraction and AI or machine-learning training and related uses. The Linkita theme submodule and any separately identified third-party material retain their own licenses.
