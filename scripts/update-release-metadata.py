#!/usr/bin/env python3
"""Write the shipped app version and GitHub publication time to both pages."""

import argparse
import html
import plistlib
import re
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
    args = parser.parse_args()

    with (args.app / "Contents/Info.plist").open("rb") as info_file:
        info = plistlib.load(info_file)
    version = html.escape(str(info["CFBundleShortVersionString"]))
    build = html.escape(str(info["CFBundleVersion"]))
    published = datetime.fromisoformat(args.published_at.replace("Z", "+00:00"))
    if published.tzinfo is None:
        parser.error("--published-at must include a time zone")
    local = published.astimezone(ZoneInfo("Europe/Belgrade"))
    timestamp = local.isoformat(timespec="seconds")
    clock = f"{local:%H:%M:%S} {local:%Z}"

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
        path.write_text(updated)

    print(f"Updated RU and EN pages: version {version}, build {build}, {timestamp}")


if __name__ == "__main__":
    main()
