# Remaining work

Reviewed against the Zola migration at `1333d5f` on 2026-11-11. Remote `develop` and `main` branches now exist at that baseline, and local site changes are on `develop`. Repository changes in this working tree implement the code and content work below. These release and owner-review items still need follow-through.

## Release gates

- [ ] **Set the repository default branch to `develop`.** Remote `develop` and `main` were created from current `master` at `1333d5f`; the local working changes are on `develop`. The remote default remains `master` because the GitHub connection has no repository-settings mutation tool and the local `gh` token is invalid.
- [ ] **Publish and verify GitHub Pages.** The workflow checks pull requests for `develop` and `main`, builds pushes to both, and deploys only pushes to `main`; the output includes `CNAME` for `john-cd.com`. Set the Pages source to **GitHub Actions**, publish a release commit to `main`, and verify HTTPS routes for `/`, `/about/`, `/contact/`, `/projects/`, `/cv/`, `/feed.xml`, `/atom.xml`, and `/cheatsheets/`. `john-cd.github.io` currently serves the old site; the `.com` root returned 404 from the local network during this work.
- [ ] **Require the PR build in branch rules.** Mark the `Build and publish site / build` check as required for `develop` and `main`. The connected GitHub integration cannot read or update branch protection, and no valid local GitHub CLI credential is available.
- [ ] **Review the original drafts and CV facts before publishing.** The three migrated 2017–2018 posts remain drafts; the Scala post is only one sentence. The CV still claims an Inspur role beginning in 2017 with no end date and contains dated experience and technology claims. Confirm what is current and which articles are ready before changing those personal facts or publishing the posts.
- [ ] **Run a visual browser check.** Verify narrow-screen navigation, search keyboard interaction, and theme operation with browser storage disabled. The local server and HTTP routes work, but Playwright's Chrome and Edge processes terminated before loading the site, and the built-in browser could not initialize in this environment.
- [ ] **Build the Dev Container image.** Compose configuration validation passes, but Docker denied access to `C:\Users\scdup\.docker\buildx\.lock`, so the image build could not run here.

## Completed in this working tree

- Pinned the build to Zola 0.19.2 with the AdiDoks submodule checkout, PR checks for `develop` and `main`, Pages deployment from `main`, and generated-route/link/asset checks.
- Replaced the theme demo homepage, sample docs, author pages, and five sample posts. Preserved the old feed filenames with valid empty feeds while no posts are public, and kept the original articles as drafts.
- Restored the historical `john-cd.com` CNAME and canonical URL, retained `/cheatsheets/` as the separate project route, and added site-owned metadata, social image, and icon assets.
- Made search results use safe DOM text nodes, added keyboard navigation and storage guards, replaced the Calendly embed with a direct link, and corrected the privacy notice.
- Removed the obsolete CV copy and empty demo directories, removed the Ruby devcontainer and duplicate CodeQL workflow, and added one CodeQL workflow for the maintained JavaScript and Python code.
- Added the Compose based Dev Container, Dependabot updates for Actions, the theme submodule, Docker, and Dev Containers, normalized Git text handling, and updated the README.
- Replaced the MIT notice with a proprietary first-party license that excludes separately licensed theme and third-party material and prohibits AI/ML training and related uses.
