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
| **E0** | Quality and acceptance | The product is proven, not assumed | 7 | 5 | 2 | 0 |
| **E1** | | | | | | |
| | **Total** | | | | | |

---

## E0 — Quality and acceptance

> **Capability**: what the product owner can say to someone else — that it
> works, that it is usable by the people it is for, and that it survives
> a bad day. Not "the tests are green".

🔴 **This epic is supplied by the template and belongs in every project.**
It is not a phase at the end: it is the set of checks that only make sense
on the whole product, and that a per-story Definition of Done structurally
cannot carry.

⚠️ **Why it is written down rather than left to good practice.** Born on
01/09/2026: eight stories shipped on a project whose `DOR_DOD.md` already
demanded a verification pass, an accessibility check, a walk on the real
device and a security review — **and not one of those boxes was ever
ticked**, because nothing scheduled them. A rule that lives only in a
document nobody opens is not a rule. The one defect that was caught was
caught by eye, in a screenshot, by the person paying for the work.

**Where these stories go in the plan**: the last batch of the project.
The template cannot know its number, so assign them when the batching is
decided. A story of this epic left out of every batch is the failure mode
this epic exists to prevent — the board will show it as `Won't Have`.

| ID | Feature | User story | Acceptance criteria | Success criterion | Pri |
|---|---|---|---|---|---|
| **US-001** | Front-end QA sweep | As the product owner, I want every screen swept for defects, so that nobody discovers them for me. | 1. Every screen, in every role, signed in and signed out.<br>2. Layout at 375, 768 and 1280 px, in both themes.<br>3. Empty, loading and error states opened.<br>4. Every link and form target reached.<br>5. No string outside the translation layer. | Defects found by the sweep outnumber those reported by users in the first month. | P1 |
| **US-002** | Accessibility audit | As a reader with a disability, I want the whole product audited, so that I am not the one who finds it unusable. | 1. Every journey completable by keyboard alone, focus always visible.<br>2. Contrast measured, not estimated, in both themes.<br>3. Images carry real alternatives.<br>4. No information carried by colour alone.<br>5. Touch targets at least 44 px. | Zero WCAG 2.1 AA failure open at launch, measured values written in the design system. | P2 |
| **US-003** | Security audit | As the product owner, I want the deployed product reviewed as a whole, so that the promise it makes is one I can defend. | 1. The product's core promise verified against the deployed host, not a development server.<br>2. Session, cookie and CSRF settings reviewed.<br>3. Headers checked: HSTS, CSP, frame options, referrer policy.<br>4. Dependencies scanned.<br>5. No secret in the repository or the image. | Every finding fixed or accepted in writing with a reason, before launch. | P1 |
| **US-004** | Acceptance by real users | As a user who did not build this, I want to complete my journey unaided, so that the product is usable by someone other than its author. | 1. Each real user completes their main journey alone, unaided.<br>2. Every hesitation is written down during the session.<br>3. Nothing is changed during the session. | Every intended user completed their journey without help, and each hesitation is filed. | P1 |
| **US-005** | Behaviour under real conditions | As a user on the connection I actually have, I want the product to work, so that it is not a product that only works on the developer's machine. | 1. The main journey walked on the slowest connection the product targets.<br>2. Page weight measured, not estimated.<br>3. What the user sees while waiting, and if it never arrives. | Measured figures written down, and every journey below the stated threshold fixed or accepted. | P1 |
| **US-006** | Backup and restore drill | As the product owner, I want a restore actually performed, so that I know the state of my backups rather than assuming it. | 1. Data and files restored end to end, on other hardware.<br>2. The duration measured and written down.<br>3. The runbook corrected wherever reality differed. | A restore was performed, its duration recorded, before the product carries anything irreplaceable. | P1 |
| **US-007** | Personal-data review | As someone whose data this holds, I want to know what is kept and for how long, so that I did not agree to something nobody wrote down. | 1. Every piece of personal data listed, with its retention.<br>2. Each retention has a deletion path, or the data is dropped.<br>3. A short plain-language page states it. | A page states what is kept and for how long, and no retention exists without a deletion path. | P2 |

---

## E1 — Epic title

> **Capability**: what the user can do that they could not before.

| ID | Feature | User story | Acceptance criteria | Success criterion | Pri |
|---|---|---|---|---|---|
| **US-101** | Short name | As a <who>, I want <what>, so that <why>. | 1. First criterion.<br>2. Second criterion.<br>3. Third. | Measured outcome, its threshold, when it is read. | P1 |
| **US-102** | | | | | P1 |

<!-- One section per epic, numbered E1, E2… Story numbers follow the
     epic: US-1nn for E1, US-12nn for E12.

     Acceptance criteria are separated by <br> and numbered. They are
     quoted verbatim into the issue, so write them as you want to read
     them there: testable by someone who did not write them.

     The success criterion is a different question, and the column is
     mandatory — build_backlog.py refuses a story without one.
     Acceptance answers "does it do what was asked", and is met the day
     of the merge. Success answers "was it worth doing", and is read
     afterwards on the running product: one outcome, its threshold, and
     when it is read. "The upload accepts a 10 MB file" is acceptance;
     "fewer than 5% of uploads abandoned over the first two weeks" is
     success. When the outcome is only readable at epic level, name the
     epic measure: "carried by E3 — median time to a booked slot under
     90 s". -->

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

**E0 Quality and acceptance** — 22 points

| ID | Story | Complexity | Nature | Pri |
|---|---|---|---|---|
| US-001 | Front-end QA sweep | **3** | QA | P1 |
| US-002 | Accessibility audit | **3** | QA | P2 |
| US-003 | Security audit | **5** | SEC | P1 |
| US-004 | Acceptance by real users | **3** | UAT | P1 |
| US-005 | Behaviour under real conditions | **3** | QA | P1 |
| US-006 | Backup and restore drill | **3** | OPS | P1 |
| US-007 | Personal-data review | **2** | SEC | P2 |

**E1 Epic title** — nn points

| ID | Story | Complexity | Nature | Pri |
|---|---|---|---|---|
| US-101 | Short name | **5** | RAILS | P1 |

<!-- One block per epic. The **n** in bold is what the scripts read.
     Every column must be filled: build_backlog.py's row pattern requires
     a non-empty Nature, and skips the row silently otherwise — the
     story then fails later with "No complexity found". -->

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
