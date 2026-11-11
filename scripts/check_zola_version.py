"""Ensure local commands use the Zola release pinned for the AdiDoks theme."""

from __future__ import annotations

import os
import subprocess
import sys


PINNED_VERSION = "0.19.2"


def main() -> int:
    """Report a clear setup error when the selected Zola version is unsupported."""
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
            f"Could not run Zola at {zola!r}: {error}. Install Zola {PINNED_VERSION} "
            "or set ZOLA to its executable path.",
            file=sys.stderr,
        )
        return 127

    version_output = (result.stdout or result.stderr).strip()
    if result.returncode != 0 or version_output != f"zola {PINNED_VERSION}":
        found = version_output or f"exit code {result.returncode}"
        print(
            f"This site requires Zola {PINNED_VERSION} for its pinned AdiDoks theme; "
            f"found {found}. Set ZOLA to the Zola {PINNED_VERSION} executable or "
            "use the Dev Container.",
            file=sys.stderr,
        )
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
