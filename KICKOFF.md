# Kickoff — how to use this template

This repository is a **project starting kit**: the method, the GitHub
scaffolding and the scripts that turn a specification into a populated
board. It is stack-agnostic at its core, with a thin layer per stack.

It exists so that no project ever rewrites a Definition of Done again.

---

## In sixty seconds

1. **Use this template** on GitHub (green button) → your new repository.
2. Clone it, fill in [`kickoff.yml`](kickoff.yml) — eight values.
3. Run the initialiser:

```bash
bin/kickoff
```

It substitutes the values everywhere, applies your stack layer, deletes
what you do not need — including itself and this file — and prints what
is left for you to do.

4. Commit. You have a repository whose method is already decided.

---

## What you get

| Axis | Files |
|---|---|
| **Engineering** | `CONTRIBUTING.md`, `.github/workflows/ci.yml`, `docs/ENVIRONMENTS.md`, `docs/CODE_HYGIENE.md`, `docs/TESTS.md`, `docs/SECRETS.md`, `.env.example` |
| **Delivery** | `docs/BOARD.md`, `docs/BACKLOG.md`, `docs/MILESTONES.md`, `docs/DEMO.md` |
| **Quality** | `GOLDEN_RULES.md`, `DOR_DOD.md`, `docs/QUALITY.md`, `docs/NAMING.md` |
| **Team** | `ROLES.md`, `TEAM_CHARTER.md`, `CEREMONIES.md`, `docs/STANDUP.md`, `docs/ONBOARDING.md` |
| **Launch** | `docs/GO_LIVE.md` |
| **Product** | `docs/PRD.md` (intent, outcomes, non-goals), `docs/specification.md` (stories), `docs/SCENARIOS.md` (Given/When/Then, mapped to the RSpec examples) |
| **Architecture** | `docs/ARCHITECTURE.md` and `docs/SCHEMA.md` — **living documents**, updated in the same commit as the change they describe |
| **Documentation** | `README.md`, `AGENTS.md`, `CLAUDE.md`, `docs/SYSTEM_DESIGN.md`, `docs/decisions/`, `docs/WIKI.md` |
| **Prompts** | `docs/PROMPTS.md` — how to ask for each deliverable above, and what to check before accepting it |
| **GitHub** | PR template, five issue templates, issue chooser, `labels.yml` |
| **Automation** | `scripts/` — specification → issues, epics, milestones, board |

## The two things that make it worth using

**The backlog is generated, not typed.** Write your stories once, in one
document, and `scripts/` turns them into labelled issues, epics with
their stories attached as sub-issues, milestones and a filled board. If
a criterion changes, it changes in the document and you re-run the
scripts. Nobody maintains a hundred issues by hand.

**Every document states a rule, not a heading.** `DOR_DOD.md` says a
story that does not meet the DoR is not started. `docs/BOARD.md` says
one story in progress per person. They are opinions, deliberately — you
change the ones you disagree with, but you never start from a blank
page.

---

## The stack layers

`stacks/<name>/` holds what is specific: the CI workflow, extra golden
rules, naming conventions, the test strategy. `bin/kickoff` merges the
one you pick into the core files and deletes the rest.

| Layer | For |
|---|---|
| `rails` | Ruby on Rails, PostgreSQL, Hotwire, plain CSS or a framework |
| `static` | Static site or small SPA, no backend |
| _(none)_ | Method only — you wire the technical side yourself |

Adding a layer is a directory and two files. See
[`stacks/README.md`](stacks/README.md).

---

## What this template is not

It is **not an application skeleton**. It does not run `rails new` for
you: your generator does that better than a copy would, and a frozen
skeleton rots in two framework releases. Generate the app, then apply
this template on top — or the reverse, both work.

It is **not a substitute for thinking about your product.** It gives you
the shape of a specification, not its content. The intelligence — a
backlog derived from a real product idea, batches sized against a real
capacity, rules specific to what you are building — is what the
companion Claude Code skill does.

---

## Provenance

Extracted from a real project after a full kick-off: 114 issues, 14
epics, six batches, a green CI and a board on day one. Everything here
was written because something in it was missing at the time.
