# Backlog

**The backlog is not this file.** It is the specification in `docs/`:
epics, user stories with their acceptance criteria, business rules, a
complexity score per story and a delivery plan in batches.

The GitHub issues are **generated from it**, never typed by hand:

```bash
python3 scripts/build_backlog.py       # spec → scripts/backlog.json
python3 scripts/create_issues.py       # labels, milestones, stories
python3 scripts/create_epic_issues.py  # epics + sub-issue links
python3 scripts/setup_project.py       # board and its fields
```

All four are idempotent. If an acceptance criterion must change, it
changes in the specification first, then the scripts are re-run — that
is what keeps a hundred issues and one document saying the same thing.

## The shape of it

| Epic | Title | Stories | Points |
|---|---|---|---|
| | | | |
| | **Total** | | |

<!-- Two readings worth writing down: which epic is heaviest for what it
     produces, and which one weighs a lot for zero committed stories.
     Both usually change the plan. -->

## What is committed

<!-- Which batches, how many points, against what capacity. -->

See [`MILESTONES.md`](MILESTONES.md).

## Adding something along the way

The backlog grows — a project that discovers nothing is a project nobody
used. Four ways in:

**A new user story.** Found in review, in a rehearsal, in a user's
mouth. Open it from the user story template, give it the next free
number in its epic, attach it as a sub-issue, label it, and **add it to
the specification in the same breath**.

**A bug** — from the bug template, severity stated. It does not enter
the backlog; it interrupts it if it is a Blocker.

**A chore** — technical work with no user story. Costed in points on the
same scale: the capacity model does not care whether work is visible.

**A spike** — a time-boxed question. It produces a written answer, not
code.

The one rule behind all four: **the specification and the issues never
diverge.** A story that exists only as an issue has no criteria anyone
reviewed; a story that exists only in the specification is not being
built. When they disagree, the specification wins and the scripts are
re-run.

**Every addition is counted.** A story added late is capacity taken from
something else — say which, on the board, at the checkpoint.

## Writing the specification

The scripts read tables. The format is deliberately plain Markdown so
the document stays readable on its own:

```markdown
## E1 — Epic title

> **Capability**: what the user can do that they could not before.

| ID | Feature | User story | Acceptance criteria | Success criterion | Pri |
|---|---|---|---|---|---|
| **US-101** | Short name | As a …, I want …, so that … | 1. …<br>2. … | Outcome, threshold, when it is read. | P1 |
```

Plus one table of complexity per story and one per batch. See
`scripts/build_backlog.py` — it states exactly which shapes it reads,
and it fails loudly rather than guessing. It also refuses a story with an
empty success criterion: acceptance says whether it does what was asked,
success says whether it was worth doing, and a story states both.
