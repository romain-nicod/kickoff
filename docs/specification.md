# {{PROJECT_NAME}} — user stories, business rules and delivery batches

**Version** v01 · <!-- date -->
**Scope** the whole product

This document is the **reference**. The GitHub issues are generated from
it by `scripts/`, so its shape matters: the tables below are parsed.
Keep them, fill them, and the board builds itself.

Everything outside the tables is yours — write as much prose as the
product deserves.

---

## Epic overview

| Epic | Title | User capability | Stories | P1 | P2 | P3 |
|---|---|---|---|---|---|---|
| **E1** | | | | | | |
| | **Total** | | | | | |

---

## E1 — Epic title

> **Capability**: what the user can do that they could not before.

| ID | Feature | User story | Acceptance criteria | Pri |
|---|---|---|---|---|
| **US-101** | Short name | As a <who>, I want <what>, so that <why>. | 1. First criterion.<br>2. Second criterion.<br>3. Third. | P1 |
| **US-102** | | | | P1 |

<!-- One section per epic, numbered E1, E2… Story numbers follow the
     epic: US-1nn for E1, US-12nn for E12.

     Criteria are separated by <br> and numbered. They are quoted
     verbatim into the issue, so write them as you want to read them
     there: testable by someone who did not write them. -->

---

## Business rules

Not user stories: the rules that govern the product. They are
implemented identically everywhere and cited by number in the code.

| ID | Rule |
|---|---|
| **BR-01** | |
| **BR-02** | |

<!-- Group them by domain if there are many. A rule that is an assumed
     hypothesis rather than a measured fact says so, in its own text —
     that sentence is what stops it reaching a slide as market data. -->

---

## Worked example

<!-- One end-to-end example with real numbers, showing the rules
     applied. It is the fastest way for a newcomer to understand the
     product, and the first test to write. -->

---

## Complexity scoring and batching

### The scale

Relative complexity, calibrated on this stack and this team. It is
neither a duration nor an effort: it is a ratio of difficulty between
stories.

| Points | Anchor |
|---|---|
| **1** | Trivial. A static page, one field, one string. |
| **2** | Simple. Standard CRUD, one view, one association. |
| **3** | Standard. Several models, a filtered query, a configured library. |
| **5** | Notable. Custom front-end code, an external API, or a non-obvious query. |
| **8** | Heavy. An algorithm, a pipeline, or coordinating several new pieces. |
| **13** | Outside what the team has done before. |

### The detail

**E1 Epic title** — nn points

| ID | Story | Complexity | Nature | Pri |
|---|---|---|---|---|
| US-101 | Short name | **5** | | P1 |

<!-- One block per epic. The **n** in bold is what the scripts read. -->

### Capacity

```
capacity = dev days × people × velocity
         = {{DEV_DAYS}} × {{TEAM_SIZE}} × {{VELOCITY}}
         = {{CAPACITY}} points
```

<!-- Then the sentence that governs the plan: what the backlog weighs
     against that capacity. If the essential scope alone is larger, say
     it — the batching then cuts inside the essential, and everyone
     needs to know that is what is happening. -->

### The batches

| Batch | Content | Stories | Points | Cumulative |
|---|---|---|---|---|
| **B0** | Technical foundation (no user stories) | — | | |
| **B1** | The demo that works | | | |

**B1 — The demo that works** — nn points

| ID | Story | Pts |
|---|---|---|
| US-101 | Short name | 5 |

<!-- One block per batch, in this exact shape: the heading line and the
     three-column table are what assigns a story to its batch. A story
     in no block is out of the committed scope, which is a decision, not
     an oversight. -->

### How to read the batches

<!-- What each batch buys, and which ones are non-negotiable. State the
     cutting order before you need it. -->

---

## Open questions

<!-- What is not settled, numbered, with what it blocks. A question
     recorded here is a question that gets answered; one that lives in
     someone's head gets rediscovered at the worst time. -->

1.
2.
