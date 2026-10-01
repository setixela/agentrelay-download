#!/usr/bin/env python3
"""Regression checks for the version/notes publication contract, without a network."""
import json
import plistlib
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReleasePagesTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        for folder in ["scripts", "content", "en"]:
            shutil.copytree(ROOT / folder, self.root / folder)
        for file in ["index.html", "styles.css", "site.js"]:
            shutil.copy2(ROOT / file, self.root / file)
        app = self.root / "Candidate.app/Contents"
        app.mkdir(parents=True)
        (app / "Info.plist").write_bytes(plistlib.dumps({"CFBundleShortVersionString": "1.1.6", "CFBundleVersion": "21"}))
        self.release = {"tag_name": "v1.1.6", "draft": False, "published_at": "2026-10-02T09:00:00Z", "html_url": "https://github.com/setixela/agentrelay-download/releases/tag/v1.1.6", "body": "## Changes\n\n- Fix branch selection\n- Keep <script>alert(1)</script> as text\n\n## Requirements\nmacOS 14"}
        self.fixture = self.root / "release.json"

    def tearDown(self):
        self.temp.cleanup()

    def run_update(self, published_at="2026-10-02T09:00:00Z"):
        self.fixture.write_text(json.dumps(self.release))
        return subprocess.run([sys.executable, str(self.root / "scripts/update-release-metadata.py"), "--app", str(self.root / "Candidate.app"), "--published-at", published_at, "--release-json", str(self.fixture)], capture_output=True, text=True)

    def snapshots(self):
        return {name: (self.root / name).read_bytes() for name in ["index.html", "en/index.html", "content/release-notes.json"]}

    def test_next_release_updates_both_languages_and_escapes_notes(self):
        result = self.run_update()
        self.assertEqual(result.returncode, 0, result.stderr)
        for name in ["index.html", "en/index.html"]:
            page = (self.root / name).read_text()
            self.assertIn("1.1.6", page)
            self.assertIn("Fix branch selection", page)
            self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", page)
            self.assertNotIn("<script>alert(1)</script>", page)
            self.assertEqual(page.count("<!-- RELEASE_META_START -->"), 1)
            self.assertIn("releases/latest/download/AgentRelay-macOS.zip", page)
        self.assertIn("Оригинальные заметки релиза", (self.root / "index.html").read_text())
        self.assertNotIn("Терминал и редактор остаются", (self.root / "index.html").read_text())
        notes = json.loads((self.root / "content/release-notes.json").read_text())
        self.assertEqual(notes["tag"], "v1.1.6")
        before = self.snapshots()
        rebuilt = subprocess.run([sys.executable, str(self.root / "scripts/build-pages.py")], capture_output=True, text=True)
        self.assertEqual(rebuilt.returncode, 0, rebuilt.stderr)
        self.assertEqual(before, self.snapshots())

    def test_wrong_tag_changes_no_files(self):
        self.release["tag_name"] = "v9.9.9"
        before = self.snapshots()
        self.assertNotEqual(self.run_update().returncode, 0)
        self.assertEqual(before, self.snapshots())

    def test_wrong_publication_time_changes_no_files(self):
        before = self.snapshots()
        self.assertNotEqual(self.run_update("2026-10-02T10:00:00Z").returncode, 0)
        self.assertEqual(before, self.snapshots())

    def test_missing_notes_changes_no_files(self):
        self.release["body"] = ""
        before = self.snapshots()
        self.assertNotEqual(self.run_update().returncode, 0)
        self.assertEqual(before, self.snapshots())

    def test_invalid_second_page_does_not_update_first_page(self):
        path = self.root / "en/index.html"
        path.write_text(path.read_text().replace("<!-- RELEASE_META_START -->", "<!-- missing -->"))
        before = self.snapshots()
        self.assertNotEqual(self.run_update().returncode, 0)
        self.assertEqual(before, self.snapshots())


if __name__ == "__main__":
    unittest.main()
