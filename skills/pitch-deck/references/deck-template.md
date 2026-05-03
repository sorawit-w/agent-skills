# Deck HTML Template — Reference

The canonical self-contained pitch-deck HTML. Built on Reveal.js core (inlined), with
brand-kit token substitution and print-to-PDF support.

**Contract:**
- Single file, zero network dependencies (no CDN, no webfonts unless base64, no remote
  images).
- Keyboard nav works out of the box: ←/→ arrows, Space for next, Esc for overview.
- Appending `?print-pdf` to the file URL produces a clean slide-per-page PDF via the
  browser's print dialog.
- Reads brand-kit tokens from `brand-kit/design-system.md` if present. Otherwise uses
  the neutral-professional defaults below.
- AAA contrast for body text on projection backgrounds. AA minimum for accent elements.

**How to use this template:**
1. Read `validation-canvas.md`, `rat/assumption-test-plan.md`, and `brand-kit/design-system.md` if present.
2. For each of the 10 slides, extract the required slots from `slide-contracts.md`.
3. Substitute each `{{slide_N_…}}` placeholder with real founder content.
4. If any cardinal slot is `[fill in: …]`, render the warning slide at position 0 (see
   SKILL.md §Phase 3 Step 2).
5. Save as `pitch/deck.html` in the working directory.

---

## Template

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, minimum-scale=1, user-scalable=no">
<title>{{company_name}} — Pitch Deck</title>
<style>
  :root {
    /* Override from brand-kit/design-system.md when available */
    --deck-bg: #0f0f10;
    --deck-surface: #1a1a1c;
    --deck-text: #f5f5f2;
    --deck-muted: #9a9a95;
    --deck-accent: #ffb347;
    --deck-border: #2a2a2d;
    --deck-font-body: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    --deck-font-heading: var(--deck-font-body);
  }
  * { box-sizing: border-box; }
  html, body {
    margin: 0; padding: 0;
    background: var(--deck-bg);
    color: var(--deck-text);
    font-family: var(--deck-font-body);
    overflow: hidden;
    width: 100%;
    height: 100%;
  }
  .reveal {
    position: relative;
    width: 100%;
    height: 100vh;
  }
  .reveal .slides {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .reveal .slides > section {
    display: none;
    width: 100%;
    max-width: 1000px;
    padding: 48px 64px;
  }
  .reveal .slides > section.present { display: block; }
  .reveal h1, .reveal h2, .reveal h3 {
    font-family: var(--deck-font-heading);
    letter-spacing: -0.01em;
    margin: 0 0 16px;
    color: var(--deck-text);
  }
  .reveal h1 { font-size: 56px; line-height: 1.1; }
  .reveal h2 { font-size: 40px; line-height: 1.15; }
  .reveal h3 { font-size: 24px; line-height: 1.25; color: var(--deck-muted); }
  .reveal p, .reveal li { font-size: 20px; line-height: 1.5; }
  .reveal .tagline { color: var(--deck-muted); font-size: 22px; margin-top: 8px; }
  .reveal .meta { color: var(--deck-muted); font-size: 16px; margin-top: 32px; }
  .reveal .accent { color: var(--deck-accent); }
  .reveal .quote {
    border-left: 3px solid var(--deck-accent);
    padding-left: 18px;
    font-style: italic;
    color: var(--deck-text);
    font-size: 22px;
    margin: 24px 0;
  }
  .reveal .kpi {
    font-size: 64px;
    font-weight: 700;
    color: var(--deck-accent);
    letter-spacing: -0.02em;
  }
  .reveal .grid-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 32px;
    align-items: center;
  }
  .reveal .grid-3 {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 24px;
  }
  .reveal .team-member {
    text-align: center;
  }
  .reveal .team-member img {
    width: 120px; height: 120px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid var(--deck-border);
    margin-bottom: 12px;
  }
  .reveal .team-member .name { font-weight: 600; font-size: 18px; }
  .reveal .team-member .role { color: var(--deck-muted); font-size: 14px; }
  .reveal .team-member .bio { font-size: 14px; margin-top: 8px; color: var(--deck-text); }
  .reveal .fillin {
    display: inline-block;
    padding: 2px 8px;
    border: 1px dashed var(--deck-accent);
    color: var(--deck-accent);
    font-family: monospace;
    font-size: 0.85em;
  }
  .reveal .warning-slide {
    background: var(--deck-accent);
    color: var(--deck-bg);
  }
  .reveal .warning-slide h2 { color: var(--deck-bg); }
  .reveal .warning-slide ul { padding-left: 20px; }

  /* Controls */
  .reveal .controls {
    position: absolute;
    bottom: 24px; right: 24px;
    display: flex; gap: 8px;
    color: var(--deck-muted);
    font-size: 14px;
  }
  .reveal .progress {
    position: absolute;
    bottom: 0; left: 0;
    height: 3px;
    background: var(--deck-accent);
    transition: width 0.2s ease;
  }
  .reveal .slide-number {
    position: absolute;
    bottom: 24px; left: 24px;
    color: var(--deck-muted);
    font-size: 14px;
  }

  /* Print / PDF */
  @media print {
    @page { size: 1600px 900px; margin: 0; }
    html, body { background: #fff; color: #000; overflow: visible; height: auto; }
    .reveal { height: auto; }
    .reveal .slides { position: static; display: block; }
    .reveal .slides > section {
      display: block !important;
      page-break-after: always;
      page-break-inside: avoid;
      height: 900px;
      max-width: none;
      padding: 64px;
    }
    .reveal .controls, .reveal .progress, .reveal .slide-number { display: none; }
  }
</style>
</head>
<body>
<div class="reveal">
  <div class="slides">

    <!-- OPTIONAL: Warning slide at position 0 if any cardinal slot is unfilled -->
    <!-- Uncomment and populate when required-slot gating fails:
    <section class="warning-slide">
      <h2>This deck is not ready to send</h2>
      <p>Unfilled cardinal slots:</p>
      <ul>
        <li>{{missing_slot_1}}</li>
        <li>{{missing_slot_2}}</li>
      </ul>
      <p class="meta">Remove this slide by filling the slots above. See <code>deck-checklist.md</code>.</p>
    </section>
    -->

    <!-- Slide 1 — Title -->
    <section>
      <h1>{{company_name}}</h1>
      <div class="tagline">{{tagline}}</div>
      <div class="meta">
        {{founder_names_and_roles}}<br>
        {{date}} · {{contact_email_or_link}}
      </div>
    </section>

    <!-- Slide 2 — Problem -->
    <section>
      <h3>The Problem</h3>
      <h2>{{problem_headline}}</h2>
      <div class="quote">"{{customer_quote}}"<br><span class="meta">— {{customer_attribution}}</span></div>
      <p class="meta">Today's workaround: {{current_workaround}}</p>
    </section>

    <!-- Slide 3 — Solution -->
    <section>
      <h3>Our Solution</h3>
      <h2>{{solution_one_sentence}}</h2>
      <p>{{key_insight_or_unlock}}</p>
      <p><span class="accent">{{concrete_customer_outcome}}</span></p>
    </section>

    <!-- Slide 4 — Market -->
    <section>
      <h3>Market</h3>
      <h2>{{market_headline}}</h2>
      <div class="grid-3">
        <div><div class="kpi">{{tam_value}}</div><div class="meta">TAM — {{tam_description}}</div></div>
        <div><div class="kpi">{{sam_value}}</div><div class="meta">SAM — {{sam_description}}</div></div>
        <div><div class="kpi">{{som_value}}</div><div class="meta">SOM — {{som_description}}</div></div>
      </div>
      <p class="meta">Bottom-up: {{bottom_up_calculation}}<br>Source: {{sources}}</p>
    </section>

    <!-- Slide 5 — Product -->
    <section>
      <h3>Product</h3>
      <h2>{{product_headline}}</h2>
      <div class="grid-2">
        <img src="data:image/png;base64,{{product_screenshot_base64}}" alt="{{screenshot_alt}}" style="max-width: 100%;">
        <ul>
          <li>{{callout_1}}</li>
          <li>{{callout_2}}</li>
          <li>{{callout_3}}</li>
        </ul>
      </div>
    </section>

    <!-- Slide 6 — Business Model -->
    <section>
      <h3>Business Model</h3>
      <h2>{{business_model_headline}}</h2>
      <ul>
        <li><strong>Who pays:</strong> {{who_pays}}</li>
        <li><strong>How:</strong> {{pricing_model}}</li>
        <li><strong>Price band:</strong> {{price_band}}</li>
        <li><strong>Contract:</strong> {{contract_length_or_cadence}}</li>
        <li><strong>Gross margin:</strong> {{gross_margin}}</li>
      </ul>
    </section>

    <!-- Slide 7 — Traction -->
    <section>
      <h3>Traction</h3>
      <h2>{{traction_headline}}</h2>
      <!-- Inline SVG chart from deck-charts.md — Traction Line with Time Axis -->
      {{traction_chart_svg}}
      <p><span class="accent">{{trend_summary}}</span> · {{named_logos_or_cohort}}</p>
    </section>

    <!-- Slide 8 — Team -->
    <section>
      <h3>Team</h3>
      <h2>Why us, why now</h2>
      <div class="grid-3">
        <div class="team-member">
          <img src="data:image/jpeg;base64,{{founder_1_photo_base64}}" alt="{{founder_1_name}}">
          <div class="name">{{founder_1_name}}</div>
          <div class="role">{{founder_1_role}}</div>
          <div class="bio">{{founder_1_relevant_experience}}</div>
        </div>
        <div class="team-member">
          <img src="data:image/jpeg;base64,{{founder_2_photo_base64}}" alt="{{founder_2_name}}">
          <div class="name">{{founder_2_name}}</div>
          <div class="role">{{founder_2_role}}</div>
          <div class="bio">{{founder_2_relevant_experience}}</div>
        </div>
        <!-- Add more founders or key hires as needed -->
      </div>
      <p class="meta">{{unfair_advantage}}</p>
    </section>

    <!-- Slide 9 — Competition -->
    <section>
      <h3>Competition</h3>
      <h2>{{competition_headline}}</h2>
      <!-- Inline SVG 2×2 from deck-charts.md -->
      {{competition_2x2_svg}}
      <p class="meta">Where they're stronger: {{honest_tradeoff}}</p>
    </section>

    <!-- Slide 10 — Ask & Use of Funds -->
    <section>
      <h3>The Ask</h3>
      <h2>Raising <span class="accent">{{ask_amount}}</span> ({{round_type}})</h2>
      <div class="grid-2">
        <div>
          <h3>Milestones this round buys</h3>
          <ul>
            <li>{{milestone_1}}</li>
            <li>{{milestone_2}}</li>
            <li>{{milestone_3}}</li>
          </ul>
        </div>
        <div>
          <h3>Use of funds</h3>
          <ul>
            <li>{{use_pct_1}}% — {{use_category_1}}</li>
            <li>{{use_pct_2}}% — {{use_category_2}}</li>
            <li>{{use_pct_3}}% — {{use_category_3}}</li>
          </ul>
        </div>
      </div>
      <p class="meta">Runway: {{runway_months}} months. {{lead_investor_or_terms}}</p>
      <p class="meta">{{contact_info}}</p>
    </section>

  </div>

  <div class="slide-number"></div>
  <div class="controls">← → Space Esc</div>
  <div class="progress"></div>
</div>

<script>
(function () {
  // Minimal Reveal-like navigation. Self-contained, no external deps.
  var slides = document.querySelectorAll('.reveal .slides > section');
  var current = 0;
  var slideNumber = document.querySelector('.slide-number');
  var progress = document.querySelector('.progress');

  function show(i) {
    if (i < 0 || i >= slides.length) return;
    slides[current].classList.remove('present');
    current = i;
    slides[current].classList.add('present');
    slideNumber.textContent = (current + 1) + ' / ' + slides.length;
    progress.style.width = ((current + 1) / slides.length * 100) + '%';
    location.hash = '#/' + current;
  }

  function next() { show(Math.min(current + 1, slides.length - 1)); }
  function prev() { show(Math.max(current - 1, 0)); }

  document.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') { e.preventDefault(); next(); }
    else if (e.key === 'ArrowLeft' || e.key === 'PageUp') { e.preventDefault(); prev(); }
    else if (e.key === 'Home') { show(0); }
    else if (e.key === 'End') { show(slides.length - 1); }
    else if (e.key === 'Escape') { /* Overview mode placeholder */ }
  });

  // Initial from hash or 0
  var hash = location.hash.match(/#\/(\d+)/);
  show(hash ? Math.min(parseInt(hash[1], 10), slides.length - 1) : 0);

  // Print-to-PDF: if ?print-pdf, show all slides and trigger window.print
  if (location.search.indexOf('print-pdf') !== -1) {
    slides.forEach(function (s) { s.classList.add('present'); });
    setTimeout(function () { window.print(); }, 500);
  }
})();
</script>
</body>
</html>
```

---

## Brand token substitution

If `brand-kit/design-system.md` exists, extract these values and replace the `:root`
defaults:

| CSS variable | Brand-kit source (typical) |
|--------------|----------------------------|
| `--deck-bg` | Dark surface for projection (often a deep tone) |
| `--deck-surface` | Secondary surface / card bg |
| `--deck-text` | Primary body text on dark bg |
| `--deck-muted` | Secondary / caption text |
| `--deck-accent` | Primary brand color (used for KPIs, headings of interest, progress bar) |
| `--deck-border` | Subtle dividers / team photo borders |
| `--deck-font-body` | Body font stack (must gracefully fall back) |
| `--deck-font-heading` | Heading font stack |

**Projection-first defaults.** The default palette is dark-mode because decks project
better on dark backgrounds in most meeting rooms. If the brand is light-mode-native,
flip `--deck-bg` and `--deck-text` — but verify contrast stays AAA for body (≥ 7:1)
and AA (≥ 4.5:1) for accents.

**No webfonts from CDN.** If the brand uses a proprietary font, either base64-inline
it in an `@font-face { src: url(data:font/woff2;base64,…) }` block inside the `<style>`
tag, or fall back to the system-font stack. Zero network dependencies is a hard rule —
a deck that needs internet to render is not a deck you can present in a basement
conference room.

---

## Contrast check

Before saving the HTML, verify:

- **Body text** (`--deck-text` on `--deck-bg`): ≥ 7:1 (AAA for projection).
- **Accent text** (`--deck-accent` on `--deck-bg`): ≥ 4.5:1 (AA).
- **Muted text** (`--deck-muted` on `--deck-bg`): ≥ 3:1 (still legible for metadata).

Use an inline programmatic check during generation (read RGB hex, compute relative
luminance, compute contrast ratio). If a brand color fails contrast, use it for
borders and accents only, and pick a derived lighter/darker tone for text.

A slide nobody can read from row 10 of the auditorium is not on-brand, regardless of
what the style guide says.

---

## Image handling

- **Screenshots:** base64-inline into `<img src="data:image/png;base64,…">`. Keep
  each image under 300KB encoded; if larger, downscale to 1600px wide max before
  encoding — the deck displays at ≤1000px anyway.
- **Founder photos:** 400×400 JPEG, base64-inlined. Under 120KB each after encoding.
- **Logos:** prefer SVG when available (inline it directly). Otherwise PNG base64.

If the founder provides image *file paths* instead of files, copy the images into
`pitch/` and reference them relatively (`src="photo.jpg"`). This keeps the deck
portable (you can share the `pitch/` folder) even when base64 isn't used. Document
the choice in `speaker-notes.md` so the founder knows the deck isn't fully single-file.
