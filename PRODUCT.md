# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Experienced developers coordinating multiple locally installed AI CLI agents on a Mac. The owner describes the central workflow as agents writing code and committing, while the human observes activity and the branch/merge graph.

## Product Purpose

AgentRelay is a native macOS workspace combining independent AI CLI sessions, shells, an editor, Git history and optional MCP coordination on one canvas.

## Positioning

Vibe coding for senior engineers: delegate implementation to agents and retain an overview of execution and repository history. This is a workflow enabled by CLI agents, not an automatic commit or merge engine built into AgentRelay.

## Operating Context

macOS 14+, Apple Silicon and Intel. Locally installed Codex, Claude Code, GitHub Copilot CLI, Hermes, Pi and custom CLI commands. Agents can work in separate Git worktrees when configured; isolation is not automatic.

## Capabilities and Constraints

- Free public ZIP download; AI CLI installation, authorization and provider terms are separate.
- Agent tmux processes survive quitting/reopening AgentRelay; not rebooting the Mac. Ordinary shells restart fresh.
- Working/Idle/Done reflect inferred activity, not verified task completion.
- Git graph, history, diff, blame, partial staging, branches, merge/rebase, worktrees and baselines. A baseline does not establish authorship.
- Built-in file editor, shared prompt composer, activity timeline, saved layout, customizable CLI launches and terminal appearance.
- Optional local MCP with four tools and temporary project authorization. Disabled by default; not a sandbox.
- English application UI; Russian and English website.
- No invented benchmarks, testimonials, pricing tiers, automatic merging claims or cloud service claims.

## Brand Commitments

Keep AgentRelay name and existing app icon. Owner requests a slogan in the sense of “Вайбкодинг для сеньоров” and informative placeholders replacing pictures and animations. New website version is reviewable before publication.

## Evidence on Hand

Canonical product catalog in the AgentRelay source repository: docs/product-feature-catalog.md, researched 2026-10-01 at 6f59534d9024de7cc51d6c6b72bbd9a9ae466b22. Public download repo contains live release metadata for 1.1.5 build 20, self-hosted fonts and signed appcast. Illustrative scenarios must be labeled; they are not real user output.

## Product Principles

- Explain the developer's workflow before enumerating features.
- Agents implement and commit; the human keeps context and supervises integration.
- Distinguish CLI behavior from AgentRelay capabilities.
- Keep claims aligned with the canonical catalog and release metadata.
