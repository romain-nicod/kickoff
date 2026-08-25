---
name: Bug
about: Something behaves differently from its acceptance criteria
title: "Bug — "
labels: "type:bug"
---

## What happens

<!-- One sentence. -->

## What should happen

<!-- Quote the acceptance criterion or the business rule: "US-102.4, the
     24 px dead zone", "BR-05, times are rounded to 5 min". -->

## Reproduce

1.
2.
3.

**Device and browser:** <!-- the real target first -->
A bug that only appears on the target device is still a bug; a bug that
only appears somewhere the product does not target may not be one.

## Severity

- [ ] **Blocker** — the core journey is broken (proposal, swipe, route).
      Fixed before anything else, whatever the batch in progress.
- [ ] **Major** — a story does not meet its criteria, but the journey
      survives. Fixed within the current batch.
- [ ] **Minor** — cosmetic or an edge case outside the demo path. Fixed
      if time allows; it is never a reason to delay a batch.

The demonstration path is the arbiter: anything the jury will see is at
least Major.
