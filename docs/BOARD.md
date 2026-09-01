# Board

<!-- URL of the GitHub Project, once created by scripts/setup_project.py
     and linked to the repository with:
     gh project link <n> --owner {{OWNER}} --repo {{REPO}} -->

**Board:** _to fill in_ — GitHub Projects v2, linked to the repository.

Items: the user stories generated from the specification, the foundation
tasks, and the epics.

**E0 — Quality and acceptance** is supplied by the template and belongs on
every board: the QA sweep, the accessibility and security audits,
acceptance by real users, behaviour under real conditions, the restore
drill, and the personal-data review. They are stories, with points, in a
batch — not a checklist at the end. See `specification.md`.

Each story is a **sub-issue of its epic**, so an epic shows its own
completion (`Sub-issues progress`). An epic is a container: it is never
worked on directly, and it closes when its stories do.

## Fields

Every field but Status and Route is filled **from the issue's labels** by
`scripts/setup_project.py`. The labels are the source, the board is the
view — see [`LABELS.md`](LABELS.md).

| Field | Values | Filled from | What it is for |
|---|---|---|---|
| **Status** | Backlog · Ready · In progress · In review · Done | — | The board columns |
| **Batch** | B0 … Bn · out of scope | `batch:` | The delivery plan |
| **Points** | 1 · 2 · 3 · 5 · 8 · 13 | `pts:` | Relative complexity, the input of the velocity measurement |
| **MoSCoW Priority** | Must · Should · Can · Won't Have | `prio:` | The phasing from the specification, in the shared language |
| **Route** | free text | — | The route the story is reached by, written before the code |

A story in no batch becomes **Won't Have**: out of the committed scope is
a decision, not an oversight.

Group the board view by **Status**, filter by **Batch** — that is the
view that answers "what are we shipping this week".

## The four views

`setup_project.py` creates them, and re-running only fills in what is
missing. They are Le Wagon's, and each answers a different question:

| View | Layout | Filter | The question it answers |
|---|---|---|---|
| **Kanban** | Board | — | Where does the work stand right now |
| **Prioritized backlog** | Table | `-status:Done` | What is left, and in what order |
| **My items** | Table | `assignee:@me` | What is mine |
| **All items** | Table | — | Everything, to sort and search |

⚠️ **One thing the API still cannot do: the grouping.** Neither
`createProjectV2View` nor `updateProjectV2View` takes a `groupBy`
argument. A board view falls back to grouping by Status — which is what
we want — but nothing guarantees it. **Look at the Kanban once**, and fix
it in the UI if it grouped by something else.

> ⚠️ This section said the opposite until 01/09/2026: *"the API cannot
> create a view"*. `createProjectV2View` has been in the public schema;
> the claim was never checked, and it sent every project off with a
> single unnamed table.

## Column rules

**Todo** — the story meets the Definition of Ready. A rough idea goes to
the specification, not to the board.

**In Progress** — someone's name is on it and a branch exists.
**Limit: one story in progress per person.** Two in progress means
neither is being finished, and unfinished work at the end is lost work.

**Done** — the story meets the Definition of Done in full, and the issue
is closed by its pull request. Merged is not Done.

🔴 **The board does not update itself.** `setup_project.py` moves an item
to Done when its issue is *closed* — so a pull request must close its
issue (`Closes #n` in the body), and **the script must be re-run after a
merge**. Neither is automatic.

⚠️ **What it costs when neither happens**, seen on 01/09/2026: eight
stories delivered, eight issues still open, every item still in Backlog.
The board said nothing had been done for three days of work. A board
nobody trusts is worse than no board — people stop reading it, and then
stop filing in it.

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
