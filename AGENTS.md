# {{PROJECT_NAME}} — working instructions

This file is the substance for any agent (Claude Code, Copilot, Cursor…)
and for any human picking the project up. `CLAUDE.md` is only a pointer
to it.

**Last updated** <!-- date -->

---

## 1. The product in five lines

<!-- What it is, for whom, and the one question it answers. Then the two
     or three promises that govern every decision — the ones you use to
     say no. -->

## 2. Where the truth lives

| Question | Document |
|---|---|
| What gets built, in what order | `docs/` — the reference specification |
| Why the product is what it is | |
| Any visual value | |
| What it looks like | `design/` |

<!-- One rule to state here: which document wins when two disagree. A
     project with two references has none. -->

## 3. The absolute rules

<!-- The five to eight rules that are not up for debate in a feature
     branch. They come from the product, not from taste. Write each one
     as a prohibition with its reason — a rule whose reason is missing
     gets negotiated away in week two.

     Examples of the shape they take:
     🔴 No hard-coded visual value: everything reads a token.
     🔴 A hard constraint is never traded against a preference.
     🔴 Data with no source is not displayed.
     🔴 No hypothesis is presented as a measurement. -->

🔴

🔴

🔴

## 4. The stack and what is already wired

| Layer | Choice |
|---|---|
| | |

```
<!-- The tree of what exists, one line each, so nobody re-creates it. -->
```

## 5. Target architecture

<!-- Routes, components, data model, performance budget. Mark clearly
     what is decided and what is still a proposal: a proposal presented
     as a decision is how a team stops arguing about the right things. -->

## 6. The rule that governs the plan

Capacity: {{DEV_DAYS}} days × {{TEAM_SIZE}} people × {{VELOCITY}} points
= **{{CAPACITY}} points**.

<!-- Then the number that matters: what the backlog weighs against that
     capacity. If the essential scope is larger than the capacity, say
     it here in one sentence — the batching then does not rank
     priorities, it cuts inside the essential. -->

See [`docs/MILESTONES.md`](docs/MILESTONES.md).

## 7. Conventions

| Prefix | Meaning |
|---|---|
| `US-nnn` | User story |
| `BR-nn` | Business rule |
| `Bn` | Delivery batch |
| `Pn` | Priority phase |

Every story carries its number in the issue title, the branch name and
the commit message. Code touching a business rule cites its number in a
comment.

Git, review and quality: [`CONTRIBUTING.md`](CONTRIBUTING.md) and
[`GOLDEN_RULES.md`](GOLDEN_RULES.md).

## 8. Known traps

<!-- The ones already paid for. Each entry: what happens, and what to do
     instead. This section is worth more than the rest of the file
     combined — it is the only one that cannot be reconstructed from the
     code. -->

-
-

## 9. Hypotheses never to present as facts

<!-- Every number in the product that was assumed rather than measured.
     Naming them here is what stops one of them reaching a slide as
     market data. -->

## 10. Still open

-
-
