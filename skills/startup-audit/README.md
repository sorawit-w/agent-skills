<p align="center">
  <img src="../../assets/startup-audit-li.svg" alt="startup-audit — fast code-grounded triage: Continue / Pivot / Kill from a codebase or URL" width="100%">
</p>

# startup-audit

Point it at an **already-built** product — a codebase and/or a live URL — and get a
fast, opinionated **Continue / Pivot / Kill** triage call. `startup-audit` infers the
business model *from what's actually built*, diffs coded reality against the claimed
story, and ships a single self-contained interactive HTML dossier that **opens with
the verdict** (a Red/Amber/Green band + the reason + a plain-English "this is opinion,
not advice" disclaimer).

It's the **built-artifact sibling of [`startup-grill`](../startup-grill/README.md)**:
this gives a *fast code-grounded triage*; grill gives the *deep adversarial verdict*
on belief artifacts (a Lean Canvas or pitch deck). For a consequential Kill or Pivot,
this skill points you to grill to confirm.

> **Install the full plugin, not just this skill.** `startup-audit` reads reference
> files from `team-composer`, `validation-canvas`, and `riskiest-assumption-test`. A
> per-skill `npx` install copies only this folder and breaks those reads — the skill
> refuses to run with a clear message. Install the whole `agent-skills` plugin.

## Why this exists

The repo's startup pipeline is all **pre-build belief work**, and `startup-grill` —
the verdict skill — only reads *text artifacts* (canvas / deck). Neither could take a
**built** product and say "keep going, change direction, or stop." `startup-audit`
reads the code/URL and gives that call, grounded in what's actually there.

## What it does

- **Extracts** deterministic business signal from the codebase — dependency
  manifests, schema, routes, auth/tenancy, `.env`, money code, README claims, commit
  recency (JS/TS + Python first-class; generic fallback otherwise).
- **Infers** the business model into a **Lean Canvas** (`validation-canvas`'s exact
  nine blocks), every field tiered **observed / inferred / unknown** and pinned to a
  **provenance pointer** — no provenance, no claim.
- **Diffs** coded reality against the claimed story, **bidirectionally** (over-claimed
  vs under-marketed) — the headline evidence.
- **Triages** through domain-aware lenses auto-composed from the inferred signals
  (single-pass), tagging findings by severity × fixability.
- **Calls it** — a **Continue / Pivot / Kill** verdict + **R/A/G** band, with the
  evidence-confidence attached (a Kill on mostly-`unknown` signals self-flags low
  confidence), a reason citing specific findings, and a mandatory **opinion-not-advice
  disclaimer**. Pivot directions are code-grounded.
- **Ships** a self-contained interactive HTML dossier (verdict on top; expandable
  provenance; tier filter; print-clean) + an `inferred-canvas.md`.

## What it doesn't do

- It does **not validate an idea** — there has to be a built artifact to read.
- It does **not give a *deep adversarial* verdict** — that's `startup-grill`'s 3-round
  job; this is a fast first read that *routes to* grill for consequential calls.
- It does **not give investment / legal / financial advice** — every verdict is
  explicitly opinion, with no valuation or outcome guarantees.
- It does **not measure real market demand** — code can't prove a market; the unknown
  blocks say so and route to testing.
- It does **not rebuild UI/UX review** — it delegates that to `ai-ux-review`.

## When to use it

- "Grill my startup from this repo / URL — should I continue, pivot, or kill it?"
- "Score my built product from the codebase."
- "Does the code match the pitch, and is it worth continuing?"
- A founder/investor pointing Claude at a built product for a fast read.
- Just the evidence, no verdict? Ask for **diligence-only mode**.

## When not to use it

- Pre-build idea validation → [`startup-launch-kit`](../startup-launch-kit/README.md)
  / [`validation-canvas`](../validation-canvas/README.md).
- A **deep adversarial verdict** on a canvas/deck, or to **confirm** a Kill/Pivot →
  [`startup-grill`](../startup-grill/README.md).
- AI-feature UX/eval review → `ai-ux-review` / `ai-eval-review`.
- Auditing a `SKILL.md`'s rule adherence → [`skill-evaluator`](../skill-evaluator/README.md).

## How it works

1. **Phase 0 — Resolve paths + mode + pre-flight.** Detect verdict vs diligence-only
   mode; fail loud if a required sibling is missing; capability-gate SocratiCode +
   URL-fetch with fallbacks.
2. **Phase 1 — Extract** signal from the codebase (secrets redacted to names only).
3. **Phase 2 — Infer** into the Lean Canvas + the bidirectional build-vs-claim diff.
   Confidence is *derived from provenance, never judged.*
4. **Phase 3 — Triage panel + verdict synthesis:** lenses emit findings tagged by
   severity × fixability; the verdict (Continue/Pivot/Kill + R/A/G + confidence) is
   derived from those tags and cites specific findings. *(Skipped in diligence-only
   mode.)*
5. **Phase 4 — Render** the self-contained interactive HTML dossier (verdict on top)
   + the `inferred-canvas.md`.

## Design choices worth knowing

- **Fast triage, honestly labeled.** Stage 2 is a single pass, not grill's 3-round
  debate — so the verdict is framed as a *first read*, and Kill/Pivot route to grill
  for the adversarial confirmation. Feed-don't-compete, at a new layer.
- **The headline carries the call; R/A/G is just heat.** Continue-with-conditions and
  Pivot are opposite actions — the headline says which; the band is a glance-level
  color, never the recommendation. No numeric score (avoids false precision).
- **Provenance is the integrity contract.** `provenance == null → cannot claim`, and a
  verdict on mostly-`unknown` evidence downgrades its own confidence.
- **Opinion, not advice — by construction.** A disclaimer ships with every verdict and
  banned terms ("valuation", "guarantee", "will succeed/fail") are refused.

## Install

```
/plugin marketplace add sorawit-w/agent-skills
/plugin install agent-skills@sorawit-w
```

Then point it at a built product ("grill my startup from this repo"). Install the
full plugin — not just this skill (see note above).

## Cross-skill integration

| Skill | Relationship |
|---|---|
| [`startup-grill`](../startup-grill/README.md) | **Sibling verdict skill, split by input + rigor.** This = fast code/URL triage; grill = deep 3-round adversarial verdict on belief artifacts. A Kill/Pivot here recommends grill to confirm; the verdict vocabulary is aligned (not forked). |
| [`validation-canvas`](../validation-canvas/README.md) | Infers into its exact Lean Canvas headings; writes a separate `inferred-canvas.md`, offers to seed `validation-canvas.md` if none exists (never overwrites). The seeded file is the bridge that lets grill confirm a Kill/Pivot. |
| [`riskiest-assumption-test`](../riskiest-assumption-test/README.md) | **Pointer handoff** — the dossier recommends running RAT on the `unknown` blocks; RAT reads its own input file, not this skill's. |
| [`pitch-deck`](../pitch-deck/README.md) | Consumes the seeded `validation-canvas.md` / diff for a deck grounded in coded reality. |
| [`startup-launch-kit`](../startup-launch-kit/README.md) | **Reuses this skill as its existing-project code-reader.** Invokes it with `mode=diligence` (no verdict) to seed the canvas, then runs the full kit on top. This skill stays the standalone triage; the kit is the full-pipeline path. |
| [`team-composer`](../team-composer/README.md) | Reads its `role-personas.md` for the triage lenses (read, not invoked). |
| `ai-ux-review` / `ai-eval-review` | Conditional — invoked when AI features are detected; the dossier embeds their output. |
| [`skill-evaluator`](../skill-evaluator/README.md) | To audit this skill's own rules (the provenance gate, the verdict-cites-a-finding rule, the diligence-only flag). |

## Status and scope

- **v1.** Supported: JS/TS + Python first-class extraction + generic fallback;
  codebase-primary with optional opt-in URL; a fast Continue/Pivot/Kill + R/A/G
  verdict (with a diligence-only no-verdict flag); interactive self-contained HTML
  dossier; separate `inferred-canvas.md` with offer-to-seed.
- The verdict is a **fast triage opinion**, not advice and not a substitute for the
  deep `startup-grill` confirmation or qualified human advisors.
- Not yet: first-class extractors beyond JS/TS + Python; multi-product audits;
  measuring real traction beyond what the product instruments.

## Contributions

Not accepting external contributions right now.

## License

MIT
