#!/usr/bin/env python3
"""Update version, publication time and GitHub release notes on both static pages."""

import argparse
import html
import json
import plistlib
import re
import runpy
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
MONTHS_RU = (
    "января", "февраля", "марта", "апреля", "мая", "июня",
    "июля", "августа", "сентября", "октября", "ноября", "декабря",
)
MONTHS_EN = (
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
)
PATTERN = re.compile(r"<!-- RELEASE_META_START -->.*?<!-- RELEASE_META_END -->", re.S)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--app", required=True, type=Path)
    parser.add_argument("--published-at", required=True)
    parser.add_argument("--release-json", type=Path, help="Optional exported GitHub release JSON for offline use")
    args = parser.parse_args()

    with (args.app / "Contents/Info.plist").open("rb") as info_file:
        info = plistlib.load(info_file)
    raw_version = str(info["CFBundleShortVersionString"])
    version = html.escape(raw_version)
    build = html.escape(str(info["CFBundleVersion"]))
    published = datetime.fromisoformat(args.published_at.replace("Z", "+00:00"))
    if published.tzinfo is None:
        parser.error("--published-at must include a time zone")
    local = published.astimezone(ZoneInfo("Europe/Belgrade"))
    timestamp = local.isoformat(timespec="seconds")
    clock = f"{local:%H:%M:%S} {local:%Z}"
    collect_notes = runpy.run_path(str(ROOT / "scripts/refresh-release-notes.py"))["collect_notes"]
    notes = collect_notes(f"v{raw_version}", args.published_at, args.release_json)
    render = runpy.run_path(str(ROOT / "scripts/build-pages.py"))["render"]

    pages = {
        ROOT / "index.html": (
            f"Версия {version} · сборка {build} · опубликовано "
            f"<time datetime=\"{timestamp}\">"
            f"{local.day} {MONTHS_RU[local.month - 1]} {local.year}, {clock}</time>"
        ),
        ROOT / "en/index.html": (
            f"Version {version} · build {build} · published "
            f"<time datetime=\"{timestamp}\">"
            f"{local.day} {MONTHS_EN[local.month - 1]} {local.year}, {clock}</time>"
        ),
    }
    pending = []
    for path, message in pages.items():
        source = path.read_text()
        replacement = (
            "<!-- RELEASE_META_START -->\n"
            f"            <p class=\"build-meta\">{message}</p>\n"
            "            <!-- RELEASE_META_END -->"
        )
        updated, count = PATTERN.subn(replacement, source)
        if count != 1:
            raise ValueError(f"Expected one release metadata block in {path}, got {count}")
        lang = "ru" if path.parent == ROOT else "en"
        copy = json.loads((ROOT / f"content/{lang}.json").read_text())
        pending.append((path, render(copy, replacement, "./" if lang == "ru" else "../", notes)))

    # Fetch and validate everything before changing either page.
    (ROOT / "content/release-notes.json").write_text(json.dumps(notes, ensure_ascii=False, indent=2) + "\n")
    for path, source in pending:
        path.write_text(source)

    print(f"Updated RU and EN pages and release notes: version {version}, build {build}, {timestamp}")


if __name__ == "__main__":
    main()
