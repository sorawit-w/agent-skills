# Selection Algorithm & Edge Cases

Detailed rules for team composition, sizing, and special scenarios.

---

## Selection Algorithm

```
team = CORE_ROLES

// Apply core exceptions
if NOT has_ui:
    remove @senior_frontend_engineer
    remove @senior_product_designer

// Score Tier 2
for each role in TIER_2:
    if ANY trigger signal matches:
        add role to team

// Domain expert special handling
if domain is specialized (not saas, social, marketplace):
    add @domain_expert, instantiated for detected domain
    run self-assessment: can AI bring substantive expertise?
    if shallow: flag limitation in persona intro

// Score Tier 3 (be selective)
for each role in TIER_3:
    if trigger signal is STRONG (explicitly mentioned or clearly implied):
        add role to team

// Apply team size cap — HARD CAP 12 for all scopes
if team.size > 12:
    prune down to 12 using the priority order below (highest priority kept):
        1. Core roles (Tier 1) — never drop
        2. Risk-blocking roles when their triggering risk is present:
           @legal_compliance_advisor (IP/regulatory/children risk)
           @security_specialist (money/PII/credentials)
           @developmental_psychologist (minors)
           @clinical_psychologist (mental health/crisis content)
        3. Roles triggered by Phase 3.5 Gap Detection "yes" answers
        4. Remaining Tier 2 roles
        5. Remaining Tier 3 roles
    note dropped roles as "available on request"
    // For planning scope: if you're hitting the cap, challenge whether all roles are essential
    // before pruning. Large teams for planning should be a deliberate exception, not default.
    // NEVER drop a risk-blocking role (level 2) to keep a non-risk role (level 4 or 5).

// Scope-based pruning
if scope == "discussion":
    keep: PM, architect, designer, copywriter + triggered Tier 2
    consider dropping: frontend, backend (unless tech discussion)
if scope == "building":
    keep: all engineering core + QA, security, devops if triggered
    consider dropping: brand_strategist, community_manager, content_strategist, marketing_manager
if scope == "review":
    keep: all core + QA, security if triggered
    add: accessibility_specialist for public-facing products
```

---

## Team Size Guidelines

| Scenario | Target Size | Rationale |
|----------|------------|-----------|
| Trivial feature (tooltip, copy change) | 3–4 | Don't over-staff. PM + relevant specialist + copywriter. |
| Quick discussion | 5–7 | Strategic roles + key engineers |
| Feature planning | 7–9 | Full core + relevant specialists |
| New product | 8–12 | Broad coverage, many unknowns |
| **Hard cap** | **12** | Beyond 12, context dilution outweighs coverage |

When signals trigger more than 12 roles, prune using this **risk-weighted priority** (highest kept first):

1. **Tier 1 (core roles)** — always keep
2. **Risk-blocking roles** — when their triggering risk is present, never drop these to fit the cap:
   - `@legal_compliance_advisor` when IP/copyright risk, regulated domain, or children's data
   - `@security_specialist` when money, PII, credentials, **health records, clinical/patient data, or regulated audit trails (e.g., 21 CFR Part 11)** are handled — if the domain is `health`, `biotech`, `pharma`, or `fintech` AND `is_regulated=true`, this role is non-droppable even when it looks redundant with other specialists
   - `@developmental_psychologist` when minors are primary users
   - `@clinical_psychologist` when mental health or crisis-adjacent content
3. **Gap-triggered roles** — any role that was added because Phase 3.5 Gap Detection answered "yes"
4. **Tier 2 roles** (not risk-blocking, not gap-triggered)
5. **Tier 3 roles** (not risk-blocking, not gap-triggered)

**Key rule (hard):** If a risk-blocking role's trigger fires, that role is NON-DROPPABLE.
This is not a tiebreaker — it is a veto. You MAY NOT drop a triggered risk-blocking role
in order to keep a Tier 3 role, and you MAY NOT justify the drop with language like
"collapse into," "defer to," or "covered by." Those phrases are the workaround this rule
exists to prevent.

Triggered risk-blocking roles and the specific trigger that locks them in:

| Role | Locked in when |
|------|----------------|
| `@legal_compliance_advisor` | IP risk OR regulated domain OR children's data |
| `@security_specialist` | money OR PII OR credentials OR health records |
| `@developmental_psychologist` | minors (primary audience) |
| `@clinical_psychologist` | mental-health OR wellness OR crisis-adjacent content |

If the triggered set plus Tier 1 already exceeds 12, the cap itself is wrong for this
project — widen the team, split the scope, or decline to compose. Do not drop a
risk-blocking role to force-fit the cap.

**Why:** A clinical psychologist and a security specialist are not redundant with a
developmental psychologist and a backend engineer. When these roles are dropped, the
team loses the capacity to SEE the risk, not just the capacity to discuss it.

**Verification step (Post-Discussion):** Add to the verification checklist —

- [ ] For each Phase 3.5 Gap Check "yes" that triggered a risk-blocking role, that role
      is present in the final Active Team. No exceptions.

Note dropped roles as "available on request" in the Team Assembly.

---

## Edge Cases

### User Specifies Exact Roles

Respect their selection. Skip detection/scoring. Still run the discussion flow.
If their selection seems incomplete for the topic (e.g., no security on a fintech
project), note the gap once but don't force additional roles.

### "Just Engineering"

Use only engineering core roles (architect, lead, frontend, backend) + any triggered
specialists (DevOps, QA, security). Drop PM, designer, copywriter.

### "Who Should I Hire?"

This skill is for virtual team composition, not hiring advice. Clarify the distinction
but offer to simulate the team so they can see what each role contributes.

### Trivial / single-asset requests

If the request is for a SINGLE ASSET or a trivial feature, scale way down AND check
the skill boundary first.

**Triggers (any one):**

- "add a tooltip" / "change this copy" / "fix this button"
- "I need a logo" / "I need a tagline" / "name this product"
- "write a subject line" / "one email" / "one social post"
- Scope fits in a single designer or copywriter session

**Boundary check (required before composing a team):**

- Logo OR brand identity system → defer to `brand-workshop`
- Naming-only (no team composition needed) → defer to a naming skill if one is
  available; otherwise compose a minimal team of `@naming_specialist` +
  `@senior_copywriter`
- UX copy only → defer to `design:ux-copy`

Only compose a team if the boundary check returns "no better skill applies." In that
case:

- 3–4 roles max (hard cap for trivial scope)
- Under 400 words (hard cap, includes all rounds)
- Skip the full Team Assembly table — name roles inline
- Single-round discussion is acceptable; rebuttal optional
- Conclusion still required (recommendation + 1–3 next steps)

**Why:** In eval runs, "I need a logo for X" produced a 6-role, 1210-word output
despite the executor explicitly naming `brand-workshop` as the better-fit skill.
Acknowledging an escape hatch is not the same as taking it. This rule makes the
boundary a required action, not a recommendation.

### Non-Tech Projects

This skill works best for projects with a tech component, but adapts to other
domains. For pure business strategy, marketing campaigns, or non-technical projects:
- Adapt the role set (drop engineers, add more strategic roles)
- The `@domain_expert` meta-role is especially useful here — instantiate it for the
  project's actual domain (event planning, supply chain, education, etc.)
- Consider suggesting a more appropriate skill if one exists

### Mid-Discussion Role Changes

**Adding a role:** Comply immediately. Briefly introduce the new role's perspective,
then let them contribute to the current thread. Don't restart the discussion.

**Removing a role:** Comply immediately. Acknowledge the departure briefly
(e.g., "Dropping @marketing_manager from the discussion."). Skip the role from
further contributions. If the removed role made significant points earlier,
preserve those in the conclusion — don't erase valid insights just because
the role was removed.

### Conflicting Signals

When signals pull in opposite directions (e.g., `is_regulated: true` triggers
@legal but `scope: discussion` + `stage: idea` suggests keeping it light):
- Include the triggered role, but brief them to contribute at the appropriate
  depth for the scope. A legal advisor in an idea-stage discussion flags high-level
  risks, not specific regulation clauses.

---

## Customization

Users can customize team composition over time:

- **"Always include @security_specialist"** → Treat as core for this user
- **"Never include @sales_manager"** → Exclude from all future assemblies
- **"I want @data_scientist on every data project"** → Add as Tier 2 trigger

When the user requests a customization, save it as a **feedback memory** so it
persists across conversations. Format:

```
Role override: always include @security_specialist.
Why: User works in regulated fintech domain where security review is non-negotiable.
How to apply: Add @security_specialist to Tier 1 (core) for all team-composer invocations.
```
