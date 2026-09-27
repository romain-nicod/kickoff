---
name: Bug
about: A defect observed (recette, production, QA review, flaky test) — same cycle as a story
title: "[BUG] "
labels: "type:bug, à revoir par Romain"
---

<!-- Title: [BUG] <the faulty behaviour>. Romain reads the stories and the bugs;
     like a story, a bug goes through Backlog, then Ready once he has reviewed it. -->

<!-- 🔴 The review header comes FIRST: it is what Romain reads before anything else
     (method § 3 bis.3). One emoji: ⚠️ while a document waits for Romain or a
     wireframe or spec is to be reviewed, 🟢 once the issue can move on without
     him. Every line is filled in or says "none". The "To validate" line only
     exists under ⚠️ and gives the document's PATH. The native relations
     (sub-issue, blocked by) are authoritative; these lines mirror them. -->

⚠️ **To validate by Romain**

- Parent: #<epic> · Blocked by: none · Blocks: none · Milestone: vX.Y.0
- Impacted pages: none <!-- route and screen name: `/map` (Trip map) -->
- Wireframes to review: none <!-- one link per screen: Trip map → <link> -->
- Specs to review: none <!-- path of each spec -->

**To validate:** `<path of the document>` — <the decision expected, in one line>

## State

- Board: **Backlog** — Romain moves the bug to *Ready* after review, and the agent then removes the `à revoir par Romain` label.
- Branch: (created when the session opens) · PR: —

## What happens

<!-- What happens, in one sentence, then how to reproduce it. -->

1.
2.
3.

- Where: production · recette · CI (flaky test) · QA review
- Version (`VERSION`) and commit:
- Screen width and browser:
- Account used (fictional; never a real password here):

## Expected behaviour

<!-- Quote the original criterion when there is one: "#12 CA-03". -->

## Acceptance criteria

- [ ] **CA-01** — the expected behaviour is back, verifiable by somebody else
- [ ] **CA-02** — a regression test proves it, seen red against the faulty code

## Impacts

<!-- Every line is filled in, or explicitly says "none". -->

| Impact | To do |
|---|---|
| Severity: blocking (main journey broken, data at stake) · major (a criterion not met) · minor | |
| Production data to correct | none |
| Documents: wiki (`docs/wiki/`), `README`, `.env.example` | none |
| Data migration | none |

## Definition of Done

- [ ] Acceptance criteria verified one by one
- [ ] Regression test written and seen red before the fix, then green
- [ ] Full suite and CI green on the last commit
- [ ] Security checks passed (Brakeman, bundler-audit, `importmap audit`)
- [ ] UI/UX pass done, screenshots attached to the pull request at 1512×982, 1280×800 and 390×844 (if there is an interface)
- [ ] Idiomatic QA of the diff done, code commented
- [ ] Trap added to `docs/wiki/Traps.md` if it can hit other stories, lessons written to the vault
- [ ] Tested on the recette environment
- [ ] Pull request reviewed and **merged by Romain**
- [ ] Deployed to production and verified, listed under "Corrections" in `CHANGELOG.md`
