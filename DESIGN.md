---
name: AgentRelay review prototype
description: Cobalt and ice code-review workbench for a native macOS agent workspace
colors:
  blue: "#203fc9"
  ink: "#162345"
  muted: "#4c5b79"
  paper: "#fff"
  ice: "#eef2fa"
  line: "#d0d8e8"
  lime: "#d8f36a"
  ui: "#7843b6"
  api: "#146c8f"
  action-hover: "#e6ff84"
  row-hover: "#dfe6f7"
  row-selected: "#dbe3fc"
  diff-surface: "#e4eaf4"
typography:
  display:
    fontFamily: "Geologica, sans-serif"
    fontSize: "clamp(44px,5.05vw,72px)"
    fontWeight: 720
    lineHeight: 1.05
    letterSpacing: "-.035em"
  headline:
    fontFamily: "Geologica, sans-serif"
    fontSize: "clamp(30px,3.25vw,48px)"
    fontWeight: 650
    lineHeight: 1.13
    letterSpacing: "-.03em"
  title:
    fontFamily: "Geologica, sans-serif"
    fontSize: "25px"
    fontWeight: 650
    lineHeight: 1.13
    letterSpacing: "-.03em"
  body:
    fontFamily: "Geologica, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.65
  label:
    fontFamily: "Geologica, sans-serif"
    fontSize: "15px"
    fontWeight: 600
    lineHeight: 1.4
  repository:
    fontFamily: "JetBrains Mono, monospace"
    fontSize: "11px"
rounded:
  inspection: "14px"
  action: "8px"
  control: "6px"
  diff: "5px"
spacing:
  compact: "12px"
  inset: "20px"
  standard: "24px"
  inspection: "28px"
  gap-medium: "48px"
  gap-large: "80px"
  section: "100px"
components:
  button-primary:
    backgroundColor: "{colors.lime}"
    textColor: "{colors.ink}"
    typography: "{typography.label}"
    rounded: "{rounded.action}"
    padding: "17px 24px"
  button-primary-hover:
    backgroundColor: "{colors.action-hover}"
  button-small:
    backgroundColor: "{colors.lime}"
    textColor: "{colors.ink}"
    rounded: "{rounded.action}"
    padding: "11px 17px"
  view-control:
    textColor: "{colors.ink}"
    rounded: "{rounded.control}"
    padding: "12px 18px"
  view-control-selected:
    backgroundColor: "{colors.blue}"
    textColor: "{colors.paper}"
  inspection-surface:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.inspection}"
    padding: "28px"
  commit-row:
    textColor: "{colors.ink}"
    rounded: "{rounded.control}"
    padding: "7px 9px"
  commit-row-selected:
    backgroundColor: "{colors.row-selected}"
---

# Design System: AgentRelay review prototype

## Overview

**Creative North Star: "The Code-Review Workbench"**

The Code-Review Workbench uses a cobalt ground, ice-white inspection surfaces, dark blue ink and an acid-lime action. Substantial geometric text carries the human explanation; compact monospaced text identifies repository material. Broad page bands and restrained ruled lists give structured information room to breathe.

This records the implemented Russian and English review prototype, not a permanent owner-approved identity. The name and existing app icon are durable product commitments; the surface narrative and first-viewport composition remain in `.impeccable/surfaces/index-html.md`.

**Key Characteristics:**
- Cobalt grounds with contrasting lime actions.
- Geologica explanation and JetBrains Mono repository detail.
- Flat inspection surfaces, thin rules and compact selectable rows.
- Shared responsive visual system for Russian and English.

## Colors

A saturated cobalt ground frames cool inspection surfaces and readable dark ink; lime highlights the primary action.

### Primary
- **Cobalt:** page bands, selected view controls and the main track.
- **Acid Lime:** primary actions, emphasis on cobalt and selection highlight.
- **Action Hover:** the brighter hover treatment for lime actions.

### Secondary
- **Track Violet** and **Track Teal:** persistent identities for the two agent tracks; violet also marks code keywords.

### Neutral
- **Dark Ink:** body text and the dark continuity band.
- **Muted Ink:** secondary explanations and metadata on light surfaces.
- **Paper** and **Ice:** page and inspection surfaces.
- **Cool Rule:** dividers and neutral control borders.
- **Row Hover** and **Row Selected:** distinct interactive states on light inspection surfaces.
- **Diff Surface:** the recessed code comparison area.

**The Track Identity Rule.** Keep cobalt, violet and teal paired consistently with the same track across branch lines, dots and activity intervals.

## Typography

**Display Font:** Geologica, with sans-serif fallback.
**Body Font:** Geologica, with sans-serif fallback.
**Label/Mono Font:** JetBrains Mono, with monospace fallback for repository material.

Self-hosted variable fonts support the substantial geometric headline and compact technical detail. Geologica has separate Latin and Cyrillic subsets; JetBrains Mono serves the Latin code examples.

### Hierarchy
- **Display:** the frontmatter records the desktop hero. At 1150px it uses `clamp(43px,5.25vw,60px)`; at 850px `clamp(45px,7.6vw,65px)`; at 520px `clamp(35px,9.65vw,48px)` with line-height (1.1).
- **Headline:** responsive section titles; the installation title has a larger contextual variant.
- **Title:** ordinary third-level headings; explanatory panel titles use a larger contextual variant (33px, line-height 1.2), reducing to (29px) and (27px).
- **Body:** default prose follows the frontmatter role and a maximum measure (70ch). Supporting copy often uses (13–15px); the hero lead uses line-height (1.8) and measure (54ch).
- **Label:** action text. Navigation uses (14px); technical metadata uses (11–12px).
- **Repository:** hashes, branch references, paths and schematic code. General code inherits a relative size (.83em); panel code may use (12px).

**The Repository Type Rule.** Use JetBrains Mono for repository identifiers and code; keep explanatory language in Geologica.

## Layout

The content container caps at (1280px), with total desktop side allowance (96px). That allowance becomes (64px) at 1150px, (48px) at 850px and (36px) at 520px. Major sections use vertical padding (100px), reducing to (72px) and (58px). Two-column explanations combine broad copy and inspection regions; common desktop gaps are (80px), reducing to (48px) and (36px).

At 850px, the principal two-column patterns become one column and navigation becomes an explicit menu when JavaScript is enabled. Without JavaScript, navigation and all inspection views remain visible. At 520px, the three-step explanatory sequence stacks and dense rows reduce their insets. Preserve the distinct compact inspection density without applying it to explanatory body copy.

## Elevation & Depth

There are no box shadows. White, ice and darker blue bands establish depth through tonal separation, thin borders and local inset surfaces. Selection is a fill change, not a raised card. There is no transition or autoplay animation vocabulary; smooth anchor scrolling changes to instant scrolling for reduced motion.

**The Flat Inspection Rule.** Separate inspection material by surface tone and thin rules, without adding shadows.

## Shapes

Inspection areas use gently rounded rectangular corners via the shared inspection radius. Actions are tighter, with compact controls tighter again. Rules are predominantly single-pixel dividers. Branch paths, circular nodes and interval rectangles convey data rather than serving as decorative silhouettes.

## Components

### Buttons
Confident lime actions contrast with cobalt grounds. The main action uses the frontmatter padding and a minimum height (54px); the small navigation variant uses minimum height (42px) and type (13px). On narrow screens, main actions use padding (15px 20px) and type (14px). Hover changes the fill. Keyboard focus uses an outline (3px) offset (5px), lime on cobalt and cobalt on light inspection material.

### Cards / Containers
Inspection surfaces are flat, rounded and locally padded. Hero inspection uses ice; inspection figures on an ice band use paper. They contain structured information, not decorative images. Diff areas use a darker cool surface and their own compact radius.

### Navigation
A horizontal cobalt-ground navigation uses compact Geologica text and lime hover. A current-language label is heavier than its alternate-language link. At the tablet breakpoint, the menu button has a transparent fill, outlined border and minimum height (44px). Escape closes the open menu and returns focus to its button.

### View Controls
Outlined rounded buttons select an inspection view. Hover shifts the border to cobalt; the `aria-pressed` selected state uses cobalt fill with white text. Minimum height is (46px). The group switches panels only when JavaScript is active.

### Commit Inspection Rows
A compact two-column row pairs a branch identifier with a hash and a full-width description. Hover and pressed fills are separate. Each graph owns its selected row and matching detail, so selecting one example does not change another. Branch labels remain visible beside colored paths.

### Disclosures
FAQ and release notes use native `details` and `summary` with thin separators, inline SVG chevrons and visible keyboard focus. The chevron rotates when open. FAQ hover shifts to cobalt; release notes use lime against their cobalt ground. A release anchor opens the disclosure before navigating to it.

## Do's and Don'ts

### Do:
- **Do** keep the existing AgentRelay icon and name.
- **Do** distinguish selected, hovered and keyboard-focused controls.
- **Do** keep synthetic inspection data explicitly labeled as illustrative.
- **Do** use the shared stylesheet for both languages and allow translated text to wrap.

### Don't:
- **Don't** treat this prototype as a standing owner-approved visual identity.
- **Don't** use branch color alone to identify a track; retain its text label.
- **Don't** replace informative schematic content with decorative autoplay animation.
