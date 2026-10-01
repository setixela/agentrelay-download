# AgentRelay website

- This repository publishes the public download page. Work in a separate branch; a new design is a review version until the owner requests publication.
- Canonical product truth lives in the source repository's `docs/product-feature-catalog.md`. Consult the current catalog before adding or changing capability claims; update both languages together.
- Edit copy in `content/ru.json` and `content/en.json`, template in `scripts/build-pages.py`, styles in `styles.css`, behavior in `site.js`. Run `python3 scripts/build-pages.py` and commit the generated HTML.
- Preserve one release metadata marker block and the exact latest ZIP URL in each language. Never hand-edit signed `appcast.xml`.
- Release publication uses `scripts/update-release-metadata.py`: version, build, publication time and release notes update together from the shipped app and exact public GitHub Release.
- Translate release notes only under the exact tag in `releaseNotes`; a new tag must not reuse old translated notes.
- Run `python3 scripts/test-release-pages.py`, `node --check site.js`, `git diff --check` and browser-check desktop/mobile after relevant changes.
- All demo values are illustrative and must stay labeled. No fabricated task-completion proof, automatic merges, benchmarks, user counts or testimonials.
- Informative placeholders are intentional in this version. Do not silently substitute generated imagery or animations.
