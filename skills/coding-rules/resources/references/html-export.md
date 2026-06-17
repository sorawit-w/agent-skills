# HTML Export — Shareable Document Snapshots

The agent's contract for producing a single self-contained HTML version of a Markdown document, on explicit request.

---

## When This Fires

Only when the developer **explicitly asks** for an HTML, shareable, or printable version of an existing document — e.g. "give me an HTML version of the postmortem", "export the roadmap as something I can send", "make this printable".

- This is **opt-in**. Never produce an HTML export automatically, and never as a substitute for the Markdown file.
- It applies to documents already authored as Markdown — postmortems, implementation plans, roadmaps, recommendations, design notes, status write-ups.
- It is **not** a website builder and **not** a document generator. `coding-rules` stays `coding-rules`. The export renders a document that already exists; it does not invent one.

> **One sanctioned exception:** the `audit` sub-command (`references/audit.md`) renders its report to HTML *automatically* as part of its contract — that auto-render is not this opt-in document-export flow. It **reuses the machinery below** (template, placeholder fill, DESIGN.md token override) but not the opt-in firing policy, and it adds escaping of untrusted repo content. No other flow may auto-render.

---

## Markdown Stays Canonical

The `.md` file is the source of truth. The `.html` is a **point-in-time snapshot** of it.

- Write the `.html` **alongside** the `.md` — `postmortem.md` → `postmortem.html`. Never replace or delete the Markdown.
- Do **not** maintain the two in parallel. When the document changes, the developer edits the `.md` and re-exports. A stale `.html` is expected and harmless — it is a photograph, not a mirror.
- The export footer states this in the artifact itself, so anyone who opens the HTML knows which file is authoritative.

---

## What "Self-Contained" Means

One file, zero network dependencies — matching the convention every HTML-producing skill in this repo already follows (`pitch-deck`, `validation-canvas`, `riskiest-assumption-test`).

- A single `.html` file. All CSS inline in one `<style>` block. No external stylesheets, no CDN links, no separate `.css` / `.js` files.
- No build step, no framework, no bundler. System font stack — do not fetch web fonts.
- Vanilla inline JavaScript **only** if the document genuinely needs interactivity (e.g. a collapsible section, a sortable table). Most exports need none. When in doubt, ship zero JS.
- The result must open offline, survive being emailed or dropped in a chat, and print to PDF cleanly from the browser.

---

## Styling — DESIGN.md First

The export has one styling decision: where the stylesheet's tokens come from.

1. **`DESIGN.md` exists at repo root** → derive the stylesheet's tokens (colors, typography, spacing, radius) from it. `DESIGN.md` is the single design authority — see `references/design-md.md`. Do not invent alternative tokens.
2. **No `DESIGN.md`** → use the bundled default stylesheet in `templates/html-export.html.template`.

The bundled template exposes its tokens as CSS custom properties in `:root`. That `:root` block **is** the override surface: when `DESIGN.md` is present, overwrite those variables with `DESIGN.md` tokens and change nothing else. One override point, deterministic result.

---

## How to Produce It

Deterministic, not improvised:

1. Convert the Markdown body to HTML with a standard converter available in the environment (`pandoc`, `markdown-it`, Python `markdown`, etc.). The body conversion is mechanical — `## H2` → `<h2>`.
2. Wrap the converted body in `templates/html-export.html.template`, filling its placeholders (`{{TITLE}}`, `{{CONTENT}}`, `{{SOURCE}}`, `{{DATE}}`).
3. Apply tokens per **Styling — DESIGN.md First** above.

Do **not** hand-author the HTML tag by tag. Hand-writing drifts in style on every run and burns tokens — the fixed template is what makes every export look the same. The styling stays deterministic even when the body converter is not pinned.

---

## Do Not Reach for UI Skills

`ui-ux-pro-max`, `taste-skill`, `impeccable`, and similar are **interface** tools — they build websites, dashboards, and app UIs with picked palettes and stacks. A document export is typography and a print stylesheet, not an interface.

- Using them over-tools the job and pulls toward framework stacks, fighting the self-contained constraint.
- They introduce a second design authority that conflicts with `DESIGN.md`. `DESIGN.md` (or the bundled default) is the only styling input.

---

## See Also

- `references/design-md.md` — the `DESIGN.md` design-token authority this export defers to.
- `templates/html-export.html.template` — the bundled wrapper + default document stylesheet.
