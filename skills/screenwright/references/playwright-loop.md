# Playwright loop — the render / audit / screenshot mechanic

Loaded in Phase 4. These are the **spike-verified** calls (2026-06-17). Run them inside the
**verify sub-agent** so the iteration noise stays out of the main thread.

## What the spike proved (and corrected)

- **`file://` is BLOCKED** by the Playwright MCP (`Access to "file:" protocol is blocked`).
  The original "render via `file://`" assumption is wrong — **do not navigate to a file.**
- **`data:` URLs work but are fragile** (encoding corruption, size limits) — avoid.
- **`page.setContent(html)` is the render target** — clean, no origin issues, no size cap
  in practice.
- **axe-core injects via `page.addScriptTag({ path })`** from a local temp file (server-side
  read — bypasses CORS and the file-protocol block).
- The loop needs **`browser_run_code_unsafe`** — the only MCP tool that exposes `page` for
  `setContent` + `addScriptTag`. It is labeled RCE-equivalent; see the fallback below if
  it's disabled.

## One-time setup per run: fetch axe-core to a temp file

axe never ships in the output HTML — it's injected only at verify time, so D4's
"no external requests in the deliverable" is not violated. Fetch the source once:

```bash
curl -sSL https://cdn.jsdelivr.net/npm/axe-core@4/axe.min.js -o /tmp/screenwright/axe.min.js
```

If the fetch fails (offline): skip the a11y gate, mark **"a11y UNVERIFIED"** in the
manifest, and still run the fidelity/visual pass. Never dead-end.

## The per-cycle call (verified working)

For each in-scope viewport, set the viewport then render + audit + screenshot. `browser_run_code_unsafe`
with a `async (page) => {…}` function:

> **Land on `about:blank` before the first `setContent`.** `setContent` calls
> `document.open()`, which throws `Only HTML documents support open()` if the page is
> currently parked on a **non-HTML document** (an SVG, an image, an XML doc — a stuck
> earlier navigation). Dogfood-confirmed. `await page.goto('about:blank')` once at the top
> of the loop guarantees an HTML document; cheap and idempotent.

```js
async (page) => {
  await page.goto('about:blank');                             // ensure an HTML document
  await page.setViewportSize({ width: 1280, height: 900 });   // from breakpoints
  await page.setContent(HTML, { waitUntil: 'load' });          // render — NOT file://
  await page.addScriptTag({ path: '/tmp/screenwright/axe.min.js' });
  const violations = await page.evaluate(async () => {
    const r = await window.axe.run(document, {
      runOnly: { type: 'tag', values: ['wcag2a','wcag2aa','wcag21aa','wcag22aa'] },
      // for a component/fragment also pass:
      // rules: { region:{enabled:false}, 'landmark-one-main':{enabled:false},
      //          'page-has-heading-one':{enabled:false}, 'document-title':{enabled:false},
      //          'html-has-lang':{enabled:false}, bypass:{enabled:false} }
    });
    return r.violations.map(v => ({ id: v.id, impact: v.impact, nodes: v.nodes.length,
                                    help: v.help }));
  });
  return JSON.stringify(violations);
}
```

Then screenshot the same rendered page for the fidelity critique:
`browser_take_screenshot` (full page). Repeat per state (empty/loading/error) by setting the
corresponding HTML/markup variant before `setContent`.

Blocking = any violation with `impact` of `serious` or `critical` (see
[verification.md](verification.md)).

## Forcing interaction states for the screenshot

To verify focus visibility / hover / disabled, drive the state before screenshotting, e.g.
inside the same `run_code_unsafe` block: `await page.locator('button').first().focus();`
then screenshot. Hover: `.hover()`. These are advisory except **focus visibility**, which
blocks.

## Fallback if `browser_run_code_unsafe` is unavailable

Some hosts disable the unsafe tool. Degraded path: navigate to a `data:text/html;base64,…`
URL (base64 to avoid the encoding corruption plain `data:` hits), then use `browser_evaluate`
to inject axe by `fetch`-ing it (may hit CORS — if so, a11y degrades to UNVERIFIED) and
`browser_take_screenshot` for fidelity. State the degradation in the manifest. The visual
gate still runs; the machine gate may not.

## Sub-agent brief

Briefing conventions (Quick/Full) and the **no-nested-sub-agents** invariant live in
`sub-agent-coordinator` — load it rather than re-deriving. The verify sub-agent's brief:
the final HTML, the DESIGN.md tokens, `a11y.wcag` + `breakpoints`, the surface type, the
list of in-scope viewports/states, and the reference image (mode A1). It returns: the
(possibly fixed) HTML, the violation/fidelity findings, and the manifest — nothing else.
