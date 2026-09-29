# AgentRelay download page

Public landing page and release assets for the private AgentRelay source repository.

The download button points to the latest GitHub Release asset named `AgentRelay-macOS.zip`. Publish a signed, notarized universal app archive under that exact name before announcing an update.

After publishing the release, update the version, build number, and exact publication time on both language pages:

```sh
python3 scripts/update-release-metadata.py --app /path/to/exported/AgentRelay.app --published-at '<GitHub Release publishedAt ISO 8601>'
```

Use the app inside the verified release ZIP and the release API's `publishedAt` value. The script displays Europe/Belgrade local time with seconds and a time-zone abbreviation. Publish the page only after the download asset works without authentication.

## Page structure

- `index.html` (Russian) and `en/index.html` (English) are static pages. Keep exactly one `<!-- RELEASE_META_START -->…<!-- RELEASE_META_END -->` block and the `AgentRelay-macOS.zip` download link on each page. The release scripts depend on both.
- `styles.css` holds the whole design system. `site.js` scales the workspace replica and runs the hero work demo (agent statuses and a file link opening in the editor) and the layout arranger. Both animations respect `prefers-reduced-motion`.
- After changing `styles.css` or `site.js`, update the `?v=` hash in both pages (`shasum styles.css | cut -c1-8`). GitHub Pages caches assets for 10 minutes, and without a new URL browsers mix new HTML with old CSS.
- `fonts/` contains self-hosted Unbounded, Geologica, and JetBrains Mono (latin and cyrillic subsets, OFL).
- `og.png` and `en/og.png` are the social previews (1200×630).
- Never edit `appcast.xml` by hand. It is signed for Sparkle.

Preview locally with `python3 -m http.server` from the repository root.
