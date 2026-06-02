# Dossier HTML Template

The single self-contained interactive dossier. Render `startup-audit.html` from
the canonical `startup-audit.md` by substituting `{{placeholders}}` into the
template below.

**Contract:**

- **Self-contained** — inline `<style>` + inline vanilla `<script>`, zero network
  requests, base64 any images. Must open offline.
- **Interactive** — expandable provenance per canvas field; confidence-tier
  filter (show/hide observed / inferred / unknown); collapsible sections.
- **Print-clean** — `@media print` collapses interactivity into a flat readable
  document; prints to PDF without layout breakage.
- **Brand tokens** — if a `DESIGN.md` exists at repo root, read its YAML front
  matter and inject `colors.primary` → `--accent`, `typography.body.family` →
  `--font-body`. Otherwise use the defaults in `:root` below (the canonical
  palette).
- **No secrets** — never render a secret value; provenance pointers are
  file paths / signal names only.

**Placeholders:**

| Token | Content |
|---|---|
| `{{PRODUCT_NAME}}` | Inferred product name |
| `{{GENERATED_DATE}}` | ISO date (passed in — do not call Date() at author time) |
| `{{LANE_NOTE}}` | Which lane ran: SocratiCode vs glob/grep; URL fetched vs skipped |
| `{{EXEC_SUMMARY}}` | Executive summary paragraph |
| `{{DIFF_ROWS}}` | Build-vs-claim diff `<tr>`s (see row shape) |
| `{{CANVAS_BLOCKS}}` | Nine canvas-block `<article>`s (see block shape) |
| `{{FINDINGS}}` | Per-lens findings blocks |
| `{{OPTIONS}}` | "Options the evidence suggests", each citing a finding-id |
| `{{HANDOFF}}` | Handoff + next steps (RAT for unknowns, grill for verdict) |
| `{{PANEL_TABLE}}` | The resolved audit-panel table + any cap-trim footnote |

**Confidence-tier CSS classes (the distinctive motif):** `.tier-observed` (green),
`.tier-inferred` (amber), `.tier-unknown` (muted). A canvas field's class is set
from its derived tier; the filter toggles visibility by class.

---

## Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Startup Audit — {{PRODUCT_NAME}}</title>
<style>
  :root {
    --bg: #f5efe6; --paper: #fdf7ea; --ink: #1f2937; --muted: #6b7280;
    --accent: #c2410c; --line: #c9b58a;
    --observed: #15803d; --observed-bg: #dcfce7;
    --inferred: #b45309; --inferred-bg: #fde68a;
    --unknown: #6b7280; --unknown-bg: #e5e7eb;
    --font-body: ui-monospace, SFMono-Regular, Menlo, monospace;
  }
  * { box-sizing: border-box; }
  body { margin: 0; background: var(--bg); color: var(--ink);
    font-family: var(--font-body); line-height: 1.5; padding: 2rem; }
  .wrap { max-width: 1100px; margin: 0 auto; }
  header { border-bottom: 3px solid var(--accent); padding-bottom: 1rem; margin-bottom: 1.5rem; }
  h1 { font-size: 1.6rem; margin: 0 0 .25rem; }
  .sub { color: var(--muted); font-size: .85rem; }
  .lane { font-size: .75rem; color: var(--muted); margin-top: .5rem; font-style: italic; }
  section { background: var(--paper); border: 1px solid var(--line);
    border-radius: 6px; padding: 1.25rem; margin-bottom: 1.25rem; }
  h2 { font-size: 1.1rem; margin: 0 0 .75rem; border-left: 4px solid var(--accent); padding-left: .5rem; }
  .collapse-toggle { cursor: pointer; user-select: none; }
  .collapse-toggle::before { content: "▾ "; color: var(--accent); }
  .collapsed > .body { display: none; }
  .collapsed > h2 .collapse-toggle::before { content: "▸ "; }

  /* filter bar */
  .filter { display: flex; gap: .5rem; flex-wrap: wrap; margin-bottom: 1rem; font-size: .8rem; }
  .filter button { font-family: inherit; cursor: pointer; border: 1px solid var(--line);
    background: var(--paper); padding: .3rem .6rem; border-radius: 4px; }
  .filter button[aria-pressed="false"] { opacity: .4; }
  .chip { display: inline-block; font-size: .65rem; text-transform: uppercase;
    letter-spacing: .08em; padding: .1rem .4rem; border-radius: 3px; font-weight: bold; }
  .tier-observed .chip { background: var(--observed-bg); color: var(--observed); }
  .tier-inferred .chip { background: var(--inferred-bg); color: var(--inferred); }
  .tier-unknown  .chip { background: var(--unknown-bg);  color: var(--unknown); }

  /* canvas grid */
  .canvas { display: grid; grid-template-columns: repeat(3, 1fr); gap: .75rem; }
  .block { border: 1px solid var(--line); border-radius: 4px; padding: .6rem; background: #fff; }
  .block h3 { font-size: .8rem; margin: 0 0 .4rem; }
  .block.hidden { display: none; }
  .block ul { margin: .3rem 0 0; padding-left: 1rem; font-size: .8rem; }
  .prov { cursor: pointer; color: var(--accent); font-size: .7rem; }
  .prov-detail { display: none; font-size: .7rem; color: var(--muted);
    background: var(--bg); padding: .3rem; border-radius: 3px; margin-top: .3rem; }
  .prov-detail.open { display: block; }

  /* diff table */
  table { width: 100%; border-collapse: collapse; font-size: .8rem; }
  th, td { border: 1px solid var(--line); padding: .5rem; text-align: left; vertical-align: top; }
  th { background: var(--bg); }
  .diff-flag { color: var(--accent); font-weight: bold; }

  footer { color: var(--muted); font-size: .75rem; text-align: center; margin-top: 2rem; }

  @media (max-width: 720px) { .canvas { grid-template-columns: 1fr; } }
  @media print {
    body { background: #fff; padding: 0; }
    .filter, .collapse-toggle { display: none !important; }
    .collapsed > .body { display: block !important; }
    .prov-detail { display: block !important; }
    .block.hidden { display: block !important; }
    section { break-inside: avoid; border-color: #999; }
  }
</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1>Startup Audit — {{PRODUCT_NAME}}</h1>
    <div class="sub">Post-build diligence readout · generated {{GENERATED_DATE}}</div>
    <div class="sub">Evidence, not validation. Every claim is tiered and pinned to provenance. No verdict — see handoff.</div>
    <div class="lane">{{LANE_NOTE}}</div>
  </header>

  <section><h2><span class="collapse-toggle"></span>Executive summary</h2>
    <div class="body">{{EXEC_SUMMARY}}</div></section>

  <section><h2><span class="collapse-toggle"></span>Build vs. claim</h2>
    <div class="body">
      <table>
        <thead><tr><th>Coded reality</th><th>Claimed story</th><th>Gap</th></tr></thead>
        <tbody>{{DIFF_ROWS}}</tbody>
      </table>
    </div></section>

  <section><h2><span class="collapse-toggle"></span>Inferred Lean Canvas</h2>
    <div class="body">
      <div class="filter" role="group" aria-label="Filter canvas by confidence tier">
        <span>Show:</span>
        <button data-tier="observed" aria-pressed="true">observed</button>
        <button data-tier="inferred" aria-pressed="true">inferred</button>
        <button data-tier="unknown"  aria-pressed="true">unknown</button>
      </div>
      <div class="canvas">{{CANVAS_BLOCKS}}</div>
    </div></section>

  <section><h2><span class="collapse-toggle"></span>Audit findings</h2>
    <div class="body">{{PANEL_TABLE}}{{FINDINGS}}</div></section>

  <section><h2><span class="collapse-toggle"></span>Options the evidence suggests</h2>
    <div class="body">{{OPTIONS}}</div></section>

  <section><h2><span class="collapse-toggle"></span>Handoff &amp; next steps</h2>
    <div class="body">{{HANDOFF}}</div></section>

  <footer>Generated by startup-audit · diligence readout · not a verdict (run startup-grill for that)</footer>
</div>

<script>
  // collapsible sections
  document.querySelectorAll('section h2 .collapse-toggle').forEach(function (t) {
    t.addEventListener('click', function () { t.closest('section').classList.toggle('collapsed'); });
  });
  // expandable provenance
  document.querySelectorAll('.prov').forEach(function (p) {
    p.addEventListener('click', function () {
      var d = p.nextElementSibling;
      if (d && d.classList.contains('prov-detail')) d.classList.toggle('open');
    });
  });
  // confidence-tier filter
  document.querySelectorAll('.filter button').forEach(function (b) {
    b.addEventListener('click', function () {
      var pressed = b.getAttribute('aria-pressed') === 'true';
      b.setAttribute('aria-pressed', String(!pressed));
      var tier = b.getAttribute('data-tier');
      document.querySelectorAll('.block.tier-' + tier).forEach(function (el) {
        el.classList.toggle('hidden', pressed);
      });
    });
  });
</script>
</body>
</html>
```

### Diff row shape (`{{DIFF_ROWS}}`)

```html
<tr><td>[coded reality]</td><td>[claimed story]</td>
    <td class="diff-flag">[F1] claims B2B; built B2C</td></tr>
```

### Canvas block shape (`{{CANVAS_BLOCKS}}`)

```html
<article class="block tier-observed">
  <h3>Revenue Streams <span class="chip">observed</span></h3>
  <ul><li>Freemium subscription, single price (Free/Pro)</li></ul>
  <span class="prov">⊕ provenance</span>
  <div class="prov-detail">users.stripeCustomerId + subscriptionId · STRIPE_PRICE_ID (single) · stripe.ts</div>
</article>
```

An `unknown` block uses `class="block tier-unknown"`, the `unknown` chip, and its
`<li>` states `[unknown — no code signal; see handoff]` with no provenance span.

---

## Markdown mirror (`startup-audit.md`)

The canonical `.md` carries the same content in plain Markdown (headings:
`## Executive summary`, `## Build vs. claim`, `## Inferred Lean Canvas`,
`## Audit findings`, `## Options the evidence suggests`, `## Handoff & next steps`)
so the dossier is diffable / editable and the HTML is a render of it. The
`inferred-canvas.md` (Lean Canvas headings) is a separate artifact per
`inference-mapping.md`.
