# BMC HTML Template — Reference

The canonical self-contained HTML Business Model Canvas. Read this before producing
`business-model.html`.

**Contract:**
- Single file, no external dependencies (no CDN links, no webfonts unless base64).
- Renders the canonical Osterwalder 9-block grid: top row split into Key Partners /
  Key Activities + Key Resources / Value Propositions / Customer Relationships +
  Channels / Customer Segments; bottom row split between Cost Structure and
  Revenue Streams.
- Prints cleanly to PDF via CSS paged media (`@page` at landscape A4 or Letter).
- Applies brand tokens from `brand-kit/design-system.md` if present in the working
  directory. Otherwise uses the neutral defaults in this template.
- Footer line: `Generated [YYYY-MM-DD] · business-model.md is the source of truth.`

**How to use this template:**
1. Read `business-model.md` — the canonical source of truth you already produced.
2. For each block, extract the bulleted claims. Preserve founder's wording.
3. Substitute the nine `{{…}}` placeholders below with the actual block content as
   semantic `<ul>` lists.
4. If `brand-kit/design-system.md` exists in the working directory, parse out the
   primary, surface, and text colors plus the body font-family, and substitute them
   into the `:root` CSS custom properties. Otherwise keep the defaults.
5. Save as `business-model.html` in the working directory.

---

## Template

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Business Model Canvas — {{business_name}}</title>
<style>
  :root {
    /* Override these from brand-kit/design-system.md when available */
    --bmc-bg: #fafaf7;
    --bmc-surface: #ffffff;
    --bmc-text: #1a1a1a;
    --bmc-muted: #6b6b6b;
    --bmc-border: #d9d9d3;
    --bmc-accent: #1a1a1a;
    --bmc-font-body: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    --bmc-font-heading: var(--bmc-font-body);
  }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    background: var(--bmc-bg);
    color: var(--bmc-text);
    font-family: var(--bmc-font-body);
    font-size: 13px;
    line-height: 1.45;
  }
  header {
    padding: 24px 32px 12px;
  }
  header h1 {
    margin: 0 0 4px;
    font-family: var(--bmc-font-heading);
    font-size: 22px;
    letter-spacing: -0.01em;
  }
  header .meta {
    color: var(--bmc-muted);
    font-size: 12px;
  }
  .canvas {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    grid-template-rows: 1fr 1fr;
    gap: 0;
    margin: 16px 32px 32px;
    border: 1px solid var(--bmc-border);
    background: var(--bmc-surface);
  }
  .block {
    padding: 16px 18px;
    border-right: 1px solid var(--bmc-border);
    border-bottom: 1px solid var(--bmc-border);
    display: flex;
    flex-direction: column;
    min-height: 180px;
  }
  .block:last-child { border-right: none; }
  .block h2 {
    margin: 0 0 10px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: var(--bmc-accent);
  }
  .block ul {
    margin: 0;
    padding: 0 0 0 16px;
    color: var(--bmc-text);
  }
  .block li { margin-bottom: 6px; }
  .block li:last-child { margin-bottom: 0; }

  /* Grid placement mirrors Osterwalder's canonical layout */
  .key-partners         { grid-column: 1; grid-row: 1 / span 2; }
  .key-activities       { grid-column: 2; grid-row: 1; }
  .key-resources        { grid-column: 2; grid-row: 2; border-top: 1px solid var(--bmc-border); }
  .value-propositions   { grid-column: 3; grid-row: 1 / span 2; }
  .customer-relationships { grid-column: 4; grid-row: 1; }
  .channels             { grid-column: 4; grid-row: 2; border-top: 1px solid var(--bmc-border); }
  .customer-segments    { grid-column: 5; grid-row: 1 / span 2; border-right: none; }

  .bottom-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    margin: 0 32px 16px;
    border: 1px solid var(--bmc-border);
    border-top: none;
    background: var(--bmc-surface);
  }
  .bottom-row .block { border-bottom: none; min-height: 150px; }
  .bottom-row .block:last-child { border-right: none; }

  footer {
    padding: 8px 32px 24px;
    color: var(--bmc-muted);
    font-size: 11px;
  }

  @media print {
    @page { size: A4 landscape; margin: 10mm; }
    body { background: #fff; font-size: 11px; }
    header, .canvas, .bottom-row, footer { margin-left: 0; margin-right: 0; }
    .canvas, .bottom-row { page-break-inside: avoid; }
  }
</style>
</head>
<body>
  <header>
    <h1>Business Model Canvas — {{business_name}}</h1>
    <div class="meta">Generated {{generated_date}}</div>
  </header>

  <div class="canvas">
    <section class="block key-partners">
      <h2>Key Partners</h2>
      {{key_partners_list}}
    </section>
    <section class="block key-activities">
      <h2>Key Activities</h2>
      {{key_activities_list}}
    </section>
    <section class="block key-resources">
      <h2>Key Resources</h2>
      {{key_resources_list}}
    </section>
    <section class="block value-propositions">
      <h2>Value Propositions</h2>
      {{value_propositions_list}}
    </section>
    <section class="block customer-relationships">
      <h2>Customer Relationships</h2>
      {{customer_relationships_list}}
    </section>
    <section class="block channels">
      <h2>Channels</h2>
      {{channels_list}}
    </section>
    <section class="block customer-segments">
      <h2>Customer Segments</h2>
      {{customer_segments_list}}
    </section>
  </div>

  <div class="bottom-row">
    <section class="block cost-structure">
      <h2>Cost Structure</h2>
      {{cost_structure_list}}
    </section>
    <section class="block revenue-streams">
      <h2>Revenue Streams</h2>
      {{revenue_streams_list}}
    </section>
  </div>

  <footer>
    Generated {{generated_date}} · <code>business-model.md</code> is the source of truth.
  </footer>
</body>
</html>
```

---

## Brand token substitution

If `brand-kit/design-system.md` exists, extract these values and replace the
`:root` defaults:

| CSS variable | Brand-kit source (typical) |
|--------------|----------------------------|
| `--bmc-bg` | Surface / background color |
| `--bmc-surface` | Card / paper color (often white) |
| `--bmc-text` | Primary text color |
| `--bmc-muted` | Secondary / caption text color |
| `--bmc-border` | Divider / border color |
| `--bmc-accent` | Primary brand color |
| `--bmc-font-body` | Body font stack |
| `--bmc-font-heading` | Heading font stack (fall back to body) |

If the brand uses non-websafe fonts and you don't have a base64 webfont available,
keep the system-font fallback — don't pull a webfont from a CDN. Zero network
dependencies is a hard rule.

---

## Contrast check

Before saving the HTML, verify:
- Body text (`--bmc-text` on `--bmc-surface`) meets WCAG AA (≥ 4.5:1 for body, ≥ 3:1 for the uppercase block headings).
- If the brand's primary is a light pastel that fails contrast as text, keep it for
  accent borders only and use a darker token for `--bmc-text`.

Hollowly brand-compliant but unreadable beats the purpose.
