# Folder Contract — Reference

Shared folder conventions across the startup plugins (`brand-workshop`,
`business-model-canvas`, and `pitch-deck`). Each plugin works
independently, but when run in the same working directory they compose via these
paths.

## Canonical paths

```
<founder-working-directory>/
├── brand-kit/                       # produced by brand-workshop
│   ├── brand-brief.md               # contains `## Positioning` + `## Voice & Tone`
│   ├── descriptions.md              # tagline + bios (pitch-deck reads tagline)
│   ├── design-system.md             # tokens (bmc + pitch-deck read)
│   ├── logos/
│   ├── favicons/
│   ├── social/
│   └── deck/
│       ├── pitch-template.html      # founder-facing self-contained stub
│       └── pitch-styles.css         # parseable companion (pitch-deck reads this)
│
├── business-model.md                # produced by business-model-canvas (this skill)
├── business-model.html              # produced by business-model-canvas (this skill)
│
└── pitch/                           # produced by pitch-deck
    ├── deck.html
    ├── speaker-notes.md
    └── deck-checklist.md
```

## Read-before-write rule

When `business-model-canvas` runs:

1. **Check for `brand-kit/design-system.md`.** If present, read the color tokens and
   font stack, and apply them to `business-model.html` via the `:root` CSS custom
   properties (see `bmc-html-template.md`).
2. **Check for an existing `business-model.md`.** If present, read it first — treat
   the interview as an *update*, not a rewrite. Surface changes explicitly to the
   founder ("You previously said X; we're now changing that to Y — confirm?").
3. **Never overwrite `brand-kit/*`.** Those files belong to `brand-workshop`. If the
   founder asks to change a color, route them back to `brand-workshop` rather than
   editing the brand kit from this skill.

## Write rule

- Write to the founder's working directory, not a scratch folder.
- Never write outside the canonical paths.
- If the working directory contains files unrelated to this plugin (code,
  unrelated docs), don't touch them — the folder is shared, not owned.

## Manifest (deferred)

A `kit-manifest.json` at the working-directory root is planned for the
`startup-launch-kit` orchestrator. Not implemented in v1 — folder conventions are
enough. When the manifest ships, each plugin will:

- Read it at start, if present, to discover which artifacts exist.
- Append/update its own entry after writing, if the manifest is present.
- Not create the manifest if it doesn't exist (that's the orchestrator's job).

Three lines of defensive read-if-present code in v1 keeps forward compatibility
cheap.
