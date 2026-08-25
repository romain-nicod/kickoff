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
     labels — docs/LABELS.md says what each family means. A story
     carries no type: label; that is what the epic and the points say. -->

> **Epic** Enn — … · **Priority** P1/P2/P3 · **Complexity** n pts ·
> **Batch** Bn

### User story

As a <who>, I want <what>, so that <why>.

<!-- One sentence. If it needs two, it is two stories. -->

### Acceptance criteria

- [ ] 1.
- [ ] 2.
- [ ] 3.

<!-- Does it do what was asked? Binary, functional, and testable by
     someone who did not write them. "The screen is fast" is not a
     criterion; "first proposal in under 3 s on 4G" is.
     They are checked before the story is closed. -->

### Success criterion

<!-- Was it worth doing? One measurable outcome, with its threshold and
     when it is read — not a restatement of the acceptance criteria.

     An acceptance criterion is met on the day of the merge; a success
     criterion is read afterwards, on the running product. "The upload
     accepts a 10 MB file" is acceptance. "Fewer than 5% of uploads are
     abandoned, measured over the first two weeks" is success.

     If the outcome cannot be read at story level, name the measure the
     epic carries and say so: "carried by E3 — median time to a booked
     slot under 90 s". Every story states one; none is left blank. -->

-

### Business rules touched

<!-- BR-nn, or "none". A rule implemented in code cites its number in a
     comment. If this story needs a rule that does not exist yet, say so:
     a new BR is a product decision. -->

### Why it was not in the specification

<!-- One line. This is the interesting part: what we learned that we did
     not know at kick-off. It is also what tells the team whether the
     scope is growing or the plan was wrong. -->

### Definition of Ready

<!-- Before the first line of code. -->

- [ ] Acceptance criteria are testable by someone else
- [ ] A success criterion is written, with its threshold and its reading date
- [ ] Dependencies are delivered, or explicitly stubbed
- [ ] Complexity estimated on the shared scale (1 · 2 · 3 · 5 · 8 · 13)
- [ ] Placed in a batch — including "out of scope", which is a decision
- [ ] **Added to `the specification`**, so the specification
      and the issues keep saying the same thing

<!-- Complexity scale:
     1 trivial · 2 simple CRUD · 3 standard · 5 custom JS, external API
     or geospatial query · 8 an algorithm or a pipeline · 13 outside the
     curriculum. -->

### Definition of Done

<!-- Before the issue is closed. Merged is not done. The reference is
     DOR_DOD.md; this copy is here so it gets ticked on the story
     itself. A change to one is a change to both. -->

- [ ] Every acceptance criterion above is checked, one by one
- [ ] The success criterion is instrumented — whatever it is read from
      exists and produces a number
- [ ] CI is green
- [ ] It respects the golden rules — no hard-coded value, business logic
      in the right layer, no string outside the translation layer
- [ ] `routes` lists exactly the paths the story needed, no more, and
      every view uses the named helper rather than a string path
- [ ] It works **on the real target device**, not only in a desktop
      browser at the right width
- [ ] Accessibility holds: touch targets, contrast, no information
      carried by colour alone
- [ ] Its error and empty states exist and lead somewhere
- [ ] No key in the code: everything is read from the environment, and
      any new variable is in `.env.example`
- [ ] The **verification pass** was asked for and done: every acceptance
      criterion walked through in the running app — plus a security
      review if the story touched auth, input, uploads, money or a
      third-party call
- [ ] The README or `AGENTS.md` is updated **in the same commit** if a
      command, a variable or a URL changed
