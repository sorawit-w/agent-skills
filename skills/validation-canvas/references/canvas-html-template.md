# Validation Canvas HTML Template — Reference

The canonical self-contained HTML rendering of the **Lean Canvas + Value
Proposition Canvas** combined artifact. Read this before producing
`validation-canvas.html`.

**Contract:**
- Single file, no external dependencies (no CDN links, no webfonts unless
  base64).
- Renders the **Lean Canvas grid** (top half) and the **VPC fit diagram**
  (bottom half).
- Lean Canvas grid mirrors Maurya's canonical layout: top row split into
  Problem / Solution + Key Metrics / UVP / Unfair Advantage + Channels /
  Customer Segments; bottom row split between Cost Structure and Revenue
  Streams.
- VPC diagram shows Customer Profile (Jobs / Pains / Gains) on the right and
  Value Map (Products & Services / Pain Relievers / Gain Creators) on the
  left, with arrows or bracket lines indicating the 1:1 fit mapping.
- Prints cleanly to PDF via CSS paged media (`@page` at landscape A4 or
  Letter, with the Lean Canvas on page 1 and the VPC on page 2).
- Applies brand tokens from `<brand-root>/design-system.md` (sibling of
  canvas root) if present, falling back to legacy `brand-kit/design-system.md`
  (cwd-relative) for backward compat. Otherwise uses the neutral defaults in
  this template.
- Footer line: `Generated [YYYY-MM-DD] · validation-canvas.md is the source
  of truth.`

**How to use this template:**
1. Read `validation-canvas.md` from the resolved canvas folder
   (`<canvas-root>/validation-canvas.md`) — the canonical source of truth
   you already produced.
2. For each block, extract the bulleted claims. Preserve founder's wording.
3. Substitute the placeholders below with the actual block content as
   semantic `<ul>` lists.
4. If the brand design system exists (`<brand-root>/design-system.md`, or
   legacy `brand-kit/design-system.md` at cwd root), parse the primary,
   surface, and text colors plus the body font-family, and substitute them
   into the `:root` CSS custom properties. Otherwise keep the defaults.
5. Save as `<canvas-root>/validation-canvas.html` (default
   `docs/canvas/validation-canvas.html` solo, `docs/startup-kit/canvas/validation-canvas.html`
   orchestrated).

---

## Template

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Validation Canvas — {{business_name}}</title>
<style>
  :root {
    /* Override these from the brand design system when available
       (<brand-root>/design-system.md, or legacy brand-kit/design-system.md) */
    --canvas-bg: #fafaf7;
    --canvas-surface: #ffffff;
    --canvas-text: #1a1a1a;
    --canvas-muted: #6b6b6b;
    --canvas-border: #d9d9d3;
    --canvas-accent: #1a1a1a;
    --canvas-font-body: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    --canvas-font-heading: var(--canvas-font-body);
  }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    background: var(--canvas-bg);
    color: var(--canvas-text);
    font-family: var(--canvas-font-body);
    font-size: 13px;
    line-height: 1.45;
  }
  header {
    padding: 24px 32px 12px;
  }
  header h1 {
    margin: 0 0 4px;
    font-family: var(--canvas-font-heading);
    font-size: 22px;
    letter-spacing: -0.01em;
  }
  header .meta {
    color: var(--canvas-muted);
    font-size: 12px;
  }
  section.canvas-section { margin: 16px 32px; }
  section.canvas-section > h2.section-title {
    margin: 0 0 8px;
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 0.02em;
    color: var(--canvas-accent);
  }

  /* ---------- Lean Canvas (top) ---------- */
  .lean {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    grid-template-rows: 1fr 1fr;
    gap: 0;
    border: 1px solid var(--canvas-border);
    background: var(--canvas-surface);
  }
  .block {
    padding: 14px 16px;
    border-right: 1px solid var(--canvas-border);
    border-bottom: 1px solid var(--canvas-border);
    display: flex;
    flex-direction: column;
    min-height: 160px;
  }
  .block:last-child { border-right: none; }
  .block h3 {
    margin: 0 0 8px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: var(--canvas-accent);
  }
  .block ul { margin: 0; padding: 0 0 0 16px; color: var(--canvas-text); }
  .block li { margin-bottom: 5px; }
  .block li:last-child { margin-bottom: 0; }

  /* Lean Canvas grid placement (Maurya's layout) */
  .problem            { grid-column: 1; grid-row: 1 / span 2; }
  .solution           { grid-column: 2; grid-row: 1; }
  .key-metrics        { grid-column: 2; grid-row: 2; border-top: 1px solid var(--canvas-border); }
  .uvp                { grid-column: 3; grid-row: 1 / span 2; }
  .unfair-advantage   { grid-column: 4; grid-row: 1; }
  .channels           { grid-column: 4; grid-row: 2; border-top: 1px solid var(--canvas-border); }
  .customer-segments  { grid-column: 5; grid-row: 1 / span 2; border-right: none; }

  .lean-bottom {
    display: grid;
    grid-template-columns: 1fr 1fr;
    border: 1px solid var(--canvas-border);
    border-top: none;
    background: var(--canvas-surface);
  }
  .lean-bottom .block { border-bottom: none; min-height: 130px; }
  .lean-bottom .block:last-child { border-right: none; }

  /* ---------- VPC (bottom) ---------- */
  .vpc {
    display: grid;
    grid-template-columns: 1fr 80px 1fr;
    border: 1px solid var(--canvas-border);
    background: var(--canvas-surface);
    margin-top: 18px;
  }
  .vpc-side { display: flex; flex-direction: column; }
  .vpc-side > .block {
    border-right: none;
    border-bottom: 1px solid var(--canvas-border);
    min-height: 140px;
  }
  .vpc-side > .block:last-child { border-bottom: none; }
  .vpc-fit {
    display: flex;
    align-items: center;
    justify-content: center;
    border-left: 1px solid var(--canvas-border);
    border-right: 1px solid var(--canvas-border);
    color: var(--canvas-muted);
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    writing-mode: vertical-rl;
    transform: rotate(180deg);
  }

  /* ---------- Stress tests ---------- */
  .stress {
    margin: 18px 32px 0;
    padding: 16px 18px;
    border-left: 3px solid var(--canvas-accent);
    background: var(--canvas-surface);
  }
  .stress h2 {
    margin: 0 0 8px;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.02em;
    color: var(--canvas-accent);
  }
  .stress ol { margin: 0; padding-left: 18px; }
  .stress li { margin-bottom: 8px; }

  footer {
    padding: 12px 32px 24px;
    color: var(--canvas-muted);
    font-size: 11px;
  }

  @media print {
    @page { size: A4 landscape; margin: 10mm; }
    body { background: #fff; font-size: 11px; }
    header, .canvas-section, footer { margin-left: 0; margin-right: 0; }
    .lean, .lean-bottom, .vpc { page-break-inside: avoid; }
    .vpc { page-break-before: always; }
  }
</style>
</head>
<body>
  <header>
    <h1>Validation Canvas — {{business_name}}</h1>
    <div class="meta">Generated {{generated_date}}</div>
  </header>

  <section class="canvas-section">
    <h2 class="section-title">Lean Canvas</h2>
    <div class="lean">
      <section class="block problem">
        <h3>Problem</h3>
        {{problem_list}}
      </section>
      <section class="block solution">
        <h3>Solution</h3>
        {{solution_list}}
      </section>
      <section class="block key-metrics">
        <h3>Key Metrics</h3>
        {{key_metrics_list}}
      </section>
      <section class="block uvp">
        <h3>Unique Value Proposition</h3>
        {{uvp_list}}
      </section>
      <section class="block unfair-advantage">
        <h3>Unfair Advantage</h3>
        {{unfair_advantage_list}}
      </section>
      <section class="block channels">
        <h3>Channels</h3>
        {{channels_list}}
      </section>
      <section class="block customer-segments">
        <h3>Customer Segments</h3>
        {{customer_segments_list}}
      </section>
    </div>
    <div class="lean-bottom">
      <section class="block cost-structure">
        <h3>Cost Structure</h3>
        {{cost_structure_list}}
      </section>
      <section class="block revenue-streams">
        <h3>Revenue Streams</h3>
        {{revenue_streams_list}}
      </section>
    </div>
  </section>

  <section class="canvas-section">
    <h2 class="section-title">Value Proposition Canvas</h2>
    <div class="vpc">
      <div class="vpc-side value-map">
        <section class="block">
          <h3>Products &amp; Services</h3>
          {{products_services_list}}
        </section>
        <section class="block">
          <h3>Pain Relievers</h3>
          {{pain_relievers_list}}
        </section>
        <section class="block">
          <h3>Gain Creators</h3>
          {{gain_creators_list}}
        </section>
      </div>
      <div class="vpc-fit">Fit Check</div>
      <div class="vpc-side customer-profile">
        <section class="block">
          <h3>Customer Jobs</h3>
          {{customer_jobs_list}}
        </section>
        <section class="block">
          <h3>Customer Pains</h3>
          {{customer_pains_list}}
        </section>
        <section class="block">
          <h3>Customer Gains</h3>
          {{customer_gains_list}}
        </section>
      </div>
    </div>
  </section>

  <section class="stress">
    <h2>Stress Tests</h2>
    {{stress_tests_ordered_list}}
  </section>

  <footer>
    Generated {{generated_date}} · <code>validation-canvas.md</code> is the source of truth.
    Next step: <code>riskiest-assumption-test</code> converts these Stress Tests into falsifiable hypotheses.
  </footer>
</body>
</html>
```

---

## Brand token substitution (strict mapping)

If the brand design system exists (`<brand-root>/design-system.md` per the
conventions doc, or legacy `brand-kit/design-system.md` at cwd root for
backward compat), map sections → CSS variables **literally by the names
below**. Do not infer or rename on the fly — the mapping is a contract with
`brand-workshop`'s `design-system.md` schema.

| CSS variable           | `design-system.md` section.key                         |
|------------------------|--------------------------------------------------------|
| `--canvas-bg`          | `Color Tokens → Neutrals.background`                   |
| `--canvas-surface`     | `Color Tokens → Neutrals.surface`                      |
| `--canvas-text`        | `Color Tokens → Neutrals.text-primary`                 |
| `--canvas-muted`       | `Color Tokens → Neutrals.text-secondary`               |
| `--canvas-border`      | `Color Tokens → Neutrals.border`                       |
| `--canvas-accent`      | `Color Tokens → Primary` (the brand hero color)        |
| `--canvas-font-body`   | `Typography → body` (family stack)                     |
| `--canvas-font-heading`| `Typography → display` (fall back to `Typography → body`) |

Note: `brand-workshop` exposes both `Color Tokens → Primary` *and* a separate
`Color Tokens → Accent`. **Map `--canvas-accent` to `Primary`, not to
`Accent`** — `Accent` is a secondary highlight color in brand-workshop's
vocabulary, while `Primary` is the brand hero that downstream plugins treat
as their accent.

> **Token contract migration note (v1 → v2).** This skill previously named
> its accent variable `--bmc-accent`. v2.0.0 renamed it to `--canvas-accent`
> in lockstep with the skill rename. Brand-workshop's Token Mapping
> Convention block has been updated to reference both names during the
> migration window.

If a section is missing from `design-system.md`, keep the neutral default
from the template's `:root` block and leave an HTML comment noting the
fallback (e.g., `<!-- fallback: --canvas-accent not found in
design-system.md -->`).

If the brand uses non-websafe fonts and you don't have a base64 webfont
available, keep the system-font fallback — don't pull a webfont from a CDN.
Zero network dependencies is a hard rule.

---

## Contrast check

Before saving the HTML, verify:
- Body text (`--canvas-text` on `--canvas-surface`) meets WCAG AA (≥ 4.5:1
  for body, ≥ 3:1 for the uppercase block headings).
- If the brand's primary is a light pastel that fails contrast as text, keep
  it for accent borders only and use a darker token for `--canvas-text`.

Hollowly brand-compliant but unreadable beats the purpose.
