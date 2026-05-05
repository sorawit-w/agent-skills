# Test Matrix HTML Template — Reference

The canonical self-contained interactive **risk × impact matrix** for the
Assumption Test Plan. Read this before producing `<rat-root>/test-matrix.html`.

**Contract:**
- Single file. All JS / CSS inline. Zero network dependencies.
- Renders a **3×3 grid** (Risk: Low/Med/High × Impact: Low/Med/High).
- Each assumption is a **draggable card**. Drop snaps to grid cells.
  Re-ranking is session-local (HTML doesn't write back to the Markdown).
- **Click to expand** a card in place — shows the hypothesis, success
  criteria, kill criteria, chosen test method, time bound, cost estimate,
  and Results status.
- **Color-coded by category:** desirability / viability / feasibility get
  three distinct accent colors (use brand tokens from `<brand-root>/DESIGN.md`
  ([Google Labs spec](https://github.com/google-labs-code/design.md), version `alpha`),
  or legacy `brand-kit/DESIGN.md`, if present; neutral defaults otherwise).
- **Top-3 highlight:** the 3 cards selected as Top 3 in Phase 2 of the
  skill get a visible badge ("⭐ TOP 3") and a thicker border.
- **Print-clean:** `@media print` collapses to a static grid that prints
  to PDF for board decks. Drag handles hide; expanded states collapse to
  a brief text summary; the matrix fits on a single landscape A4.
- Footer line: `Generated [YYYY-MM-DD] · assumption-test-plan.md is the
  source of truth.`

See the `riskiest-assumption-test` SKILL.md Phase 0 Step 0.0 for the full
path-resolution chain.

**How to use this template:**

1. Read `assumption-test-plan.md` from the resolved RAT folder
   (`<rat-root>/assumption-test-plan.md`, with legacy fallback to
   `rat/assumption-test-plan.md` at cwd root) — the canonical source you
   already produced.
2. For each assumption row, extract: id, label, category (D/V/F), risk
   level, impact level, hypothesis (full text), success criteria, kill
   criteria, test method, time bound, cost estimate, top-3 flag, results
   status.
3. Inject the assumption objects into the `ASSUMPTIONS` JS array in the
   template below.
4. If the brand design system exists (`<brand-root>/DESIGN.md`, or
   legacy `brand-kit/DESIGN.md` at cwd root), read the YAML front matter
   at the top of the file (delimited by `---` lines) and extract `colors.primary`,
   `colors.secondary`, and `colors.neutral` (the hex strings), plus `typography.body-md.fontFamily`.
   Substitute them into the `:root` CSS custom properties. Otherwise keep the defaults.
5. Save as `<rat-root>/test-matrix.html` (default `docs/rat/test-matrix.html`
   solo, `docs/startup-kit/rat/test-matrix.html` orchestrated).

---

## Template

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Assumption Test Matrix — {{business_name}}</title>
<style>
  :root {
    --rat-bg: #fafaf7;
    --rat-surface: #ffffff;
    --rat-text: #1a1a1a;
    --rat-muted: #6b6b6b;
    --rat-border: #d9d9d3;
    --rat-accent: #1a1a1a;
    --rat-cat-desirability: #b34a4a;  /* red-ish */
    --rat-cat-viability:    #4a7fb3;  /* blue-ish */
    --rat-cat-feasibility:  #4ab37a;  /* green-ish */
    --rat-top3-glow: rgba(212, 175, 55, 0.35); /* gold */
    --rat-font-body: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    background: var(--rat-bg);
    color: var(--rat-text);
    font-family: var(--rat-font-body);
    font-size: 13px;
    line-height: 1.45;
  }
  header { padding: 24px 32px 12px; }
  header h1 {
    margin: 0 0 4px;
    font-size: 22px;
    letter-spacing: -0.01em;
  }
  header .meta { color: var(--rat-muted); font-size: 12px; }

  .legend {
    display: flex;
    gap: 18px;
    margin: 12px 32px 0;
    font-size: 12px;
    color: var(--rat-muted);
    flex-wrap: wrap;
  }
  .legend-item { display: inline-flex; align-items: center; gap: 6px; }
  .legend-swatch {
    display: inline-block;
    width: 12px; height: 12px;
    border-radius: 2px;
  }

  .matrix {
    display: grid;
    grid-template-columns: 80px repeat(3, 1fr);
    grid-template-rows: 36px repeat(3, minmax(160px, 1fr));
    margin: 16px 32px 24px;
    border: 1px solid var(--rat-border);
    background: var(--rat-surface);
    gap: 0;
  }
  .matrix .corner,
  .matrix .col-header,
  .matrix .row-header {
    background: var(--rat-bg);
    border-right: 1px solid var(--rat-border);
    border-bottom: 1px solid var(--rat-border);
    display: flex; align-items: center; justify-content: center;
    font-size: 11px; font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.06em;
    color: var(--rat-muted);
  }
  .matrix .row-header { writing-mode: vertical-rl; transform: rotate(180deg); }
  .matrix .col-header { padding: 6px 0; }
  .matrix .cell {
    border-right: 1px solid var(--rat-border);
    border-bottom: 1px solid var(--rat-border);
    padding: 8px;
    display: flex; flex-direction: column; gap: 6px;
    min-height: 160px;
    background: var(--rat-surface);
  }
  .matrix .cell.target { background: rgba(212, 175, 55, 0.04); } /* high-risk + high-impact */

  .card {
    background: var(--rat-surface);
    border: 1px solid var(--rat-border);
    border-radius: 6px;
    padding: 8px 10px;
    cursor: grab;
    user-select: none;
    border-left-width: 4px;
    font-size: 12px;
  }
  .card[data-category="desirability"] { border-left-color: var(--rat-cat-desirability); }
  .card[data-category="viability"]    { border-left-color: var(--rat-cat-viability); }
  .card[data-category="feasibility"]  { border-left-color: var(--rat-cat-feasibility); }
  .card.top3 {
    border-width: 2px;
    border-left-width: 4px;
    box-shadow: 0 0 0 3px var(--rat-top3-glow);
  }
  .card.dragging { opacity: 0.5; cursor: grabbing; }
  .card .card-title {
    font-weight: 600;
    margin: 0 0 2px;
    display: flex; align-items: center; justify-content: space-between;
    gap: 6px;
  }
  .card .badge {
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--rat-muted);
  }
  .card .badge.top3-badge { color: #8a6f00; font-weight: 700; }
  .card .card-meta { color: var(--rat-muted); font-size: 11px; }
  .card .card-detail {
    margin-top: 8px;
    padding-top: 8px;
    border-top: 1px dashed var(--rat-border);
    color: var(--rat-text);
    font-size: 12px;
    display: none;
  }
  .card.expanded .card-detail { display: block; }
  .card .card-detail dt { font-weight: 600; margin-top: 6px; font-size: 11px; }
  .card .card-detail dd { margin: 0 0 4px; padding-left: 0; }

  footer {
    padding: 12px 32px 24px;
    color: var(--rat-muted);
    font-size: 11px;
  }

  @media print {
    @page { size: A4 landscape; margin: 10mm; }
    body { background: #fff; font-size: 10px; }
    .legend, header, .matrix, footer { margin-left: 0; margin-right: 0; }
    .card { cursor: default; }
    .card .card-detail { display: block !important; }
    .card .badge { display: none; }
    .matrix { page-break-inside: avoid; }
  }
</style>
</head>
<body>
  <header>
    <h1>Assumption Test Matrix — {{business_name}}</h1>
    <div class="meta">Generated {{generated_date}} · drag cards to re-rank · click to expand</div>
  </header>

  <div class="legend">
    <span class="legend-item"><span class="legend-swatch" style="background:var(--rat-cat-desirability)"></span> Desirability</span>
    <span class="legend-item"><span class="legend-swatch" style="background:var(--rat-cat-viability)"></span> Viability</span>
    <span class="legend-item"><span class="legend-swatch" style="background:var(--rat-cat-feasibility)"></span> Feasibility</span>
    <span class="legend-item"><span class="legend-swatch" style="background:var(--rat-top3-glow);border:1px solid #8a6f00"></span> ⭐ Top 3 (test these first)</span>
  </div>

  <div class="matrix" id="matrix">
    <div class="corner"></div>
    <div class="col-header">Low Risk</div>
    <div class="col-header">Med Risk</div>
    <div class="col-header">High Risk</div>

    <div class="row-header">High Impact</div>
    <div class="cell" data-cell="High-Low"></div>
    <div class="cell" data-cell="High-Med"></div>
    <div class="cell target" data-cell="High-High"></div>

    <div class="row-header">Med Impact</div>
    <div class="cell" data-cell="Med-Low"></div>
    <div class="cell" data-cell="Med-Med"></div>
    <div class="cell" data-cell="Med-High"></div>

    <div class="row-header">Low Impact</div>
    <div class="cell" data-cell="Low-Low"></div>
    <div class="cell" data-cell="Low-Med"></div>
    <div class="cell" data-cell="Low-High"></div>
  </div>

  <footer>
    Generated {{generated_date}} · <code>assumption-test-plan.md</code> is the source of truth.
    Re-ranking in this view is session-only — re-run the skill to persist changes.
  </footer>

<script>
  const ASSUMPTIONS = [
    /* Inject assumption objects here. Example shape:
    {
      id: "h1",
      label: "VPs of People feel acute pain about new-manager flameout",
      category: "desirability",          // "desirability" | "viability" | "feasibility"
      risk: "High",                       // "Low" | "Med" | "High"
      impact: "High",                     // "Low" | "Med" | "High"
      top3: true,
      hypothesis: "We believe X. We'll know this is true if Y within Z.",
      successCriteria: "≥ 6 of 10 ...",
      killCriteria: "≤ 1 of 10 ...",
      method: "5-Interview Rule",
      timeBound: "14 days from start",
      costEstimate: "8 hours + $0",
      result: ""                           // "" | "confirmed" | "invalidated" | "in progress"
    }
    */
  ];

  const matrix = document.getElementById('matrix');

  function makeCard(a) {
    const card = document.createElement('div');
    card.className = 'card' + (a.top3 ? ' top3' : '');
    card.draggable = true;
    card.dataset.id = a.id;
    card.dataset.category = a.category;
    card.innerHTML = `
      <div class="card-title">
        <span>${escapeHtml(a.label)}</span>
        <span class="badge ${a.top3 ? 'top3-badge' : ''}">${a.top3 ? '⭐ TOP 3' : a.category[0].toUpperCase()}</span>
      </div>
      <div class="card-meta">${escapeHtml(a.method)} · ${escapeHtml(a.timeBound)} · ${escapeHtml(a.costEstimate)}${a.result ? ' · <strong>' + escapeHtml(a.result) + '</strong>' : ''}</div>
      <dl class="card-detail">
        <dt>Hypothesis</dt><dd>${escapeHtml(a.hypothesis)}</dd>
        <dt>Success</dt><dd>${escapeHtml(a.successCriteria)}</dd>
        <dt>Kill</dt><dd>${escapeHtml(a.killCriteria)}</dd>
        <dt>Method</dt><dd>${escapeHtml(a.method)}</dd>
        <dt>Time bound</dt><dd>${escapeHtml(a.timeBound)}</dd>
        <dt>Cost</dt><dd>${escapeHtml(a.costEstimate)}</dd>
        ${a.result ? `<dt>Result</dt><dd>${escapeHtml(a.result)}</dd>` : ''}
      </dl>
    `;
    card.addEventListener('click', (e) => {
      if (e.target.closest('.card-detail')) return;
      card.classList.toggle('expanded');
    });
    card.addEventListener('dragstart', (e) => {
      card.classList.add('dragging');
      e.dataTransfer.setData('text/plain', a.id);
    });
    card.addEventListener('dragend', () => card.classList.remove('dragging'));
    return card;
  }

  function escapeHtml(s) {
    return String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  }

  // Place cards in their initial cells based on risk × impact
  for (const a of ASSUMPTIONS) {
    const cell = matrix.querySelector(`[data-cell="${a.impact}-${a.risk}"]`);
    if (cell) cell.appendChild(makeCard(a));
  }

  // Wire up drop targets
  matrix.querySelectorAll('.cell').forEach(cell => {
    cell.addEventListener('dragover', e => e.preventDefault());
    cell.addEventListener('drop', e => {
      e.preventDefault();
      const id = e.dataTransfer.getData('text/plain');
      const card = matrix.querySelector(`.card[data-id="${id}"]`);
      if (card && card.parentNode !== cell) cell.appendChild(card);
    });
  });
</script>
</body>
</html>
```

---

## Brand token substitution (DESIGN.md YAML mapping)

If the brand design system exists (`<brand-root>/DESIGN.md` per the
[Google Labs DESIGN.md spec](https://github.com/google-labs-code/design.md),
version `alpha`, or legacy `brand-kit/DESIGN.md` at cwd root for
backward compat), read the YAML front matter and map to CSS variables **literally by the names below**.

Extract the hex strings from the YAML `colors` and `typography` objects:

| CSS variable                | DESIGN.md YAML path        |
|-----------------------------|-------------------------------------------------|
| `--rat-bg`                  | `colors.neutral`            |
| `--rat-surface`             | `colors.surface`            |
| `--rat-text`                | `colors.on-surface`         |
| `--rat-muted`               | `colors.secondary`          |
| `--rat-border`              | `colors.neutral` (dim by 30%) or use as-is |
| `--rat-accent`              | `colors.primary`            |
| `--rat-font-body`           | `typography.body-md.fontFamily` |
| `--rat-cat-desirability`    | (keep neutral default unless brand provides a semantic "warning" or "danger" color) |
| `--rat-cat-viability`       | (keep neutral default unless brand provides a semantic "info" or "primary" color) |
| `--rat-cat-feasibility`     | (keep neutral default unless brand provides a semantic "success" color) |

The category accent colors are deliberately left at neutral defaults — they
need to be visually distinct from each other AND from the brand accent.
Override only if the brand kit provides explicit semantic tokens.

---

## Print fallback

In print mode (`@media print`), all cards expand automatically and the
drag-handle indicators hide. The grid prints in landscape A4 with one
page per matrix. Cell colors are preserved (the high-impact + high-risk
cell gets a faint gold tint to highlight the Top 3 zone).
