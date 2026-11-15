# Mock fonts

Copied byte for byte from the current website source
[`setixela/agentrelay-download`](https://github.com/setixela/agentrelay-download) at
`3a325754a0140be00a47ecc4e0cf85a4ee649a72` (`fonts/`), so the mock renders in the typefaces
DESIGN.md specifies. Unbounded is not copied because the new design drops it.

| File | Family | Weights | Subset | License |
| --- | --- | --- | --- | --- |
| `geologica-latin.woff2`, `geologica-cyrillic.woff2` | Geologica (variable) | 300–700 | Latin, Cyrillic | [OFL 1.1](OFL-Geologica.txt) |
| `jetbrainsmono-latin.woff2`, `jetbrainsmono-cyrillic.woff2` | JetBrains Mono (variable) | 400–600 | Latin, Cyrillic | [OFL 1.1](OFL-JetBrainsMono.txt) |

The license texts come from the [Google Fonts repository](https://github.com/google/fonts)
(`ofl/geologica/OFL.txt`, `ofl/jetbrainsmono/OFL.txt`). The `@font-face` rules and
`unicode-range` values in [mock.html](../mock.html) match the current site's `styles.css`.
