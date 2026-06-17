# DESIGN.md schema — Google Labs format + screenwright's two keys

DESIGN.md is an **established shared contract** in this repo: `brand-workshop` writes it,
`pitch-deck` / `validation-canvas` / `riskiest-assumption-test` read it, and screenwright
both reads and bootstraps it. Keep the format in sync — schema changes ripple across all of
them. The source-of-truth template is `skills/brand-workshop/SKILL.md` (the "DESIGN.md
(Starter Tokens)" section).

## Base format (do not invent — it's the Google Labs spec)

Format: [Google Labs `design.md`](https://github.com/google-labs-code/design.md), spec
version `alpha`. Two parts:

1. **YAML front matter** — machine-readable tokens. Recognized keys:
   `version, name, description, colors, typography, rounded, spacing, components`.
   - `colors` uses spec names `primary, secondary, tertiary, neutral, surface, on-surface,
     error`. **`colors.primary` is the cross-plugin contract key** — downstream plugins bind
     their accent variable to it. Don't rename it.
2. **Markdown body** — canonical section order (subset is fine; present sections must follow
   order): `Overview → Colors → Typography → Layout → Shapes → Do's and Don'ts → Voice`.

Scope is **tokens, not components** at "starter" level (button/form/grid specs are
stack-dependent). A richer adopted template *may* include component sections — keep them as
bonus context, don't strip them.

## screenwright's extension — two custom YAML keys

Verified against the live spec: the `design.md` linter **tolerates custom top-level YAML
keys** (it warns only on probable typos of known keys). So these are lint-clean *and*
machine-readable, and both are **optional / backward-compatible**:

```yaml
a11y:
  wcag: "2.2-AA"        # → axe runOnly tags: wcag2a, wcag2aa, wcag21aa, wcag22aa.
                        # This is the blocking ruleset for the machine gate.
breakpoints:
  mobile: 390           # px viewport widths screenwright renders + screenshots at,
  tablet: 768           # and the set it generates when a mock covers only one viewport.
  desktop: 1280
```

### Defaults when a key is absent

A hand-authored, older, or brand-workshop-emitted DESIGN.md won't have these. **Default
them — never block on their absence:**

| Key | Default |
|---|---|
| `a11y.wcag` | `"2.2-AA"` |
| `breakpoints` | `{ mobile: 390, tablet: 768, desktop: 1280 }` |

Existing readers (pitch-deck, validation-canvas, riskiest-assumption-test) ignore unknown
keys, so adding them has **zero blast radius**. `brand-workshop` may start emitting them
later (additive); screenwright does not depend on that.

### When DESIGN.md is present but incomplete

Absent `a11y` / `breakpoints` default cleanly (above). A *malformed* file is different: if
DESIGN.md exists but is missing the cross-plugin contract key `colors.primary`, or core
token groups (`colors` / `typography`) are absent or malformed, do **not** guess silently.
Treat it as a **partial Rung 1**, not a hard failure:

- In a project → infer the missing token(s) from the repo's other styling (Rung 2's
  inference, applied to just the gaps).
- Outside a project → ask one targeted question for the missing brand-load-bearing token.

State that you patched a partial DESIGN.md so the user can correct it. Never proceed to
paint against a token set you silently invented.

## When screenwright persists a bootstrapped DESIGN.md

Write the full base format (tokens + body sections it can fill) **plus** the two keys with
concrete values (not just defaults — pin the WCAG level and breakpoints you actually used).
Mark inferred/templated origin in the `description` or Overview so the user can correct it.
A persisted DESIGN.md should pass `npx @google/design.md lint`.
