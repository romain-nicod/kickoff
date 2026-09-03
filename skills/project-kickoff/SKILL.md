---
name: project-kickoff
description: Start a project from the kickoff template — create the repository, fill the method documents, write the specification in the parsed format, and generate the issues, epics, milestones and board. Use when the user is starting a new project, says "kick off", "new project", "set up the repo", "bootstrap", or asks to turn a product brief or specification into GitHub issues and a board.
---

# Project kickoff

Turn a product idea into a repository whose method is already decided
and whose board is already populated.

The template `romain-nicod/kickoff` carries everything that does not
change from one project to the next. **This skill carries what does**:
reading a brief, deriving a backlog from it, sizing it against a real
capacity, and naming the rules that are specific to this product.

Never re-type what the template already holds. If a document exists
there, it is filled in, not rewritten.

---

## 1. Establish the ground before writing anything

Ask only what you cannot deduce, and ask it once:

| Value | Why it matters |
|---|---|
| Project name and one-sentence pitch | Every document's first line |
| GitHub owner and repository name | The scripts deduce it from the remote afterwards |
| Stack | Picks the layer: `rails`, `static`, or `none` |
| Development days, team size | Capacity — the number that governs the plan |
| Demo or delivery date | Milestone dates, backwards from it |
| Where the product specification lives | A document, a conversation, or nothing yet |

If the user has no specification, say so plainly and offer to write one
with them before touching GitHub. **A board generated from a vague brief
is a hundred issues nobody trusts.**

## 2. Create the repository from the template

```bash
gh repo create <owner>/<name> --template romain-nicod/kickoff --private --clone
```

Then fill `kickoff.yml` with the eight values and run:

```bash
bin/kickoff
```

It substitutes everywhere, merges the stack layer, and deletes itself.
Read its output: it lists the four gaps left on purpose.

Then generate the application skeleton, in the cloned repository:

```bash
rails new -d postgresql \
  -m https://raw.githubusercontent.com/romain-nicod/rails-ready/main/template.rb \
  --skip .
```

🔴 **`rails-ready` is the default and needs no discussion** — it derives from Le Wagon's
Rails template of that name, the base the team learnt on. `--skip` keeps
the files the clone already holds. Not using it is a legitimate choice
that gets **written into `README.md` under "Structural decisions"**, in
the same commit. See `docs/BOILERPLATE.md`.

Add `dotenv-rails` in the same move (rule 28 needs it):

```ruby
group :development, :test do
  gem "dotenv-rails"
end
```

## 3. Fill the method documents — briefly

The template's documents are complete method, with holes where a project
must speak for itself. Fill only those:

- `README.md` — what the product does, how it works, the stack, the
  structural decisions
- `AGENTS.md` — sections 1, 3, 8 and 9: the product in five lines, the
  absolute rules, the known traps, the hypotheses never to present as
  facts
- `ROLES.md`, `TEAM_CHARTER.md` — names and real working hours, if
  known; otherwise leave the placeholders and say so
- `docs/MILESTONES.md` — dates derived backwards from the demo

**Section 3 of `AGENTS.md` is the one that earns its keep.** Five to
eight prohibitions specific to this product, each with its reason. They
come from the specification and from the design, not from a generic
list. If you cannot write five, the product is not understood yet.

Two of them arrive already written and stay: **every key in `.env`**
(rule 28) and **the skeleton comes from `rails-ready`**. Do not paraphrase
them into something weaker.

🔴 **Fill the vault pointer at the top of `AGENTS.md`** with the real
folder — `~/Documents/Claude/ObsiClaud/<domaine>/<projet>/` — and create
that folder now, with its card (`<Projet>.md`) and its `CLAUDE.md`. A
project whose memory has no home writes it into the repository, and the
repository is not where it belongs.

## 4. Write the specification in the parsed format

`docs/specification.md` is a shape, not a form: the tables in it are
what `scripts/build_backlog.py` reads. Fill it with real content —
epics, stories with testable acceptance criteria, business rules,
complexity per story, batches.

Four things that make it worth reading rather than merely parseable:

**Acceptance criteria are testable by someone who did not write them.**
"The screen is fast" is not one; "first result in under 3 s on 4G" is.

**Every story also carries a success criterion, and the build fails
without one.** It answers a different question: acceptance is met the day
of the merge, success is read afterwards on the running product — one
outcome, its threshold, when it is read. "The upload accepts a 10 MB
file" is acceptance; "fewer than 5% of uploads abandoned over the first
two weeks" is success. When the outcome only exists at epic level, name
the epic measure rather than inventing a story-level one.

**Complexity is relative, and the anchors are in the template.** Score
every story, then sum. That sum against the capacity is the sentence
that governs everything — write it explicitly, especially when the
essential scope alone exceeds the capacity.

**Batches cut, they do not rank.** B0 foundation, B1 the demo that works
on its own, then the rest. Say what B1 delivers in one sentence: if it
is not already the whole pitch, the batching is wrong.

## 5. Generate GitHub

```bash
python3 scripts/build_backlog.py       # spec → scripts/backlog.json
python3 scripts/create_issues.py       # labels, milestones, stories
python3 scripts/create_epic_issues.py  # epics + sub-issue links
python3 scripts/setup_project.py       # board and its fields
gh project link <n> --owner <owner> --repo <owner>/<name>
```

Check the totals `build_backlog.py` prints against the specification's
own totals. **If they differ, the specification is malformed** — fix the
document, never the script's output.

Two things the API cannot do, to hand to the user step by step:

1. `gh auth refresh -s project --hostname github.com` — the token has no
   project scope by default, and `setup_project.py` fails without it.
2. Creating the **Board view**: `+` next to the view tabs → Board, group
   by Status.

## 6. Keys, before anything is pushed

🔴 **Every key lives in `.env`, and `.env` is never pushed** — golden rule
28, and the one thing on this list that cannot be fixed afterwards. Check
three things before the first push:

1. `git check-ignore -v .env` answers. If it does not, stop.
2. No literal key anywhere: `git grep -nE '(sk_|pk_|ghp_|AKIA|BEGIN .*PRIVATE KEY)'`
   comes back empty.
3. Every variable the app reads is in `.env.example`, with an empty
   value and a line saying what it is for.

Never ask the user to paste a secret into the conversation. Host secrets
are set by them, in the host's dashboard, step by step.

## 7. Record what was decided

Write the structural decisions as ADRs in `docs/decisions/` while the
reasons are fresh — especially the one about what you deliberately did
not build. In six weeks nobody remembers why, and the choice gets
reversed by accident.

If the user keeps a knowledge base outside the repository, write the
project's memory there too: decisions, traps met, state of play.

## 8. Register the repository in the repository map

🔴 **Before the first push**, add the new repository to
`~/Documents/Claude/ObsiClaud/dev/Dépôts AI-GMENTED.md` — the map of every
repository on the account. Three edits, in the same commit as the creation:

1. **A row in the overview table** (§1), in the right family: name,
   visibility, whether a local clone exists, one line on what it is.
2. **A paragraph in §2**: what it holds, its state, its live URL if it has
   one, its GitHub account if it is not `romain-nicod`.
3. **An overlap entry in §3** — *only if it applies, and it usually does*.
   Does this repository carry material that already lives elsewhere: content,
   a method document, a skill, shared site code? Then say so, and **name
   which copy is authoritative**. An unwritten overlap is an overlap that
   will silently diverge.

Then bump the note's footer version and date.

**Judge visibility on what is actually served, not on the repository
setting.** A private repository with GitHub Pages enabled publishes its
content to everyone. Check before writing "private" in the table.

The map covers the repository's whole life, not just its birth: flipping
visibility, renaming, transferring or deleting it is written there in the
same move — including what the change breaks (forks, stars, watchers,
Pages). A map that lags behind GitHub is worse than no map.

---

## Who is authoritative

Each subject has one home — the table is in `KICKOFF.md`, section "Who is
authoritative".

⚠️ **Amorce used to be a second route to the same documents.** It was taken out
of the method circuit on 27/08/2026: still online, no longer served, and
authoritative for nothing. The historical comparison is kept in
`ObsiClaud/dev/Kickoff et Amorce - recouvrement et arbitrage.md`, marked closed.

The three that get confused most often:

| Subject | Authoritative |
|---|---|
| The three Claude skills | **`kickoff`** (`skills/`) — `~/.claude/skills/` is an install, never an edit |
| The executable `template.rb` | **`rails-ready`** |
| `docs/PROMPTS.md` | **`kickoff`** — was generated by Amorce until 27/08/2026, maintained here since |
| How to switch each optional gem on | **`rails-ready`** (`docs/CONFIGURATION.md`) |

⚠️ **Historical note — never apply Amorce to a kickoff repository.** They wrote
the same subjects under different file names: `docs/MILESTONES.md` against
`docs/JALONS.md`, and two Definitions of Done that disagreed about
estimation.

---

## What good looks like at the end

- A repository whose README a stranger can follow to a running app
- `AGENTS.md` with five real prohibitions, not five generic ones
- Issues generated, each a sub-issue of its epic, each labelled by
  batch, priority and complexity
- A board with Status, Batch, Points and Priority filled for every item
- A green CI on the first push
- Four gaps explicitly left for the kick-off meeting, not silently
  invented
- A row, a paragraph and — where it applies — an overlap entry in the
  repository map, written before the first push
- A vault folder for the project, with its card and its `CLAUDE.md`, and
  `AGENTS.md` pointing at it
- `.env` gitignored, `.env.example` filled with names only, and no
  literal key anywhere in the history

## Traps

**Do not invent the capacity.** Ask for the real days and the real
people. A capacity model built on a guess produces a plan nobody
believes.

**Do not translate acceptance criteria.** They are quoted verbatim into
the issues. If the specification is in another language than the
repository, say so once and keep them as they are.

**Do not create issues by hand to "get started".** An issue with no
counterpart in the specification is an issue with no reviewed criteria.

**Do not fill the wiki.** See `docs/WIKI.md` in the template: anything
describing how the code works lives in the repository.

**Check which GitHub account is active** before creating anything:
`gh api user --jq .login`. Creating the repository under the wrong owner
costs a delete and a re-clone.
