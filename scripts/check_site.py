from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
BASE_URL = "https://john-cd.com"
EXTERNAL_PROJECT_ROUTES = {"/cheatsheets", "/cheatsheets/"}
REQUIRED_FILES = {
    "index.html",
    "404.html",
    "sitemap.xml",
    "robots.txt",
    "search_index.en.js",
    "main.css",
    "js/main.js",
    "js/search.js",
    "plugins/elasticlunr.min.js",
    "about/index.html",
    "blog/index.html",
    "projects/index.html",
    "cv/index.html",
    "contact/index.html",
    "privacy-policy/index.html",
    "atom.xml",
    "feed.xml",
    "CNAME",
    "site.webmanifest",
    "favicon.ico",
    "favicon-16x16.png",
    "favicon-32x32.png",
    "apple-touch-icon.png",
    "android-chrome-192x192.png",
    "android-chrome-512x512.png",
    "img/social-card.png",
}


class HTMLReferences(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.references: list[str] = []
        self.ids: set[str] = set()
        self.titles: list[str] = []
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        for name in ("href", "src", "poster"):
            value = values.get(name)
            if value:
                self.references.append(value)
        if values.get("id"):
            self.ids.add(values["id"] or "")
        if tag == "a" and values.get("name"):
            self.ids.add(values["name"] or "")
        if tag == "title":
            self._in_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.titles.append(data)


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def output_path_for_url(path: str, source: Path) -> Path:
    if not path or path == "/":
        return PUBLIC / "index.html"

    relative = unquote(path).lstrip("/")
    target = PUBLIC / relative
    if path.endswith("/"):
        return target / "index.html"
    if target.suffix:
        return target
    if target.is_file():
        return target
    return target / "index.html"


def check_reference(reference: str, source: Path, ids_by_file: dict[Path, set[str]]) -> bool:
    parsed = urlsplit(reference)
    if parsed.scheme or parsed.netloc:
        if parsed.scheme not in {"http", "https"} or parsed.netloc.lower() != "john-cd.com":
            return False
        path = parsed.path or "/"
    else:
        path = parsed.path

    if path in EXTERNAL_PROJECT_ROUTES:
        return False

    if not path:
        target = source
    elif path.startswith("/"):
        target = output_path_for_url(path, source)
    else:
        target = (source.parent / unquote(path)).resolve()

    if not target.exists():
        fail(f"{source.relative_to(PUBLIC).as_posix()} references missing {reference!r}")

    if parsed.fragment and target.suffix.lower() == ".html":
        target_ids = ids_by_file.get(target)
        if target_ids is None:
            parser = HTMLReferences()
            parser.feed(target.read_text(encoding="utf-8"))
            target_ids = parser.ids
            ids_by_file[target] = target_ids
        if unquote(parsed.fragment) not in target_ids:
            fail(f"{source.relative_to(PUBLIC).as_posix()} references missing anchor {reference!r}")

    return True


def main() -> None:
    global PUBLIC
    if len(sys.argv) > 1:
        PUBLIC = Path(sys.argv[1]).resolve()

    if not PUBLIC.is_dir():
        fail("Zola output directory public/ does not exist")

    missing = sorted(path for path in REQUIRED_FILES if not (PUBLIC / path).is_file())
    if missing:
        fail("required generated files are missing: " + ", ".join(missing))

    if (PUBLIC / "CNAME").read_text(encoding="utf-8").strip() != "john-cd.com":
        fail("public/CNAME does not contain the configured custom domain")

    manifest = json.loads((PUBLIC / "site.webmanifest").read_text(encoding="utf-8"))
    for icon in manifest.get("icons", []):
        if not (PUBLIC / icon["src"].lstrip("/")).is_file():
            fail(f"web manifest references missing icon {icon['src']!r}")

    for feed in ("atom.xml", "feed.xml", "sitemap.xml"):
        try:
            ET.parse(PUBLIC / feed)
        except ET.ParseError as error:
            fail(f"{feed} is not valid XML: {error}")

    html_files = sorted(PUBLIC.rglob("*.html"))
    ids_by_file: dict[Path, set[str]] = {}
    local_reference_count = 0
    for html_file in html_files:
        parser = HTMLReferences()
        parser.feed(html_file.read_text(encoding="utf-8"))
        ids_by_file[html_file] = parser.ids
        if html_file == PUBLIC / "index.html" and "".join(parser.titles).strip() != "John Cruchon-Dupeyrat":
            fail("the homepage title is not site-specific")
        for reference in parser.references:
            if check_reference(reference, html_file, ids_by_file):
                local_reference_count += 1

    for css_file in PUBLIC.rglob("*.css"):
        css = css_file.read_text(encoding="utf-8")
        for match in re.finditer(r"url\(\s*(['\"]?)(.*?)\1\s*\)", css, re.IGNORECASE):
            reference = match.group(2).strip()
            if reference:
                if reference.startswith("/"):
                    if check_reference(reference, css_file, ids_by_file):
                        local_reference_count += 1
                elif not urlsplit(reference).scheme:
                    target = (css_file.parent / unquote(reference.split("#", 1)[0].split("?", 1)[0])).resolve()
                    if not target.is_file():
                        fail(f"{css_file.relative_to(PUBLIC).as_posix()} references missing asset {reference!r}")
                    local_reference_count += 1

    print(f"Checked {len(html_files)} generated HTML files and {local_reference_count} local links/assets.")


if __name__ == "__main__":
    main()
