#!/usr/bin/env python3
"""Fetch public GitHub release notes for the exact app version."""
import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
REPO = "setixela/agentrelay-download"


def collect_notes(tag, published_at=None, release_json=None):
    if release_json:
        release = json.loads(Path(release_json).read_text())
    else:
        request = Request(
            f"https://api.github.com/repos/{REPO}/releases/tags/{quote(tag, safe='')}",
            headers={"Accept": "application/vnd.github+json", "User-Agent": "AgentRelay-website"},
        )
        with urlopen(request, timeout=30) as response:
            release = json.load(response)
    if release.get("tag_name") != tag or release.get("draft"):
        raise ValueError("Expected a published release for the exact app tag.")
    if published_at:
        actual = datetime.fromisoformat(release["published_at"].replace("Z", "+00:00"))
        expected = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
        if actual != expected:
            raise ValueError("Publication time does not match the GitHub release.")
    expected_url = f"https://github.com/{REPO}/releases/tag/{quote(tag, safe='')}"
    if release.get("html_url") != expected_url:
        raise ValueError("Unexpected GitHub release URL.")
    body = (release.get("body") or "").strip()
    if not body:
        raise ValueError("Add release notes to the GitHub release before updating the website.")
    section = re.search(r"^##\s+(?:Changes|What's new|What’s new|Changelog|Что нового)\s*\n(.*?)(?=^##\s|\Z)", body, re.M | re.S | re.I)
    source = section.group(1).strip() if section else body
    changes = []
    for line in source.splitlines():
        if line.startswith(("- ", "* ")):
            changes.append(line[2:].strip())
        elif line.startswith(("  ", "\t")) and changes:
            changes[-1] += " " + line.strip()
    if not changes:
        changes = [paragraph.strip() for paragraph in source.split("\n\n") if paragraph.strip()]
    if not changes:
        raise ValueError("The release has no readable changes.")
    return {"tag": tag, "published_at": release["published_at"], "url": expected_url, "body": body, "changes": changes}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tag", required=True)
    parser.add_argument("--published-at")
    parser.add_argument("--release-json", type=Path, help="Use an exported GitHub release JSON instead of the network")
    args = parser.parse_args()
    notes = collect_notes(args.tag, args.published_at, args.release_json)
    (ROOT / "content/release-notes.json").write_text(json.dumps(notes, ensure_ascii=False, indent=2) + "\n")
    print(f"Refreshed release notes for {args.tag}. Run scripts/build-pages.py to rebuild.")


if __name__ == "__main__":
    main()
