# GitHub Actions workflows

<!-- workflow-operations-reference:start -->

<!-- TODO Reviewed ??-??-2026. -->

## Workflow operations reference

The workflow YAML files own execution behavior. Their inline comments explain the purpose and
the boundaries that must survive future refactoring. This reference records the current job map;
repository-level Actions enable/disable settings remain independent of these tracked definitions.

### Changes in this review

- codeql.yml: Bound analyze to 30 minutes.
- site.yml: Bound build to 30 minutes.
- site.yml: Bound deploy to 30 minutes.

### [CodeQL](codeql.yml)

Events: `workflow_dispatch, push, pull_request, schedule`. Branch/path filters and manual defaults are defined in the linked file.

| Job     | Runs on / reuse | Dependencies | Guard                             | Main checks or side effects                           |
| ------- | --------------- | ------------ | --------------------------------- | ----------------------------------------------------- |
| analyze | "ubuntu-latest" | []           | Successful dependencies (default) | Check out repository; Initialize CodeQL; Analyze code |

### [Build and publish site](site.yml)

Events: `workflow_dispatch, pull_request, push`. Branch/path filters and manual defaults are defined in the linked file.

| Job    | Runs on / reuse | Dependencies | Guard                                                          | Main checks or side effects                                                                                                                                                                                            |
| ------ | --------------- | ------------ | -------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| build  | "ubuntu-latest" | []           | Successful dependencies (default)                              | Check out the site and theme; Install Zola supported by Linkita; Check content and external links; Build site; Preserve feed routes when no posts are public; Check generated routes and assets; Upload Pages artifact |
| deploy | "ubuntu-latest" | "build"      | github.event_name == 'push' && github.ref == 'refs/heads/main' | Publish to GitHub Pages                                                                                                                                                                                                |

### Caches, permissions and failures

- Keep package downloads and compiler outputs separate. Match cache keys to compiler, OS, dependency locks, build profiles and features; a cache is an optimization, not a prerequisite for correctness.
- Matrix jobs start on separate machines. Build/test commands in one job reuse local outputs; moving them to separate jobs requires an explicit compatible artifact handoff.
- Read-only validation and live publication have different lifecycles. Preserve existing credentials, event/ref conditions, environments and non-cancelling deployment groups.
- Timeouts bound hung or unexpectedly expensive runs. Diagnose a timeout before increasing it; never convert a failed check into an unconditional success.
- A queued/disabled/billing-blocked run is not a passed check. Record hosted results separately from local workflow parsing/format validation.

### Local validation

```sh
actionlint
git diff --check
```

Use the repository formatter for edited YAML/Markdown. Run the commands named by the affected
jobs when their executable behavior changes; platform/container/credential-dependent checks
must be reported at the scope actually executed. Do not run publishing commands merely to test
a comment or validation-only change.

<!-- workflow-operations-reference:end -->
