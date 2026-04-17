# agent-skills (meta-plugin)

One-command install for the whole [`sorawit-w/agent-skills`](https://github.com/sorawit-w/agent-skills) shelf.

This plugin ships no skill of its own — it only declares every other plugin in the marketplace as a dependency, so a single install pulls them all in.

## Install

```
/plugin marketplace add sorawit-w/agent-skills
/plugin install agent-skills@sorawit-w
```

That's equivalent to installing each shelf plugin individually:

```
/plugin install skill-evaluator@sorawit-w
/plugin install team-composer@sorawit-w
```

## What's bundled

- [`skill-evaluator`](../skill-evaluator) — audit whether a skill's rules actually land in practice.
- [`team-composer`](../team-composer) — assemble a virtual team and run a 3-round discussion that produces real disagreement.

New plugins added to the marketplace get rolled into this bundle on the next version bump. Pin a specific version of `agent-skills` if you want a frozen set.

## When not to use it

If you only want one of the shelf plugins, install that one by name instead — the bundle is for people who want the whole shelf, not a sampler.

## License

MIT — see the [LICENSE](https://github.com/sorawit-w/agent-skills/blob/main/LICENSE) file at the repo root.
