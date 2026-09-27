# AgentRelay download page

Public landing page and release assets for the private AgentRelay source repository.

The download button points to the latest GitHub Release asset named `AgentRelay-macOS.zip`. Publish a signed, notarized universal app archive under that exact name before announcing an update.

After publishing the release, update the version, build number, and exact publication time on both language pages:

```sh
python3 scripts/update-release-metadata.py --app /path/to/exported/AgentRelay.app --published-at '<GitHub Release publishedAt ISO 8601>'
```

Use the app inside the verified release ZIP and the release API's `publishedAt` value. The script displays Europe/Belgrade local time with seconds and a time-zone abbreviation. Publish the page only after the download asset works without authentication.
