# System design

<!-- The five-minute sketch, for a short project: what talks to what, and which
     external dependency will be the one that fails during the demo.

     For a project that lives beyond the first week, `docs/wiki/Architecture.md`
     is the document of record — C4 context and containers, structural
     decisions, critical flows, security, environments, accepted debt — kept
     up to date in the pull request that changes the structure, and published
     to the wiki. This file is the sketch; that one is the map. Do not
     maintain both: past the first week, fill Architecture.md and let this
     one go. -->

## The shape of the thing

```
<!-- An ASCII diagram of the pieces and what talks to what. Not a
     beautiful diagram: an honest one, that shows every external
     dependency on the critical path. Those are the ones that fail
     during the demo. -->
```

External dependencies on the critical path: <!-- list them. Each one is
a thing that can be down while you are presenting. -->

## Data model

```
<!-- The entities and their relations, in five lines. -->
```

| Model | Carries | Key rules |
|---|---|---|
| | | |

## The request that matters

<!-- Every product has one path that must be fast, and it is usually the
     first screen. Write its budget, and the design decisions that
     budget forces. -->

| Metric | Budget |
|---|---|
| | |

## What is deliberately not built

<!-- The heaviest thing you skipped, what replaces it, and what makes
     the choice reversible later. Record it as an ADR page in
     docs/wiki/ as well — this section is the summary, the ADR is the
     reasoning. -->

## Routes

| Screen | Route | Action |
|---|---|---|
| | | |
