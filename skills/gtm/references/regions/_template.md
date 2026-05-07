# Region Adapter Template — `_template.md`

Copy this file to `references/regions/{country-code}.md` and fill in the
region-specific details. The {code} should be ISO 3166-1 alpha-2
(`us`, `gb`, `de`, `th`, `jp`, `br`, `mx`, etc.) or a recognized
sub-region (`uk-en`, `cn-zh-hant`).

GTM loads this file when the region is listed in `config.yaml#regions`.
The file's role: **wrap channel-worker outputs with regional context** so
the same hero piece adapts cleanly across markets without rewriting.

---

## Cultural notes

Brief notes on how to write FOR this audience (not just IN this language).

- **Formality default:** [casual | semi-formal | formal] — match audience expectation
- **Humor norms:** [self-deprecating? observational? wordplay? what's off-limits?]
- **Honorifics / titles:** [are first names ok? do you use Mr/Ms by default?]
- **Direct vs indirect:** [does this market prefer direct claims or indirect framing?]
- **Taboos:** [topics, gestures, imagery to avoid]
- **In-group references:** [memes, shows, recent events that signal you "get" the market]

## Platform map

Which platforms matter here, ranked by audience density. Some markets are
served by global platforms (X, IG); others have regional ones that
dominate (LINE in Japan/Thailand, KakaoTalk in Korea, WeChat in China,
VK in Russia, Facebook still dominates in some markets).

| Platform | Position | Notes |
|---|---|---|
| [name] | [primary / secondary / niche] | [audience, format, tone] |

## Language profile

- **Primary language(s):** [list with BCP 47 codes]
- **Local variants matter?** [e.g., en-US vs en-GB; pt-BR vs pt-PT]
- **Mix patterns:** [e.g., Thai with English loanwords vs pure Thai]
- **Translation guidance:** content drafts route through
  `i18n-contextual-rewriting` — link to or summarize any project-specific
  glossary

## Local regulations

Compliance overlays that apply on top of the global defaults.

- **Privacy regime:** [GDPR / PDPA / LGPD / CCPA / etc.] — what does this
  mean for collection, consent, retention?
- **Marketing-specific rules:** [opt-in requirements, time-of-day
  restrictions for SMS, telemarketing rules, COPPA-equivalents]
- **Disclosure language:** [local conventions for #ad, sponsored,
  affiliate]
- **Sector-specific rules:** [if fintech / health / gambling / alcohol —
  jurisdiction-specific add-ons]

## Holidays and observances

Calendar awareness that shapes scheduling. Posting on a public holiday
without acknowledgment reads tone-deaf; posting through a regional
mourning period reads worse.

- **Major commercial moments:** [equivalents of Black Friday — when, what
  expectations]
- **Cultural observances to avoid:** [periods where commercial messaging
  is inappropriate]
- **Local equivalents of common Western dates:** [e.g., Singles' Day,
  Songkran, Setsubun]

## Channel adaptations

How specific channels adapt to this region. Override global defaults here.

- **X/Twitter:** [is this audience on X, or have they moved to threads /
  bluesky / something local?]
- **TikTok:** [trending hooks, local creator landscape]
- **Email:** [send-time conventions, subject-line norms]
- **SEO:** [primary search engine — Google or local — and what local
  ranking factors matter]

## Things to never do

A short list of categorical no-gos for this market. Specific. Defensible.

1. [thing] — [why]
2. [thing] — [why]
3. [thing] — [why]

## When this region is added

When the founder adds this region to `config.yaml#regions`, GTM:

1. Loads this file
2. Wraps channel-worker prompts with the cultural and linguistic context
   from above
3. Routes non-primary-language drafts through `i18n-contextual-rewriting`
   (or warns if not installed)
4. Adds applicable compliance flags from local regulations to
   `config.yaml#compliance.*`
5. Surfaces a one-time confirmation to the founder: *"Added [region]
   adapter. Compliance flags updated: [list]. Confirm before next
   external action."*

## When this region is missing

If the founder lists a region in config but no adapter file exists, GTM:

1. Surfaces a warning at load time
2. Falls back to the global defaults for that region
3. Recommends the founder either author a region adapter (copy this
   template) or remove the region from config
4. Continues running — does not crash on missing region adapter
