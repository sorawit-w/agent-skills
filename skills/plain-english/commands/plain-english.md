---
description: Install, update, or check the plain-English rules — or rewrite a passage in plain words
argument-hint: "[install|update|status|uninstall|<text to rewrite>]"
---

Run the `plain-english` skill (`skills/plain-english/SKILL.md`).

- **No argument**, or **`install`** — install the rule block into
  `~/.claude/CLAUDE.md`. Show the exact change first and wait for an explicit
  yes. If a hand-written plain-language section is already there, offer to
  replace it.
- **`update`** — compare the installed block against the current one and offer
  to update it if the version is older.
- **`status`** — report whether the block is installed, which version, and
  whether a hand-written section is also present. No edits.
- **`uninstall`** — remove the block and nothing else.
- **Any other text** — rewrite that text in plain English and return only the
  rewritten version.
