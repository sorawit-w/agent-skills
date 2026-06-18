# Verification — two gates, 8 dimensions, axe rulesets, the manifest

Loaded in Phase 4. The mechanics of driving Playwright + injecting axe are in
[playwright-loop.md](playwright-loop.md); this file defines **what "pass" means.**

## The scope filter (governs every "should we check X?")

screenwright owns a quality dimension only if **(1)** the eyes can verify it by screenshot
**AND (2)** it survives the handoff to a real stack. Motion fails (2). Performance, flows,
copy, and information architecture fail entirely → out of scope, not advisory.

**Runtime metrics stay out — and have a home.** Performance, **Core Web Vitals** (LCP / INP /
CLS), **Lighthouse**-perf/SEO/best-practices, and SaaS speed tests (**SpeedVitals**) all need a
*running app at a real URL* with a real network. screenwright renders self-contained HTML via
`setContent` — offline, no waterfall, no async loading — so those numbers would be **fiction**
here (CLS is ~0 by construction; LCP/INP have no real load to measure). Hand them to
[`web-quality-skills`](https://github.com/addyosmani/web-quality-skills) run against the served
build. Note Lighthouse's *a11y* category **is axe-core** — already our blocking gate, so adding
it is pure redundancy. **AMP** is deprecated (lost its ranking/Top-Stories preference in 2021)
and its restricted-HTML format conflicts with self-contained output — not supported.

## Two stacked gates (asymmetric)

- **Gate A — axe a11y.** Machine, deterministic, **always blocks**. Runs per in-scope
  viewport and per state.
- **Gate B — visual fidelity.** Judgment from the screenshot. **Blocks only in mode A1**,
  and only for the viewport the **reference image** actually shows. Everywhere else
  (derived viewports, A2/B/C, text-only briefs) it's **advisory** — there's no ground truth
  to gate on, and judgment-as-gate rationalizes "good enough" or loops forever.

## The quality set — tight gate

| Dimension | Tier | How the eyes check it |
|---|---|---|
| **axe a11y** | **BLOCK** | inject axe, run with `a11y.wcag` tags, per viewport + state (incl. `target-size`, WCAG 2.5.8 — but only when **explicitly enabled**; see ruleset note) |
| **Required states** | **BLOCK** | render empty/loading/error the surface needs; each present & sane |
| **Responsive** | **BLOCK** | both in-scope viewports render without overflow/reflow breakage |
| **Reflow @ 320px** (WCAG 1.4.10) | **BLOCK** | re-render at 320 CSS-px width; no horizontal scroll, no clipped or overlapping content |
| **Token consistency** | **BLOCK** | rendered colors/radii/type match DESIGN.md; no rogue values |
| **Focus visibility** | **BLOCK** | tab/focus a control → visible focus indicator in the screenshot |
| Visual hierarchy | advisory | the single primary action is the most salient element |
| Alignment & spacing rhythm | advisory | gaps sit on the `spacing` scale; edges align |
| Real-content robustness | advisory | long names / empty / huge numbers / missing images don't break layout |
| Text spacing (WCAG 1.4.12) | advisory | inject the spacing override; text doesn't clip or overlap |
| Render-variants (dark-mode / reduced-motion / RTL) | advisory — **only when declared** | if DESIGN.md/brief declares the variant, emulate it + screenshot; skip otherwise |
| Interaction end-states | advisory | hover / active / disabled are visibly distinct |
| Motion / animation | advisory **always** | (not screenshot-verifiable; doesn't survive handoff) |

Advisory items **inform fixes and go in the manifest**; they never block the loop. Don't
let an advisory miss burn a fix cycle unless a blocking item also needs that cycle.

## axe rulesets & severity, per surface type

**Ruleset** = the WCAG level from `a11y.wcag`. `"2.2-AA"` → `runOnly` tags
`['wcag2a','wcag2aa','wcag21aa','wcag22aa']`.

**`target-size` (WCAG 2.5.8) must be enabled explicitly.** axe-core ships it `enabled:false`,
so the `wcag22aa` tag alone does **not** run it — pass `rules: { 'target-size': { enabled: true } }`
(see [playwright-loop.md](playwright-loop.md)). Without that, do not claim tap-target coverage in
the manifest.

**Blocking severity:** axe `impact` of **`critical` or `serious` blocks**; `moderate` and
`minor` are advisory (manifest only).

**Surface-aware rules.** A component/fragment is not a full page, so page-structure rules
false-positive on it. Run the full ruleset for a **page**; for a **component/fragment**,
disable these page-level rules:

```
region, landmark-one-main, page-has-heading-one, document-title, html-has-lang, bypass
```

(Disable via axe's `rules: { <id>: { enabled: false } }` option, not by ignoring output.)

## Token-consistency check (mechanism)

Token consistency is a BLOCK dimension, so it needs a *check*, not a vibe. In the verify
sub-agent, after render, spot-check computed styles against the DESIGN.md tokens via
`page.evaluate(() => getComputedStyle(el))`:

- the primary CTA's background/color resolves to `colors.primary`,
- border-radius values sit on the `rounded` scale,
- font-family matches `typography`.

Exact-match the few **brand-load-bearing** values, not every element — a rogue hex or
radius outside the token set is the blocking signal. If a surface has no clean element to
spot-check (or the comparison is genuinely ambiguous), **record token consistency as soft in
the manifest** rather than asserting a hard pass — never claim a machine check you didn't run.

## Design-quality backstop (impeccable, if available)

The advisory visual dimensions (hierarchy, spacing rhythm, alignment, AI-slop) are otherwise
judgment from the screenshot. If [`impeccable`](https://github.com/pbakaus/impeccable) is
available (its `/impeccable` skill, its auto-firing design hook, or the deterministic CLI
`npx impeccable detect <file> --json`), run it on the painted HTML to turn that judgment into
a **deterministic check** — it has 44 rules for cramped padding, visual rhythm, line length,
font hierarchy, card nesting, and AI-slop patterns.

Rules for using it, so it complements rather than fights screenwright:

- **Complement to axe, not a replacement.** impeccable explicitly does **not** check WCAG
  contrast or comprehensive a11y — that stays axe's job (the blocking gate). impeccable owns
  *visual design-quality*; axe owns *accessibility*. Disjoint surfaces.
- **Advisory, never blocking.** Fold impeccable findings into the advisory bucket / manifest
  (consistent with the tight gate). They inform fixes; they don't gate the loop.
- **Suppress the rules that conflict with screenwright's contract** (via
  `.impeccable/config.json` ignores): **font-pairing / single-font / overused-font** —
  screenwright uses a self-contained **system-font stack** by design, so a "pair a display
  font" finding is a false positive against the no-external-requests output; and
  **performance** — screenwright de-scopes perf (the output is a throwaway proof).
- **Capability-gated.** If impeccable isn't available, skip silently — the advisory
  dimensions fall back to screenshot judgment. Do not synthesize its rule set.

## The verification manifest (always attached to the handoff)

A short, honest record of confidence — three buckets:

```
## screenwright verification
- Surface: <page | screen | component> · mode <A1|A2|B|C>
- Hard-verified (gate passed):
  - axe a11y: desktop ✓ / mobile ✓ (WCAG 2.2-AA, 0 serious+critical; incl. target-size 2.5.8)
  - reflow @ 320px ✓ · required states: empty ✓ loading ✓ error ✓
  - token consistency ✓ · focus visibility ✓
- Soft-verified (judgment):
  - fidelity vs reference: desktop ✓ (mode A1); mobile = derived, no reference
  - hierarchy / spacing / text-spacing (1.4.12) / real-content: <notes or ✓>
- NOT verified:
  - <e.g. motion (out of scope); a11y on tablet (not requested); fidelity on derived mobile>
  - runtime perf / Core Web Vitals (LCP·INP·CLS) / SEO → out of gate; run `web-quality-skills` on the served build
```

If axe could not run (offline / no `browser_run_code_unsafe`), say **"a11y UNVERIFIED"**
explicitly — never imply a pass you didn't reach.
