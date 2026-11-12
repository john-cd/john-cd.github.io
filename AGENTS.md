# Repository Instructions

## Windows command sandbox

- On Windows, if Git Bash/MSYS, `git.exe`, or `gh.exe` fails to start or access a path because of the command sandbox (for example `NtCreateDirectoryObject(\BaseNamedObjects\...)`, `0xC0000022`, or `0xC0000142`), rerun only that command with Codex elevated access (`sandbox_permissions: require_escalated`). Keep other commands sandboxed; do not change filesystem ACLs or disable the sandbox to work around it.
