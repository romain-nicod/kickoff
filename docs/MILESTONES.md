# Milestones and prioritisation

## The number that governs everything

Capacity: {{DEV_DAYS}} development days × {{TEAM_SIZE}} people ×
{{VELOCITY}} points per person-day = **{{CAPACITY}} points**.

<!-- Then the number that matters: what the backlog weighs against that
     capacity, and what the *essential* part alone weighs. If the
     essential is larger than the capacity, write it here in one
     sentence. The batching then does not rank priorities — it cuts
     inside the essential, which is a different exercise and a harder
     conversation. -->

## The batches

| Batch | Content | Points | Status |
|---|---|---|---|
| **B0** | Technical foundation, no user story | | Non-negotiable |
| **B1** | The demo that works | | Non-negotiable |
| **B2** | | | |
| **B3** | | | Decision zone |
| **B4** | | | Decision zone |
| **B5** | If time allows | | Assumed bonus |

Each batch is a GitHub milestone, created by `scripts/create_issues.py`.

**Write down what B1 delivers in one sentence.** If that sentence is not
already the whole pitch, the batching is wrong: B1 exists to be
demonstrable on its own.

## Dates

Derived from the demo date, backwards.

| Milestone | Target date |
|---|---|
| B0 complete | |
| B1 complete | |
| Velocity measurement | end of week one |
| Feature freeze | demo day − 1 |
| Demo rehearsal | demo day − 1 |
| **Demo** | |

**Feature freeze one day before the demo** is not a nicety. The last day
is for the data, the rehearsal and the bugs found during it.

## Prioritisation method

Priorities come from the specification and are **not renegotiated story
by story**. What is negotiated is the batch: at the velocity
measurement, a whole batch enters or leaves the scope.

**Who decides:** the product owner, on the measured velocity — not on
optimism. A tie is broken by the question *"does the demonstration
survive without it?"*.

**Cutting order:** _write it here, before you need it._ Deciding what to
sacrifice while you are behind schedule is how teams sacrifice the wrong
thing.

## What is deliberately not built

<!-- The heaviest thing you decided to skip, and what replaces it. Every
     project has one: a pipeline replaced by a fixture, a real-time
     feature replaced by a refresh, an integration replaced by a mock.
     Name it, say what it costs and what it frees — and record it as an
     ADR in docs/decisions/.

     Two conditions keep such a choice honest: the README says it is the
     planned next step, and the replacement is good enough that the
     demonstration does not depend on luck. -->
