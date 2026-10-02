---
name: User story
about: A user journey, or the answer to a need, reviewed by Romain before Ready
title: "[US] "
labels: "type:user-story, à revoir par Romain"
---

<!-- Template of the "delivery by user story" method (§ 3 and § 4.7).
     Title: [US] <need or journey>. Romain only reads the stories; the story is a
     sub-issue of its [Epic], and the [Task] issues are sub-issues of this one. -->

<!-- 🔴 The review header comes FIRST: it is what Romain reads before anything else
     (method § 3 bis.3). One checkbox per impacted screen, per wireframe to validate
     and per spec; Romain ticks what he has validated, and the issue turns 🟢 when
     every box is ticked. Each list is filled in or says "none". A screen impacted
     means a wireframe the agent creates and links — in Claude Design, live in the
     session: one board per screen on the project's design canvas, the board's link
     here, the canvas sources exported to projects/<domain>/<project>/wireframes/
     (method § 3 bis.3, rule of 28/09/2026). A spec needed means one the agent
     writes. Native relations (sub-issue, blocked by) are authoritative; the last
     line mirrors them. -->

⚠️ **To validate by Romain**

**Impacted screens**
- [ ] none <!-- one per screen: Trip map — `/stages` -->

**Wireframes to validate**
- [ ] none <!-- one per impacted screen: Trip map → <link to its Claude Design board> -->

**Specs to validate**
- [ ] none <!-- one per spec: `<path>` -->

Parent: #<epic> · Blocked by: none · Blocks: none · Milestone: vX.Y.0

## State

- Board: **Backlog** — Romain moves the story to *Ready* after review, and the agent then removes the `à revoir par Romain` label.
- Branch: `us-NNN-slug` (created when the session opens) · PR: —

## User story

As <who>, I want <what>, so that <why>.

## Acceptance criteria

<!-- Verifiable by somebody else. The identifier appears in the name of the test
     that verifies it (`test "CA-01 ..."`): no separate test plan. -->

- [ ] **CA-01** —
- [ ] **CA-02** —
- [ ] **CA-03** —

## Impacts

<!-- Every line is filled in, or explicitly says "none". -->

| Impact | To do |
|---|---|
| Wireframe (approved at review, before *Ready*) | none |
| Documents: data schema, wiki (`docs/wiki/`), `README`, `.env.example`, deployment | none |
| Data migration | none |

## Out of scope

-

## Tasks

<!-- [Task] sub-issues, created and kept by the agent. -->

- [ ] #

## Definition of Done

- [ ] Acceptance criteria verified one by one
- [ ] Unit, integration, system (if there is an interface) and regression tests written, seen red then green
- [ ] Full suite and CI green on the last commit
- [ ] Security checks passed (Brakeman, bundler-audit, `importmap audit`, permission tests, CSRF, injection, XSS)
- [ ] UI/UX pass done, screenshots attached to the pull request at 1512×982, 1280×800 and 390×844 (if there is an interface)
- [ ] Idiomatic QA of the diff done, code commented
- [ ] Story documented in the project wiki (the journey delivered; an architecture diagram if the structure changed; an ADR if a decision was taken), `README` and `.env.example` up to date, lessons written to the vault
- [ ] Tested on the recette environment
- [ ] Pull request reviewed and **merged by Romain**
- [ ] Deployed to production and verified
