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
| **Boilerplate** | `docs/BOILERPLATE.md` (stack layer) — `rails-ready`, our Rails template, and what it decides for you |
| **Skills** | `skills/` — three Claude skills; two are installed into the project's `.claude/skills/` |
| **GitHub** | PR template, five issue templates, issue chooser, `labels.yml` + `docs/LABELS.md` — six label families, the naming convention, and GitHub's stock labels deleted |
| **Automation** | `scripts/` — specification → issues, epics, milestones, board ; and `setup_repo.py`, which configures the repository itself |

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

It is **not a frozen application skeleton**, and it never will be: a
skeleton copied into a repository rots in two framework releases.

But it does have an opinion about which generator you run. On the
`rails` layer the default is **`rails-ready`** — our Rails template,
derived from Le Wagon's `minimal.rb` and fixing four defects it has —
with the exact command and every choice it makes documented in
`docs/BOILERPLATE.md`. You run it after `bin/kickoff`, in the cloned
repository, with `--skip` so that what is already there wins. Not using
it is fine; not saying why, in `README.md`, is not.

It is **not a substitute for thinking about your product.** It gives you
the shape of a specification, not its content. The intelligence — a
backlog derived from a real product idea, batches sized against a real
capacity, rules specific to what you are building — is what the
companion Claude Code skill does.

---

## Who is authoritative

Two places carry the same method, on purpose — the skills drive Claude, this
template starts a repository. They must agree, so each subject has **one**
home. Change it there; the other follows.

⚠️ There was a third, Amorce's generators, until 27/08/2026. It is out of the
circuit: still online, no longer served.

| Subject | Authoritative | Why |
|---|---|---|
| Method documents (DoR/DoD, roles, charter, ceremonies, Git conventions, review) | **`kickoff`** | Written to be read, not derived |
| Golden rules, per-stack layers | **`kickoff`** | Only lives here |
| Specification → issues, epics, milestones, board | **`kickoff`** | Only lives here |
| The three Claude skills | **`kickoff`** (`skills/`) | Moved here on 24/08/2026; `~/.claude/skills/` is an install, never an edit |
| The boilerplate default (`rails-ready`) and its reasons | **`kickoff`** (`docs/BOILERPLATE.md`) | Which generator we start from is a method decision |
| The executable `template.rb` | **`rails-ready`** | The generator itself. A copy here would rot |
| How to switch each optional gem on | **`rails-ready`** (`docs/CONFIGURATION.md`) | It ships them commented; it owns the steps |
| `docs/PROMPTS.md` | **`kickoff`** | Was generated by Amorce until 27/08/2026; now maintained here |
| Repository configuration (labels, wiki, PR settings, branch protection, board) | **`kickoff`** | `gh` from a terminal |

⚠️ **Amorce no longer appears in this table.** It was taken out of the method
circuit on 27/08/2026 — it is still online and is not deleted, it simply
receives no new rules. Anything it used to own is listed above under its new
owner. See `~/.claude/CLAUDE.md`, "Les deux relais".

🔴 **Never apply both to the same repository.** They write the same
subjects to different file names — you end up with `docs/MILESTONES.md`
*and* `docs/JALONS.md`, and two Definitions of Done that disagree about
estimation.

The full comparison, and the ten contradictions found on 24/08/2026:
`ObsiClaud/dev/Kickoff et Amorce - recouvrement et arbitrage.md`.

## This template's own memory

The long memory of **this repository** lives in the vault, not here:

```
~/Documents/Claude/ObsiClaud/dev/kickoff/
```

`AGENTS.md` in this repository is a **template for the project you are
creating** — its vault pointer is a placeholder you fill in with your own
project's folder. It is not this repository's own agent file.

---

## Provenance

Extracted from a real project after a full kick-off: 114 issues, 14
epics, six batches, a green CI and a board on day one. Everything here
was written because something in it was missing at the time.
