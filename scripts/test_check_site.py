"""Regression tests for generated-site link validation."""

import io
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest.mock import patch

import check_site


class DirectoryLinkTests(unittest.TestCase):
    """Exercise link resolution against a synthetic generated-site directory."""

    def test_directory_links_require_an_index_and_a_matching_anchor(self):
        """Accept dotted directory names and reject missing index pages or anchors."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "nested" / "index.html"
            article = root / "nested" / "article.v1"
            article.mkdir(parents=True)
            source.touch()
            empty = root / "nested" / "empty"
            empty.mkdir()
            (article / "index.html").write_text(
                '<h1 id="present">Article</h1>', encoding="utf-8"
            )
            with patch.object(check_site, "PUBLIC", root):
                for reference in ("article.v1/#present", "/nested/article.v1#present"):
                    with self.subTest(reference=reference):
                        self.assertTrue(
                            check_site.check_reference(reference, source, {})
                        )
                for reference in (
                    "article.v1/#missing",
                    "/nested/article.v1#missing",
                    "empty/",
                ):
                    with (
                        self.subTest(reference=reference),
                        redirect_stderr(io.StringIO()),
                    ):
                        with self.assertRaises(SystemExit):
                            check_site.check_reference(reference, source, {})
