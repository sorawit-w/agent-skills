# Honesty rubric

The non-negotiable safety discipline. Confidence reflects **source-backing, not fluency**. This file specifies how that is enforced mechanically rather than aspirationally.

## The source→claim map

From the first retrieval in Phase 2, maintain a mapping: every factual claim points to the source(s) that back it. Carry it through curation and into synthesis **unchanged** — curation reorganizes claims, it never detaches one from its source.

At synthesis time, this map is what makes the invariant *structural*: a line with no mapped source **cannot** be rendered as verified. It is tagged `[unverified / reasoning-only]` or it does not ship as fact. There is no path where confident prose substitutes for a missing source.

## Tagging rule

- **Source-backed claim** → cite it inline (source name/URL, or footnote-style reference). Multiple sources strengthen it.
- **No source** → prefix or suffix `[unverified / reasoning-only]`. This applies to reasoning, inference, and "common knowledge" alike — if retrieval didn't back it, it carries the tag.
- **Retrieval unavailable entirely** (dry run / no tool) → the *whole* output is tagged. This is the acceptance check: remove retrieval and the briefing is entirely `[unverified]`. If any line escapes the tag without a source, the invariant is broken.

## Confidence scoring (peer-review pass)

Score each finding by **source-backing**, never by how well it reads:

| Confidence | Criterion |
|---|---|
| High | Multiple independent sources, no unrefuted contradiction |
| Medium | Single solid source, or multiple sources that trace to one origin |
| Low | Weak/biased source, or sources disagree |
| Unverified | No source — reasoning only |

A well-written, un-sourced claim scores **Unverified**, full stop. Fluency must never buy confidence.

## STORM's two self-flagged failure modes

The peer-review pass exists primarily to catch the failures STORM's *own authors* named. Check for both explicitly — this is why the pass is not cosmetic:

1. **Source-bias transfer** — the synthesis inherits the slant of its sources. Mitigation: check source concentration (are most findings tracing to one outlet/author/community?), and surface *challenging* sources alongside supporting ones in the briefing. A finding backed only by sources that share an interest is flagged, not presented as settled.
2. **Over-association of unrelated facts** — stitching two true-but-unconnected facts into a false implied relationship. Mitigation: for each synthesized claim that *links* facts, verify the link itself is sourced, not just the endpoints. "A is true" + "B is true" does not license "A because B" unless a source asserts the connection.

## Peer-review output

A short block, four items:

- **Confidence per finding** (the table above).
- **Weakest link** — the single finding most likely to be wrong, and why.
- **Bias check** — source-concentration / source-bias-transfer assessment.
- **Missing perspective** — the lens that would most change the picture if added.

## Why structural, not aspirational

A prose reminder ("be careful about sources") drifts on contact with a real run. The source→claim map makes the constraint *checkable*: the dry-run acceptance test (no retrieval ⇒ all-`[unverified]` output) either passes or fails mechanically. That is the observable feedback loop the honesty discipline rests on — not the agent's good intentions.
