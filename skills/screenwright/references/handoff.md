# Handoff — how the final HTML is delivered

Loaded in Phase 6. A skill returns no "variable" — it's instructions an agent runs in its
own context. So "handoff" means either **inline HTML in context** (the agent reads & ports
it) or **a file path** (the agent `Read`s it). Render itself needs only the **transient**
`setContent` target — **no durable file is ever required.**

## Gate on project-context, not agent-vs-user

You **cannot** reliably detect "an agent invoked me" vs "a user invoked me" from inside a
skill — both look identical. Gate on the **detectable** signal instead: *is there a project
context?* (a repo / cwd with files / a DESIGN.md). This proxy matches the intent.

| Context | Deliver as | Durable file? |
|---|---|---|
| **In a project** (repo/cwd present) | **inline HTML** in context so the host agent can port it to the real stack | No — repo stays clean |
| In a project **but the artifact is large** | a **temp file path** (e.g. `/tmp/screenwright/<surface>.html`); agent `Read`s on demand | Temp only; clean up |
| **Non-project / interactive user** | a **durable named `.html`** at a sensible path + return the path | Yes — the file is the deliverable |

"Large" = roughly when inlining the HTML would dominate the main context (tens of KB+). Default
to inline; fall back to path only when size warrants it.

## Mode B also returns a change description

For **fix-from-code** (mode B), the input was real-stack code; the agent has to re-apply the
fix in its own framework. So the deliverable is the updated HTML **plus a plain-language
description of the visual changes made** ("increased card padding to 24px; added a visible
focus ring on the primary button; stacked the two columns below 768px"). That lets the agent
port the change without diffing HTML against framework source.

## Always attach the manifest

Every handoff includes the verification manifest (see [verification.md](verification.md)) —
hard-verified / soft-verified / not-verified. The consuming agent needs to know the
confidence: what the gate guarantees, what's judgment, and what wasn't checked (derived
viewports, advisory dimensions, or a11y if axe couldn't run).

## Persisted DESIGN.md

If Phase 2 bootstrapped a DESIGN.md (rungs 2/3), that file **does** persist to the repo/output
root regardless of the HTML delivery mode — it's the durable brand contract for the next
surface, not a throwaway. Mention you wrote it.
