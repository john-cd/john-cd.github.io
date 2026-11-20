<!-- Open repository, release, and owner-review follow-ups. -->
# Remaining work

Reviewed on 2026-11-12. The site fixes and release guidance are synchronized on `develop` and `main`. GitHub Pages uses the Actions publisher, `main` is allowed by the `github-pages` environment, and the custom domain is configured with an approved HTTPS certificate.

## Release gates

- [ ] **Review the original drafts and CV facts before publishing.** The three migrated 2017–2018 posts remain drafts; the Scala post is only one sentence. The CV still claims an Inspur role beginning in 2017 with no end date and contains dated experience and technology claims. Confirm what is current and which articles are ready before changing those personal facts or publishing the posts.
- [ ] **Build the Dev Container image.** Compose configuration validation passes. The Docker build could not run because the Docker Desktop Linux engine pipe `npipe:////./pipe/dockerDesktopLinuxEngine` was unavailable.
