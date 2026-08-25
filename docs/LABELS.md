# Labels

A label is a **filter**, not a decoration. It exists only if someone
types it into a search bar, or a script reads it.

Everything else — what the story does, why it matters, what blocks it —
belongs in the issue body, on the board, or in the specification. A
repository that labels everything is a repository where labels mean
nothing, and it is the state GitHub hands you on day one: nine stock
labels nobody chose, applied by nobody, filtered on by nobody.

---

## The convention

**`family:value`. Always. No bare labels.**

One rule, no exception — not even for `bug`, which GitHub itself ships
unprefixed. A bare label is the beginning of a second convention, and two
conventions in one list is no convention.

| Part | Form | Why |
|---|---|---|
| `family` | lowercase, singular, one word | it is what you type first; `epic:` narrows the list before you have finished typing |
| `:` | no space, either side | GitHub treats the whole string as the name; a space makes it quotable-only |
| `value` | **verbatim from the specification** when the specification names it | otherwise lowercase kebab-case |

**The value is quoted, not translated.** `E1`, `P1`, `B1`, `5` are the
identifiers `docs/specification.md` uses. `epic:E1` is greppable against
the document; `epic:discovery` is not, and drifts the day the epic is
retitled. The same reason acceptance criteria are quoted verbatim into
the issue.

This is why `prio:P1` is not a stutter. The family is `prio`; the value
is `P1`, which is a name in the specification, not an abbreviation of the
family.

**Six families, and a seventh is a decision.** Adding a family is adding
a way to slice the backlog. If nobody can say which search it serves,
it serves none.

---

## The six families

### Generated — the specification's own vocabulary

Created by `scripts/create_issues.py` from `scripts/backlog.json`, which
`scripts/build_backlog.py` reads out of the specification. **They are not
declared anywhere by hand**, and only the values the specification
actually uses are created: a three-batch plan gets three batch labels,
not six.

| Family | Values | What it answers | Read by |
|---|---|---|---|
| `epic:` | `E1`, `E2`… one per epic | which capability does this belong to | `create_epic_issues.py` |
| `prio:` | `P1` · `P2` · `P3` | is it committed scope | the board's **MoSCoW Priority** field |
| `pts:` | `1` `2` `3` `5` `8` `13` | relative complexity | the board's **Points** field |
| `batch:` | `B0`…`Bn`, `out-of-scope` | when is it delivered | the board's **Batch** field |

🔴 **These four are data, not decoration.** `scripts/setup_project.py`
reads them off the issue to fill the board. Removing one by hand empties
a column.

The scale is closed: `1 · 2 · 3 · 5 · 8 · 13`. `build_backlog.py` refuses
anything else. A `4` is not a finer estimate, it is a story nobody argued
about.

`batch:out-of-scope` is the only generated value that is not a
specification identifier, and it is deliberate: a story in no batch is
**out of the committed scope, which is a decision**, not an oversight.
The board turns it into `Won't Have`.

### Declared — what a human applies

Declared in [`.github/labels.yml`](../.github/labels.yml), applied by the
issue templates, identical on every project.

| Label | When |
|---|---|
| `type:bug` | it behaves differently from its acceptance criteria |
| `type:chore` | technical work carrying no user story — setup, tooling, data |
| `type:spike` | a time-boxed investigation that answers one question |
| `status:blocked` | stopped by something outside the story |

**A user story carries no `type:`.** It is already recognisable — it has
an epic, a priority, points and a batch. Labelling it `type:story` would
put a label on 95 issues out of 100, which is the definition of a filter
that filters nothing.

**`type:spike` is not `type:chore`.** A chore is work to be done; a spike
is a question to be answered, with a time box and an output. Filing one
as the other is how an investigation quietly becomes an implementation.

**`status:blocked` is the only status the board cannot say.** Its Status
field runs Backlog · Ready · In progress · In review · Done — none of
them means *stopped, and not by us*. Without the label, a blocked story
sits in `In progress` looking exactly like work. Applying it without
saying **what** blocks it, in a comment, makes it useless.

---

## Colour

The palette is the template's, and it carries one distinction only:

| Colour | | Meaning |
|---|---|---|
| `FF8A3D` | ember | act on this now — `prio:P1`, `status:blocked` |
| `A8410A` | deep ember | committed, second wave — `prio:P2` |
| `C9C0B4` | ink, light | structural, neutral — `batch:` |
| `6E665B` | ink | reference, neutral — `epic:`, `pts:`, `prio:P3`, `batch:out-of-scope` |
| `17130E` | ink, black | `type:` |

Warm means *act*. Two families are warm, and the prefix tells them apart.
Colour never encodes a second meaning on top of the family — a label that
is orange **and** in the `pts:` family would be saying something the
family does not.

---

## What was removed, and why

The set used to be larger. Three things went:

**GitHub's nine stock labels.** `enhancement`, `question`, `wontfix`,
`good first issue`, `duplicate`, `invalid`, `documentation`, `help
wanted`, `bug`. Nothing here creates them, nothing here filters on them,
and on a fresh repository they outnumbered the ones the project chose.
`scripts/setup_repo.py` now deletes them — **except any an issue still
carries**, since deleting a label strips it from every issue with no
warning and no undo. Those are reported and left alone.

**The pre-declared `batch:` and `pts:` labels.** `labels.yml` declared
`B0`…`B5` and seven point values on every project, while
`create_issues.py` created the real ones from the specification, with the
real batch titles. Every project therefore carried empty labels for
batches it did not have, and two descriptions competed for the same name.
The specification is the source; a label is its shadow.

**`pts:4`.** Off a scale that every other document in this template
states as `1 · 2 · 3 · 5 · 8 · 13`.

---

## Adding one

Before adding a label, the same three questions each time:

1. **What search does it serve?** Name it — `is:open label:…`. If you
   cannot, it is not a label.
2. **Does something already say it?** The board has Status, Batch,
   Points, MoSCoW and Route. The issue body has the acceptance criteria,
   the success criterion and the business rules. A label that repeats one
   of them is a second answer to a settled question.
3. **Does it fit a family?** If not, you are adding a family — see the
   convention above, and say in this document what it slices.

Then: add it to `.github/labels.yml` **and to this document, in the same
commit**, and re-run `python3 scripts/setup_repo.py`.

⚠️ A label generated from the specification is never added by hand. It is
added to the specification, and `build_backlog.py` + `create_issues.py`
do the rest — otherwise the board and the document stop agreeing.
