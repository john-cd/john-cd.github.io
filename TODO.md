<!-- Open repository, release, and owner-review follow-ups. -->
# Remaining work

Reviewed on 2026-11-12. `develop` and `main` now point to `05bf314`, with four focused site fixes on top of the existing migration. GitHub Pages uses the Actions publisher, `main` is allowed by the `github-pages` environment, and the custom domain is configured with an approved HTTPS certificate.

## Release gates

- [x] **Publish the Zola artifact.** The `main` build and GitHub Pages deployment both succeeded in run [43277278468](https://github.com/john-cd/john-cd.github.io/actions/runs/43277278468). The Pages API reports the Actions source, `john-cd.com`, and an approved certificate covering the apex and `www`.
- [ ] **Verify public routes after cache refresh.** At 2026-11-12 18:17 UTC, this network still received a cached GitHub Pages “Site not found” response for `.com`; `john-cd.github.io` redirects to the custom domain. Recheck `/`, `/about/`, `/contact/`, `/projects/`, `/cv/`, `/feed.xml`, `/atom.xml`, and `/cheatsheets/` after the edge cache refreshes.
- [ ] **Require the PR build in branch rules.** Mark the `Build and publish site / build` check as required for `develop` and `main`.
- [ ] **Review the original drafts and CV facts before publishing.** The three migrated 2017–2018 posts remain drafts; the Scala post is only one sentence. The CV still claims an Inspur role beginning in 2017 with no end date and contains dated experience and technology claims. Confirm what is current and which articles are ready before changing those personal facts or publishing the posts.
- [ ] **Run a visual browser check.** Verify narrow-screen navigation, search keyboard interaction, and theme operation with browser storage disabled. The local server and HTTP routes work, but Playwright's Chrome and Edge processes terminated before loading the site, and the built-in browser could not initialize in this environment.
- [ ] **Build the Dev Container image.** Compose configuration validation passes. The Docker build could not run because the Docker Desktop Linux engine pipe `npipe:////./pipe/dockerDesktopLinuxEngine` was unavailable.

## Completed in this working tree

- Replaced AdiDoks with the Linkita theme, migrated the site configuration and navigation, and set Zola 0.23.6 as the supported minimum for local, CI, and container builds.
- Kept PR checks for `develop` and `main`, Pages deployment from `main`, and generated-route/link/asset checks in place after the theme migration.
- Created `develop` and `main` on origin, set `develop` as the GitHub default branch, and synchronized the focused site commits to both branches using a fast-forward.
- Replaced the theme demo homepage, sample docs, author pages, and five sample posts. Preserved the old feed filenames with valid empty feeds while no posts are public, and kept the original articles as drafts.
- Restored the historical `john-cd.com` CNAME and canonical URL, retained `/cheatsheets/` as the separate project route, and added site-owned metadata, social image, and icon assets.
- Made search results use safe DOM text nodes, added keyboard navigation and storage guards, replaced the Calendly embed with a direct link, and corrected the privacy notice.
- Removed the obsolete CV copy and empty demo directories, removed the Ruby devcontainer and duplicate CodeQL workflow, and added one CodeQL workflow for the maintained JavaScript and Python code.
- Added the Compose based Dev Container, Dependabot updates for Actions, the theme submodule, Docker, and Dev Containers, normalized Git text handling, and updated the README.
- Replaced the MIT notice with a proprietary first-party license that excludes separately licensed theme and third-party material and prohibits AI/ML training and related uses.
- Added the `justfile` command runner and file-level comments/docstrings to repository-owned code, configuration, and templates.
