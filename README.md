# VibeVizor website

Public RU and EN landing pages at https://vibevizor.com/ and https://vibevizor.com/en/.
The GitHub Pages mirror serves the same static source.

The interface uses the application palette and supplied PNG mark and wordmark.
Fonts are self-hosted with their OFL licenses. The workspace illustrations are examples.
HTML contains its styles and scripts; legacy styles.css and site.js are retained for cached pages.

Downloads use the existing `AgentRelay-macOS.zip` GitHub Release asset. Version, build and
publication time describe the linked published binary. Keep exactly one RELEASE_META_START /
RELEASE_META_END block per language. Refresh these with `scripts/update-release-metadata.py`
using the verified release app and GitHub release publication time. Never edit the signed appcast.xml
by hand. Website publication does not publish a new application binary.

Preview: `python3 -m http.server` from this directory.
