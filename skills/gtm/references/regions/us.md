# Region Adapter — `us` (United States)

Default region for unspecified projects. The B2C-primary defaults in
GTM's main config are tuned for this market.

## Cultural notes

- **Formality default:** semi-casual for B2C; semi-formal for B2B. Tech
  founder voice trends toward casual-confident.
- **Humor norms:** observational and self-deprecating land well; sarcasm
  is fine but reads dry in text. Wordplay works.
- **Direct vs indirect:** direct claims expected — vague benefit-speak
  reads as evasive.
- **In-group references:** US tech audiences pattern-match to specific
  references (HN, Stripe, YC, indie hackers); brand voice should signal
  membership of the right tribe rather than chase trend cycles.
- **Taboos:** politically charged content polarizes audiences quickly —
  avoid unless the brand stance is intentional and consistent. Avoid
  weight/diet humor.

## Platform map

| Platform | Position | Notes |
|---|---|---|
| X (Twitter) | primary for tech B2C/B2B | high signal, low engagement; threads land |
| Reddit | primary for niche communities | rules vary per sub; lurk before posting |
| TikTok | primary for consumer | hook in first 1.5s; under-30 audience |
| Instagram | primary for lifestyle/D2C | Reels > feed > stories for reach |
| YouTube | primary for evergreen | long-form 8-12min sweet spot |
| LinkedIn | primary for B2B | thought leadership format works; sales-pitch posts don't |
| Hacker News | niche for dev tools | one shot per launch; community detects astroturfing |
| Discord | growing for community | indie / creator-economy audiences live here |
| Newsletter | niche evergreen | substack/beehiiv landscape; CTR > raw subscriber count |
| Threads / Bluesky | secondary | smaller audiences; X still dominant for tech |

## Language profile

- **Primary language:** `en-US`
- **Local variants matter?** Yes — en-US vs en-GB spellings (color/colour) and idiom (parking lot vs car park) are noticeable. Default to en-US unless config says otherwise.
- **Mix patterns:** None significant.
- **Translation guidance:** N/A for primary content; if the project has en-GB or other variants, route through `i18n-contextual-rewriting`.

## Local regulations

- **Privacy regime:** CCPA (California — applies to most US-targeted products), VCDPA (Virginia), CPA (Colorado), CTDPA (Connecticut), MOPA (Montana). State patchwork — use the strictest applicable as the floor.
- **Marketing rules:** CAN-SPAM (commercial email — unsubscribe link mandatory, identity disclosure, no deceptive subject lines), TCPA (text/voice — explicit opt-in required), FTC Endorsement Guides (sponsored content disclosure — `#ad`, `#sponsored`).
- **Disclosure language:** `#ad` or `#sponsored` for paid promotion. `#partner` is FTC-acceptable in context but `#ad` is clearer.
- **Sector-specific rules:** COPPA applies if any user under 13. HIPAA applies for health-adjacent. Securities/financial advertising has its own rules.

## Holidays and observances

- **Commercial moments:** Black Friday (post-Thanksgiving Friday), Cyber Monday, Memorial Day (late May), Independence Day (Jul 4), Labor Day (early Sep), Halloween, Christmas/holiday season.
- **Cultural observances to avoid:** Sep 11 anniversary (memorial tone only, no commercial), MLK Day (Jan, third Monday — observance-appropriate), Memorial Day (military observance, commercial sales OK but acknowledge tone).
- **Time zone awareness:** US spans 4 contiguous time zones plus AK, HI. Default email send: 08:00 ET reaches East Coast morning, lands in West Coast inbox by 06:00 PT (still acceptable). For broad B2C, 10:00 ET works better.

## Channel adaptations

- **X/Twitter:** thread-first format for substantive content; single tweets for one-liners and replies. Thread length 6-12 tweets sweet spot. Hook tweet must include the value claim.
- **TikTok:** vertical, hook in 1.5 seconds, 60-90s for substantive content, < 30s for engagement plays. Captions add context but don't carry the message.
- **Email:** subject line < 50 chars, preheader complements (not duplicates) subject. Preferred send: Tuesday-Thursday, 10:00 ET. Avoid Monday morning (busy) and Friday afternoon (gone).
- **SEO:** Google primary. Topic clusters > one-shot pieces. Schema.org markup helps for product/article/howto.
- **Reddit:** read each subreddit's rules. Most ban promotional posts but allow value-add discussions. Karma matters — established account > new account; new accounts get auto-flagged in many subs.

## Things to never do

1. **Run a Reddit promotion post under a fresh account** — gets flagged as astroturfing, burns the brand. Establish karma first or partner with a community member with their consent.
2. **Send commercial email without an unsubscribe link** — CAN-SPAM violation, $50,000 per email maximum penalty. Even one fine kills a startup.
3. **Use FTC-prohibited claim phrasing** — "guaranteed" "scientifically proven" "FDA approved" without backing documentation. Liability moves to the founder personally for false advertising.
4. **Ignore CCPA "Do Not Sell" requests** — specific to California users; legal exposure scales fast. Even if not subject to all of CCPA, the cost of compliance is much lower than the cost of a violation.
5. **Post during major tragedies** — pause scheduled content within 24h of a major US event (mass casualty, presidential transition, etc.). Reads tone-deaf otherwise.
