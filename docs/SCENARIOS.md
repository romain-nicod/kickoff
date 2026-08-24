# {{PROJECT_NAME}} — Behaviour scenarios

<!-- 🔴 A LIVING DOCUMENT. Every user story adds or updates its scenarios here,
     IN THE SAME COMMIT as the specs that verify them.

     Written in plain English so that someone who does not read Ruby can check
     whether the product does what it was asked to do. This is the document you
     hand to a stakeholder, a jury, or your future self. -->

**Last updated:** <!-- YYYY-MM-DD --> · **Suite green as of:** <!-- date + commit -->

---

## How to read this

Each scenario is written **Given / When / Then** and maps to the RSpec example
that verifies it.

🔴 **The mapping is by `it` description, never by line number.** A line number is
wrong the moment someone inserts a line above it, and nobody notices — the `it`
description survives edits and is greppable:

```bash
bundle exec rspec spec/system/recipes_spec.rb -e "shows every published recipe"
```

**The rule that keeps this honest:** the `Then` clause below and the `it`
description in the spec say **the same thing, in the same words**. When they
drift, the document becomes decoration. If you reword one, reword the other in
the same commit.

**Traceability:** `FR-n` ([`PRD.md`](PRD.md)) → user story → `S-n` here → RSpec
example. Any `FR-n` with no scenario is unverified; any scenario with no spec is
a promise.

---

## S-1 — <!-- Short scenario title -->

**Covers:** <!-- FR-1, FR-2 --> · **Story:** <!-- #12 -->

> **Given** <!-- the starting state, in plain English -->
> **When** <!-- the action the user takes -->
> **Then** <!-- the observable outcome — no implementation detail -->

**Verified by:** `spec/system/<file>_spec.rb` → `"<it description>"`

<!-- Edge cases belong here too, as their own scenario. The happy path alone
     is not coverage: the empty state, the refusal and the error are where
     products actually break. -->

## S-2 — <!-- Edge case: what happens when it goes wrong -->

**Covers:** <!-- FR-n --> · **Story:** <!-- #n -->

> **Given**
> **When**
> **Then**

**Verified by:** `spec/models/<file>_spec.rb` → `"<it description>"`

---

## Coverage

<!-- Filled in at each milestone. A gap named is a decision; a gap unnamed is a
     surprise during the demo. -->

| FR | Scenarios | Verified | Gap |
|---|---|---|---|
| FR-1 | S-1 | ✅ | |
| FR-2 | — | ❌ | <!-- why not, and when --> |

## Change log

| Date | Scenario | Change | Story |
|---|---|---|---|
| | | | |
