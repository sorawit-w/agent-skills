# Block 5 — Errors & Graceful Failure

## Definition

The catalog of how the system fails, ranked by severity, with the recovery
path for each tier. "Failure" here includes both *system failures* (timeout,
quota, model unavailable) and *output failures* (the AI returned something,
but it's wrong, off-topic, refusing, or unsafe).

This block depends on Block 4 (feedback & control) — every failure mode
should have a corresponding recovery affordance in Block 4, or be flagged
as a gap.

## Primary probe

> "List the four most likely failure modes for this feature. For each, what
> does the UI show, and what's the user's path forward?"

## Secondary probes

1. **System failures vs. output failures.** Have you separated them?
   System failures are usually well-handled (toast + retry). Output
   failures (fluent but wrong, refusal, off-topic) are where teams
   underdesign.
2. **Severity tiers.** What's the difference between a minor failure
   (regenerate solves it) and a critical failure (user makes a decision
   based on wrong info)? How do you communicate severity in the UI?
3. **Detectability.** Which failures does the system know it's having?
   Which require the user to notice? Detectable failures get prompts;
   user-detected failures need a path for the user to flag them.
4. **Refusal handling.** When the AI declines to do something (safety,
   capability, scope), how does that read to the user? "I can't help
   with that" is a UX choice — what does the UI do next?
5. **Failure-mode recovery in a multi-turn flow.** If turn 3 fails, what
   happens to turns 1 and 2? Conversation history matters.
6. **Latency as failure.** Is 15 seconds a failure mode? 30? At what
   point does the user assume it's broken and refresh?

## Acceptance criteria

- [ ] **Failure catalog with at least 4 modes.** Mix of system and
      output failures.
- [ ] **Severity tier per mode.** Minor / material / critical, or
      equivalent.
- [ ] **Recovery path per tier.** What the user does next, what the UI
      shows.
- [ ] **Refusal explicitly handled.** Even "we won't show refusals" is
      a stated choice.
- [ ] **At least one user-detected failure has a flagging path.** Not
      every failure can be detected by the system; the user needs a
      way to say "this is wrong."

## Common gap patterns

- **System failures only.** The catalog covers timeouts, rate limits,
  service unavailable — the easy stuff. Output failures (fluent but
  wrong) are absent. This is the most common gap.
- **No severity tiering.** Every failure shows the same banner. Users
  can't tell whether "AI had a hiccup, regenerate" is the same severity
  as "AI said the meeting is on Tuesday but you said Thursday."
- **No user-flagging path.** The user notices a fluent-but-wrong output;
  the only path is "edit the output" (Block 4) — there's no way to
  signal *to the system or team* that this was a failure. Useful
  signal lost.
- **Refusal treated as edge case.** When the AI declines to help, the
  user is dropped into an empty state with no path forward. Refusal
  is a regular mode for many AI products, not an edge case.
- **Latency unconsidered.** The team built a feature with 8-second
  median latency and never asked whether that's a failure mode. For
  some products it's fine; for others it's the dominant failure.
- **Conversation continuity broken.** Turn 3 fails; the UI clears
  everything and the user has to restart from turn 1. Multi-turn
  features must consider failure-state continuity.

## Worked example (LLM email drafting)

| Mode | Severity | UI behavior | Recovery |
|------|----------|-------------|----------|
| Generation timeout (>15s) | Minor | Skeleton stays + "Still working…" then "Try again?" | Retry button; option to switch to template library |
| Output rejects user's intent ("As an AI, I can't…") | Material | Inline message: "Skipped — the model declined this prompt." | Switch to template library; surface the prompt back so user can rephrase |
| Output uses wrong factual claim user can detect | Material | Not auto-detected | "Report this draft" button next to send; pre-fills feedback with the draft + intended ask |
| Output uses wrong factual claim user can't detect | Critical | Not auto-detected by system | Block 3's "verify this" chip on factual spans is the user-side detection path; Block 6 adds structured extraction guards |
| Service unavailable | Minor | Full banner: "Email AI is unavailable — switch to templates?" | Template library auto-loads inline |
| User mid-turn fails to load voice samples | Material | Side panel shows error; draft generates with default voice tone | Side-panel reload button; "We used the default voice this time — adjust below if needed" |

The "wrong factual claim user can't detect" mode is the most important row.
It's unrecoverable inside this block — it has to be prevented in Block 6
or made detectable in Block 3. Surface this dependency in the Phase 2
cross-block check.

## When the block is "complete enough"

When there's a catalog of at least 4 failure modes spanning system and
output failures, each tagged with severity and a recovery path, refusal
is treated as a regular mode, and at least one path exists for the user
to flag failures the system can't detect.
