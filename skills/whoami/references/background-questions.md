# whoami — Background Questions

Asked in Step 4, conversationally, one at a time, in the agent's voice. Every
item is **opt-out** — if the user passes, move on without friction. On a re-run,
confirm known answers rather than re-asking.

## The questions

1. **Role** — "First — what do you do? Your role, or the kind of work you spend
   your time on." → `background.role`
2. **Field** — "And what field or industry is that in?" → `background.field` +
   `domain_bucket`
3. **AI experience** — "How much have you worked with AI agents before — new to
   this, dabbled, or part of your daily kit?" → `background.ai_experience`
   (`new` | `some` | `high`)
4. **Primary uses** — "What do you mostly want to use me for? Code, writing,
   research, planning — whatever comes to mind." → `background.primary_uses`
5. **Language** — "What language, or languages, do you want to work in?" →
   `background.languages`
6. **Anti-patterns** — "When you work with AI assistants — me or any other —
   what do they most often get *wrong*? The concrete moments: things like
   'buries the answer instead of leading with it,' 'keeps relitigating after
   I've decided,' or 'over-explains things I already know.'" → `anti_patterns`.
   Capture 2–3 as short, checkable phrases; if an answer is abstract ("too
   verbose"), ask one follow-up to pin it to an observable moment.
7. **Free text** — "Anything else you'd want me to know about you or how you
   like to work? Totally optional." → routed per the policy below

For a `new` user, briefly say why you're asking ("this helps me tailor how I
work with you"). `field` + `primary_uses` set the domain bucket for
`adaptive-phrasing.md`; `ai_experience` sets the explanation level.

## Data-handling policy

- **Never solicit protected attributes.** Questions 1–6 stay scoped to
  collaboration-relevant facts. The free-text field is the *only* entry point
  for anything sensitive, and only if the user volunteers it. Protected
  attributes — treat every one of these as sensitive (never scored, never in
  the whoami profile, kept only as a separate confirmed memory): race,
  ethnicity, national origin, religion, age, sex, sexual orientation, gender
  identity, immigration status, disability, serious illness, union
  membership. Same list the runtime memory rules and `handshake`'s never-ask
  list use — keep them aligned.
- **Volunteered sensitive/protected info:** keep only with explicit per-item
  confirmation ("want me to remember that?"). Store as a *separate*, standard
  `user`-type memory — never in the whoami profile, never scored, never on
  shareable artifacts.
- **Secrets** (SSNs, bank/account numbers, passwords, government IDs): never
  store. If volunteered, drop them and say so once.
- Defer to the host runtime's data policy; never override it.
