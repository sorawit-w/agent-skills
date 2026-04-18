---
name: i18n-contextual-rewriting
description: >
  A comprehensive skill for handling internationalization (i18n) translation files and producing
  culturally authentic translations. Use when: (1) Editing, creating, or modifying translation
  files (JSON, YAML, TypeScript, JS) — especially large ones that risk exceeding token limits,
  (2) Translating UI strings into any supported language/dialect,
  (3) Reviewing translations for cultural accuracy and naturalness,
  (4) Syncing translation keys across multiple locale files,
  (5) Adding new languages or regional variants to an existing i18n setup.
  Triggers on phrases like "translate", "i18n", "localization", "translation file",
  "locale", "add language", "translation keys", or any mention of specific locale codes
  (e.g., th, ja, ko, zh-CN, de, fr, es, it, zh-TW, zh-HK, th-bupphe).
---

# i18n Contextual Rewriting Skill

This skill has two parts:

1. **File Handling** — How to safely edit translation files without hitting token limits.
2. **Translation Teams** — How to produce culturally authentic translations using a
   multi-role review process.

---

# Part 1: Handling Translation / i18n Files

## Why This Matters

Translation files can be extremely large (thousands of keys). Attempting to rewrite
an entire translation file will likely exceed output token limits and cause errors.
Always use **surgical, minimal edits** instead.

## File Formats

Translation files may exist in any of these formats:

| Format | Example | Notes |
|--------|---------|-------|
| JSON   | `en.json`, `messages.json` | Most common. Flat or nested key-value. |
| YAML   | `en.yml`, `messages.yaml` | Common in Rails, Spring, etc. |
| TypeScript | `en.ts`, `translations.ts` | Used when types are shared across projects. Often exports an object `as const` or uses `satisfies`. |
| JS/MJS | `en.js`, `en.mjs` | Legacy or framework-specific. |

## Rules

### 1. NEVER rewrite an existing translation file in full

- Do NOT output the full file content when editing an existing file.
- Do NOT use a "replace entire file" operation to change a few keys.
- If a tool only supports full-file writes (no partial edit), use the **script approach** (see below).

**Exceptions — full-file writes are fine when:**
- **Creating a new locale file** from scratch (e.g., adding `it.json` for the first time).
- **Generating an initial translation** of an entire file into a new language.
- The file is small enough (< 200 keys) that a full rewrite won't risk token limits.

The rule exists to prevent token-limit blowups on large existing files, not to
block legitimate file creation.

### 2. Prefer surgical edits

When adding, updating, or removing keys, target **only the affected lines**.

**Example — adding keys to a JSON file:**

```diff
   "dashboard.title": "Dashboard",
+  "dashboard.subtitle": "Welcome back",
+  "dashboard.empty_state": "No data available",
   "dashboard.footer": "© 2025"
```

**Example — adding keys to a TypeScript file:**

```diff
 export const en = {
   dashboard: {
     title: 'Dashboard',
+    subtitle: 'Welcome back',
+    emptyState: 'No data available',
     footer: '© 2025',
   },
 } as const;
```

### 3. Use a script for bulk operations

When changes are too numerous or complex for surgical edits (e.g., adding 50+ keys,
restructuring namespaces, syncing across locales), write a **one-off script** that
reads, transforms, and writes the file programmatically.

**For JSON files:**

```ts
import fs from 'fs';

const filePath = './locales/en.json';
const translations = JSON.parse(fs.readFileSync(filePath, 'utf-8'));

const newKeys = {
  'feature.title': 'New Feature',
  'feature.description': 'This is a new feature',
};

Object.assign(translations, newKeys);
fs.writeFileSync(filePath, JSON.stringify(translations, null, 2) + '\n');
```

**For TypeScript files:**

TS translation files cannot be naively JSON-parsed. Use one of these strategies:

- **Strategy A — Dynamic import** (preferred when structure is `export default` or named export):

  ```ts
  const mod = await import('./locales/en.ts');
  const translations = mod.default ?? mod.en;
  // Merge new keys, then serialize back
  ```

  > ⚠️ This loses `as const` / `satisfies` type annotations. You must re-apply
  > them when writing back. See serialization note below.

- **Strategy B — AST manipulation** (when type safety must be preserved exactly):

  Use `ts-morph` or similar to add properties to the exported object without
  altering the rest of the file.

  ```ts
  import { Project, SyntaxKind } from 'ts-morph';

  const project = new Project();
  const sourceFile = project.addSourceFileAtPath('./locales/en.ts');
  const obj = sourceFile
    .getVariableDeclarationOrThrow('en')
    .getInitializerIfKindOrThrow(SyntaxKind.ObjectLiteralExpression);

  obj.addPropertyAssignment({
    name: "'newKey'",
    initializer: "'New Value'",
  });

  await sourceFile.save();
  ```

- **Strategy C — Regex/text insertion** (simple cases only):

  Find the closing `}` of the target object and insert before it. Fragile but
  acceptable for appending a few keys to a well-known structure.

**Serialization note for TS files:**

When writing back a TS translation file, preserve the original structure:

```ts
// If the original uses `as const`:
const output = `export const en = ${JSON.stringify(merged, null, 2)} as const;\n`;

// If the original uses `satisfies`:
const output = `export const en = ${JSON.stringify(merged, null, 2)} satisfies Translations;\n`;
```

Ensure the import statement for the type (e.g., `Translations`) is preserved.

### 4. When syncing across locales

If the task is "add these keys to all locale files":

1. Define the new keys in a single object/variable.
2. Write a script that iterates over all locale files.
3. For each file, read → merge (without overwriting existing keys) → write.
4. Log which files were updated and which keys were added.

Do NOT manually edit each locale file one by one — this is error-prone and
token-expensive.

### 5. Validate after changes

After any translation file modification:

- Verify the file is valid (parseable JSON, valid TS syntax, etc.).
- Run any existing i18n linting or type-checking commands if available.
- Confirm no existing keys were accidentally removed or overwritten.

---

# Part 2: Translation Teams — Role-Based Contextual Rewriting

## Philosophy

Translation is **not** word-for-word substitution. It is **contextual rewriting
inside cultural reality**. Every string a user reads should feel like it was
originally written in their language — by someone who lives in their market,
uses their apps, and thinks in their idioms.

To achieve this, adopt a **multi-role review process** before finalizing any
translation. Each role contributes a different lens. Internally simulate all
applicable roles and reconcile their perspectives before producing final output.

## Workflow

1. **Identify the target locale** — language alone isn't enough. Thai (standard)
   ≠ Thai (Gen Z) ≠ Thai Isan. Each has its own team.
2. **Draft** an initial translation considering UI context, intent, and tone.
3. **Pass the draft through each role's lens** for the target locale.
4. **Handle pluralization** — apply the target language's pluralization rules
   (see Pluralization section below).
5. **Reconcile** conflicting feedback (e.g., copywriter wants flair, UX reviewer
   wants brevity) with a bias toward **clarity and cultural fit**.
6. **Output** the final translation. Add a brief note if a key required
   non-obvious cultural adaptation.

## Shared Roles (All Languages)

These roles apply to **every** target locale:

- `@ux localization reviewer` — Ensures translations work within UI constraints
  (character length, button labels, truncation). Validates that tone matches the
  interaction context (error message vs. celebration vs. onboarding).

- `@i18n engineer` — Handles interpolation variables (`{count}`, `{name}`),
  pluralization rules, gender agreement, and format consistency (dates, numbers,
  currency). Ensures the translated string won't break at runtime.

---

## Pluralization Rules

Different languages handle plurals differently. The agent **must** account for
the target language's pluralization category when producing translation keys.

| Category | Languages (from this list) | Forms |
|----------|---------------------------|-------|
| No plural forms | Japanese, Korean, Thai (all variants), Chinese (all variants) | `other` only |
| Two forms (one/other) | English, French, German, Italian, Spanish, Hong Kong Chinese* | `one`, `other` |

> \* Hong Kong Chinese generally doesn't pluralize, but borrowed English terms in
> mixed-code writing sometimes do. Default to "no plural forms" unless the key
> contains an English loanword that inflects.

**What this means in practice:**

- For Japanese, Korean, Thai, Chinese: **do not generate separate plural keys.**
  Use a single key with quantity handled by context or counter words.
- For European languages: generate `one` and `other` forms at minimum. Some i18n
  frameworks (ICU MessageFormat) support `zero`, `few`, `many` — use them when
  the framework supports it and the language needs it.
- For German/French/Italian/Spanish: watch for **gendered nouns** that change
  with quantity. The `@i18n engineer` must flag these.

**Counter words / classifiers:**

Thai, Japanese, Korean, and Chinese use counter words (ลักษณนาม, 助数詞, 분류사,
量词). When a translation involves quantities, include the appropriate classifier.
Do not omit it — it sounds unnatural to native speakers.

---

## Language-Specific Teams

---

### 🇺🇸 English — Gen Z (`en-genz`)

| Role | Focus |
|------|-------|
| `@gen z voice copywriter (english)` | Writes in authentic Gen Z digital-native voice. Knows the line between relatable and cringe. Fluent in current slang without overdoing it — the goal is natural, not "how do you do, fellow kids." |
| `@internet culture insider (english)` | Tracks meme cycles, platform-specific language (TikTok vs. Discord vs. Twitter), and understands which references land and which are already dead. Knows that slang has a shelf life. |
| `@social psychologist (youth culture)` | Ensures the tone resonates with Gen Z values: authenticity, inclusivity, skepticism toward corporate speak. Flags anything that feels performative or out of touch. |
| `@inclusive language reviewer` | Reviews for gender-neutral language, accessibility, neurodiversity awareness, and cultural sensitivity across Gen Z's diverse demographics. |

> **en-genz-specific notes:**
> - Gen Z voice ≠ slang dump. It's about **tone**: casual, direct, slightly
>   self-aware, low tolerance for corporate filler.
> - Emoji and punctuation carry meaning. "okay." ≠ "okay!" ≠ "okay" ≠ "ok 👍"
> - Avoid: "Don't miss out!", "synergy", "leverage", anything LinkedIn-coded.
> - This variant should feel like a friend texting, not a brand trying to be hip.
> - Slang dates fast. Flag any slang with a `[shelf-life: short]` note so it can
>   be reviewed on a cycle.

---

### 🇩🇪 German (`de`)

| Role | Focus |
|------|-------|
| `@native market copywriter (german)` | Writes clear, modern German. Manages compound nouns without creating unreadable monsters. Knows when to use du vs. Sie based on product voice. |
| `@german precision reviewer` | Ensures technical accuracy — German users expect precise, unambiguous language. Catches vague translations that work in English but feel sloppy in German. |
| `@german cultural consultant` | Navigates data privacy sensitivities (GDPR awareness is culturally ingrained), formality expectations, and regional differences (DE/AT/CH). |

> **de-specific notes:**
> - German strings are often **20–35% longer** than English. UI must accommodate.
> - Compound nouns are one word — don't break them (Datenschutzeinstellungen).
> - du (informal) vs. Sie (formal) is a **product-level decision**. Tech products
>   increasingly use "du" but it's not universal.
> - Austria (de-AT) and Switzerland (de-CH) have vocabulary differences. "Jänner"
>   vs. "Januar", "Velo" vs. "Fahrrad". Decide if you need regional variants.

---

### 🇪🇸 Spanish (`es`)

| Role | Focus |
|------|-------|
| `@native market copywriter (spanish)` | Writes clear, modern Spanish. Must specify target variant: Spain (es-ES), Latin America neutral (es-419), or country-specific (es-MX, es-AR, etc.). |
| `@spanish regional variant reviewer` | Catches vocabulary and tone differences across regions. "computadora" vs. "ordenador", "celular" vs. "móvil", voseo vs. tuteo. Ensures the chosen variant is consistent. |
| `@spanish cultural consultant` | Flags formality mismatches (tú vs. usted), culturally loaded phrases, and humor/idioms that don't cross borders within the Spanish-speaking world. |

> **es-specific notes:**
> - Latin American neutral (es-419) is a common starting point but it's a
>   compromise — no region fully identifies with it.
> - Gendered language is a live issue. Decide on a product policy for inclusive
>   language (e.g., "usuarios" vs. "usuarios/as" vs. "usuaries").
> - Strings may be **10–20% longer** than English.

---

### 🇫🇷 French (`fr`)

| Role | Focus |
|------|-------|
| `@native market copywriter (french)` | Writes modern, clear French. Navigates the tu/vous distinction based on product voice. Avoids overly anglicized phrasing. |
| `@french linguistic standards reviewer` | Ensures compliance with Académie Française guidelines where appropriate, and knows when to break from them for natural digital communication. Handles Quebec French (fr-CA) differences when needed. |
| `@french cultural consultant` | Flags cultural assumptions, humor that doesn't translate, and sensitivities around formality. French users tend to expect a more polished, formal tone than English speakers. |

> **fr-specific notes:**
> - French strings are typically **15–30% longer** than English. Plan for overflow.
> - France French (fr-FR) and Canadian French (fr-CA) have meaningful vocabulary
>   and tone differences — treat as separate locales if both markets matter.
> - Typographic conventions differ: French uses non-breaking spaces before
>   `:`, `;`, `!`, `?`.

---

### 🇮🇹 Italian (`it`)

| Role | Focus |
|------|-------|
| `@native market copywriter (italian)` | Writes natural, modern Italian for digital products. Balances warmth and clarity. Comfortable with concise UI copy — Italian can be elegant and compact when needed. |
| `@italian linguistic reviewer` | Ensures proper use of formal (Lei) vs. informal (tu) register. Catches awkward anglicisms and ensures grammatical precision — Italian speakers notice errors. |
| `@italian cultural consultant` | Navigates regional sensitivities (north/south cultural differences), humor norms, and any content that could feel patronizing or culturally tone-deaf. |

> **it-specific notes:**
> - Italian strings are typically **15–25% longer** than English.
> - Lei (formal) vs. tu (informal) is a product-level decision. Most modern apps
>   use "tu" but financial/healthcare products often use "Lei".
> - Double consonants and accents matter — typos in Italian feel more jarring
>   than in English. "perché" ≠ "perche".
> - Many tech terms are borrowed from English but italianized: "cliccare",
>   "scaricare" (download), "loggarsi" (to log in). Use established conventions.

---

### 🇯🇵 Japanese (`ja`)

| Role | Focus |
|------|-------|
| `@native market copywriter (japanese)` | Writes natural Japanese for digital products. Masters the balance between polite (です/ます) and casual forms depending on product voice. Comfortable with extremely concise UI writing. |
| `@japanese cultural consultant` | Navigates keigo (敬語) levels, seasonal/contextual appropriateness, and indirect communication norms. Flags anything that feels too direct or presumptuous for the Japanese market. |
| `@japanese ux terminology reviewer` | Ensures consistency with established Japanese software/UX conventions (e.g., 保存 for Save, キャンセル for Cancel). Catches cases where katakana loanwords are preferred over native Japanese and vice versa. |

> **ja-specific notes:**
> - Three scripts (hiragana, katakana, kanji) serve different purposes. Katakana
>   is standard for foreign loanwords and many tech terms.
> - Japanese UI strings are often **shorter** than English. Don't pad them.
> - Honorific tone must be consistent across the entire product.
> - Counter words (助数詞) are mandatory when expressing quantities.

---

### 🇰🇷 Korean (`ko`)

| Role | Focus |
|------|-------|
| `@native market copywriter (korean)` | Writes modern Korean for digital contexts. Navigates the formal (합니다) vs. polite-casual (해요) spectrum based on product voice. |
| `@korean cultural consultant` | Manages hierarchical language (honorifics, age-related nuances), Confucian-influenced communication patterns, and sensitivities around Japan/China references. |
| `@korean digital-native reviewer` | Catches unnatural phrasing, ensures consistency with Korean app/web conventions (e.g., 로그인, 회원가입). Knows current slang boundaries — what's acceptable in a product vs. too informal. |

> **ko-specific notes:**
> - Korean has strict SOV (subject-object-verb) order — English sentence structure
>   rarely maps directly.
> - Honorific level must be decided at the product level and applied consistently.
> - Many UI terms use English loanwords in Hangul (로그인, 비밀번호, 다운로드).
> - Spacing rules differ from English — Korean spaces between words but not always
>   where you'd expect.

---

### 🇹🇭 Thai — Standard (`th`)

| Role | Focus |
|------|-------|
| `@native market copywriter (thai)` | Writes natural, modern standard Thai. Avoids overly formal royal/literary registers unless the product context demands it. Understands the tonal gap between written and spoken Thai and lands in the right register. |
| `@thai cultural consultant` | Flags religious sensitivities (Buddhist references, monarchy-related terms), superstition-adjacent language (colors, numbers), and social hierarchy nuances (pronouns, politeness particles). |
| `@thai digital-native reviewer` | Reviews for how Thai internet users actually communicate. Catches translations that sound like textbooks instead of apps. Knows when transliterated English (ทับศัพท์) is more natural than a forced Thai equivalent. |

> **th-specific notes:**
> - Thai has **no spaces between words** — line-break behavior matters for UI.
> - Politeness particles (ครับ/ค่ะ) imply speaker gender. Decide on a product-level
>   policy: omit them, use gender-neutral alternatives (นะ), or parameterize.
> - Many tech terms use transliterated English and should NOT be translated:
>   "อีเมล" not "ไปรษณีย์อิเล็กทรอนิกส์", "แดชบอร์ด" not "แผงควบคุม".
> - Counter words (ลักษณนาม) are mandatory for quantities.
> - No pluralization in Thai. Do not generate plural key variants.

---

### 🇹🇭 Thai — Gen Z (`th-genz`)

| Role | Focus |
|------|-------|
| `@gen z voice copywriter (thai)` | Writes in the voice of young, digitally fluent Thai users. Blends Thai with code-switched English, internet slang, and platform-native expressions. Knows the difference between authentic Gen Z Thai and a boomer trying. |
| `@thai internet culture insider` | Tracks Thai Twitter/TikTok/Dek-D culture, meme cycles, fandom language (วงการ), and platform-specific norms. Understands that Thai Gen Z online culture borrows heavily from K-pop, anime, and Western internet culture — but remixes it. |
| `@social psychologist (thai youth culture)` | Ensures tone aligns with Thai Gen Z sensibilities: irreverent but not disrespectful, casual but self-aware, allergic to corporate ภาษาราชการ. Understands how Thai generational dynamics shape communication. |
| `@thai cultural consultant` | Same as standard Thai — monarchy/religious/hierarchy sensitivities still apply regardless of audience age. Gen Z doesn't mean boundary-free. |

> **th-genz-specific notes:**
> - Heavy **code-switching** between Thai and English, sometimes mid-sentence:
>   "เรา vibe กับ feature นี้มาก" is natural; fully Thai equivalent sounds stiff.
> - Emoji, kaomoji, and ตัวอักษรยืด (stretched text like "มากกกก") are part of
>   the voice. Use them judiciously — the tone should feel native, not forced.
> - ครับ/ค่ะ particles are often dropped entirely in Gen Z casual register.
> - Sarcasm and self-deprecation (เซลฟ์, มุก) are common tones. Direct sincerity
>   can read as cringe if overdone.
> - Slang cycles fast. Flag terms with `[shelf-life: short]` for periodic review.
>   Examples that may already be dated: "อิอิ", "555+", "ชิมิ".
> - This variant should feel like a LINE group chat with friends, not an ad.

---

### 🇹🇭 Thai — Isan (`th-isan`)

| Role | Focus |
|------|-------|
| `@native isan copywriter` | Writes in authentic Isan (อีสาน) voice. Fluent in Isan vocabulary, particles, and sentence patterns that diverge from Central Thai. Knows which Isan words are widely understood vs. deeply regional. |
| `@isan regional cultural advisor` | Understands Isan identity, Lao-Isan linguistic overlap, rural-urban dynamics, and cultural pride. Flags content that might feel patronizing or that reduces Isan to a stereotype. |
| `@sociolinguistic consultant (isan)` | Navigates the code-switching reality of Isan speakers — most are bilingual Isan/Central Thai. Decides when to use pure Isan vs. Isan-flavored Thai vs. Central Thai with Isan particles, depending on product context. |
| `@thai cultural consultant` | Monarchy/religious/hierarchy sensitivities still apply. Additionally, Isan has its own Buddhist and animist cultural references. |

> **th-isan-specific notes:**
> - Isan (ภาษาอีสาน) is closely related to Lao. Many words are shared but
>   written in Thai script when used in Thai digital contexts.
> - Tone and particle differences from Central Thai are significant:
>   "บ่" (not) instead of "ไม่", "เด้อ/เด๊อ" instead of "นะ", "สิ" for future tense.
> - Vocabulary diverges for everyday concepts: "แซบ" (delicious) vs. "อร่อย",
>   "เว้า" (speak) vs. "พูด", "บักหำ/อีหลี" as intensifiers.
> - The product must decide its **register strategy**: pure Isan for cultural
>   authenticity, or Isan-accented Central Thai for broader accessibility.
> - Using Isan language in a product is a **cultural respect signal** — but doing
>   it poorly is worse than not doing it at all. Isan speakers will notice.
> - No pluralization. Counter words may differ from Central Thai.

---

### 🇹🇭 Thai — Lanna (`th-lanna`)

| Role | Focus |
|------|-------|
| `@native lanna copywriter` | Writes in authentic Lanna (ล้านนา / คำเมือง) voice. Understands the Lanna vocabulary, tonal system, and sentence structures that distinguish it from Central Thai. Knows which คำเมือง terms are still in active use vs. archaic. |
| `@lanna regional cultural advisor` | Deep understanding of Northern Thai identity and Lanna cultural heritage. Navigates the tension between preserving Lanna language and making it accessible in digital contexts. Understands Lanna-specific customs, festivals (ยี่เป็ง, สงกรานต์เมือง), and values. |
| `@sociolinguistic consultant (lanna)` | Navigates the reality that many younger Lanna speakers primarily use Central Thai and may recognize but not actively speak คำเมือง. Decides on an appropriate blend that feels authentic without being inaccessible. |
| `@thai cultural consultant` | Core Thai cultural sensitivities apply, plus Lanna-specific Buddhist traditions and local spiritual practices. |

> **th-lanna-specific notes:**
> - Lanna (คำเมือง) has its own historical script (ตัวเมือง/อักษรธรรม), but modern
>   digital usage writes Lanna words in standard Thai script.
> - Key vocabulary differences: "อู้" (speak) vs. "พูด", "แอ่ว" (visit/go out)
>   vs. "เที่ยว", "ลำ" (beautiful) vs. "สวย", "ตะกี้" (just now).
> - Particles differ: "เจ้า" is the quintessential Lanna politeness particle.
> - **Lanna language preservation** is a cultural cause. Using คำเมือง in a product
>   carries cultural weight — it signals respect for Northern identity.
> - Younger speakers (especially urban Chiang Mai) may use only a handful of
>   Lanna words mixed with Central Thai. The product must decide if it targets
>   fluent คำเมือง speakers or the Lanna-flavored-Thai majority.
> - No pluralization. Counter words may differ from Central Thai.

---

### 🇹🇭 Thai — Southern (`th-south`)

| Role | Focus |
|------|-------|
| `@native southern thai copywriter` | Writes in authentic Southern Thai (ภาษาใต้) voice. Captures the fast, direct, no-nonsense communication style that characterizes Southern speech. Knows the vocabulary, particles, and rhythms. |
| `@southern thai regional cultural advisor` | Understands Southern Thai identity, maritime/fishing culture influences, Muslim-Buddhist cultural coexistence in the South, and regional pride. Flags content that could be insensitive to the South's cultural diversity. |
| `@sociolinguistic consultant (southern thai)` | Navigates the directness and intensity of Southern speech patterns — what sounds normal in ภาษาใต้ might sound aggressive in Central Thai. Calibrates tone for digital product context. |
| `@thai cultural consultant` | Core sensitivities apply, plus awareness of the Muslim-majority deep South provinces (Pattani, Yala, Narathiwat) and their unique cultural context. |

> **th-south-specific notes:**
> - Southern Thai (ภาษาใต้) is known for being **fast, direct, and expressive**.
>   Translations should capture this energy without sounding harsh in text.
> - Key vocabulary: "หว่า" (particle, similar to นะ but more assertive),
>   "ดิ" (particle), "แหละ" used differently from Central Thai,
>   "เหลียว" (to look), "หรอย" (delicious) vs. "อร่อย".
> - Southern Thai has distinct contracted forms and elisions that make it
>   sound faster: words are often shortened.
> - **Cultural sensitivity**: Southern Thailand includes Muslim-majority provinces.
>   Content should not assume Buddhist cultural context for all Southern users.
> - The product must decide whether to target the broadly understood "Southern
>   accent" register or go deep into specific sub-regional variations
>   (Nakhon Si Thammarat vs. Surat Thani vs. Songkhla all differ).
> - No pluralization. Counter words may differ from Central Thai.

---

### 🇹🇭 Thai — Bupphe / Ayutthaya Classical (`th-bupphe`)

| Role | Focus |
|------|-------|
| `@ayutthaya court copywriter` | Writes in the บุพเพสันนิวาส-flavored classical Thai voice — modern concepts expressed through Ayutthaya-era diction, pronouns, and particles. Not museum-piece archaic, but charming and evocative, like Kadesurang navigating the old world with modern wit. Knows the balance between classical elegance and playful warmth that made the show beloved. |
| `@thai historical language consultant` | Deep knowledge of Ayutthaya-period Thai language: ราชาศัพท์ (royal vocabulary), Pali/Sanskrit-derived terms, archaic sentence structures, and classical literary registers. Ensures historical vocabulary is used correctly — not just sprinkled randomly for flavor. Catches anachronisms. |
| `@bupphe tone calibrator` | The show's magic was blending old and new — Kadesurang's modern personality in an ancient setting. This role ensures the translation hits that same sweet spot: classical enough to feel distinctly Ayutthaya, modern enough to be understood and delightful. Prevents the translation from becoming either a dry textbook or a costume-drama parody. |
| `@thai cultural consultant` | Core Thai cultural sensitivities apply with extra weight. Monarchy language (ราชาศัพท์) must be used correctly — misuse of royal vocabulary is not just a translation error, it's a cultural offense. Buddhist and Brahmanical references from the Ayutthaya period carry specific meaning. |

> **th-bupphe-specific notes:**
>
> - **This is NOT pure archaic Thai.** It is a modern-classic blend inspired by
>   the voice of บุพเพสันนิวาส (Love Destiny, 2018) — the mega-hit lakorn set
>   during King Narai's reign in กรุงศรีอยุธยา (1656–1688). The show popularized
>   a charming, accessible classical Thai voice that Thai audiences fell in love with.
>
> - **Pronouns** — the most immediately distinctive feature:
>   - **ข้า** (I/me) — used for self-reference, gender-neutral in this context
>   - **เจ้า** (you) — intimate/equal address, THE signature of the show
>   - **ท่าน** (you) — respectful, for addressing superiors or strangers
>   - **ออเจ้า** — the iconic affectionate address particle, became the catchphrase
>     of 2018 Thailand. Use it, but don't overdo it.
>   - Avoid modern ฉัน/คุณ/ผม/หนู entirely.
>
> - **Particles and politeness markers:**
>   - **เพคะ** (female polite particle) instead of modern ค่ะ
>   - **ขอรับ** (male polite acknowledgment) instead of modern ครับ
>   - **เจ้าค่ะ / เจ้าขา** (female polite, Ayutthaya-flavored)
>   - **ดอก** (softening particle, archaic)
>   - **แล** / **เล่า** (question/emphasis particles)
>   - **เถิด** (urging particle, "go ahead", "please do")
>
> - **ราชาศัพท์ (Royal vocabulary)** — use judiciously, not for every word:
>   - เสวย (eat, royal) — but only when contextually appropriate
>   - บรรทม (sleep, royal)
>   - ทรงพระกรุณา (to be gracious)
>   - ประทาน (to give, from superior)
>   - สิ้นพระชนม์ (to pass away, royal) vs. ตาย
>   - The product must decide **how much ราชาศัพท์ to use**. The show used it
>     for court scenes but relaxed it for informal character interactions.
>
> - **Pali/Sanskrit-heavy diction:**
>   - Prefer classical loan words where they add flavor: บุพเพสันนิวาส (destined
>     connection from past lives), กรรม (karma), วาสนา (fortune/destiny),
>     ลิขิต (fate/decree), พระคุณ (kindness/grace).
>   - But don't force them where modern Thai is clearer. The show succeeded
>     because it was *accessible* classical, not academic.
>
> - **Sentence structure and cadence:**
>   - More formal, sometimes inverted word order for poetic effect.
>   - Longer, more elaborate phrasing is acceptable — this register is not
>     optimized for brevity like modern UI Thai.
>   - Sentences may begin with "ข้า..." or address with "ออเจ้า..." naturally.
>
> - **Archaic vocabulary highlights:**
>   - "จัก" (will/shall) instead of modern "จะ"
>   - "มิ" (not) instead of modern "ไม่" in formal contexts
>   - "หม่อมฉัน" (I, humble female to royalty)
>   - "นางใน" (inner court women)
>   - "พ่อเจ้าประคุณ" (respectful address)
>   - "สิ้นกรรม" (exclamation of exasperation — Kadesurang's signature!)
>
> - **The Kadesurang effect** — the show's charm was a modern woman reacting
>   to an ancient world. The best th-bupphe translations capture this duality:
>   classical words expressing modern feelings. For example:
>   - "Loading..." → "กำลังเตรียมการ... โปรดรอสักครู่เถิด ออเจ้า"
>   - "Are you sure?" → "เจ้าแน่ใจแล้วหรือ?"
>   - "Delete" → "ลบทิ้ง" (some modern terms stay modern — don't force it)
>   - "Welcome back" → "ยินดีต้อนรับกลับมา ออเจ้า"
>   - "Error" → "เกิดเหตุขัดข้อง"
>   - "Settings" → "การตั้งค่า" (technical terms stay modern)
>
> - **When to stay modern:** Technical/UI terms that have no classical equivalent
>   should remain in modern Thai or transliterated English. Don't invent fake
>   archaic terms — it breaks immersion worse than a modern word does.
>   "อีเมล" is fine. "แดชบอร์ด" is fine. Don't try to make them classical.
>
> - **Register consistency:** Pick a register level and stick with it across the
>   product. The recommended default is **"casual court"** — as if two educated
>   Ayutthaya nobles are having a friendly conversation, not a formal audience
>   with the king. This matches the show's dominant tone.
>
> - No pluralization. Counter words (ลักษณนาม) follow standard Thai conventions.
> - The locale name "bupphe" comes from the Thai abbreviation บุพเพฯ, commonly
>   used by fans to refer to the show.

---

### 🇨🇳 Simplified Chinese (`zh-CN`)

| Role | Focus |
|------|-------|
| `@native market copywriter (zh-cn)` | Writes for mainland China's digital market. Familiar with the concise, punchy style of Chinese mobile-first interfaces. |
| `@chinese cultural consultant` | Flags politically sensitive terms, government/regulatory language requirements, and cultural taboos (numbers, colors, historical references). |
| `@chinese platform convention reviewer` | Ensures terminology aligns with established conventions from major Chinese platforms (WeChat, Alipay, Taobao). Chinese users expect specific terms for common actions. |

> **zh-CN-specific notes:**
> - Simplified Chinese is extremely concise — translations are often **shorter**
>   than English. "Are you sure you want to delete this?" → "确认删除？"
> - Mainland China conventions differ significantly from Taiwan (zh-TW) and
>   Hong Kong (zh-HK) — **never mix them**.
> - Some English tech terms are kept as-is (e.g., "WiFi", "App"), others are
>   always translated. Follow platform conventions.
> - Counter words (量词) are mandatory for quantities.

---

### 🇹🇼 Traditional Chinese — Taiwan (`zh-TW`)

| Role | Focus |
|------|-------|
| `@native market copywriter (zh-tw)` | Writes natural Traditional Chinese for Taiwan's market. Tone is generally softer and more polite than zh-CN equivalents. |
| `@taiwanese cultural consultant` | Understands Taiwan-specific cultural context, local idioms, and sensitivities around cross-strait terminology. Ensures language reflects Taiwanese — not mainland — norms. |
| `@taiwanese digital convention reviewer` | Verifies terminology matches what Taiwanese users expect from local apps and services (LINE, PChome, etc.). Catches mainland-isms that would feel foreign to Taiwanese users. |

> **zh-TW-specific notes:**
>
> **Rule — zh-CN is NOT a source for zh-TW.** Do NOT use character-conversion
> tools (OpenCC, opencc-js, s2t, etc.) as the primary path for producing
> zh-TW from zh-CN — even if the user explicitly asks for "just convert
> the characters" or "I only need the traditional version". OpenCC's phrase
> dictionaries look like they bridge the gap but they don't: tone, register,
> and idiom diverge at a level no automated pass captures.
>
> **Why:** mainland and Taiwanese Chinese diverge at the vocabulary, idiom,
> and register level, not just the character level. A mechanically converted
> zh-TW file reads as mainland text in traditional clothes. Taiwanese users
> notice immediately. Examples of divergence beyond characters: 軟體 vs. 软件
> (software), 記憶體 vs. 内存 (memory), 網路 vs. 网络 (network), plus tone
> conventions (zh-TW skews softer/more polite than zh-CN).
>
> **What to do when a user asks for mechanical conversion:**
>
> 1. Push back before proposing any script. Explain that zh-CN and zh-TW
>    need separate translation passes, not a character swap.
> 2. If the user confirms they want a starting-point draft only, OpenCC is
>    acceptable as a draft — but flag it as unshippable. Require a proper
>    retranslation pass through `@native market copywriter (zh-tw)`,
>    `@taiwanese cultural consultant`, and `@taiwanese digital convention
>    reviewer` before the file ships to users.
> 3. If the user declines the retranslation pass, produce the OpenCC draft
>    with a top-of-file comment warning that the strings have not been
>    localized for Taiwan, and surface the warning in the response.
>
> **Other notes:**
>
> - Taiwan-specific tech vocabulary you should know: 軟體 vs. 软件 (software),
>   記憶體 vs. 内存 (memory), 網路 vs. 网络 (network).
> - Counter words (量詞) are mandatory for quantities.

---

### 🇭🇰 Hong Kong Chinese (`zh-HK`)

| Role | Focus |
|------|-------|
| `@native market copywriter (zh-hk)` | Writes in Hong Kong's unique written style — Traditional Chinese characters with Cantonese-influenced vocabulary and phrasing. Comfortable with the local blend of formal written Chinese and colloquial Cantonese expressions used in digital products. |
| `@hong kong cultural consultant` | Understands HK-specific cultural identity, local idioms, and sensitivities. Navigates the distinct position of Hong Kong culture relative to both mainland China and Taiwan. Knows local references (TVB culture, local food terms, HK humor). |
| `@cantonese linguistic consultant` | Decides when to use standard written Chinese (書面語) vs. colloquial written Cantonese (粵語白話文) based on product context. Formal products lean toward 書面語; casual/consumer products can incorporate Cantonese. |
| `@hong kong digital convention reviewer` | Ensures terminology matches local HK app/web conventions. HK has its own established terms that differ from both zh-CN and zh-TW (e.g., 巴士 for bus vs. 公交車/公車). |

> **zh-HK-specific notes:**
> - Hong Kong Chinese is **not just Traditional Chinese**. It is not zh-TW with
>   different vocab. HK has its own written voice shaped by Cantonese.
> - Two written registers coexist:
>   - **書面語 (written Chinese)**: formal, used in news, government, business.
>   - **粵語白話文 (written Cantonese)**: informal, used in messaging, social media,
>     casual apps. Uses Cantonese-specific characters (嘅, 唔, 咁, 嗰, 係).
> - Product must decide: **書面語 for formality, or allow written Cantonese for
>   warmth and authenticity?** Many modern HK apps use a blend.
> - HK-specific vocabulary: 巴士 (bus), 士多 (store), 的士 (taxi), 雪糕 (ice cream),
>   手機 (mobile phone — same as TW, not 手机 as in CN).
> - English loanwords and code-mixing are extremely common in HK: "send 個 email",
>   "book 咗 table". The product should decide how much code-mixing is acceptable.
> - Counter words (量詞) follow Cantonese conventions, which sometimes differ from
>   Mandarin: 部 (for vehicles, machines) is more common than 辆/輛 in spoken usage.

---

## Adding More Languages

When adding a new language or variant, follow this template:

```markdown
### [Flag] Language — Variant (`locale-code`)

| Role | Focus |
|------|-------|
| `@native market copywriter (language)` | [How this person writes for the local market] |
| `@[language] cultural consultant` | [What cultural landmines they watch for] |
| `@[language] [specialty] reviewer` | [Language-specific technical concern] |

> **locale-specific notes:**
> - [Key linguistic characteristic that affects UI]
> - [Common translation pitfall]
> - [Product-level decision that must be made]
> - [Pluralization behavior]
```

### Minimum Team Per Language

1. `@native market copywriter` — gets the voice right
2. `@cultural consultant` — prevents cultural missteps
3. A **specialist reviewer** — unique to the language's challenges

### Additional Roles to Consider

Depending on the language/variant, you may also need:

- `@internet culture insider` — for Gen Z or digital-native variants
- `@social psychologist (youth culture)` — for age-targeted variants
- `@regional cultural advisor` — for dialects and regional variants
- `@sociolinguistic consultant` — for languages with complex register/dialect dynamics
- `@inclusive language reviewer` — for languages navigating gendered language debates
- `@rtl/layout reviewer` — for RTL languages (Arabic, Hebrew, Urdu, etc.)
- `@linguistic consultant` — for languages with complex grammar, honorifics, or script systems
- `@historical language consultant` — for period-specific or archaic language variants
- `@tone calibrator` — for variants that blend registers (e.g., classical + modern)
