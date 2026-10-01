# AgentRelay download page

Public landing page and release assets for the private AgentRelay source repository.

The download button points to the latest GitHub Release asset named `AgentRelay-macOS.zip`. Publish a signed, notarized universal app archive under that exact name before announcing an update.

After publishing the release, update the version, build number, and exact publication time on both language pages:

```sh
python3 scripts/update-release-metadata.py --app /path/to/exported/AgentRelay.app --published-at '<GitHub Release publishedAt ISO 8601>'
```

Use the app inside the verified release ZIP and the release API's `publishedAt` value. The script displays Europe/Belgrade local time with seconds and a time-zone abbreviation. Publish the page only after the download asset works without authentication.

## Page structure

- `content/ru.json` and `content/en.json` hold the copy. `scripts/build-pages.py` generates the static language pages and refreshes CSS/JS cache hashes. Edit the copy/template, then run `python3 scripts/build-pages.py`.
- `index.html` (Russian) and `en/index.html` (English) keep exactly one `<!-- RELEASE_META_START -->…<!-- RELEASE_META_END -->` block and the `AgentRelay-macOS.zip` download link. Both are required by release verification.
- `styles.css` holds the design system; `site.js` handles menu, example commit selection, schematic switching and opening release notes. Schematics are informative placeholders with illustrative data. There are no autoplay animations.
- `docs/website-content.md` records positioning, sections, actions, placeholder briefs and the mapping to the canonical feature catalog.
- `content/release-notes.json` holds the exact public release notes. The existing metadata command now refreshes notes and builds both pages together. No runtime API request is needed on GitHub Pages.
- Optional Russian release-note translations live in `content/ru.json` under `releaseNotes`, keyed by exact tag. New releases fall back to a labeled English original until translated.
- `fonts/` contains self-hosted Unbounded, Geologica, and JetBrains Mono (latin and cyrillic subsets, OFL).
- Social metadata uses the app icon and current localized copy. Older `og.png` assets are retained but no longer referenced by the new design.
- Never edit `appcast.xml` by hand. It is signed for Sparkle.

Preview locally with `python3 scripts/preview.py` from the repository root, then open `http://127.0.0.1:8791/`. This serves only public site artifacts. GitHub Pages excludes authoring docs and design briefs through `_config.yml`.

Check publication behavior with `python3 scripts/test-release-pages.py`; it covers next-version notes, stale-translation fallback, escaping and failure before writes. For an offline release update, add `--release-json /path/to/exported-github-release.json` to the metadata command.
