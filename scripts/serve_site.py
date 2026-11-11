from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

from fill_empty_feeds import fill_empty_feeds


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    zola = os.environ.get("SITE_ZOLA_BIN", "zola")
    interface = os.environ.get("SITE_SERVE_INTERFACE", "127.0.0.1")
    port = os.environ.get("SITE_SERVE_PORT", "1111")
    command = [zola, "serve", "--interface", interface, "--port", port, *sys.argv[1:]]
    server = subprocess.Popen(command, cwd=ROOT)

    try:
        while server.poll() is None:
            try:
                fill_empty_feeds(ROOT / "public")
            except FileNotFoundError:
                # Zola may still be building or replacing its output directory.
                pass
            time.sleep(0.5)
    except KeyboardInterrupt:
        server.terminate()
    finally:
        if server.poll() is None:
            server.terminate()
        server.wait()

    return server.returncode or 0


if __name__ == "__main__":
    raise SystemExit(main())
