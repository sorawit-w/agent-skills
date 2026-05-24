---
schema_version: 2
whoami_version: "{{WHOAMI_VERSION}}"
generated: "{{DATE}}"
source: "{{SOURCE}}"                  # fresh | mbti-import | profile-import
dials:                                # 0–10
  initiative: {{INITIATIVE}}
  depth: {{DEPTH}}
  breadth: {{BREADTH}}
  rationale: {{RATIONALE}}
  warmth: {{WARMTH}}
  challenge: {{CHALLENGE}}
class: "{{CLASS}}"
subclass: "{{SUBCLASS}}"              # "" if none
flexible_traits: {{FLEXIBLE_TRAITS}}  # [{name, value}] up to 5, seeded from background; [] only if none surfaced
anti_patterns: {{ANTI_PATTERNS}}      # 2–3 short strings — agent failure modes to avoid; [] if none surfaced
background:
  role: "{{ROLE}}"
  field: "{{FIELD}}"
  domain_bucket: "{{DOMAIN_BUCKET}}"
  ai_experience: "{{AI_EXPERIENCE}}"  # new | some | high
  primary_uses: {{PRIMARY_USES}}      # list
  languages: {{LANGUAGES}}            # list
---

# whoami — {{CLASS_DISPLAY}}

{{SUMMARY}}
