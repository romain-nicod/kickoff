# Contributing

{{DEV_DAYS}} development days, {{TEAM_SIZE}} people, one shared `main`.
These conventions exist so that nobody spends an afternoon resolving a
conflict.

## Git conventions

**One branch per issue**, named after the story it delivers:

```
us-102-reject-by-swipe
us-201-time-rule
```

Never work directly on `main`. Never reuse a branch after its pull
request is merged.

**Commit messages in English**, `Subject: detail` format, one intent per
commit:

```
US-102: reject by swipe, with the 24 px dead zone
Security: rate-limit the login endpoint
```

Hardening passes (security, accessibility, QA) are **separate commits**
from feature commits: a reviewer must be able to read a feature without
wading through a formatting sweep.

**Rebase, do not merge `main` into your branch.** A short project
produces a readable history or an unreadable one; the difference is this
single rule.

```bash
git fetch origin
git rebase origin/main
```

## Pull requests

- One PR per issue, closing it with `Closes #12` in the description.
- The PR template is filled in, not deleted.
- **A PR is reviewed within 4 hours during working hours.** Past that,
  ping in the team channel — a PR waiting overnight is a day lost at
  this scale.
- One approval is enough. Two people cannot block each other.

### What blocks a merge

| Blocks | Does not block |
|---|---|
| CI red | A naming preference |
| An acceptance criterion not met | A refactor the reviewer would have done differently |
| A secret committed | A missing test on a trivial view |
| A golden rule broken, named by its number | A golden rule you would have written differently |
| Business logic in the view instead of the model | Formatting the linter already accepts |
| No verification pass on a story that changed behaviour | The reviewer would have verified differently |

Everything in the right-hand column is a comment, not a request for
changes. **A blocked PR must state which rule it breaks**, by number.

## Before opening a PR

<!-- The two commands CI will run. Filled in with the stack. -->

```bash
```

Then the **verification pass**: the app running, every acceptance
criterion of the issue walked through in it. And a **security review** if
the story touched auth, input, uploads, money or a third-party call — at
minimum once a week whatever happened. Both are described in
[`docs/QUALITY.md`](docs/QUALITY.md).

🔴 **Both are asked for explicitly.** Whoever did the work names which
one is due; a story handed over without either is a story nobody
checked.

## Definition of Ready and Definition of Done

See [`DOR_DOD.md`](DOR_DOD.md). A story that does not meet the DoR is not
started; a story that does not meet the DoD is not moved to Done, even
if the code is merged.

## Where the rules live

- How we write code: [`GOLDEN_RULES.md`](GOLDEN_RULES.md) — a blocked PR
  names the rule by number
- Product rules, constraints, traps: [`AGENTS.md`](AGENTS.md)
- Naming: [`docs/NAMING.md`](docs/NAMING.md)
- Board columns and their meaning: [`docs/BOARD.md`](docs/BOARD.md)
- Roles and ceremonies: [`ROLES.md`](ROLES.md),
  [`CEREMONIES.md`](CEREMONIES.md)
