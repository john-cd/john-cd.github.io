"""Ensure local commands use a Zola version supported by the Linkita theme."""

from __future__ import annotations

import os
import re
import subprocess
import sys


MINIMUM_VERSION = (0, 23, 6)
MINIMUM_VERSION_TEXT = ".".join(map(str, MINIMUM_VERSION))


def main() -> int:
    """Reject missing or outdated Zola installations with an actionable message."""
    zola = os.environ.get("SITE_ZOLA_BIN", os.environ.get("ZOLA", "zola"))
    try:
        result = subprocess.run(
            [zola, "--version"],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as error:
        print(
            f"Could not run Zola at {zola!r}: {error}. Install Zola {MINIMUM_VERSION_TEXT} "
            "or set ZOLA to its executable path.",
            file=sys.stderr,
        )
        return 127

    version_output = (result.stdout or result.stderr).strip()
    match = re.fullmatch(r"zola (\d+)\.(\d+)\.(\d+)", version_output)
    found_version = tuple(map(int, match.groups())) if match else None
    if result.returncode != 0 or found_version is None or found_version < MINIMUM_VERSION:
        found = version_output or f"exit code {result.returncode}"
        print(
            f"This site requires Zola {MINIMUM_VERSION_TEXT} or newer for its pinned "
            f"Linkita theme; found {found}. Set ZOLA to a supported Zola executable "
            "or use the Dev Container.",
            file=sys.stderr,
        )
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
