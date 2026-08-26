# {{PROJECT_NAME}} — working instructions

> ⚙️ Règles de travail communes à tout ce dossier : `~/Documents/Claude/CLAUDE.md`.

> 🔴 **La mémoire de ce projet vit dans le vault**, pas ici :
> `~/Documents/Claude/ObsiClaud/<domaine>/{{REPO_NAME}}/`
> — remplacer `<domaine>` par `perso`, `le-wagon`, `ai-gmented` ou `dev`,
> et créer le dossier avec sa carte (`{{PROJECT_NAME}}.md`) et son
> `CLAUDE.md` **le jour où le dépôt naît**, pas plus tard.
> Ce fichier-ci ne porte que les règles de travail sur ce dépôt.

This file is the substance for any agent (Claude Code, Copilot, Cursor…)
and for any human picking the project up. `CLAUDE.md` is only a pointer
to it.

**Last updated** <!-- date -->

---

## 1. The product in five lines

<!-- What it is, for whom, and the one question it answers. Then the two
     or three promises that govern every decision — the ones you use to
     say no. -->

## 2. Where the truth lives

| Question | Document |
|---|---|
| What gets built, in what order | `docs/` — the reference specification |
| Why the product is what it is | |
| Any visual value | |
| What it looks like | `design/` |
| How a key reaches the app | `.env` only — golden rule 28, `docs/SECRETS.md` |
| Which generator the skeleton came from | `docs/BOILERPLATE.md` |
| The long memory: decisions, traps already paid | the vault folder above |

<!-- One rule to state here: which document wins when two disagree. A
     project with two references has none. -->

## 3. The absolute rules

<!-- The five to eight rules that are not up for debate in a feature
     branch. They come from the product, not from taste. Write each one
     as a prohibition with its reason — a rule whose reason is missing
     gets negotiated away in week two.

     Examples of the shape they take:
     🔴 No hard-coded visual value: everything reads a token.
     🔴 A hard constraint is never traded against a preference.
     🔴 Data with no source is not displayed.
     🔴 No hypothesis is presented as a measurement.

     Three are already decided for every project and are not up for
     debate here — keep them: -->

🔴 **Every key lives in `.env`, and `.env` is never pushed.** One
mechanism, no exception, no "just for this test". Read through
`ENV.fetch(...)`, declare the name in `.env.example` in the same commit.
A key in the history is compromised even in a private repository — see
golden rule 28.

🔴 **The application skeleton comes from `minimal`, Le Wagon's Rails
template.** Not a bare `rails new`, not a hand-assembled stack: it is the
base everyone here learnt on, and day one is not spent relearning where
the CSS lives. Departing from it is allowed and gets written down in
`README.md` — see `docs/BOILERPLATE.md`.

🔴 **Nothing that costs money without the account owner's explicit
approval, asked for and given BEFORE the command runs.** Name the owner
here. The hosting account is billed to a person, and that person is
usually the only one who can see what a command charges to it.

**What is gated**, on Heroku and on every equivalent: `heroku run` (a
one-off dyno, billed by the second, every time), `addons:create` (a
recurring monthly line, immediately), `ps:scale` and `ps:type`,
`pg:upgrade` and any plan change, and anything that adds a **worker
dyno** or a **second database**.
**What is not**: pushing a deploy, reading logs, releases and config.

⚠️ **It applies to the agent as much as to the human.** An agent asked
to "set that up", helpfully running `addons:create`, spends money
belonging to somebody who was not consulted. Stop and ask, even when it
interrupts the task — **especially** then.

🔴 A cost approved once is approved for **that command, that time**.

⚠️ **And a written rule binds only the agents that read this file.** If
somebody outside the repository can spend on the account, the rule that
actually holds is the collaborator list, not this paragraph. Say which
one you chose, and why.

🔴

🔴

🔴

## 4. The stack and what is already wired

| Layer | Choice |
|---|---|
| | |

```
<!-- The tree of what exists, one line each, so nobody re-creates it. -->
```

## 5. Target architecture

<!-- Routes, components, data model, performance budget. Mark clearly
     what is decided and what is still a proposal: a proposal presented
     as a decision is how a team stops arguing about the right things. -->

## 6. The rule that governs the plan

Capacity: {{DEV_DAYS}} days × {{TEAM_SIZE}} people × {{VELOCITY}} points
= **{{CAPACITY}} points**.

<!-- Then the number that matters: what the backlog weighs against that
     capacity. If the essential scope is larger than the capacity, say
     it here in one sentence — the batching then does not rank
     priorities, it cuts inside the essential. -->

See [`docs/MILESTONES.md`](docs/MILESTONES.md).

## 7. Conventions

| Prefix | Meaning |
|---|---|
| `US-nnn` | User story |
| `BR-nn` | Business rule |
| `Bn` | Delivery batch |
| `Pn` | Priority phase |

Every story carries its number in the issue title, the branch name and
the commit message. Code touching a business rule cites its number in a
comment.

Git, review and quality: [`CONTRIBUTING.md`](CONTRIBUTING.md) and
[`GOLDEN_RULES.md`](GOLDEN_RULES.md).

## 8. Known traps

<!-- The ones already paid for. Each entry: what happens, and what to do
     instead. This section is worth more than the rest of the file
     combined — it is the only one that cannot be reconstructed from the
     code. -->

-
-

## 9. Hypotheses never to present as facts

<!-- Every number in the product that was assumed rather than measured.
     Naming them here is what stops one of them reaching a slide as
     market data. -->

## 10. Still open

-
-
