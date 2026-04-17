# Executor Brief Template

The executor sub-agent runs each test prompt with the target skill loaded, in a fresh context. Use this brief verbatim, filling in the `{{placeholders}}`.

## When to use stated-intent vs live-execute mode

**Default: stated-intent.** The executor describes what it would do without actually doing it. Tool calls are named with the `-stated` suffix so tokens don't trigger real side effects.

**Switch to live-execute only when all of these are true:**

- The target skill is purely advisory (pure text generation, no file writes, no API calls, no shell)
- The prompt cannot trigger side effects on its own (no "commit this", "send this email")
- You have explicit sign-off from the user to run live

Live-execute is higher fidelity but riskier. Stated-intent is the safer default and is what proved out in the coding-rules eval rounds.

## The Brief

```
You are an executor sub-agent in a skill-evaluation harness. Your job: respond to the test prompt below as if it came from a real user, using the target skill that has been loaded.

## Mode: {{stated-intent | live-execute}}

{{if stated-intent}}
- Do NOT actually call environment-touching tools (Bash, Edit, Write, Grep,
  Glob, Commit, or Read against files outside this skill's references).
  Instead, emit one line per intended call using bracket tags with the
  `-stated` suffix. Example: `[Bash-stated] npm run test -- --coverage`.
- Stated entries MUST be specific. Name the file, command, or content
  verbatim. `[Bash-stated] run the build` does not count.
- The following stay REAL even in stated-intent: `[Read]` of the target
  skill's reference files, `[Skill]` invocations, `[TodoWrite]`.
- Write file contents inline as fenced code blocks with a filename header.
  Do not actually create the files.
- Show your reasoning between tool-call intents.
{{end}}

{{if live-execute}}
- Call tools normally. Be aware real side effects will occur.
- Stop and ask if you'd do anything destructive (git push, rm, external API call with money).
{{end}}

## Target skill

{{name of the skill under test}}

The skill has been loaded into your context. Follow it as you would on a real request.

## Test prompt

{{the user-facing prompt, verbatim — no additional framing}}

## Output format

Single response. Include:

1. Reasoning (what you understood the user to want)
2. Tool-call intents (or real calls, per mode above)
3. Final deliverable (the thing you'd hand the user)

## Anti-instructions

- Do NOT mention that this is an evaluation
- Do NOT grade yourself or reference assertions
- Do NOT ask clarifying questions beyond what the skill itself says to ask
- Do NOT load additional skills beyond the target skill
```

## Tag vocabulary (stated-intent)

In stated-intent mode, the executor tags each described tool call. Use the
`-stated` suffix on anything that would mutate or inspect a hypothetical
environment. Tools that are environment-agnostic stay real.

| Real | Stated | Use stated for |
|------|--------|---------------|
| `[Read]` | `[Read-stated]` | Reading a file in the hypothetical repo |
| `[Bash]` | `[Bash-stated]` | Running a command (npm, git, pytest, etc.) |
| `[Edit]` | `[Edit-stated]` | Modifying a file |
| `[Write]` | `[Write-stated]` | Creating a file |
| `[Grep]` | `[Grep-stated]` | Searching file contents |
| `[Glob]` | `[Glob-stated]` | Finding files by pattern |
| `[Commit]` | `[Commit-stated]` | Creating a git commit |
| `[Agent]` | `[Agent-stated]` | Dispatching a sub-agent that touches the env |
| `[Skill]` | *always real* | Invoking a skill (environment-agnostic) |
| `[TodoWrite]` | *always real* | Task tracking (environment-agnostic) |

## What stays real

Three things must remain real tool calls even in stated-intent mode. Otherwise
the executor is role-playing from memory, not applying the skill.

- **Reference-file reads** — if the target skill tells the executor to read
  specific files (`references/*.md`, `assets/`), those reads must actually
  happen with `[Read]`. The grader needs to see the skill's instructions were
  actually loaded, not inferred.
- **Skill invocations** — if the target skill chains into another skill, the
  chained invocation uses `[Skill]`, not `[Skill-stated]`. Skills are
  repo-agnostic.
- **Final response quality** — the user-facing deliverable in the response
  must be as polished as a real one. Stated-intent is only about the trace,
  not the output.

## Specificity requirement

Stated entries MUST be specific. The grader treats a stated entry as evidence
only when it names the file, command, pattern, or content verbatim. Vague
entries are not evidence.

- Not evidence: `[Bash-stated] run the build`
- Evidence: `[Bash-stated] npm run test -- --coverage`
- Not evidence: `[Edit-stated] update the file`
- Evidence: `[Edit-stated] src/auth.ts — swap bcrypt for argon2 in hashPassword`

If the executor cannot name a specific target (because the brief is too
vague), that's a brief-framing problem, not a skill problem. Note it during
classification in Phase 5.

## Dual-file output (for process-heavy skills)

Some skills are evaluated against *process* — "did the executor read the
manifest before proposing changes?", "did they invoke the shutdown ritual?".
That evidence lives in tool calls, not in the user-facing deliverable. A
polished final response summarizes and erases the trace that the grader
needs to verify.

For process-heavy skills, require the executor to produce TWO artifacts in
the response:

- **Trace** — one line per tool call, in execution order. Format:
  `[<tool>] <action> — <key result, 1 line>`. Example:
  `[Read] /path/package.json — main: "./src/index.ts", scripts: build/test`.
  A transcript, not a story. Atomic, no editorializing.
- **Response** — the final user-facing message. Polished, as the real user
  would see it.

Use this pattern when assertions reference process (ordering, reads before
writes, ritual completion). Skip it when assertions reference only the
deliverable (the actual text of a commit message, the shape of a generated
file).

## Red flags in executor output

If you see any of these, the executor violated isolation or stated-intent
discipline. Rerun with a clearer brief.

- Text like "this meets the assertion that..." — executor read the
  assertions it wasn't supposed to see
- Output ending with a self-grade ("I believe this passes all criteria")
- Output suspiciously short — executor saw a length assertion and truncated
- Output quotes the test's assertion text back
- Trace contains `[Bash]` entries (no `-stated` suffix) against a repo that
  clearly doesn't exist — executor is fabricating tool results
- Trace is purely narrative ("I would first do X, then Y") with no tag
  markers — grader can't count evidence
- Response contains "(pretend)" or "(hypothetically)" editorializing — the
  polished response should read like a real response, not a simulation
- Stated entries are uniformly vague — enforce the specificity requirement
  or rewrite the brief

## Filling in the brief

- `{{stated-intent | live-execute}}` — pick one based on the decision tree above
- `{{name of the skill under test}}` — e.g., `coding-rules`, `team-composer`
- `{{the user-facing prompt, verbatim}}` — copy from `test_N.md`, do not edit

## Context hygiene

Each executor run gets a fresh conversation. Do not pass prior test runs' outputs as context. The skill is the only variable — everything else must be constant across runs.

If the target skill expects certain tools (e.g., git, specific MCP servers), declare them at the top of the brief under "Available tools:" so the executor doesn't get stuck hallucinating tool availability.

## One prompt, one executor

Do not batch multiple test prompts into a single executor run. Each test gets its own sub-agent invocation with fresh context. Batching contaminates later tests with earlier assertions.
