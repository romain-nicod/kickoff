# Board

<!-- URL of the GitHub Project, once created by scripts/setup_project.py
     and linked to the repository with:
     gh project link <n> --owner {{OWNER}} --repo {{REPO}} -->

**Board:** _to fill in_ — GitHub Projects v2, linked to the repository.

Items: the user stories generated from the specification, the foundation
tasks, and the epics.

Each story is a **sub-issue of its epic**, so an epic shows its own
completion (`Sub-issues progress`). An epic is a container: it is never
worked on directly, and it closes when its stories do.

## Fields

| Field | Values | What it is for |
|---|---|---|
| **Status** | Todo · In Progress · Done | The board columns |
| **Batch** | B0 … Bn · out of scope | The delivery plan |
| **Points** | 1 · 2 · 3 · 5 · 8 · 13 | Relative complexity, the input of the velocity measurement |
| **Priority** | P1 · P2 · P3 | The phasing from the specification |

Group the board view by **Status**, filter by **Batch** — that is the
view that answers "what are we shipping this week".

> The API cannot create a board *view*. After running the script, add it
> in the UI: `+` next to the view tabs → **Board**, group by **Status**.

## Column rules

**Todo** — the story meets the Definition of Ready. A rough idea goes to
the specification, not to the board.

**In Progress** — someone's name is on it and a branch exists.
**Limit: one story in progress per person.** Two in progress means
neither is being finished, and unfinished work at the end is lost work.

**Done** — the story meets the Definition of Done in full, and the issue
is closed by its pull request. Merged is not Done.

## How a story moves

```
Todo ──▶ In Progress ──▶ (pull request) ──▶ Done
  ▲                                          │
  └──────────── does not meet the DoD ───────┘
```

A story that comes back from review goes back to **In Progress**, never
straight to Done "because the fix is small".

## What the board is not

It is not the backlog. The backlog is the specification, and the issues
are generated from it. An item created directly on the board has no
acceptance criteria anyone reviewed, so nobody can say when it is done.

## Reading it in ten seconds

- Points in **Done** ÷ person-days consumed = the measured velocity.
  That number is the only one that changes the plan.
- An item In Progress for more than two days is a blocker that has not
  been said out loud.
- **out of scope** shows what the product becomes. It is not a pool to
  pull from.
