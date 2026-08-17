# The wiki: what goes in it, and what must not

**Recommendation: the wiki stays nearly empty.**

A GitHub wiki is a second repository with no pull request, no review, no
CI and no link to the commit that made its content wrong. Everything
that describes *how the code works* therefore lives **in the
repository**, next to the code, and changes in the same pull request as
the code. A wiki diverges within a week.

## What lives in the repository, never in the wiki

| Content | Where |
|---|---|
| What the product is, how to run it | `README.md` |
| Absolute rules, traps, architecture | `AGENTS.md` |
| How we write code | `GOLDEN_RULES.md` |
| Branches, review, what blocks a merge | `CONTRIBUTING.md` |
| Ready / Done | `DOR_DOD.md` |
| Roles, charter, ceremonies | `ROLES.md`, `TEAM_CHARTER.md`, `CEREMONIES.md` |
| Board, backlog, milestones, demo | `docs/` |
| Structural decisions | `docs/decisions/` |
| The specification | `docs/` |

If you are about to write one of those in the wiki, you are about to
create a second source of truth.

## What the wiki is genuinely good for

Things with **no versioned lifecycle** — dated, never wrong, nobody
needs to review them:

1. **Meeting notes** — checkpoints, the velocity measurement with its
   actual numbers, the retrospective.
2. **The project journal** — one section per day, three lines: what
   moved, what broke, what we decided. This is what makes the final
   presentation writable in an hour instead of an evening.
3. **Demo notes** — questions asked and the answers given.
4. **External resources** — links to design files, datasets, studies,
   with the date they were consulted.
5. **Onboarding transcripts** — the questions a newcomer actually asked.
   If the same one comes twice, its answer moves to `ONBOARDING.md`.

## Suggested pages

```
Home          one screen: what this wiki is, links to the repo docs
Journal       one section per day, newest first
Meetings      checkpoints, measurements, retrospective
Demo-notes    rehearsal findings, questions asked
Resources     external links, with consultation dates
```

Five pages. A wiki with twenty pages is a wiki nobody reads.

## How to populate it

The wiki is a git repository of its own:

```bash
git clone git@github.com:{{REPO}}.wiki.git
cd {{REPO_NAME}}.wiki
git add -A && git commit -m "Journal: week 1, day 3" && git push
```

It must be initialised once from the GitHub UI (Wiki tab → create the
first page) before that clone works.

## The rule that keeps it honest

**Nothing in the wiki is a prerequisite for writing code.** If a
newcomer needs a wiki page to run the project, that page is in the wrong
place — move it to `docs/` and leave a link behind.
