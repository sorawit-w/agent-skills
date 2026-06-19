---
name: screenwright
description: >
  Paints one self-contained HTML surface (page, mobile screen, or component) to a brand
  spec, then SEES it: renders via the Playwright MCP, screenshots, runs an axe-core
  accessibility audit, critiques fidelity, and fixes in a bounded loop until it passes —
  then hands the verified HTML back for conversion to a real stack. Triggers when the user
  or an agent mid-build wants a UI surface built or fixed with the render actually checked:
  "build this screen", "paint a component", "match this mockup", "fix this UI", "make this
  accessible", "the layout looks off", "screenwright this". Resolves brand from a DESIGN.md,
  or bootstraps one from the repo / a template / a described vibe. Does NOT trigger for:
  multi-page flows, routing, or full app builds; framework/stack conversion (it outputs
  portable HTML for the host to port); pure copywriting (use ghostwriter); brand-identity
  or logo work (use brand-workshop); pixel-art or illustration (use pixel-art); backend,
  data, or non-UI code.
tags:
  - frontend
  - ui-ux
  - accessibility
  - verification
  - html
metadata:
  tier: draft
---

# screenwright

> **The wedge is the eyes.** Generating UI is solved; *verifying the render against a
> brand + accessibility bar, in a loop* is not. screenwright paints one self-contained
> HTML surface, then renders → screenshots → audits → fixes until it passes, and hands the
> result back. It does the painting and verification; it does **not** ship a runtime or
> convert to a framework — that's the host's job.

Agents write frontend blind: the markup looks right but misses the small obvious things —
a 4px misalignment, a missing focus ring, text that overflows on a long name, a mobile
layout that never got built. screenwright gives the agent eyes.

**Two stacked gates, asymmetric:**
- **axe a11y** — machine, deterministic, **always blocks**. The defensible core.
- **Visual fidelity** — judgment from the screenshot. **Blocks only when a reference image
  exists**; advisory otherwise (no reference = no ground truth to gate on).

---

## Phase 0 — Capability gate (run first)

screenwright renders through the **Playwright MCP**. It is a **hard dependency** — gate on
its presence, not on which agent you are (capability-gated, not vendor-gated).

- If Playwright MCP tools (`browser_navigate`, `browser_run_code_unsafe`,
  `browser_take_screenshot`) are **not** available → **stop**. Tell the user screenwright
  needs the Playwright MCP, give install instructions
  (`claude mcp add playwright npx '@playwright/mcp@latest'` or the host's equivalent), and
  do not attempt a degraded render. A skill that paints without seeing is the problem it
  exists to solve.
- If available → proceed.

Then confirm this is a screenwright job (a UI **surface** to build/fix with the render
checked), not one of the anti-triggers in the frontmatter. When in doubt, one question.

---

## Phase 1 — Intake

Classify the **mode** from what the user gave you, gather the brief, ask only what you
can't infer. Full classifier + the gap-question set: [references/intake.md](references/intake.md).

| Mode | Input | Output |
|---|---|---|
| **A1 match** | target mockup image + brief | HTML built to match; fidelity diffed against the image |
| **A2 fix-from-image** | screenshot of current (wrong) state + brief | HTML fixed toward the brief/DESIGN.md |
| **B fix-from-code** | existing UI code + change brief | updated HTML **+ a plain-language change description** + before/after check |
| **C bootstrap** | no DESIGN.md present | resolve brand (Phase 2), then run as A or B |

**Match-vs-fix is load-bearing** (it flips the verification path). If an image is provided
but intent is ambiguous, **ask exactly one question**. Default lean: a polished mock →
match; a rough/broken render described with problems → fix.

**Unit of work = one surface**: a page, a mobile screen, or a component. Not a flow, not an
app. Batch your gap-questions, default aggressively, let the user correct the draft — never
interrogate.

---

## Phase 2 — Resolve brand (the ladder)

Stop at the first rung that hits. Full heuristics + fetch details:
[references/brand-ladder.md](references/brand-ladder.md). Schema:
[references/design-md-schema.md](references/design-md-schema.md).

1. **`DESIGN.md` exists** → use it.
2. **In a project, no DESIGN.md** → infer tokens from the repo's styles → **persist a
   `DESIGN.md`** so later surfaces stay consistent.
3. **Greenfield / outside a project** → either **a named template** (fetch one from
   `github.com/VoltAgent/awesome-design-md`, 73 ready-made DESIGN.md files) **or imply from
   the user's described vibe** (via `ui-ux-pro-max`'s style vocabulary if installed, else
   judgment) → **persist a `DESIGN.md`**.

screenwright is both a *consumer* and a *bootstrapper* of DESIGN.md — same Google Labs
`design.md` format either way, extended with two custom keys (`a11y`, `breakpoints`) that
screenwright defaults when absent. If a fetch fails or you're offline, fall back to
imply-from-description — **the ladder never dead-ends**.

---

## Phase 3 — Paint

**One author writes the whole file.** Do not split generation across sub-agents by aspect
(a11y, layout, interactions) — they're cross-cutting concerns over the same markup, and
splitting them guarantees merge conflicts and an internally-inconsistent file.

Output contract — **one self-contained HTML file**:
- Inline `<style>`, inline SVG, no external requests (no CDN, no web fonts, no `<script
  src>`). It must render offline and port cleanly to any stack.
- Semantic HTML with the a11y target woven in (aria, labels, focus order) — not bolted on.
- **Generate what the brief implies, don't wait for it:** if the mock is desktop-only,
  build the **mobile** layout too (and vice-versa); add the **states** the surface needs
  (empty / loading / error) and **interaction end-states** (focus / hover / active /
  disabled). Implied surfaces are verified later but never silently dropped.

**Anti-slop (capability-gated):** if `taste-skill` is installed, apply its **visual** dials
(`DESIGN_VARIANCE`, `VISUAL_DENSITY`) to push away from generic AI defaults. **Clamp
`MOTION_INTENSITY` low / ignore its GSAP skeletons** — motion is out of screenwright's
gate and its libraries break self-containment. If not installed, suggest it and proceed on
judgment; do not synthesize the dials.

---

## Phase 4 — Verify (in a sub-agent)

Run the render→audit→screenshot→fix **loop inside one sub-agent** — it's verbose
(screenshots, axe dumps, iterations) and you want it out of the main thread. The sub-agent
returns the final HTML (or a path) + the manifest, nothing else. Briefing conventions and
the no-nested-sub-agents invariant live in `sub-agent-coordinator`. Exact Playwright calls
and the axe-injection mechanic: [references/playwright-loop.md](references/playwright-loop.md).
Gate definitions, the 8 dimensions, axe rulesets per surface type:
[references/verification.md](references/verification.md).

Per cycle, for each in-scope viewport and state:
1. **Render** — `page.setContent(html)` (the MCP blocks `file://`; do not use it).
2. **Audit** — inject axe-core (`addScriptTag({path})`), run with the WCAG tags from
   `a11y.wcag`. Collect violations by impact.
3. **Screenshot** — capture for the fidelity critique.
4. **Judge** against the two gates over the quality set.

After the in-scope viewports pass, run one **reflow pass at 320 CSS-px** (WCAG 1.4.10, BLOCK):
a horizontal scrollbar there = clipped content. Snippet + the optional text-spacing (1.4.12)
override: [references/playwright-loop.md](references/playwright-loop.md).

---

## Phase 5 — Loop (bounded)

- **Fix blocking violations**, re-render, re-audit. **Cap at ~3 cycles.**
- If a cycle doesn't reduce the blocking count, **cheapen the loop** before grinding:
  re-read the brief, attack the single highest-impact violation in isolation, don't
  re-paint the whole surface.
- After the cap, if blockers remain, **stop and report honestly** in the manifest — do not
  claim a pass you didn't reach.

---

## Phase 6 — Handoff

Render needs only a **transient** target (the `setContent` call) — **no durable file is
required.** Decide delivery by **project-context** (not by guessing agent-vs-user, which
you can't detect). Details: [references/handoff.md](references/handoff.md).

- **In a project** → deliver the final HTML **inline** so the host agent can port it;
  write a temp file and hand the **path** instead only if the artifact is large. Leave the
  repo clean.
- **Non-project / interactive user** → write a **durable named `.html`** and return the
  path. The file is the deliverable.

Always attach the **verification manifest**: what was checked hard (axe pass per
viewport/state), what was checked soft (fidelity vs a reference, if any), and what is
**unverified** (derived viewports, advisory dimensions, a11y if axe couldn't run). Honesty
about confidence is the point.

---

## The quality set — tight gate

screenwright owns a quality dimension only if **(1) the eyes can verify it by screenshot
AND (2) it survives the handoff to a real stack.** That filter answers every "should we
check X?" — motion fails (2); performance / Core Web Vitals / Lighthouse-perf / flows / copy
fail entirely (they need a *running app at a URL* screenwright doesn't have — see "What this
skill is NOT").

| Dimension | Tier |
|---|---|
| **axe a11y** | **BLOCK** — always, machine, per viewport + state (incl. `target-size` 2.5.8 — explicitly enabled; axe ships it off) |
| **Required states** (empty/loading/error the surface needs) | **BLOCK** |
| **Responsive** (both in-scope viewports present & sane) | **BLOCK** |
| **Reflow @ 320px** (WCAG 1.4.10 — no horizontal scroll) | **BLOCK** |
| **Token consistency** (rendered values match DESIGN.md) | **BLOCK** |
| **Focus visibility** (visible focus indicator) | **BLOCK** |
| Visual hierarchy (primary action is most salient) | advisory |
| Alignment & spacing rhythm (on the scale, edges align) | advisory |
| Real-content robustness (long names, empty, huge numbers, missing images) | advisory |
| Text spacing (WCAG 1.4.12 — survives the spacing override) | advisory |
| Render-variants (dark-mode / reduced-motion / RTL) | advisory — **only when declared** |
| Interaction end-states (hover/active/disabled distinct) | advisory |
| Motion / animation | advisory — **always** |

Advisory dimensions inform fixes and appear in the manifest; they never block the loop.
Visual fidelity vs a **reference image** blocks only in mode A1, for the viewport the
reference actually shows.

---

## What this skill is NOT

- **Not a multi-page / app builder** — one surface, then handoff. No routing, no flows.
- **Not a framework converter** — outputs portable HTML; the host ports it to React/Vue/etc.
- **Not a motion/animation system, performance auditor, or copywriter** — out of scope by
  the verify-and-survive filter. Copy → `ghostwriter`; brand identity → `brand-workshop`;
  illustration → `pixel-art`.
- **Not a runtime / Core Web Vitals / Lighthouse-perf / SEO auditor** — those need a *running
  app at a real URL* (TTFB, network waterfall, async loading, INP); screenwright renders
  self-contained HTML via `setContent`, so those numbers would be fiction. Run
  [`web-quality-skills`](https://github.com/addyosmani/web-quality-skills) against the served
  build instead. Lighthouse's a11y category *is* axe (already our gate). **AMP** is deprecated
  and conflicts with self-contained output — not supported.
- **Not a runtime** — it drives the host's Playwright MCP; it ships no server.

---

## Cross-skill integration

| Skill | Relationship |
|---|---|
| **Playwright MCP** | Hard dependency — the render/audit/screenshot engine. Missing → stop (Phase 0). |
| `brand-workshop` | Authors a thorough `DESIGN.md` greenfield (interview-driven). screenwright reads it, or bootstraps a lighter one when absent — same format. Prefer brand-workshop when the user wants a full brand identity first. |
| [`ui-ux-pro-max`](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) *(if installed)* | Style/palette/font vocabulary for the imply-from-vibe rung of the brand ladder. Suggest install if absent and the user wants a vibe-bootstrapped brand; do not synthesize its catalog. |
| [`taste-skill`](https://github.com/Leonxlnx/taste-skill) *(if installed)* | Paint-time anti-slop **visual** dials (variance, density). Motion dial clamped — its GSAP output breaks self-containment. Capability-gated; suggest if absent, don't synthesize. |
| [`impeccable`](https://github.com/pbakaus/impeccable) *(if available)* | **Verification** companion, not a style source: a deterministic design-quality linter for the *advisory* visual dimensions (spacing rhythm, hierarchy, AI-slop). Complements axe (design-quality vs WCAG — disjoint), stays advisory, suppress its font-pairing + performance rules (they fight self-containment / de-scoped perf). See [references/verification.md](references/verification.md). |
| `sub-agent-coordinator` | Briefing conventions for the isolated verify-loop sub-agent + the no-nested-sub-agents invariant. |
| `ghostwriter` | Owns copy/microcopy. screenwright paints the surface; it does not write the words. |
| [`web-quality-skills`](https://github.com/addyosmani/web-quality-skills) *(if installed)* | **Runtime layer handoff** — the home for everything screenwright's static gate can't measure: Lighthouse, Core Web Vitals (LCP/INP/CLS), performance, SEO, best-practices, run against the *served* build. screenwright verifies the surface pre-handoff; this verifies the running app. The manifest points users here for perf. Do not synthesize Lighthouse-grade audits inline — it tracks Lighthouse v13+ migrations we wouldn't keep current. |
| [`cerby`](https://github.com/sorawit-w/cerby) *(if installed)* | When screenwright runs mid-build inside a guard-railed repo, defer to its loop/validation discipline for the surrounding work. |

---

## Slash invocation

`/agent-skills:screenwright` (or natural language matching the triggers). Optional argument:
a mode hint or a path/URL to a mockup or code file. With no argument, screenwright asks the
one or two intake questions it can't infer, then proceeds.
