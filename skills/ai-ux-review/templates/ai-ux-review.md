# AI UX Review — {{PRODUCT_NAME}}

> Generated on {{DATE}}. Lifecycle: {{LIFECYCLE}}. AI type: {{AI_TYPE}}.
>
> Edit this file as the design evolves. Headings (`## Block N — …` and
> `## Gap Summary`) are load-bearing — downstream tools parse them.

## Block 1 — Why AI Here?

- **User task:** {{user task in user words}}
- **Non-AI alternative:** {{the simplest tool that would partially solve the task}}
- **Reason AI wins:** {{specific dimension — open-ended input, scale, latency, judgment, etc.}}
- **Cost acknowledged:** {{at least one cost the AI imports that the alternative doesn't have}}

## Block 2 — Mental Model

- **User's model (paragraph):** {{what a typical user believes is happening}}
- **Misalignment 1:** {{where their model diverges from reality}}
  - Mitigation: {{teaching affordance or accepted-risk note}}
- **Misalignment 2:** {{...}}
  - Mitigation: {{...}}
- **Evidence basis:** {{user-research backed, or explicitly inferred}}

## Block 3 — Trust Calibration

- **Trust-surfacing moment 1:** {{specific UI moment + what the user does with it}}
- **Trust-surfacing moment 2:** {{...}}
- **Trust-surfacing moment 3:** {{...}}
- **Confidence strategy:** {{numerical / linguistic / visual / deliberately none — with reason}}
- **Under-trust failure path:** {{specific scenario + mitigation}}
- **Over-trust failure path:** {{specific scenario + mitigation}}

## Block 4 — Feedback & Control

- **Correction granularities:** {{word / sentence / regenerate / manual edit, etc.}}
- **Override path:** {{non-AI completion in the same UI, or explicit absence note}}
- **Autonomy level:** {{suggest / draft / act — per surface}}
- **Hand-off path:** {{escalation to human with continuity, or no hand-off note}}
- **Take-over:** {{user can suspend AI involvement — how}}
- **Feedback acknowledgment:** {{does the system signal it noticed corrections}}

## Block 5 — Errors & Graceful Failure

| Mode | Severity | UI behavior | Recovery |
|------|----------|-------------|----------|
| {{system failure mode}} | {{minor / material / critical}} | {{what the UI shows}} | {{what the user does}} |
| {{output failure mode — fluent but wrong}} | {{...}} | {{...}} | {{...}} |
| {{refusal handling}} | {{...}} | {{...}} | {{...}} |
| {{user-detected failure with flagging path}} | {{...}} | {{...}} | {{...}} |

- **Latency threshold:** {{at what latency does this become a failure mode}}
- **Multi-turn continuity:** {{what happens to prior turns when a later turn fails}}

## Block 6 — Output Integrity

- **Verifiability strategy:** {{path for the user to verify, or accepted-risk note}}
- **Provenance scheme:** {{sources / citations / intermediate steps / explicit absence}}
- **Hallucination defense:** {{specific design response, not just a disclaimer}}
- **Prompt-injection surface:** {{where user input enters the prompt + the response}}
- **Multi-turn drift** (LLM): {{re-grounding strategy, or accepted-risk note}}
- **Autonomy level:** {{suggest / draft / act / auto-act — for each user-facing action}}
- **Reversibility:** {{which actions are reversible / irreversible — confirmation gates}}
- **OOD behavior** (classical ML, if applicable): {{response to inputs unlike training data}}

## Block 7 — Success & Evaluation

- **Offline success criterion:** {{what "good enough to ship" looks like, measurable before launch}}
- **Online success metric:** {{specific number + threshold}}
  - Proxy or direct: {{state which}}
- **Gap to truth:** {{what the metric doesn't capture + compensating signal}}
- **Failure signal:** {{a metric that would catch silent feature degradation}}
- **Per-segment measurement:** {{which segments + hypothesis about differences}}
- **Drift detection:** {{signal for model or behavior shifting over time}}
- **Eval gap to companion:** {{out-of-scope eval work — names what a future `ai-eval-rubric` would pick up}}

---

## Gap Summary

The three to five most urgent unmade design decisions. For each: the gap in
plain language, why it matters, and the cheapest design experiment to
resolve it.

1. **{{Gap in one line}}**
   - Why it matters: {{which block surfaced it; what fails if left unresolved}}
   - Cheapest design experiment to resolve: {{specific test, ideally <1 week}}

2. **{{Gap in one line}}**
   - Why it matters: {{...}}
   - Cheapest design experiment to resolve: {{...}}

3. **{{Gap in one line}}**
   - Why it matters: {{...}}
   - Cheapest design experiment to resolve: {{...}}

---

*This review was produced by the `ai-ux-review` skill in
[sorawit-w/agent-skills](https://github.com/sorawit-w/agent-skills). Inspired
by Google's [People + AI Guidebook](https://pair.withgoogle.com/guidebook/)
(CC BY-NC-SA 4.0); authored from first principles. See the skill's README
for the full influences note.*
