# Labels

A label is a **filter**: it only exists if somebody searches for it, or if a script reads it. What
says where a story stands lives on the board, not in a label.

Declared in [`.github/labels.yml`](../.github/labels.yml), created by
`python3 scripts/setup_repo.py`, which also deletes the nine labels GitHub ships (except those an
issue still carries).

| Label | Set by | When |
|---|---|---|
| `type:user-story` | `[US]` template | every user story; Romain reads the stories and the bugs |
| `Task` | `[Task]` template | a concrete action of a story, filed as its sub-issue; kept by the agent |
| `type:bug` | `[BUG]` template | a defect observed on the recette environment, in production, in a QA review, or a flaky test; same cycle as a story |
| `à revoir par Romain` | `[US]` and `[BUG]` templates | created by the agent; **removed by the agent** once Romain has moved the issue to *Ready* |
| `status:blocked` | by hand | stopped by something outside the story — say what, in a comment |

The `à revoir par Romain` name is an identifier: the issue templates apply it literally, and GitHub
silently drops a label the repository does not declare.

In an organisation that exposes the native issue types, the `User story` or `Task` type can replace
the matching label; on a personal account, the labels are authoritative.

**Adding a label**: write it in `.github/labels.yml` and in the table above, in the same commit, then
run `python3 scripts/setup_repo.py` again. Before that, ask which search it serves; if nobody can say,
it is not a label.
