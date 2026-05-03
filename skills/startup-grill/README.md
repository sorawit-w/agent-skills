<p align="center">
  <img src="https://raw.githubusercontent.com/sorawit-w/agent-skills/main/assets/startup-grill-li.svg" alt="startup-grill — probe for failure, ship the kill report" width="100%"/>
</p>

# startup-grill

A Claude Code skill that adversarially probes a startup idea with a panel of domain-aware grillers (VC partner, growth marketer, founder strategist, UX researcher, plus a flexible technical-or-brand fifth seat and up to 3 domain specialists), and ships a structured kill report ranked across two axes — **severity** (lethal vs material) and **fixability** (fixable vs unfixable). Default mode is one-shot: probe → forced steelman defense → verdict → file. Optional second mode is interactive defense, where the founder picks a weakness, brings new evidence, and the relevant panelists re-probe that line item only.

## Why this exists

"Tell me what you think of my startup" is almost never really about feedback. The founder either wants validation or wants to know what would kill it. Most one-shot prompts produce the validation version, even when the founder asked for the kill version — because collaborative roles default to constructive, and constructive defaults to polite, and polite suppresses the lethal weakness that actually matters.

The fix is structure, not harshness: a fixed adversarial panel that probes for failure, a forced-steelman defense round so the panel hears the strongest founder rebuttal before issuing a verdict, and a deliverable shape (the kill report) that ranks weaknesses on two axes the founder actually cares about — *will this kill us?* and *can we do something about it?*

That's what this does. It's not a thinking partner. It's the panel after a deck got handed around the table.

## What it does

- **Reads upstream artifacts** if present — `validation-canvas.md` (especially the Stress Tests section, which is direct grilling ammunition), `rat/assumption-test-plan.md` (top-3 hypotheses + results — invalidated results that haven't propagated to the canvas are red flags), `pitch/deck.html` and speaker notes, `brand-kit/brand-brief.md`. Refuses to grill on a single sentence; minimum input is one paragraph each on Problem, Solution, ICP, GTM motion, and Team.
- **Classifies the variant** — idea / pre-seed / seed / Series A+ — with one mandatory question. Variant tunes evidence thresholds (LOIs vs cohort retention vs revenue curve), not panel composition.
- **Resolves the panel deterministically** — 4 fixed core roles (`@vc_partner`, `@growth_marketer`, `@startup_strategist`, `@ux_researcher`), one flex slot 5 that resolves to `@senior_software_architect` (technical due diligence) by default and to `@brand_strategist` for consumer-brand-dominant products, plus 0–3 specialists injected from signals (legal, clinical, security, AI safety, game design, etc.). Cap is 8 total panelists.
- **Imports persona definitions from `team-composer`'s `references/role-personas.md`** as the canonical base, then applies grill-mode overlays so each panelist probes for failure rather than collaborates. Universal grill posture: probes for failure, demands evidence, states severity declaratively, names failure modes specifically, closes with a falsifier.
- **Runs three rounds** — Round 1 probes (60–100 words per panelist, falsifier required), Round 2 forced steelman defense using only evidence in the brief (probes that the brief credibly answers get downgraded; probes that survive stand), Round 3 synthesis with `@startup_strategist` assembling sections and `@vc_partner` writing the verdict.
- **Ships a structured kill report** at `grill/kill-report.md` with seven required sections in fixed order: Verdict / Lethal & Fixable / Lethal & Unfixable / Material & Fixable / Diligence Asks / Panel / Iteration Evidence. Verdict label is one of four canonical labels: `Investable as-is`, `Investable with conditions`, `Pivot signal`, `Pass`. Iteration Evidence (added in v2.0.0) yellow-flags pristine pipelines where the canvas wasn't updated after RAT testing.
- **Refuses to ship a soft report** — Round 1 must surface at least one lethal-fixable or lethal-unfixable read; if every probe is `material` or `pass`, the panel was too soft and Round 1 re-runs with sharper posture. The skill enforces this before assembling the file.
- **Offers interactive defense mode** after the report ships — the founder picks a weakness number (e.g., `L1`), brings new evidence (a metric, a customer quote, a teardown), the relevant 1–2 panelists re-probe that line, and the verdict on that item only updates. Other items stay frozen. A single weakness can be defended at most 3 times per session before the verdict stands.
- **Logs defenses to `grill/defense-log.md`** — append-only, dated. The kill report's affected line item gains a `Defended on YYYY-MM-DD` pointer rather than being rewritten in place.
- **Composes downstream of `validation-canvas`, `riskiest-assumption-test`, and `pitch-deck`** — reads their outputs as input, surfaces the Stress Tests, RAT results, and slide-contract anti-patterns as starting probes. Composes upstream of fix work — when the verdict is `Pivot signal`, the kill report's `Suggested attacks` route to `team-composer` for a multi-role workshop on the new direction.

## What it doesn't do

- **Brainstorm or shape the idea.** Use `team-composer` (or `superpowers:brainstorming` if installed) for that. Grilling a half-formed idea produces a kill report full of *not enough information* findings, which is worse than no kill report.
- **Build artifacts.** No validation canvas, no test plan, no deck, no brand kit — those route to `validation-canvas`, `riskiest-assumption-test`, `pitch-deck`, and `brand-workshop` respectively. Run those first; grill after.
- **Improve the idea.** The kill report's `Suggested attack` lines are next moves, not improvements the skill makes for you. The founder acts on them, then optionally re-grills.
- **Soften the verdict on request.** "Be nicer" is rejected. The report is what it is. The interactive defense mode is the right path to update verdicts — bring evidence, not vibes.
- **Operate on a single sentence.** Refuses inputs below the minimum brief threshold. Garbage in produces a generic kill report; the skill won't pretend otherwise.
- **Replace human due diligence.** The cap of 3 specialists means real-world deals will surface concerns this run didn't cover. The kill report names what got cut by the cap so the user knows what's missing.

## When to use it

- **You have a startup idea, deck, or business model and want it probed adversarially** before you commit time, money, or a fundraise.
- **You want a verdict you can act on** — `Investable as-is`, `Investable with conditions`, `Pivot signal`, or `Pass` — not a list of "thoughts to consider".
- **You want the lethal weakness named declaratively**, with a falsifier (what evidence would change our minds) attached, so you know exactly what to bring to the next conversation.
- **You want one or two of the weaknesses re-probed** after you bring evidence, without rerunning the whole grill.

## When not to use it

- **You're still shaping the idea.** Brainstorm first; grill after the idea has structure.
- **You want constructive feedback or a plan.** Use `team-composer` with `scope=review` or `scope=planning`. The grill produces a verdict, not a plan.
- **You want a deck, test plan, or canvas built.** Use `pitch-deck`, `riskiest-assumption-test`, or `validation-canvas`. Then grill.
- **The team you're assembling is for a non-startup decision** (architecture review, hiring debate, regulatory analysis). Use `team-composer`.

## How it works — 4 phases

1. **Intake.** Read the working directory for `validation-canvas.md`, `rat/assumption-test-plan.md`, `pitch/deck.html`, `brand-kit/brand-brief.md`. Run the iteration-evidence check. Classify the variant (idea / pre-seed / seed / Series A+). Detect signals.
2. **Panel resolution.** 4 fixed core + slot 5 resolved by detection rule + 0–3 specialists injected from signals + cap-and-trim if specialists exceed 3. Show the panel summary block to the user before grilling — they can challenge the panel before Round 1 starts.
3. **Grilling — three rounds.**
   - **Round 1 (Probe).** Each panelist contributes one probe per startup-axis they own. Per-probe shape: probe / what I'm looking for / read (lethal-fixable | lethal-unfixable | material | pass) / falsifier.
   - **Round 2 (Forced steelman defense).** The skill responds *as the founder would*, using only evidence in the brief. Probes the brief credibly answers get downgraded; probes that survive stand.
   - **Round 3 (Synthesis).** `@startup_strategist` assembles the report sections; `@vc_partner` writes the 3–6 sentence verdict.
4. **Ship + invite defense.** Write `grill/kill-report.md`, run the verifier checklist, present the file. Close with the interactive-mode invitation. If the founder picks a weakness and defends with new evidence, run a defense round and append to `grill/defense-log.md`.

## What the output looks like

A single file by default, with a second file for interactive defense logs:

```
grill/
├── kill-report.md     — Verdict, Lethal & Fixable, Lethal & Unfixable, Material & Fixable, Diligence Asks, Panel, Iteration Evidence
└── defense-log.md     — (only if interactive mode engages) dated defense rounds with re-probe outcomes
```

The kill report ranks weaknesses on **two axes** — severity (lethal vs material) and fixability (fixable vs unfixable) — then names them in four sections that read in priority order: *attack now / pivot signal / roadmap items / diligence asks*. Verdict label sits at the top, ≤ 6 sentences, leading with one of four canonical labels and naming a single specific weakness from the body. No hedged verdicts.

## Design choices worth knowing

- **Fixed grill core, flex slot 5.** Universal axes (capital, distribution, narrative, user reality) are always probed by the same four roles. The fifth slot resolves to *technical due diligence* by default and to *brand-strategist* only for consumer-brand-dominant products that aren't regulated and don't make novel ML claims. This avoids the failure mode where a consumer brand startup gets technical-only grilling, or a deeply technical startup gets brand-only grilling.
- **Symmetric specialist injection.** When slot 5 flips to one lens, the other becomes a *forced specialist* if signals warrant — a consumer-brand startup with high technical complexity gets `@senior_software_architect` injected as a specialist, and vice versa. The demoted axis still gets covered.
- **Two axes for ranking, not one.** A flat severity list tells the founder "you're dying" without telling them what to do. A flat fixability list buries lethal-unfixable findings under easy wins. The 2×2 split forces the report to answer two questions the founder actually asks: *what kills me?* and *what do I do Monday morning?*
- **Persona import, posture overlay.** The skill imports `team-composer/references/role-personas.md` as the canonical persona base — same role catalog, no drift. Then applies grill-mode overlays: every panelist probes for failure, demands evidence, states severity declaratively, names failure modes specifically, closes with a falsifier. Politeness norms that suppress grilling value (compliment sandwiches, "have you considered…", recursive uncertainty) are explicitly forbidden.
- **Forced steelman defense.** Round 2 isn't optional. The skill responds *as the founder would* using brief evidence before any verdict, so the panel hears the strongest rebuttal before the verdict ships. Probes the brief credibly answers get downgraded; probes that survive stand. This prevents lazy lethal calls.
- **One-shot first, interactive on request.** Founders bail more often than not after the kill report. Default mode delivers immediate value; interactive mode is opt-in and re-probes one weakness at a time. A single weakness gets defended at most 3 times per session before the verdict stands — to prevent infinite re-debate.
- **Vibes-only defenses rejected.** Interactive defense mode requires *new information* — a metric, a quote, an artifact. Argument without evidence gets the response: *"You pushed back, but I didn't see new evidence. The verdict stands."* The defense round is for evidence-driven updates, not for arguing the panel into softer language.
- **Boundaries published, not implied.** The STOP gate at the top of `SKILL.md` enumerates the five most common wrong-skill scenarios (brainstorming, building, plan review, brand voice review, diligence prep) and routes each to the right skill. The skill knows what it isn't, in writing.

## Install

This skill is distributed as a [Claude Code](https://docs.claude.com/en/docs/claude-code) plugin inside the [`sorawit-w/agent-skills`](https://github.com/sorawit-w/agent-skills) marketplace. From Claude Code or Cowork:

```
/plugin marketplace add sorawit-w/agent-skills
/plugin install agent-skills@sorawit-w
```

Once installed, Claude picks the skill up automatically from the description in its `SKILL.md` frontmatter. Invocation triggers on phrases like "grill my startup", "grill this idea", "stress-test my pitch", "kill my idea", "pre-mortem my startup", "what would a VC hate about this", "tear apart my deck", "where would this fail", or "is this fundable".

## Cross-skill integration

| Skill | When it kicks in |
|---|---|
| [`team-composer`](../team-composer/README.md) | Instead of this skill when the user wants brainstorming, planning, or constructive review. After this skill when the kill report's `Suggested attack` lines need a multi-role workshop. |
| [`validation-canvas`](../validation-canvas/README.md) | Upstream input. If `validation-canvas.md` exists, this skill reads its Stress Tests + un-relieved Pains as direct grilling ammunition. After a `Pivot signal` verdict to rebuild the canvas. |
| [`riskiest-assumption-test`](../riskiest-assumption-test/README.md) | Upstream input. If `rat/assumption-test-plan.md` exists, this skill reads top-3 hypotheses + results. The iteration-evidence check yellow-flags pristine pipelines. After a verdict that names untested assumptions. |
| [`pitch-deck`](../pitch-deck/README.md) | Upstream input. If `pitch/deck.html` exists, this skill probes the deck's required-slot answers. After this skill when the kill report demands a re-cut deck. |
| [`brand-workshop`](../brand-workshop/README.md) | Upstream input when slot 5 = `@brand_strategist`. The panel reads `brand-brief.md`'s Positioning section. |
| [`skill-evaluator`](../skill-evaluator/README.md) | When you want to audit this skill end-to-end. Good targets: the verdict-vs-body consistency rule, the no-lethal-skip rule, the interactive-invitation rule. |
| `superpowers:brainstorming` (if installed) | *Before* this skill when the user is still shaping the idea. |

## Companion plugins

This skill sits at the **end** of the startup-artifact chain in this repo. The pipeline:

```
brand-workshop ──▶ validation-canvas ──▶ riskiest-assumption-test ──▶ pitch-deck ──▶ startup-grill
 (identity kit)    (Lean Canvas + VPC)    (test plan + results)         (HTML deck)    (kill report)
```

The first four *produce*; this one *probes*. Run them in order in the same working directory — they compose via shared folder conventions (`brand-kit/`, `validation-canvas.md`, `rat/`, `pitch/`, `grill/`). Each is its own plugin and triggers on its own description; you don't have to chain them manually. Pipeline gates are weighted: light → medium → heavy → light. Loop-back is first-class — invalidated assumptions trigger canvas updates, not pipeline restarts.

## Status and scope

v0.1. The fixed grill core (4 roles + slot 5) and the specialist injection table cover the canonical startup framings (B2B SaaS, dev tools, consumer brand, regulated consumer, AI consumer, indie game, biotech, fintech, climate). Edge cases that don't fit the matrix are surfaced explicitly — the kill report's panel section names *why* slot 5 resolved to what it did, so drift is visible in regression review.

- **Supported:** idea / pre-seed / seed / Series A+ variants; fixed and adaptive panels; one-shot and interactive defense; composition with `validation-canvas`, `riskiest-assumption-test`, `pitch-deck`, and `brand-workshop` upstream artifacts; iteration-evidence check (v2.0.0).
- **Adaptive:** slot 5 resolution by signal; specialist injection by signal; symmetric specialist forcing when one lens loses the core slot.
- **Not supported:** softening the verdict by request; replacing human due diligence; grilling on inputs below the minimum brief threshold; auto-engaging interactive mode without an explicit defend message.

## Contributions

Not accepting external contributions right now. Feel free to fork.

## License

MIT — see the [LICENSE](https://github.com/sorawit-w/agent-skills/blob/main/LICENSE) file at the repo root.
