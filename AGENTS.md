# Repository Instructions

These instructions apply to all work in this repository. Keep the site, its documentation, and its release process aligned with the rules below.

## Project Overview and Ownership

- This repository builds John Cruchon-Dupeyrat's personal site with Zola and the Linkita theme, pinned as the `themes/linkita` Git submodule.
- `config.toml` owns the site configuration; `content/` owns first-party pages and posts; `templates/` owns site templates and empty-feed fallbacks; `static/` contains files copied to the published site; `scripts/` contains local build and validation helpers.
- Treat `themes/linkita/` as third-party code. Do not edit it as part of site work. Review theme upgrades as dependency changes to the submodule reference.
- Treat `public/` as generated output. Never edit or commit it.
- The first-party site content is proprietary under `LICENSE`. Keep it in this repository and do not reuse it in unrelated examples or generated artifacts.

## Privacy and Public Content

- **Never publish the owner's direct phone number or email address.** Do not add either to the CV, contact page, project pages, metadata, structured data, source comments, examples, assets, or any other public output. Do not restore contact details from an older resume or commit.
- Before a site release, inspect the generated output for the owner's phone and email details and confirm they are absent. Keep values out of command output and review notes.
- Preserve the canonical URL `https://john-cd.com`, the `static/CNAME` value, and the separate Cheatsheets route unless the owner explicitly requests a domain or route change.
- Keep migrated 2017–2018 blog posts as drafts. Do not publish a draft or change biographical, employment, education, or CV claims without the owner's review.
- Public summaries of private-repository work may describe broad areas and outcomes when requested. Do not link to private repositories or expose names, implementation details, credentials, customer information, or other non-public data without explicit direction.
- Keep the contact page limited to the public scheduling link unless the owner requests another public contact method.

## Repository Map

- `.github/workflows/site.yml`: build and validate the site for pull requests and pushes; deploy a successful `main` push to GitHub Pages.
- `.github/workflows/codeql.yml`: scheduled and change-triggered security analysis of maintained Python and first-party JavaScript code.
- `.github/dependabot.yml`: update GitHub Actions, the theme submodule, the container image, and Dev Container metadata.
- `.devcontainer/`: Compose-based development container and its public build pins. The image uses a small Ubuntu base and installs the Zola release pinned by version and SHA-256.
- `justfile`: supported local check, build, preview, and generated-site validation commands.
- `README.md`: environment setup, commands, script behavior, CI, and release operations.

## Comments and Documentation

- Add a concise file-level comment to maintained source and configuration files when their format supports comments. Use Python module, class, and function docstrings for maintained Python code.
- Explain non-obvious workflow triggers, permissions, environment variables, release pins, and workarounds where they are defined. Comments should describe current behavior and why it exists.
- Keep `README.md`, this file, workflow comments, and script behavior synchronized. Explain the role and invocation of each maintained script and both CI workflows.
- Do not add comments to strict JSON, generated output, plain data such as `static/CNAME`, legal text, binary assets, or third-party theme files. Do not add source comments to published prose unless they clarify content metadata.
- Keep Markdown readable: use a blank line after headings, descriptive link text, and fenced code blocks with a language tag.

## Zola and Local Commands

- Use Zola 0.23.6 or newer. Linkita's current Tera components require this minimum. GitHub Actions and the Dev Container pin the build version; the container verifies the downloaded archive checksum.
- Run commands from the repository root. Prefer the `justfile` recipes:
  - `just check` validates the Zola version and runs `zola check` for content and links.
  - `just build` validates the version, builds to `public/`, restores only missing empty feed files, then checks required routes, assets, XML, and local references.
  - `just preview` starts the local preview server and maintains empty feed routes while Zola rebuilds.
  - `just site-check [directory]` validates an existing generated-site directory.
- Python is selected as `python` on Windows and `python3` on Unix-like systems. `SITE_ZOLA_BIN` takes precedence over `ZOLA`; both can select a supported Zola executable.
- The tracked `.devcontainer/.env` contains public build inputs only, such as image/tool versions, verified checksums, and a Compose project name. Keep credentials and machine-specific overrides in the ignored `.devcontainer/.env.local`.

## Maintained Scripts

- `scripts/check_zola_version.py` selects the configured Zola binary and rejects missing or outdated versions before local commands run.
- `scripts/fill_empty_feeds.py` copies valid empty RSS and Atom feeds only when Zola did not emit those files. Do not overwrite a feed generated from public content.
- `scripts/check_site.py` checks required generated files, the custom domain, manifest icons, feed and sitemap XML, HTML/CSS local links, and HTML anchors. It rejects paths that resolve outside the generated site directory.
- `scripts/serve_site.py` starts `zola serve`, supports `SITE_SERVE_INTERFACE` and `SITE_SERVE_PORT`, and restores missing empty-feed routes while the preview server rebuilds.

## CI Workflows

- `site.yml` runs for pull requests and pushes to `develop` and `main`. It checks out the theme submodule, installs the pinned Zola version, runs `zola check`, builds the site, restores missing empty feeds, validates generated files and local links, and uploads the Pages artifact. Only a successful push build on `main` can run the deployment job.
- The Pages deployment uses the `github-pages` environment with `pages: write` and `id-token: write`. GitHub Pages must use **GitHub Actions** as its source, the custom domain must be configured in repository settings, and the environment's deployment branch policy must allow `main`.
- `codeql.yml` analyzes Python and JavaScript on pushes and pull requests to both branches and on its weekly schedule. The maintained first-party code is Python; theme JavaScript is supplied by the upstream submodule and is not checked out in that workflow.
- Dependabot updates Actions, the theme submodule, Dockerfile image inputs, and Dev Container configuration on their configured weekly schedules.
- When workflows change, document their trigger, job purpose, required permissions, and release behavior in comments and `README.md`.

## Review and Release Process

- `develop` is the integration branch and `main` is the release branch. Keep history linear; promote a validated `develop` commit to `main` with a fast-forward. Never force-push.
- Before publishing, inspect `git status`, review the full diff, run `just check` and `just build`, and confirm the relevant GitHub Actions build succeeds. Keep unrelated staged, unstaged, and untracked work out of the change.
- After publishing, verify the custom-domain route, the GitHub Pages hostname/redirect, key pages and feed routes, and the absence of direct phone and email details from the published output.
- GitHub Pages uses an Actions artifact; it ignores a `CNAME` file in custom Actions artifacts. The domain is configured in repository settings. If deployment is rejected before a runner starts, check that `main` is permitted by the `github-pages` environment policy.
- To roll back a faulty deployment, revert the source commit and publish the revert. For a wider outage, pause Pages publishing in repository settings while repairing the source.

## Git and Windows Command Sandbox

- Preserve all existing staged, unstaged, and untracked work. Inspect status before edits and before commits.
- Commit only when requested. When requested, create focused commits with clear messages, include only task-owned files, and synchronize the requested branches without rewriting published history.
- On Windows, if Git Bash/MSYS, `git.exe`, or `gh.exe` fails to start or access a path because of the command sandbox (for example `NtCreateDirectoryObject(\\BaseNamedObjects\\...)`, `0xC0000022`, or `0xC0000142`), rerun only that command with Codex elevated access. Keep other commands sandboxed; do not change filesystem ACLs or disable the sandbox to work around it.
