<p align="center">
  <img src="https://raw.githubusercontent.com/sorawit-w/agent-skills/main/assets/screenwright-li.svg" alt="screenwright — paint a screen, then actually look at it" width="100%"/>
</p>

# screenwright

**🚧 BETA.** Paints one self-contained HTML surface to a brand spec, then *sees* it —
renders, screenshots, runs an accessibility audit, and fixes in a loop until it passes —
before handing the verified result back to you to build for real.

## Why this exists

Agents are bad at frontend in a specific way: the markup usually looks *structurally*
right, but the render misses the small obvious things — a 4px misalignment, a missing focus
ring, text that overflows on a long name, a mobile layout that never got built. That's a
**seeing** failure: the agent reasons from structure + CSS without ever looking at the
pixels.

Generating UI is solved. **Verifying the render against a brand + accessibility bar, in a
loop, is not.** That loop is screenwright's wedge.

## What it does

- **Paints one surface** — a page, mobile screen, or component — as a single self-contained
  HTML file (inline styles + SVG, no external requests), portable to any stack.
- **Sees it** via the Playwright MCP: renders, runs an **axe-core** WCAG audit, screenshots
  for a fidelity critique, then **fixes and re-checks in a bounded loop**.
- **Two stacked gates:** axe a11y always blocks; visual fidelity blocks only when you gave
  it a reference image to match.
- **Generates what's implied:** desktop-only mock → it builds the mobile layout too; adds
  empty/loading/error and focus/hover states the surface needs.
- **Resolves brand** from a `DESIGN.md`, or bootstraps one — from your repo's styles, a
  ready-made template, or a described vibe.
- **Hands off honestly** — inline HTML when you're in a project (repo stays clean), a real
  file when you're not, always with a manifest of what was verified vs not.

## What it doesn't do

- **No multi-page flows, routing, or app builds** — one surface, then handoff.
- **No framework conversion** — it outputs portable HTML; you (or the host agent) port it
  to React/Vue/etc.
- **No motion systems, performance audits, or copywriting** — out of scope by design.
- **No runtime** — it drives your Playwright MCP; it ships no server of its own.

## When to use it

- "Build this screen / paint this component" and you want the render actually checked.
- "Match this mockup" — you have a target image and want fidelity verified.
- "Fix this UI / the layout looks off" — you have code or a screenshot of something wrong.
- "Make this accessible" — you want an axe-backed pass, not a vibe.

## When not to use it

- You want a **brand identity** (logo, tagline, full system) → `brand-workshop`.
- You want **copy / microcopy** → `ghostwriter`.
- You want **pixel art or illustration** → `pixel-art`.
- You want a **whole app or multi-page flow** — screenwright does one surface at a time.

## How it works

1. **Capability gate** — needs the Playwright MCP; missing → it stops and tells you how to
   install it (it won't paint blind).
2. **Intake** — classifies the mode (match a mockup / fix from image / fix from code /
   bootstrap), asks only what it can't infer.
3. **Resolve brand** — the `DESIGN.md` ladder (exists → infer from repo → template / vibe),
   persisting one when it bootstraps.
4. **Paint** — one author writes the whole self-contained file.
5. **Verify in a sub-agent** — render → axe → screenshot → judge, looped (~3 cycles) until
   the gates pass.
6. **Handoff** — inline or file, plus the verification manifest.

## Design choices worth knowing

- **The eyes are the mechanism; a11y/states/responsive are the targets.** axe is the
  always-on machine gate; the screenshot critique catches what axe can't (the visual
  misses). Both, not either.
- **Verification is asymmetric.** A reference image anchors fidelity for the viewport it
  shows; everything screenwright *implies* (the other viewport, states) is verified by the
  gate + checklist, not pixel-diffed against nothing.
- **One author, not parallel-by-aspect.** a11y, layout, and interactions are cross-cutting
  concerns over the same markup — splitting them across agents just makes merge conflicts.
- **`page.setContent()`, not `file://`.** The Playwright MCP blocks the file protocol;
  screenwright renders by setting content directly and injects axe from a temp file.
- **It bootstraps DESIGN.md, it doesn't depend on brand-workshop.** Same format, lighter
  path, with two added keys (`a11y`, `breakpoints`) that default cleanly when absent.

## Install

```
/plugin marketplace add sorawit-w/agent-skills
/plugin install agent-skills@sorawit-w
```

Then invoke with `/agent-skills:screenwright` or natural language ("paint this screen and
check it"). Requires the Playwright MCP for rendering.

## Cross-skill integration

| Skill | Relationship |
|---|---|
| **Playwright MCP** | Hard dependency — the render/audit/screenshot engine. |
| `brand-workshop` | Authors a full `DESIGN.md` greenfield; screenwright reads it or bootstraps a lighter one. |
| `ui-ux-pro-max` *(if installed)* | Style/palette/font vocabulary for the imply-from-vibe brand rung. |
| `taste-skill` *(if installed)* | Paint-time anti-slop visual dials (motion clamped — breaks self-containment). |
| [`impeccable`](https://github.com/pbakaus/impeccable) *(if available)* | Verification companion — a deterministic design-quality linter that backstops the advisory visual checks. Complements axe (design-quality vs accessibility); findings stay advisory. |
| `sub-agent-coordinator` | Briefing conventions for the isolated verify-loop sub-agent. |
| `ghostwriter` | Owns the words; screenwright paints the surface. |
| `coding-rules` | When running mid-build in a guard-railed repo, defer to its loop discipline. |

## Status and scope

**🚧 BETA.** New, and the verification loop is freshly proven against the Playwright MCP but
not yet battle-tested across many real screens. Supported: single self-contained surfaces
(page / mobile screen / component), the four intake modes, the two-gate verification loop,
and DESIGN.md bootstrap. Not supported: multi-page flows, framework conversion, motion
systems. Expect the gate thresholds and gap-questions to tune as it's dogfooded.

## Contributions

Not accepting external contributions right now.

## License

MIT
