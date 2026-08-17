---
name: User story
about: A new user capability, discovered along the way
title: "US-nnn — "
labels: ''
---

<!-- Two legitimate ways a story exists, and both keep the specification
     and the issues in sync:

     1. It is already in the specification → it was created
        by scripts/create_issues.py. Do not re-open it here.
     2. It is new — found in review, in a demo rehearsal, in a user's
        mouth. Open it here, then add it to the specification. The
        specification stays the reference; this template is how a story
        reaches it, not a way around it.

     Numbering: take the next free number in its epic (if E1 runs to US-110,
     the next one is US-111). Attach it as a sub-issue of its
     epic, and give it the epic:Enn, prio:Pn, pts:n and batch:Bn
     labels. -->

> **Epic** Enn — … · **Priority** P1/P2/P3 · **Complexity** n pts ·
> **Batch** Bn

### User story

As a <who>, I want <what>, so that <why>.

<!-- One sentence. If it needs two, it is two stories. -->

### Acceptance criteria

- [ ] 1.
- [ ] 2.
- [ ] 3.

<!-- Testable by someone who did not write them. "The screen is fast" is
     not a criterion; "first proposal in under 3 s on 4G" is. -->

### Business rules touched

<!-- BR-nn, or "none". A rule implemented in code cites its number in a
     comment. If this story needs a rule that does not exist yet, say so:
     a new BR is a product decision. -->

### Why it was not in the specification

<!-- One line. This is the interesting part: what we learned that we did
     not know at kick-off. It is also what tells the team whether the
     scope is growing or the plan was wrong. -->

### Definition of Ready

- [ ] Acceptance criteria are testable by someone else
- [ ] Dependencies are delivered, or explicitly stubbed
- [ ] Complexity estimated on the shared scale (1 · 2 · 3 · 5 · 8 · 13)
- [ ] Placed in a batch — including "out of scope", which is a decision
- [ ] **Added to `the specification`**, so the specification
      and the issues keep saying the same thing

<!-- Complexity scale:
     1 trivial · 2 simple CRUD · 3 standard · 5 custom JS, external API
     or geospatial query · 8 an algorithm or a pipeline · 13 outside the
     curriculum. -->
