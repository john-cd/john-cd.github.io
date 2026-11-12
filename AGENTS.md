# Repository Instructions

## Project overview

- This repository builds John Cruchon-Dupeyrat's personal website with Zola and the pinned Linkita theme submodule.
- Site configuration lives in `config.toml`; first-party pages and blog posts live in
  `content/`; custom templates live in `templates/`; files copied
  verbatim to the site live in `static/`.
- Treat `themes/linkita/` as a third-party Git submodule. Do not edit its files as part
  of this repository's changes. Theme upgrades are gitlink updates and must be reviewed as
  dependency changes.
- `public/` is generated output. Never commit it.

## Content and publication

- Keep the existing draft status of migrated blog posts. Do not publish a draft or change personal
  biographical or CV claims without the owner's review.
- Preserve the site's canonical domain, `https://john-cd.com`, and the `static/CNAME` value unless the owner explicitly requests a domain change.
- Preserve the separate Cheatsheets project route and its external links.
- First-party content is proprietary under `LICENSE`; do not copy it into unrelated examples or generated artifacts.

## Zola, scripts, and local commands

- Use Zola 0.23.6 or newer. The GitHub Actions workflow and Dev Container pin 0.23.6; the Dev
  Container verifies the downloaded release archive against `.devcontainer/.env`.
- Run commands from the repository root. Prefer the `justfile` recipes:
  - `just check` checks the installed Zola version and runs `zola check`.
  - `just build` builds the site, fills any missing empty feeds, then checks generated routes, assets, XML, and local links.
  - `just preview` starts the local preview and maintains empty feed routes.
  - `just site-check [directory]` validates an existing generated site directory.
- The maintained Python scripts are:
  - `scripts/check_zola_version.py`: rejects missing or unsupported Zola installations.
  - `scripts/fill_empty_feeds.py`: copies valid empty RSS and Atom feeds only when Zola emitted no feed files.
  - `scripts/check_site.py`: checks required generated files and local HTML/CSS references, including anchors.
  - `scripts/serve_site.py`: starts Zola's preview server and keeps the empty feed routes available.
- The tracked `.devcontainer/.env` may contain only public build inputs such as a tool
  version, a verified checksum, and a Compose project name. Never put credentials or personal tokens
  in it; keep machine-specific values in the ignored `.devcontainer/.env.local`.

## Comments and documentation

- Keep a concise file-level comment in maintained source and configuration files where the format
  supports comments. Use language docstrings for Python modules, classes, and functions.
- Explain why a setting or workflow step exists when its purpose is not clear from its name. Keep comments accurate when behavior changes.
- Keep `README.md`, this file, and workflow descriptions aligned with the actual scripts and deployment behavior.
- Do not add comments to strict JSON, plain data files such as `static/CNAME`, generated output, binary assets, or third-party theme files.

## CI and release flow

- `.github/workflows/site.yml` builds and validates pull requests and pushes to `develop` and `main`. Only a push to `main` runs the GitHub Pages deployment job.
- `.github/workflows/codeql.yml` runs CodeQL's JavaScript and Python analyzers on pushes,
  pull requests, and its weekly schedule. The current first-party source is Python; the Linkita
  JavaScript remains in its upstream submodule.
- `develop` is the integration branch; `main` is the release branch. Keep release history linear and advance `main` with a fast-forward from a reviewed, validated `develop` commit. Never force-push.
- Before publishing, run `just check` and `just build`, review the diff,
  and confirm the GitHub Actions build passed. After publishing, verify the custom domain, the
  GitHub Pages hostname, and the required content and feed routes.
- The repository uses GitHub Actions as the Pages source and publishes the `CNAME` file with the generated artifact.

## Git and Windows command sandbox

- Preserve existing staged, unstaged, and untracked work. Inspect `git status` before editing and before committing.
- Commit only when requested. When requested, make focused commits with clear messages; preserve linear history and synchronize the intended branches with `origin`.
- On Windows, if Git Bash/MSYS, `git.exe`, or `gh.exe` fails to start or
  access a path because of the command sandbox (for example
  `NtCreateDirectoryObject(\BaseNamedObjects\...)`, `0xC0000022`, or
  `0xC0000142`), rerun only that command with Codex elevated access. Keep other
  commands sandboxed; do not change filesystem ACLs or disable the sandbox to work around it.
