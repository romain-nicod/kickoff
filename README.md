# Kickoff — how to use this template

> **This template applies the delivery method by user story**, from the
> first commit of a project:
> `/Users/albert/Documents/Claude/ObsiClaud/dev/methode/Méthode - Livraison applicative par user story.md`.
> That note is authoritative. The template carries what applies it — the
> issue and pull-request templates, the board and its labels, the CI, the
> recette, the wiki and the release tooling — and no copy of the method.

This repository is a **project starting kit** for Romain's web sites and
applications, all built with Rails: the GitHub scaffolding and the
scripts that configure a repository and its board. Its core is
stack-agnostic, with a thin layer per stack.

---

## In sixty seconds

1. **Use this template** on GitHub (green button) → your new repository.
2. Clone it, fill in [`kickoff.yml`](kickoff.yml) — five values.
3. Run the initialiser:

```bash
bin/kickoff
```

It substitutes the values everywhere, applies your stack layer, deletes
what you do not need (including itself and this file), puts
`README.template.md` in place as your project's README, and prints what
is left for you to do.

4. Commit. You have a repository whose method is already decided.

---

## What you get

| Axis | Files |
|---|---|
| **Agents** | `AGENTS.md` — 25 lines at most: vault folder, method, repository, board, wiki, commands, ports, deployment, three prohibitions — and `CLAUDE.md`, three lines pointing at it |
| **Issues** | `.github/ISSUE_TEMPLATE/` — `[US]` (state, story, criteria `CA-01…`, impacts, out of scope, tasks, Definition of Done), `[Task]`, `[BUG]` |
| **Pull requests** | `.github/PULL_REQUEST_TEMPLATE.md` for a story; `.github/PULL_REQUEST_TEMPLATE/deploiement.md` for `[Déploiement] vX.Y.Z` |
| **Board and labels** | `scripts/setup_project.py` — the seven statuses; `.github/labels.yml`, `scripts/setup_repo.py`; `docs/BOARD.md`, `docs/LABELS.md` |
| **Versions** | `VERSION`, `CHANGELOG.md` — each section is the release note —, `scripts/publish_release.py`, `docs/DEPLOIEMENT.md` |
| **Recette** | `docs/RECETTE.md`, `docs/ENVIRONMENTS.md`; on the rails layer `bin/recette` and `lib/recette.rb` |
| **Wiki** | `docs/wiki/` — the pages, reviewed in pull requests — and `.github/workflows/wiki.yml`, which publishes them; `docs/WIKI.md` |
| **Engineering** | `CONTRIBUTING.md`, `.github/workflows/ci.yml` (stack layer), `docs/CODE_HYGIENE.md`, `docs/TESTS.md`, `docs/SECRETS.md`, `.env.example`; `docs/PARALLEL_WORK.md` — several stories at once without two writers overwriting each other |
| **Quality** | `GOLDEN_RULES.md`, `docs/QUALITY.md`, `docs/NAMING.md`; `scripts/check_placeholders.py` — what the template left blank and nobody filled, which no linter, test or scan can see |
| **Product and design** | `docs/PRD.md`, `docs/SCHEMA.md`, `docs/SYSTEM_DESIGN.md`, `docs/DESIGN_CHECKLIST.md`, `docs/PROMPTS.md` |
| **Boilerplate** | `docs/BOILERPLATE.md`, `docs/GEMS.md` (stack layer) — `rails-ready`, our Rails template, and what it decides for you |
| **Skill** | `skills/project-kickoff/` — applies the method with this template; installed by symbolic link, see [`skills/README.md`](skills/README.md) |

## The two things that make it worth using

**A project starts on the method, not next to it.** The first issue is
an `[US]` on its template, the board already has the seven statuses, the
CI already runs the browser tests, and the first deployment already has
its pull request and its release note.

**Every document states a rule, not a heading.** They are opinions,
deliberately — you change the ones a project disagrees with, in its
`AGENTS.md`, but you never start from a blank page.

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
the shape of a user story, not its content. Stories derived from a real
need, and the rules specific to what you are building, are what the
`project-kickoff` skill helps write.

---

## Who is authoritative

Two places carry the same method, on purpose — the skills drive Claude, this
template starts a repository. They must agree, so each subject has **one**
home. Change it there; the other follows.

| Subject | Authoritative | Why |
|---|---|---|
| The delivery method: statuses, story cycle, tests, recette, review, deployment, documentation | **The vault note** named at the top of this file | One method for every project; no copy in a repository |
| Its application: issue and PR templates, board, labels, CI, recette tooling, release script | **`kickoff`** | Only lives here |
| Golden rules, per-stack layers | **`kickoff`** | Only lives here |
| The `project-kickoff` skill | **`kickoff`** (`skills/`) | `~/.claude/skills/project-kickoff` is a symbolic link to it, never a copy |
| The boilerplate default (`rails-ready`) and its reasons | **`kickoff`** (`docs/BOILERPLATE.md`) | Which generator we start from is a method decision |
| The executable `template.rb` | **`rails-ready`** | The generator itself. A copy here would rot |
| How to switch each optional gem on | **`rails-ready`** (`docs/CONFIGURATION.md`) | It ships them commented; it owns the steps |
| `docs/PROMPTS.md` | **`kickoff`** | One prompt per design deliverable, with what to check in the answer |
| Repository configuration (labels, wiki, PR settings, branch protection, board) | **`kickoff`** | `gh` from a terminal |

🔴 **Never apply two project templates to the same repository.** They write
the same subjects under different file names, and you end up with two
Definitions of Done that disagree about estimation. Pick one and delete the
other before the first commit.

## A word on `AGENTS.md`

The `AGENTS.md` in this repository is a **template for the project you are
creating**, not this repository's own agent file. It stays under 25 lines:
the vault folder comes from `kickoff.yml`, the board URL, production and
deployment script are filled in by hand, and everything else is a link to
the method.

---

## Provenance

Extracted from a real project after a full kick-off: 114 issues, 14
epics, six batches, a green CI and a board on day one. Everything here
was written because something in it was missing at the time.

---

## Licence

[CC BY 4.0](LICENSE). Reuse it, adapt it, sell what you build with it. Keep
the credit visible, as [`NOTICE`](NOTICE) explains. The projects you generate
with it are yours, and choose their own licence.
