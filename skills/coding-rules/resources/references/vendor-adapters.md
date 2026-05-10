# Vendor Adapters — Ports-and-Adapters for Third-Party Services

A doctrine for keeping third-party vendor coupling out of business logic. Define domain-shaped interfaces (**ports**) at the project boundary, implement vendor-specific **adapters**, and wire the concrete in a **composition root**. The pattern is always-on from project setup; adapters are added per vendor, only when a vendor enters the project.

> **Why a doctrine, not a framework.** TypeScript has DI containers (Inversify, tsyringe, NestJS DI, Effect.ts), but most projects don't need them. The pattern below is hand-rolled — roughly 50 lines of boilerplate per service — and travels across runtimes (Bun, Node, Deno, edge). DI frameworks stay opt-in (`references/external-resources.md`).

The rule's value is **platform longevity**. Developers leave; projects stay. Direct vendor imports throughout the codebase make vendor switching expensive and make domain code harder to read for anyone who doesn't speak fluent AWS / Stripe / Clerk.

---

## File Structure

Recommended layout under the project's source root:

```
src/
├── ports/              # Domain-shaped interfaces (no vendor types)
│   ├── database.ts
│   ├── auth.ts
│   └── payments.ts
├── adapters/           # Vendor-specific implementations
│   ├── neon/
│   ├── clerk/
│   └── stripe/
└── composition.ts      # The ONLY file that imports vendor SDKs
```

Business logic imports from `ports/` only. Adapters import from both `ports/` (to implement) and the vendor SDK (to translate). The composition root wires concrete adapters to the ports.

> **Naming escape hatch.** `ports/` is the recommended directory name (pairs with "ports-and-adapters"; signals the architectural intent to anyone Googling the term). If the project already uses `contracts/`, `interfaces/`, or similar, follow existing convention — don't relitigate.

---

## The Non-Negotiable Rule

**No business logic imports the vendor SDK directly.** That's the testable property — agents and reviewers can grep for vendor package imports outside `adapters/` and `composition.ts` and flag any matches.

```ts
// ❌ in src/services/billing.ts
import Stripe from 'stripe'

// ✅ in src/services/billing.ts
import type { Payments } from '../ports/payments'
```

---

## Pattern Always-On From Day One

The structure (`ports/`, `adapters/`, `composition.ts`) is established at project setup, even with a single vendor and no plan to switch. The pattern earns its keep regardless:

- **Domain vocabulary.** `userRepo.findById(id)` reads cleanly; `db.execute(neon.sql\`SELECT...\`)` leaks the storage choice into business logic
- **Test seams come free.** Every port is automatically mockable; no retrofit when tests are added later
- **Migration path stays open.** The cost of direct imports compounds with every call site; the cost of the abstraction is paid once, upfront
- **Onboarding.** New developers learn the project's domain language, not the vendor's API surface

The cost asymmetry is the core argument: building the pattern when never needed is small overhead; needing the pattern when it isn't there is N files of refactor (often the cost that blocks a vendor switch outright).

---

## Adapters Are Added Per Vendor

The pattern is the structure; adapters are the work. Don't pre-build adapters for hypothetical vendors. When a new vendor connection enters the project:

1. Define (or extend) the relevant port from **consumer needs**, not the vendor's API surface
2. Implement the adapter in `src/adapters/<vendor>/`
3. Wire it in `composition.ts`

> **Critical guardrail.** Defining the port by reverse-engineering the vendor's API produces a "Neon-shaped abstraction" that no other vendor fits cleanly. Write the port *before* opening the vendor's docs; let the adapter absorb the impedance mismatch.

---

## Existing-Code Rule

**Agents do NOT refactor existing direct vendor imports.** The doctrine applies to **new vendor connections** and new code paths through new ports. Legacy code stays as-is until migration is deliberately scheduled.

If touching a legacy file for an unrelated reason, no opportunistic refactor — keep the diff minimal. Migration is a workstream tracked in `ROADMAP.md`, not a side effect of unrelated work.

### What counts as refactoring (extension to legacy files)

When a user asks to add code to a file that already imports a vendor SDK directly, the *additions* should match the file's existing pattern — even though that pattern violates the always-on rule. Specifically:

- **Adding a constructor parameter** to a class that uses direct vendor imports counts as refactoring; don't.
- **Creating a new port or adapter** for a vendor that's already imported directly in the file you're editing counts as refactoring; don't.
- **Adding a new method that uses a different vendor-access pattern** than the surrounding code counts as refactoring; the new method should look like it was written by whoever wrote the surrounding methods.

**Rule of thumb:** if the user asked you to add a method to a legacy file, the resulting diff should be confined to that file and consist of new lines that match the file's existing style. New ports, new adapters, and constructor changes belong to a separate, deliberate migration workstream — never to a method-add request.

---

## Throwaway Code Exemption

The pattern is for production business logic that will outlive the current developer. Exempt:

- One-off scripts (data migrations, audit queries)
- Internal CLI tools
- Throwaway prototypes
- Anything that won't live past a quarter

For these, importing the vendor SDK directly is fine. The abstraction overhead exceeds the lifespan benefit.

---

## Handling Vendor-Specific Features

Not every vendor capability fits the common port. Three honest tiers:

### Tier 1 — Domain operations → main port

Every vendor must implement. CRUD on entities, standard auth flows, charge / refund / void:

```ts
// ports/database.ts
export interface Database {
  findUser(id: UserId): Promise<User | null>
  createUser(input: NewUser): Promise<User>
  updateUser(id: UserId, patch: Partial<User>): Promise<User>
}
```

### Tier 2 — Vendor-specific capabilities → capability ports

Some vendors support; some don't. Define a separate role interface and have the adapter implement multiple ports:

```ts
// ports/database-branching.ts
export interface DatabaseBranching {
  createBranch(name: string): Promise<BranchRef>
  switchBranch(ref: BranchRef): Promise<void>
}

// adapters/neon/index.ts
export class NeonDatabase implements Database, DatabaseBranching { /* both */ }

// adapters/supabase/index.ts
export class SupabaseDatabase implements Database { /* only the base port */ }
```

Business logic that needs branching imports `DatabaseBranching`. When you switch Neon → Supabase, every file importing `DatabaseBranching` fails to compile. **That's the feature** — vendor-specific dependencies are surfaced at compile time, not at runtime.

This pattern is sometimes called "role interfaces" (Steve Freeman, *Growing Object-Oriented Software*) or "interface segregation" (the I in SOLID).

### Tier 3 — Opaque pass-through → `Record<string, unknown>`

Truly opaque data the adapter can't interpret and business logic never reads — webhook payloads logged for audit, vendor metadata kept for replay tooling:

```ts
interface WebhookEvent {
  eventType: string
  occurredAt: Date
  raw: Record<string, unknown>  // logged, never inspected by business logic
}
```

The contract is: business logic NEVER reads `raw`. If you find yourself reaching into it, that's a signal to add a typed field to the port — the data has graduated from opaque to semantic.

> **Avoid `extras<Partial<T>>` patterns.** A typed-extras field looks generic but either pollutes the port with vendor types (`T = NeonExtras`) or degrades to opaque untyped access. It encourages business logic to read vendor-specific fields, defeating the abstraction.

---

## Worked Example

```ts
// src/ports/auth.ts
export interface Auth {
  signIn(email: Email, password: Password): Promise<Session>
  verify(token: Token): Promise<UserId | null>
  signOut(token: Token): Promise<void>
}

// src/adapters/clerk/index.ts
import { createClerkClient } from '@clerk/clerk-sdk-node'
import type { Auth } from '../../ports/auth'

export class ClerkAuth implements Auth {
  constructor(
    private clerk = createClerkClient({ secretKey: process.env.CLERK_SECRET! }),
  ) {}

  async signIn(email: Email, password: Password): Promise<Session> {
    const result = await this.clerk.signIns.create({ identifier: email, password })
    return {
      token: result.token,
      userId: result.userId,
      expiresAt: new Date(result.expiresAt),
    }
  }
  // verify, signOut...
}

// src/composition.ts
import { ClerkAuth } from './adapters/clerk'
import { NeonDatabase } from './adapters/neon'
import type { Auth } from './ports/auth'
import type { Database } from './ports/database'

export const auth: Auth = new ClerkAuth()
export const db: Database = new NeonDatabase(process.env.DATABASE_URL!)

// src/services/onboarding.ts
import type { Auth } from '../ports/auth'
import type { Database } from '../ports/database'

export async function onboardUser(auth: Auth, db: Database, input: NewUser) {
  const user = await db.createUser(input)
  // No `import Stripe`, no `import { createClerkClient }`. Domain ops only.
  return user
}
```

To switch Clerk → Auth0: write `src/adapters/auth0/index.ts` implementing `Auth`, change one line in `composition.ts`. Business logic untouched.

---

## Pitfalls

- **Lowest-common-denominator trap.** Making the port so generic it can't use either vendor's good parts. Counter: define the port from *your* needs; if a feature isn't in the application's domain, it doesn't belong on the port.
- **Vendor-shaped abstraction.** Reverse-engineering the vendor's API into the port. Counter: write the port before opening the vendor's docs; use domain language.
- **Leaky abstractions.** Vendor-native features (Neon branching, Supabase RLS, Stripe Checkout) won't always fit cleanly. Counter: capability ports (Tier 2) for common cases; accept vendor-specific code for the rare ones — be honest rather than pretending.
- **Maintenance debt.** Each adapter is code you own — types, error mapping, tests, docs. Real cost. Counter: adapters are per-vendor on demand, not pre-built; the cost is bounded.
- **DI framework drift.** Reaching for Inversify/tsyringe at the first sign of complexity. Counter: hand-rolled wiring covers 80% of cases. Reach for a framework only when lifecycle management is real (scoped instances, request-scoped resolution, complex dependency graphs).

---

## Relationship to Other Docs

- **`references/working-patterns.md`** — pattern-matching applies: if `ports/` exists in the codebase, follow it; don't introduce a parallel `services/` or `interfaces/` folder.
- **`references/external-resources.md`** — DI frameworks (Inversify, tsyringe, Awilix, NestJS DI, Effect.ts) belong as passive pointers, not in the core doctrine.
- **`references/roadmap.md`** — migrating legacy direct imports to ports/adapters is a roadmap item, not a side effect of touching unrelated files.
- **`workflows/new-project.md`** — should scaffold `ports/`, `adapters/`, `composition.ts` at project setup so the structure exists before the first vendor lands. (Workflow wiring is a follow-up; this doctrine establishes the shape only.)

---

## When NOT to Use

- **Throwaway code** (above)
- **Single-use vendor SDKs in CLI tooling** with no business logic to protect
- **Vendor-as-product**: if the application's *value proposition* is being built ON a specific vendor (e.g., a Stripe-native dashboard, a Supabase admin tool), the adapter is theater — the vendor IS the product
- **Tiny apps** with no plan to grow past one vendor and no test seams needed — a 200-line CRUD demo doesn't need this pattern

---

> **Stack-agnostic note.** Examples above are TypeScript. The pattern travels: Python (Protocols), Go (interfaces), Rust (traits), Kotlin/Java (interfaces). The directory structure and the non-negotiable rule (no vendor SDK in business logic) are the same.
