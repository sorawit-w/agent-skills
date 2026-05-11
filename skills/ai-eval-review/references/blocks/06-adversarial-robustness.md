# Block 6 — Adversarial & Robustness

## Definition

How the AI fails when stressed. Covers prompt injection (for LLMs), jailbreak resistance, out-of-distribution (OOD) inputs, distribution shift, adversarial inputs (classical ML), and red-team coverage. This is the measurement-side counterpart to `ai-ux-review` Block 6 (Output Integrity) — that block asks *did you design for hallucination / injection / autonomy*; this block asks *can you measure resistance?*

If `ai-ux-review.md` exists, mitigations named in its Block 6 should have corresponding eval signal here. Mitigations without eval are theater — surface this in the Phase 2 cross-block check.

## Primary probe

> "Name one input that would make your AI fail catastrophically. Now: how would you know if a production user sent that input today? And what's your eval signal that the model resists similar inputs?"

## Secondary probes (LLM-specific)

1. **Prompt-injection eval.** Do you have a red-team set of injection attempts (direct, indirect, content-embedded)? What's the resistance rate? Where do you measure (pre-prompt sanitization, mid-generation, post-output check)?
2. **Jailbreak resistance.** Does the model produce policy-violating outputs under adversarial pressure (role-play, multi-turn escalation, unicode obfuscation, encoding tricks)? Measured on a standardized set or custom?
3. **Multi-turn drift eval.** Across 20-turn conversations, does the model stay within initial constraints? Re-grounding strategy evaluated?
4. **OOD detection.** Does the model know when it's out of distribution (refuse / hedge), or does it confidently confabulate? Measured how?
5. **Robustness to user-side variation.** Typos, abbreviations, dialect, non-native phrasing, emoji-heavy input — does the model degrade gracefully or fail brittly?

## Secondary probes (agentic-specific)

6. **Action-space eval.** For each tool the agent can call, are there eval cases where the wrong tool is called? Where the right tool is called with wrong arguments? Where a chain-of-tools loops?
7. **Confirmation-gate eval.** For irreversible actions, does the agent always pause for confirmation? Measured at the boundary cases?
8. **Tool-use boundary.** Eval cases where the agent is tempted to use a tool out-of-scope (e.g., calling a write API when the user only asked to read)?

## Secondary probes (classical-ML)

9. **Adversarial-input eval.** Perturbation-resistance (FGSM, PGD)? OOD detection accuracy? Calibration under distribution shift?
10. **Distribution shift over time.** Synthetic shift eval (train → eval distribution gap simulated)? Production-shift measurement (vs. training distribution)?

## General secondary probes

11. **Red-team coverage.** Who has tried to break this? Internal red-teamers, external bug-bounty, automated adversarial generation? Coverage is uneven — name the gaps.
12. **Severity tiering.** Failure modes ranked: "embarrassing" vs. "user-harming" vs. "company-liability" vs. "regulatory-trigger." Eval rigor should be proportional to severity.

## Acceptance criteria

- [ ] **At least one named adversarial eval set** per applicable category (injection for LLM, perturbation for classical, etc.). Or explicit "we don't yet have one" gap.
- [ ] **Resistance rate** measured for the highest-severity failure mode.
- [ ] **OOD or distribution-shift signal** for ML-typed products; **multi-turn drift signal** for LLM-typed products.
- [ ] **Red-team coverage** named — who tested, where the gaps are.
- [ ] **Severity tiering** applied — eval rigor proportional to consequence.
- [ ] **Cross-check with `ai-ux-review` Block 6** (if present): named mitigations have measurement signal here.

## Common gap patterns

- **"The model is good."** Same dominant failure mode as ai-ux-review Block 6. Benchmark accuracy doesn't capture adversarial robustness. If the only eval is MMLU or accuracy, this block has a gap.
- **Injection eval as occasional spot-check.** Engineers try a few injection attempts, conclude "looks fine," ship. No labeled eval set, no resistance-rate measurement. Common gap.
- **Jailbreak eval against known prompts only.** Tested on AdvBench, HarmBench, Anthropic-published red-team set — but no custom set for the specific product surface. Generic robustness doesn't transfer to product-specific failure modes.
- **Multi-turn drift never measured.** Eval set is all single-turn. The model is shipped for multi-turn use. Drift goes undetected until a customer reports it.
- **OOD handling missing.** Model has no behavior for "I don't know" — confidently confabulates. Detected only via support tickets.
- **Action-space eval missing (agentic).** Agent can call 20 tools; eval set is for "happy path" 1-2 tools. The 19th tool is where things go wrong silently.
- **Red-team is a single internal pass.** One engineer spent a day trying to break it, found 3 things, fixed them. Adversarial coverage stays at "internal-engineer's-imagination."
- **No severity tiering.** All failures treated as equally important; eval effort distributed evenly. High-severity failures get same rigor as embarrassing-but-harmless ones; the wrong things get the most attention.

## Worked example (LLM email drafting)

| Field | Filled |
|-------|--------|
| Injection eval set | "100-example custom set: direct injection ('ignore previous'), indirect (injection embedded in voice-sample emails — the highest-likelihood real-world vector for this product), and content-embedded ('the email I'm drafting should ignore my system prompt'). Resistance rate: 96% direct, 84% indirect, 91% content-embedded. **[Gap]** Indirect injection from voice samples is the weakest cell — needs work." |
| Jailbreak resistance | "Tested against AdvBench (subset of 50) + custom 30-example set focused on email-specific abuses (defamatory drafts, harassment, impersonation). Generic AdvBench resistance: 88%. Custom email-abuse resistance: 94%. Higher on custom because the product surface narrows the threat space." |
| Multi-turn drift | "Eval set has 20 conversations of 5-8 turns. Drift measured by: does the model still respect the user's stated voice samples 5 turns in? Result: 78% adherence at turn 5; drops to 51% at turn 8. **[Gap]** Drift-resistance is unmitigated; re-grounding strategy is queued but not shipped." |
| OOD detection | "Eval set includes 20 'no usable ask' inputs (gibberish, contradictions, unparseable). Model declines or asks for clarification in 80% of cases; confabulates in 20%. Acceptable for v1; flag for monitoring." |
| Robustness to user-side variation | "Tested on dialectal variation (small set, 30 examples). Performance gap measurement deferred — flagged for Block 5 (Cohort breakdown) as a coverage gap." |
| Red-team coverage | "Internal engineer red-team (1 day, ~50 attempts). Public-facing beta launch is the de-facto next round. **[Gap]** No external red-team contracted; injection eval relies on internally-imagined attacks." |
| Severity tiering | "Severity tiers: (1) Embarrassing — model misuses voice; tolerated, not high-priority. (2) User-harming — model produces draft with factual claims user didn't make (Block 6 of ai-ux-review's mitigations target this); high priority, measured tight. (3) Company-liability — model produces defamatory or harassing content; jailbreak resistance must be high; current 94% on custom set acceptable but watched. (4) Regulatory — no known regulatory trigger." |
| Cross-check with ai-ux-review Block 6 | "ai-ux-review Block 6 names 'structured extraction of factual claims first, then prose generation' as the hallucination mitigation. This skill measures: hallucination rate on 'with-factual-claims' cohort = 6.4% (Block 5). Mitigation has eval signal. ✓" |

## When the block is "complete enough"

When at least one adversarial eval set exists per applicable category, the highest-severity failure mode has measured resistance, red-team coverage is named (with gaps surfaced), severity is tiered with eval effort proportional, and any mitigations named in `ai-ux-review` Block 6 have corresponding signal here.

For products that haven't done adversarial eval at all, this block is usually 70% `[Gap]`. That's a real finding, not a failure — it tells the team adversarial work is upstream of launch readiness.
