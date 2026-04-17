# sorawit-w — Claude Code marketplace

A personal shelf of Claude Code plugins. Each plugin bundles a single skill so you can pick the ones you want, one by one.

## Install

Add the marketplace once:

```bash
/plugin marketplace add sorawit-w/agent-skills
```

Then install any plugin by name:

```bash
/plugin install <plugin-name>@sorawit-w
```

## Available plugins

| Plugin | What it does |
|--|--|
| [`skill-evaluator`](plugins/skill-evaluator) | Audit a skill to see whether its rules actually land in practice. |

More plugins will be added over time. Each lives under [`plugins/`](plugins/) with its own `SKILL.md` and reference docs.

## Notes

- Primary target agent: Claude (Claude Code, Cowork). Support for other agents may come later.
- This is an early-stage shelf — versions stay below `1.0.0` while interfaces stabilize.
- Feedback, issues, and contributions welcome via GitHub.
