---
name: i18n
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
  Does NOT trigger on defining or glossing a single word/phrase inside a sentence
  ("what does X mean here", "define X in context") — that is the `define` skill. This
  skill is for i18n files and shipping localized strings, not inline word-meaning lookups.
---

# i18n — Translation Files & Cultural Rewriting

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

## Per-locale teams, pluralization & cultural notes

The per-locale **translation teams**, **pluralization rules**, **counter-word
rules**, and all **cultural notes** live in a shared reference:
[`references/locale-knowledge.md`](references/locale-knowledge.md).

This is the shared cultural engine for two skills — `i18n` (this one: translation-file
production) and `define` (inline contextual definition/translation). When working a
specific locale, load it: it carries the per-locale role tables, register systems,
dialect vocabulary, classical forms (e.g. th-bupphe), honorifics, classifiers, the
pluralization category table, and the zh-CN → zh-TW "not a character swap" rule.

Edit locale facts there once; both skills inherit. This skill layers its file-handling
discipline (Part 1) and its `@ux localization reviewer` / `@i18n engineer` roles on top;
`define` layers its own comprehension lenses (lexicographer, etymology, register) for
learner-facing glosses.

