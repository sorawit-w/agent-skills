---
schema_version: 1
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
flexible_traits: {{FLEXIBLE_TRAITS}}  # [] on a fresh run; else [{name, value}], <=5
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
