# Playwright grader shape

Concrete grader template for skills that produce **web output** (HTML, SVG, rendered DOM). Companion to [`calibration-loop.md`](./calibration-loop.md) — that file explains *when* to use a gold+negative pair; this one shows *how* the grader is shaped.

Pattern adapted from [`GoogleChrome/modern-web-guidance-src`](https://github.com/GoogleChrome/modern-web-guidance-src) (Apache-2.0).

## When to recommend this

Recommend in findings when the target skill produces gradable web output AND the audit surfaced an assertion that needs a calibrated discriminator. Examples in this repo: `pixel-art` (rendered SVG), `pitch-deck` (rendered HTML deck), `validation-canvas` + `ai-ux-review` + `ai-eval-review` (rendered HTML reports).

Do NOT recommend for non-web skills — there is no rendered surface to assert against.

## Shape

A grader pair lives next to the skill, not inside `skill-evaluator`. Two files plus a runner:

```
skills/<target-skill>/
  evals/
    <rule-name>/
      gold.html               # rendered output following the rule
      negative.html           # same output deliberately broken on the rule's dimension
      <rule-name>.spec.ts     # Playwright assertions
```

The `.spec.ts` runs the same assertions against both fixtures and inverts the expected result for `negative.html`. Pseudocode:

```ts
import { test, expect } from '@playwright/test';

const fixtures = [
  { path: 'gold.html', shouldPass: true },
  { path: 'negative.html', shouldPass: false },
];

for (const { path, shouldPass } of fixtures) {
  test(`${path} — accessible error announcement`, async ({ page }) => {
    await page.goto(`file://${__dirname}/${path}`);
    const input = page.locator('input[aria-invalid="true"]');
    const matched = await input.count() > 0;
    if (shouldPass) {
      expect(matched).toBe(true);
    } else {
      expect(matched).toBe(false);
    }
  });
}
```

## Assertion targets that travel well

These are the assertion dimensions Modern Web Guidance's graders use most heavily. They translate directly to web-output skills in this repo:

- **Computed styles** — `await element.evaluate(el => getComputedStyle(el).<property>)`. Use for layout / color / spacing rules.
- **Accessibility tree state** — `aria-*` attributes, focusable order, role semantics. Use for accessibility-rule assertions.
- **Runtime behavior** — clicks / focus / scroll events triggering the right DOM mutations. Use for interaction-pattern rules.
- **Resource load behavior** — network panel / `performance.getEntriesByType('resource')` for fetch priority, preloads, deferred work.

What does NOT travel: visual-diff / pixel-perfect assertions. Pixel diffs are too brittle for fixture pairs that share most-but-not-all DOM; prefer attribute and computed-style assertions.

## Where to run

Local invocation: `pnpm exec playwright test` from the skill's `evals/<rule-name>/` directory. CI: optional — most of this repo's skills don't have CI gates, and ad-hoc local runs are usually enough for fixture pair calibration.

## Attribution

Grader shape (paired gold + negative HTML fixtures, Playwright assertions on computed styles / a11y tree / runtime behavior, the `shouldPass` inversion pattern) adapted from `GoogleChrome/modern-web-guidance-src` — see their `guides/grader-gen.ts`, `guides/negative-gen.ts`, and `guides/template.grader.ts`. Apache-2.0. Re-expressed here for skill-output audits rather than web-platform agent benchmarking; the assertion-target catalog above is this repo's own selection of what transfers cleanly.
