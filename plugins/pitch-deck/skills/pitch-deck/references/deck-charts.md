# Deck Charts — Reference

Inline SVG chart templates for the three charts that cover ~95% of pitch-deck needs:

1. **Market** — bar or stack showing TAM / SAM / SOM
2. **Traction** — line chart with a time axis (the one non-negotiable chart)
3. **Competition** — 2×2 positioning quadrant

All charts are hand-built SVG. No Chart.js, no D3, no external library. They must
render without internet, scale cleanly at any size, and print to PDF without
rasterization artifacts.

---

## Design principles

- **One chart, one message.** A chart in a pitch deck answers one question. If it
  tries to answer two, redesign it or split into two slides.
- **Absolute numbers on the axes, not indexed percentages.** "5× growth" hides
  whether you went from 100 to 500 or from $100M to $500M. Show the actual number.
- **Color earns its place.** Use `--deck-accent` for the one line or bar the viewer
  should focus on. Every other color in the chart is muted.
- **Labels on the chart, not only in a legend.** Eyes track labels faster than
  legend-to-color matching — especially at projection distance.
- **Every chart has a 1-line title and a source/date line below.** The source line
  builds trust; its absence signals the number came from nowhere.

---

## Chart 1 — Market (TAM / SAM / SOM bar)

Use for the Market slide. Shows scale relationship without drowning in precision.

```html
<svg viewBox="0 0 900 360" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;font-family:var(--deck-font-body);">
  <!-- Title -->
  <text x="20" y="30" fill="var(--deck-text)" font-size="18" font-weight="600">Market sizing</text>

  <!-- TAM bar -->
  <rect x="20" y="60" width="860" height="64" fill="var(--deck-border)" />
  <text x="36" y="96" fill="var(--deck-text)" font-size="16" font-weight="600">TAM</text>
  <text x="864" y="96" fill="var(--deck-text)" font-size="16" font-weight="600" text-anchor="end">$XXB</text>
  <text x="36" y="114" fill="var(--deck-muted)" font-size="12">{{tam_description}}</text>

  <!-- SAM bar (width scaled to fraction of TAM) -->
  <rect x="20" y="144" width="430" height="64" fill="var(--deck-muted)" opacity="0.6" />
  <text x="36" y="180" fill="var(--deck-text)" font-size="16" font-weight="600">SAM</text>
  <text x="434" y="180" fill="var(--deck-text)" font-size="16" font-weight="600" text-anchor="end">$XB</text>
  <text x="36" y="198" fill="var(--deck-muted)" font-size="12">{{sam_description}}</text>

  <!-- SOM bar (width scaled to fraction of SAM) -->
  <rect x="20" y="228" width="95" height="64" fill="var(--deck-accent)" />
  <text x="36" y="264" fill="var(--deck-bg)" font-size="16" font-weight="600">SOM</text>
  <text x="130" y="264" fill="var(--deck-text)" font-size="16" font-weight="600">$XM (3-yr)</text>
  <text x="36" y="282" fill="var(--deck-muted)" font-size="12">{{som_description}}</text>

  <!-- Footer / source -->
  <text x="20" y="332" fill="var(--deck-muted)" font-size="11">Source: {{market_source}} · Bottom-up: {{bottom_up_calc_short}}</text>
</svg>
```

**Substitutions:**
- Width scaling: SAM width = 860 × (SAM / TAM); SOM width = 860 × (SOM / TAM).
  Cap minimum at 60px so the SOM bar is still readable if SOM is <2% of TAM.
- Replace `$XXB`, `$XB`, `$XM` with actual values formatted consistently.
- Replace `{{…_description}}` with one-line qualifiers (e.g., "U.S. dental practices,
  all sizes").

**Anti-patterns avoided:**
- Three nested circles (Venn-style) — illegible at projection distance.
- Pie chart of TAM/SAM/SOM — implies they sum to a whole, which they don't.

---

## Chart 2 — Traction (line with time axis)

Use for the Traction slide. **The time axis is non-negotiable** — this is cardinal
sin #2 in SKILL.md. A traction number without a time axis blocks the deck.

```html
<svg viewBox="0 0 900 400" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;font-family:var(--deck-font-body);">
  <!-- Title -->
  <text x="20" y="30" fill="var(--deck-text)" font-size="18" font-weight="600">{{traction_metric_name}}</text>

  <!-- Y-axis (left) -->
  <line x1="80" y1="60" x2="80" y2="340" stroke="var(--deck-border)" stroke-width="1" />
  <!-- Y-axis labels (5 gridlines) -->
  <g fill="var(--deck-muted)" font-size="12">
    <text x="72" y="344" text-anchor="end">0</text>
    <text x="72" y="274" text-anchor="end">{{y_tick_1}}</text>
    <text x="72" y="204" text-anchor="end">{{y_tick_2}}</text>
    <text x="72" y="134" text-anchor="end">{{y_tick_3}}</text>
    <text x="72" y="64" text-anchor="end">{{y_tick_4}}</text>
  </g>
  <!-- Horizontal gridlines -->
  <g stroke="var(--deck-border)" stroke-width="1" stroke-dasharray="2 4" opacity="0.5">
    <line x1="80" y1="270" x2="870" y2="270" />
    <line x1="80" y1="200" x2="870" y2="200" />
    <line x1="80" y1="130" x2="870" y2="130" />
    <line x1="80" y1="60" x2="870" y2="60" />
  </g>

  <!-- X-axis (bottom) -->
  <line x1="80" y1="340" x2="870" y2="340" stroke="var(--deck-border)" stroke-width="1" />
  <!-- X-axis labels (months/quarters) -->
  <g fill="var(--deck-muted)" font-size="12">
    <text x="80"  y="362" text-anchor="middle">{{x_label_1}}</text>
    <text x="238" y="362" text-anchor="middle">{{x_label_2}}</text>
    <text x="396" y="362" text-anchor="middle">{{x_label_3}}</text>
    <text x="554" y="362" text-anchor="middle">{{x_label_4}}</text>
    <text x="712" y="362" text-anchor="middle">{{x_label_5}}</text>
    <text x="870" y="362" text-anchor="middle">{{x_label_6}}</text>
  </g>

  <!-- Data line: replace points with real coords. Example shows 6 months of growth -->
  <polyline
    points="80,320 238,290 396,240 554,180 712,120 870,80"
    fill="none"
    stroke="var(--deck-accent)"
    stroke-width="3"
    stroke-linejoin="round"
    stroke-linecap="round" />
  <!-- Data point dots -->
  <g fill="var(--deck-accent)">
    <circle cx="80"  cy="320" r="4" />
    <circle cx="238" cy="290" r="4" />
    <circle cx="396" cy="240" r="4" />
    <circle cx="554" cy="180" r="4" />
    <circle cx="712" cy="120" r="4" />
    <circle cx="870" cy="80"  r="5" />
  </g>
  <!-- Callout: last-point label -->
  <text x="870" y="66" fill="var(--deck-text)" font-size="14" font-weight="600" text-anchor="end">{{last_value_label}}</text>

  <!-- Footer: growth rate + window -->
  <text x="20" y="390" fill="var(--deck-muted)" font-size="11">{{growth_rate_summary}} · Window: {{window_start}}–{{window_end}}</text>
</svg>
```

**Substitutions:**
- Y-axis labels: 5 evenly-spaced ticks based on max value. E.g., for $0 to $1M, use
  0, 250K, 500K, 750K, 1M.
- X-axis labels: 6 time points (months or quarters). Always show the actual dates.
- `points="..."`: plot the polyline. X-coord for n-th point = 80 + (n-1) × 158.
  Y-coord = 340 - (value / y_max) × 280.
- `{{last_value_label}}`: the current/final value in plain text (e.g., "$842K ARR").
- `{{growth_rate_summary}}`: e.g., "+22% MoM avg", "3× YoY".

**Anti-patterns avoided:**
- Cumulative charts dressed up as growth — check whether it's cumulative or
  period-over-period and label explicitly.
- Hockey-stick without dots — dots make the data points inspectable; a smoothed line
  without markers is a suggestion, not a chart.

---

## Chart 3 — Competition (2×2 positioning)

Use for the Competition slide. The two axes are the two attributes where you want
to claim the upper-right quadrant.

```html
<svg viewBox="0 0 700 500" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;font-family:var(--deck-font-body);">
  <!-- Axes -->
  <line x1="50"  y1="450" x2="650" y2="450" stroke="var(--deck-muted)" stroke-width="1" marker-end="url(#arr)" />
  <line x1="50"  y1="450" x2="50"  y2="50"  stroke="var(--deck-muted)" stroke-width="1" marker-end="url(#arr)" />
  <defs>
    <marker id="arr" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="var(--deck-muted)" />
    </marker>
  </defs>

  <!-- Quadrant gridlines (midpoint dashed) -->
  <g stroke="var(--deck-border)" stroke-width="1" stroke-dasharray="2 4" opacity="0.6">
    <line x1="350" y1="50"  x2="350" y2="450" />
    <line x1="50"  y1="250" x2="650" y2="250" />
  </g>

  <!-- Axis labels -->
  <text x="670" y="455" fill="var(--deck-text)" font-size="14" font-weight="600">{{x_axis_label}}</text>
  <text x="50"  y="40"  fill="var(--deck-text)" font-size="14" font-weight="600">{{y_axis_label}}</text>
  <text x="60"  y="470" fill="var(--deck-muted)" font-size="12">{{x_axis_low}}</text>
  <text x="640" y="470" fill="var(--deck-muted)" font-size="12" text-anchor="end">{{x_axis_high}}</text>
  <text x="40"  y="445" fill="var(--deck-muted)" font-size="12" text-anchor="end">{{y_axis_low}}</text>
  <text x="40"  y="60"  fill="var(--deck-muted)" font-size="12" text-anchor="end">{{y_axis_high}}</text>

  <!-- Competitor dots (muted) -->
  <g>
    <circle cx="130" cy="380" r="10" fill="var(--deck-muted)" opacity="0.7" />
    <text x="145" y="384" fill="var(--deck-text)" font-size="13">{{competitor_1_name}}</text>
  </g>
  <g>
    <circle cx="250" cy="200" r="10" fill="var(--deck-muted)" opacity="0.7" />
    <text x="265" y="204" fill="var(--deck-text)" font-size="13">{{competitor_2_name}}</text>
  </g>
  <g>
    <circle cx="420" cy="330" r="10" fill="var(--deck-muted)" opacity="0.7" />
    <text x="435" y="334" fill="var(--deck-text)" font-size="13">{{competitor_3_name}}</text>
  </g>
  <g>
    <circle cx="200" cy="420" r="10" fill="var(--deck-muted)" opacity="0.7" />
    <text x="215" y="424" fill="var(--deck-text)" font-size="13">Status quo<br/>(customer workaround)</text>
  </g>

  <!-- Us (accent, upper-right) -->
  <g>
    <circle cx="540" cy="110" r="14" fill="var(--deck-accent)" />
    <text x="560" y="115" fill="var(--deck-text)" font-size="16" font-weight="700">{{company_name}}</text>
  </g>

  <!-- Footer caveat -->
  <text x="50" y="495" fill="var(--deck-muted)" font-size="11">Where they're stronger: {{honest_tradeoff_short}}</text>
</svg>
```

**Substitutions:**
- `{{x_axis_label}}` / `{{y_axis_label}}`: the two dimensions you want to claim
  (e.g., "Depth of integration" and "Speed to implement"). Axes must be directional
  — not "quality" vs "price" clichés.
- Competitor positions: place each competitor honestly based on how customers actually
  perceive them. **Do not** park every competitor in the lower-left to make yourself
  look dominant — that's the #1 anti-pattern on this slide.
- Include "Status quo" as a competitor. The customer's current workaround is the
  real incumbent.

**Anti-patterns avoided:**
- Feature checklist table with only the company's column filled in.
- "No one does this" implied by leaving the chart empty except for you.

---

## Optional: Small multiples

For Traction when multiple metrics each matter (e.g., MRR + retention + NPS), use a
row of three small multiples instead of stacking three large charts. Each small
multiple is 280×160, same axis structure as the main line chart, with a one-line
header per panel.

Keep small-multiples to **three panels max**. More than three and the slide stops
being skimmable.

---

## What NOT to put in the deck

- Cohort retention heatmaps — too complex for a pitch slide. Put in appendix or
  speaker notes and mention verbally.
- Sankey diagrams of funnel — interesting to build, unreadable at projection.
- World maps dotted with customer locations — belongs in a sales deck, not an
  investor deck. (Exception: if geography *is* the thesis.)
- Logos-of-customers wall with 40+ logos — investors will be skeptical of
  "customers" vs "trials vs "pilots". Show 6–10 real ones with a label (Logos in
  production vs Logos in pilot).

---

## Accessibility

All charts must:
- Have a text summary below the chart (the `{{growth_rate_summary}}` or equivalent)
  so the slide still communicates if the SVG fails to render or the viewer is
  color-blind.
- Use at least one non-color encoding (size, position, labels) to distinguish
  important elements — never rely on color alone. In the Competition 2×2, the
  company dot is both larger *and* accent-colored.
