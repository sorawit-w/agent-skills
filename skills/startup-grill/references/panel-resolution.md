# Panel Resolution

How to resolve who is in the room before grilling starts. Read this whole file
before assembling the panel — the rules are deliberately small and they
interact.

The panel is **never empty Tier 1 collaborative team from team-composer**. We
borrow team-composer's persona catalog as a base, then resolve roles that fit
adversarial probing on a startup idea.

---

## Phase A — Detect signals

Reuse `team-composer`'s Phase 1 signal table. The signals that matter most to
panel resolution:

| Signal | Values | Why it matters here |
|---|---|---|
| `audience` | `b2b`, `b2c`, `b2b2c`, `developer` | Drives slot 5; drives specialist injection |
| `domain` | open-ended (fintech, health, biotech, climate, ai, social, content, media, consumer, lifestyle, dating, creator, game, manufacturing, education, mental_health, etc.) | Drives specialist injection |
| `is_regulated` | `true` / `false` | Forces `@legal_compliance_advisor`; locks slot 5 |
| `involves_minors` | `true` / `false` | Forces `@developmental_psychologist` |
| `is_data_intensive` AND `has_novel_ml_claim` | `true` / `false` | Locks slot 5 onto technical DD even for consumer products |
| `complexity` | `low` / `medium` / `high` | Forces symmetric specialist when slot 5 flipped |
| `has_brand_impact` | `true` / `false` | Forces `@brand_strategist` as specialist when slot 5 = technical |
| `stage` | `idea` / `pre-seed` / `seed` / `Series A+` | Tunes diligence ask depth, not panel composition |

**Detection rule:** if a signal is genuinely ambiguous, default to the more
*risk-blocking* interpretation (assume `is_regulated=true` if unsure). Grilling
errs toward including more specialists, not fewer.

---

## Phase B — The fixed core (4 roles)

Always present, no exceptions:

| # | Role | Adversarial lens |
|---|------|------------------|
| 1 | `@vc_partner` | Capital efficiency, defensibility, comparable deals, term-sheet math |
| 2 | `@growth_marketer` *(use `@marketing_manager` in grill mode)* | Distribution, CAC, channel reality, "who else can do this and why haven't they?" |
| 3 | `@startup_strategist` | Wedge, narrative, founder-market fit, 18-month-arc credibility |
| 4 | `@ux_researcher` | Actual user reality vs. founder-reported user reality; "what did your users actually do, not what they said" |

These four cover the universal axes any startup is graded on. They are
**non-droppable** — even for a single-question-grill, all four show up.

---

## Phase C — Resolve slot 5 (the flex slot)

Slot 5 is the **fifth core role** and resolves to one of two roles based on
the detected signals.

```
slot_5 = @brand_strategist  IF all of:
   audience = b2c
   AND domain ∈ {social, content, media, consumer, lifestyle, fashion,
                  food, dating, creator, game, entertainment, music, art}
   AND is_regulated = false
   AND NOT (is_data_intensive AND has_novel_ml_claim)

ELSE slot_5 = @senior_software_architect  (default — technical due diligence)
```

**Why two roles, not more:** the consumer-brand vs. technical-execution split is
the single biggest axis on which startups fail differently. Other axes
(regulatory, behavioral, clinical) are handled by specialists. Don't expand
slot 5 to three or four options — it stops being a flex and becomes a panel.

**Worked examples** (canonical — use as regression checks):

| Startup framing | Slot 5 | Why |
|---|---|---|
| B2B SaaS for accounting teams | `@senior_software_architect` | Default; not consumer-brand-dominant |
| Developer tools / API platform | `@senior_software_architect` | Technical claims dominate |
| New social app for runners | `@brand_strategist` | Consumer + community + brand-driven |
| Direct-to-consumer skincare | `@brand_strategist` | Consumer; brand-defined category |
| Consumer mental-health app | `@senior_software_architect` | `is_regulated=true` carve-out fires |
| AI-powered consumer photo app | `@senior_software_architect` | Novel-ML carve-out fires; @brand_strategist injected as specialist (see Phase E) |
| Multiplayer indie game | `@brand_strategist` | Consumer + voice-driven; @game_designer injected as specialist |
| Climate / carbon-accounting SaaS | `@senior_software_architect` | Default; technical complexity dominates |
| Crypto consumer wallet | `@senior_software_architect` | `is_regulated=true` carve-out fires |

If a new framing doesn't fit any of these examples, write it down explicitly
in the kill report's panel section: *"Slot 5 resolved to X because Y" — one
line._ This makes drift visible in regression review.

---

## Phase D — Specialist injection table

Specialists are added based on signals. Each row is a hard rule — if the
signal fires, inject the role. Cap is **3 specialists** (panel ≤ 8 total).

| Signal trigger | Specialist injected |
|---|---|
| `is_regulated = true` (fintech, health, insurance, voting, crypto) | `@legal_compliance_advisor` |
| `domain = health` or `biotech` AND product makes evidence-based claims | `@clinical_researcher` |
| `domain ∈ {mental_health, wellness, therapy}` | `@clinical_psychologist` |
| `involves_minors = true` | `@developmental_psychologist` |
| `domain = game` OR significant gamification mechanics | `@game_designer` |
| `domain = ai` AND high autonomy or fairness stakes | `@ai_safety_specialist` |
| Handles money / PII / credentials at scale | `@security_specialist` |
| `audience = developer` (dev tools, APIs, infra) | `@developer_advocate` |
| `is_international = true` AND consumer-brand context | `@i18n_specialist` |

---

## Phase E — Symmetry rules (forced specialists)

When slot 5 flipped to one lens, the *other* lens doesn't disappear — it just
got demoted from the core. These are **forced specialists** — they cannot be
displaced by lower-priority specialists when the cap of 3 is hit.

| Condition | Forced specialist |
|---|---|
| `slot_5 = @brand_strategist` AND `complexity = high` | `@senior_software_architect` (technical DD as specialist) |
| `slot_5 = @senior_software_architect` AND `has_brand_impact = true` AND `audience = b2c` | `@brand_strategist` (brand as specialist) |

Why "forced": a consumer-brand-dominant startup with high technical complexity
*will* fail on technical execution if no one probes it; the same logic applies
in reverse. Symmetry preserves coverage of the demoted axis.

---

## Phase F — Cap and trim (panel ≤ 8)

Total panel is **5 core (4 fixed + slot 5) + up to 3 specialists**.

If specialist injection rules fire more than 3 times, trim by this priority
order — **higher rows survive, lower rows get cut**:

1. **Risk-blocking specialists** — `@legal_compliance_advisor`,
   `@developmental_psychologist`, `@clinical_psychologist`, `@ai_safety_specialist`
   (these never get cut if their trigger fired)
2. **Forced symmetry specialists** — `@brand_strategist` or
   `@senior_software_architect` injected via Phase E
3. **Domain-specific specialists** — `@clinical_researcher`, `@game_designer`,
   `@security_specialist`, `@developer_advocate`, `@i18n_specialist`
4. **Nice-to-have specialists** — none currently defined; reserved for future
   additions

Specialists trimmed by the cap are **named in the kill report's panel
footnote** along with the diligence concern they didn't get to probe. The user
must see what was left out.

Worked example of cap-trim:

> A children's mental-health app with novel ML and an international rollout
> would trigger: legal (regulated), developmental psych (minors), clinical
> psych (mental_health), AI safety (novel ML), i18n (international). That's 5
> specialists. Cap forces 2 cuts. By priority order, i18n drops first
> (nice-to-have for grilling, important for shipping), then the next-lowest
> domain specialist depending on framing — likely AI safety only if guardrails
> are out of scope for this grill round. The kill report records:
> *"Cap forced @i18n_specialist out — locale-readiness diligence is not
> covered in this run."*

---

## Phase G — Final panel write-up

Before Round 1 begins, the skill outputs a one-block panel summary in the
response. Format:

```markdown
**Panel resolved (5 core + N specialists):**

| Role | Why included | Slot |
|---|---|---|
| @vc_partner | Core | Fixed |
| @growth_marketer | Core | Fixed |
| @startup_strategist | Core | Fixed |
| @ux_researcher | Core | Fixed |
| @senior_software_architect | Slot 5 — technical DD default | Flex |
| @legal_compliance_advisor | is_regulated=true | Specialist |
| @security_specialist | Handles PII | Specialist |

**Signals detected:** audience=b2b, domain=fintech, is_regulated=true, ...

**Slot 5 reasoning:** [one line — e.g., "Default — not consumer-brand-dominant"]
```

This block goes into the kill report's Section 6 verbatim, and also gets
echoed in the response so the user can challenge the panel before grilling
starts. **If the user redirects ("drop X, add Y"), accept and re-run Phase F
trimming, then proceed.** Don't re-debate the entire panel.
