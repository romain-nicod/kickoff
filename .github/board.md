# {{PROJECT_NAME}} — livraison

Delivery board of **{{PROJECT_NAME}}**. Repository: [{{REPO}}](https://github.com/{{REPO}}).

This text is the board's README, set by `scripts/setup_project.py` from
`.github/board.md`. It opens from the **☰** button at the top of the board, and
it is the first place where somebody who arrives understands how we work here.

## What goes on it

A functional increment is a **user story**: « En tant que <rôle>, je peux
<action> ». A technical piece of work is a **task**, titled in the imperative.
A defect of the product is a **bug**; an error of the agent is a **defect**.

Templates: `[EPIC]`, `[US]`, `[Task]`, `[BUG]`, `[DEFECT]` — see
`.github/ISSUE_TEMPLATE/`.

## The seven statuses

| Status | Set by |
|---|---|
| Backlog | the agent, when a `[US]` or a `[BUG]` is created (label `à revoir par Romain`) |
| Ready | **Romain** |
| In progress | the agent, when the worktree opens |
| En recette | the agent, branch merged into the recette environment, every test green |
| In review | the agent, pull request opened and CI green |
| À déployer | the board's workflow, on merge |
| Done | the agent, once the deployment is verified |

A defect found on the recette environment or in review sends the story back to
**In progress**. A story stopped by something outside itself takes the
`status:blocked` label and shows up in the *Blocked* view: the board has no
status for that.

## The fields

`Status` · `MoSCoW` (Must / Should / Could / Won't have) · `Phase` · `Sprint`
(iterations) · `Estimate` (points) · `Start date` · `Target date`.

The `Phase` options shipped by the template are examples: rename them to the
project's own phases before the first story.

## The views

`Kanban` · `À revoir par Romain` · `Current sprint` · `Prioritized backlog` ·
`Roadmap` · `Epics` · `Defects` · `Blocked` · `All items`.

## Cadence

<!-- One two-week sprint, starting on the first Wednesday after the board is
     created. Replace with the project's real cadence, and say what each
     sprint aims at. -->

| Sprint | Dates | Goal |
|---|---|---|
| Sprint 1 | — | |
| Sprint 2 | — | |

## Definition of done

- Acceptance criteria of the issue ticked
- Pull request linked to the issue, saying what and how
- Tests written, full suite green locally; linter and security scan green
- Review, then merge by **Romain alone**
- Deployed, deployment verified, issue closed
