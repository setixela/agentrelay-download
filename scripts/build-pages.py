#!/usr/bin/env python3
"""Generate static RU/EN pages. Release markers remain owned by the release script."""
import hashlib
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOWNLOAD = "https://github.com/setixela/agentrelay-download/releases/latest/download/AgentRelay-macOS.zip"
RELEASES = "https://github.com/setixela/agentrelay-download/releases"
META = re.compile(r"<!-- RELEASE_META_START -->.*?<!-- RELEASE_META_END -->", re.S)


def e(value):
    return html.escape(str(value), quote=True)


def arrow():
    return '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14m-6-6 6 6-6 6"/></svg>'


def download(t, small=False):
    return f'<a class="button button-primary{" button-small" if small else ""}" href="{DOWNLOAD}">{e(t["nav"][3] if small else t["download"])}{arrow()}</a>'


def definitions(items, cls="definition-list"):
    return f'<dl class="{cls}">' + "".join(f'<div><dt>{e(title)}</dt><dd>{e(body)}</dd></div>' for title, body in items) + '</dl>'


def graph(t, prefix):
    branches = ["main", "agent/ui", "agent/api"]
    hashes = ["8d4c2f1", "c2e7a91", "4b8f603"]
    buttons = "".join(
        f'<button class="commit-row" type="button" data-commit="{i}" aria-pressed="{"true" if i == 0 else "false"}" aria-controls="{prefix}-detail">'
        f'<span class="branch-ref">{branches[i]}</span><code>{hashes[i]}</code><strong>{e(title)}</strong></button>'
        for i, title in enumerate(t["commitTitles"])
    )
    snippets = [
        ("payment.status = 'pending'", "payment.status = 'confirmed'"),
        ("button.disabled = false", "button.disabled = isSubmitting"),
        ("return response", "return validate(response)"),
    ]
    details = "".join(
        f'<div data-commit-detail="{i}"{"" if i == 0 else " hidden"}><p class="commit-explanation">{e(note)}</p>'
        f'<div class="file-summary"><span>{e(t["files"][0])}</span><code>{["src/api.ts · src/checkout.tsx", "src/checkout.tsx", "src/api.ts"][i]}</code></div>'
        f'<pre class="diff"><code><span class="diff-remove">- {e(snippets[i][0])}</span>\n<span class="diff-add">+ {e(snippets[i][1])}</span></code></pre></div>'
        for i, note in enumerate(t["commitNotes"])
    )
    return f'''<div class="git-example" data-git-example>
      <div class="graph-hint">{e(t["commitHint"])}</div>
      <div class="graph-list">
        <svg class="branch-lines" viewBox="0 0 86 232" preserveAspectRatio="none" aria-hidden="true">
          <path class="track-main" d="M18 18V214"/>
          <path class="track-ui" d="M18 214C18 186 47 194 47 166V74C47 44 18 50 18 18"/>
          <path class="track-api" d="M18 214C18 180 76 190 76 154V130C76 68 18 88 18 18"/>
          <circle class="node-main" cx="18" cy="18" r="5"/><circle class="node-ui" cx="47" cy="74" r="5"/>
          <circle class="node-api" cx="76" cy="130" r="5"/><circle class="node-base" cx="18" cy="214" r="5"/>
        </svg>
        {buttons}<div class="commit-origin"><code>main</code><span>Initial checkout</span><code>a7d301e</code></div>
      </div>
      <div class="commit-detail" id="{prefix}-detail" aria-live="polite">{details}</div>
    </div>'''


def release_notes(t, release, notes=None):
    match = re.search(r"(?:Версия|Version)\s+([^ ]+)", release)
    if not match:
        raise ValueError("Cannot determine the version from release metadata")
    version = match[1]
    if notes is None:
        notes = json.loads((ROOT / "content/release-notes.json").read_text())
    if notes["tag"] != f"v{version}":
        raise ValueError("Release notes and metadata versions differ; refresh release notes before building.")
    translation = t.get("releaseNotes", {})
    translated = translation.get("tag") == notes["tag"]
    items = translation["items"] if translated else notes["changes"]
    ru = t["lang"] == "ru"
    title = "Что нового" if ru else "What’s new"
    original = '<p class="notes-language">Оригинальные заметки релиза · English</p>' if ru and not translated else ""
    changes = "".join(f"<li>{e(item)}</li>" for item in items)
    return f'<details class="release-notes" id="release-notes"><summary>{title} · {e(version)}<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg></summary><div class="release-notes-body">{original}<ul>{changes}</ul><a href="{e(notes["url"])}">{e(t["releases"])}{arrow()}</a></div></details>'


def render(t, release, prefix, notes=None):
    lang = t["lang"]
    other = "en" if lang == "ru" else "ru"
    version = re.search(r"(?:Версия|Version)\s+([^ ]+)", release).group(1)
    whats_new = ("Что нового в " if lang == "ru" else "What’s new in ") + version
    hashes = {name: hashlib.sha1((ROOT / name).read_bytes()).hexdigest()[:8] for name in ["styles.css", "site.js"]}
    nav = "".join(f'<a href="#{target}">{e(label)}</a>' for target, label in zip(["workflow", "capabilities", "faq"], t["nav"][:3]))
    steps = "".join(f'<li><span class="step-number">{i+1}</span><h3>{e(title)}</h3><p>{e(body)}</p></li>' for i, (title, body) in enumerate(t["steps"]))
    agents = "".join(f'<div class="agent-strip-item agent-{i}"><span class="agent-dot" aria-hidden="true"></span><strong>{e(agent)}</strong><span class="status">{["Done", "Done", "Working"][i]}</span></div>' for i, agent in enumerate(t["agents"]))
    switches = "".join(f'<button type="button" data-view="{view}" aria-pressed="{"true" if i == 0 else "false"}" aria-controls="workflow-{view}">{e(label)}</button>' for i, (view, label) in enumerate(zip(["branches", "activity", "editor"], t["views"])))
    timeline = "".join(f'<div class="timeline-row"><span>{agent}</span><div class="timeline-track" aria-label="{e(t["timelineKey"][0])}"><i class="interval interval-{i}"></i></div><span class="status">{["Done", "Idle", "Working"][i]}</span></div>' for i, agent in enumerate(["Codex", "Claude Code", "Copilot"]))
    canvas = "".join(f'<div class="canvas-window canvas-window-{i}"><div class="canvas-window-title">{e(title)}</div><code>{["agent/api", "agent/ui", "npm run test", "src/checkout.tsx"][i]}</code><p>{e(t["canvasTexts"][i])}</p></div>' for i, title in enumerate(t["canvasNames"]))
    faq = "".join(f'<details><summary>{e(q)}<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg></summary><p>{e(a)}</p></details>' for q, a in t["faq"])
    install = "".join(f'<li><h3>{e(title)}</h3><p>{e(body)}</p></li>' for title, body in t["installSteps"])
    tools = "".join(f'<div><code>{tool}</code><span>{e(label)}</span></div>' for tool, label in t["mcpTools"])
    return f'''<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#203fc9">
  <title>{e(t["title"])}</title>
  <meta name="description" content="{e(t["description"])}">
  <meta property="og:title" content="{e(t["title"])}">
  <meta property="og:description" content="{e(t["description"])}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://setixela.github.io/agentrelay-download/{'en/' if lang == 'en' else ''}">
  <meta property="og:image" content="https://setixela.github.io/agentrelay-download/app-icon-256.png">
  <meta name="twitter:card" content="summary">
  <link rel="canonical" href="https://setixela.github.io/agentrelay-download/{'en/' if lang == 'en' else ''}">
  <link rel="alternate" hreflang="ru" href="https://setixela.github.io/agentrelay-download/">
  <link rel="alternate" hreflang="en" href="https://setixela.github.io/agentrelay-download/en/">
  <link rel="icon" type="image/png" href="{prefix}app-icon-64.png">
  <link rel="apple-touch-icon" href="{prefix}app-icon-256.png">
  <link rel="preload" href="{prefix}fonts/geologica-{'cyrillic' if lang == 'ru' else 'latin'}.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="{prefix}styles.css?v={hashes["styles.css"]}">
  <script src="{prefix}site.js?v={hashes["site.js"]}" defer></script>
</head>
<body id="top">
<a class="skip-link" href="#main">{e(t["skip"])}</a>
<div class="hero-band">
  <header class="site-header wrap">
    <a class="brand" href="#top" aria-label="{e(t["top"])}"><img src="{prefix}app-icon-64.png" width="36" height="36" alt=""><span>AgentRelay</span></a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="main-nav">{e(t["menu"])}<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
    <nav id="main-nav" aria-label="{e(t["navLabel"])}">{nav}<div class="language-switch" aria-label="{e(t["language"])}"><span aria-current="page">{lang.upper()}</span><a data-language href="{t["otherPath"]}" lang="{other}" hreflang="{other}">{t["otherLang"]}</a></div>{download(t, True)}</nav>
  </header>
</div>
<main id="main">
  <section class="hero-band" aria-labelledby="hero-title"><div class="hero wrap">
    <div class="hero-copy">
      <h1 id="hero-title">{e(t["headline"][0])}<span>{e(t["headline"][1])}</span></h1>
      <p class="hero-promise">{e(t["promise"][0])}<br>{e(t["promise"][1])}</p>
      <p class="hero-lead">{e(t["lead"])}</p>
      <div class="hero-actions">{download(t)}<a class="text-link" href="#workflow">{e(t["explore"])}</a></div>
      <p class="platform">{e(t["platform"])}</p><p class="hero-fine">{e(t["free"])}</p>
      <a class="hero-release" data-open-notes href="#release-notes">{e(whats_new)}{arrow()}</a>
    </div>
    <figure class="hero-diagram">
      <div class="diagram-heading"><span>{e(t["demoProject"])}</span><span>Git</span></div>
      <h2>{e(t["demoTitle"])}</h2>
      <div class="agent-strip">{agents}</div>
      {graph(t, "hero")}
      <figcaption>{e(t["demoLabel"])}</figcaption>
    </figure>
  </div></section>
  <section class="providers wrap" aria-labelledby="provider-title">
    <div><h2 id="provider-title">{e(t["providerLead"])}</h2><p>{e(t["providerNote"])}</p></div>
    <ul aria-label="CLI"><li>Codex</li><li>Claude Code</li><li>GitHub Copilot CLI</li><li>Hermes</li><li>Pi</li><li>Custom CLI</li></ul>
  </section>
  <section class="section wrap flow" id="workflow" aria-labelledby="flow-title">
    <div class="section-heading"><h2 id="flow-title">{e(t["flowTitle"])}</h2><p>{e(t["flowLead"])}</p></div>
    <ol class="flow-steps">{steps}</ol>
  </section>
  <section class="observation section" id="capabilities" aria-labelledby="observe-title"><div class="wrap">
    <div class="section-heading"><h2 id="observe-title">{e(t["observeTitle"])}</h2><p>{e(t["observeLead"])}</p></div>
    <div class="view-switch" role="group" aria-label="{e(t["viewLabel"])}">{switches}</div>
    <noscript><p>{e(t["jsNote"])}</p></noscript>
    <div class="workflow-panel" id="workflow-branches" data-panel="branches">
      <div class="panel-copy"><h3>{e(t["branchTitle"])}</h3><p>{e(t["branchText"])}</p><p class="note">{e(t["branchNote"])}</p></div>
      <figure class="inspection-surface">{graph(t, "feature")}<figcaption>{e(t["previewLabel"])}</figcaption></figure>
    </div>
    <div class="workflow-panel" id="workflow-activity" data-panel="activity">
      <div class="panel-copy"><h3>{e(t["activityTitle"])}</h3><p>{e(t["activityText"])}</p><p class="note">{e(t["activityNote"])}</p></div>
      <figure class="inspection-surface timeline"><h4>{e(t["timeline"])}</h4><div class="time-axis"><span>10:00</span><span>10:30</span><span>11:00</span></div>{timeline}<div class="timeline-key"><span><i></i>{e(t["timelineKey"][0])}</span><span><i></i>{e(t["timelineKey"][1])}</span></div><figcaption>{e(t["previewLabel"])}</figcaption></figure>
    </div>
    <div class="workflow-panel" id="workflow-editor" data-panel="editor">
      <div class="panel-copy"><h3>{e(t["editorTitle"])}</h3><p>{e(t["editorText"])}</p><p class="note">{e(t["editorNote"])}</p></div>
      <figure class="inspection-surface editor-example"><div class="editor-path"><code>src/checkout.tsx</code><span>UTF-8</span></div><pre><code><span class="line-number">41</span> <span class="code-keyword">const</span> submit = <span class="code-keyword">async</span> () =&gt; {{
<span class="line-number">42</span>   setSubmitting(<span class="code-keyword">true</span>);
<span class="line-number">43</span>   <span class="code-keyword">try</span> {{
<span class="line-number">44</span>     <span class="code-keyword">await</span> createPayment();
<span class="line-number">45</span>   }} <span class="code-keyword">finally</span> {{
<span class="line-number">46</span>     setSubmitting(<span class="code-keyword">false</span>);
<span class="line-number">47</span>   }}
<span class="line-number">48</span> }};</code></pre><div class="editor-diff"><span>{e(t["files"][2])}</span><code><span class="diff-remove">- disabled={{false}}</span><span class="diff-add">+ disabled={{isSubmitting}}</span></code></div><figcaption>{e(t["previewLabel"])}</figcaption></figure>
    </div>
  </div></section>
  <section class="section wrap workspace" aria-labelledby="workspace-title">
    <div class="workspace-intro"><h2 id="workspace-title">{e(t["workspaceTitle"])}</h2><p>{e(t["workspaceLead"])}</p>{definitions(t["workspaceFeatures"])}</div>
    <figure class="canvas-example"><div class="canvas-top"><span>AgentRelay</span><code>checkout</code></div><div class="canvas-windows">{canvas}</div><div class="composer-example"><span>Message</span><code>Codex · Claude Code</code></div><figcaption>{e(t["canvasLabel"])}</figcaption></figure>
  </section>
  <section class="persistence section" aria-labelledby="persist-title"><div class="wrap persistence-layout">
    <div><h2 id="persist-title">{e(t["persistTitle"])}</h2><p>{e(t["persistText"])}</p><p class="note">{e(t["persistNote"])}</p></div>
    <div class="persistence-diagram"><div>{e(t["persistDiagram"][0])}</div><div class="process-line"><code>tmux</code><strong>{e(t["persistDiagram"][1])}</strong></div><div>{e(t["persistDiagram"][2])}</div></div>
  </div></section>
  <section class="section wrap mcp" aria-labelledby="mcp-title"><div><h2 id="mcp-title">{e(t["mcpTitle"])}</h2><p>{e(t["mcpText"])}</p><p class="note">{e(t["mcpNote"])}</p></div><div class="mcp-tools">{tools}</div></section>
  <section class="section wrap everyday" aria-labelledby="details-title"><h2 id="details-title">{e(t["detailsTitle"])}</h2>{definitions(t["details"], "detail-grid")}</section>
  <section class="section wrap faq" id="faq" aria-labelledby="faq-title"><h2 id="faq-title">{e(t["faqTitle"])}</h2><div class="faq-items">{faq}</div></section>
  <section class="install section" id="install" aria-labelledby="install-title"><div class="wrap">
    <div class="install-layout"><div><h2 id="install-title">{e(t["installTitle"]).replace(chr(10), "<br>")}</h2><p>{e(t["installLead"])}</p>{download(t)}<p class="platform">{e(t["platform"])}</p></div><ol class="install-steps">{install}</ol></div>
    <div class="release-info">{release}<a href="{RELEASES}/latest">{e(t["releases"])}{arrow()}</a></div>
    {release_notes(t, release, notes)}
  </div></section>
</main>
<footer class="site-footer wrap"><div><a class="brand" href="#top">AgentRelay</a><p>{e(t["footer"])}</p></div><div class="footer-links"><a href="{RELEASES}">{e(t["allReleases"])}</a><a data-language href="{t["otherPath"]}" lang="{other}">{t["otherLang"]}</a><a href="#top">{e(t["backTop"])}{arrow()}</a></div><span class="copyright">© 2026 AgentRelay</span></footer>
</body>
</html>
'''


def main():
    pending = []
    for path, lang, prefix in [(ROOT / "index.html", "ru", "./"), (ROOT / "en/index.html", "en", "../")]:
        t = json.loads((ROOT / f"content/{lang}.json").read_text())
        blocks = META.findall(path.read_text())
        if len(blocks) != 1:
            raise ValueError(f"Expected exactly one release metadata block in {path}")
        pending.append((path, render(t, blocks[0], prefix)))
    for path, source in pending:
        path.write_text(source)
    print("Built RU and EN pages; preserved release metadata and refreshed asset hashes.")


if __name__ == "__main__":
    main()
