"""Create empty RSS and Atom files when Zola has no public posts to emit."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FALLBACKS = ROOT / "templates" / "feed-fallbacks"
FEED_NAMES = ("atom.xml", "feed.xml")


def fill_empty_feeds(output_dir: Path) -> list[str]:
    """Copy only missing feed files into a generated site directory."""
    if not output_dir.is_dir():
        raise FileNotFoundError(f"Zola output directory does not exist: {output_dir}")

    added: list[str] = []
    for name in FEED_NAMES:
        output = output_dir / name
        if output.exists():
            continue
        fallback = FALLBACKS / name
        if not fallback.is_file():
            raise FileNotFoundError(f"Feed fallback does not exist: {fallback}")
        shutil.copyfile(fallback, output)
        added.append(name)
    return added


if __name__ == "__main__":
    public_dir = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT / "public"
    added_feeds = fill_empty_feeds(public_dir)
    if added_feeds:
        print("Created empty feed fallback(s): " + ", ".join(added_feeds))
    else:
        print("Zola generated both feeds; no fallback was needed.")
