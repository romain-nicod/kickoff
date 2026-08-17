# Naming

One rule above the others: **identifiers in English, product vocabulary
in the language of the domain.** The interface may speak French; the
code does not.

## Everywhere

**A quantity carries its unit in its name.** `wait_minutes`, not `wait`.
`price_cents`, not `price`. The day someone stores another unit in it,
the bug is silent and the product lies.

**A boolean reads as a question.** `published?`, `takeaway?`. Never
`flag`, never `status` for something with two values.

**No abbreviation nobody else uses.** `venue`, not `vn`. The three
characters you save cost the next reader a lookup.

**No `data`, `info`, `manager`, `utils`, `helper`.** They name nothing.
If a class is a `Manager`, you have not decided what it does.

## Files

`snake_case` or `kebab-case` consistently — pick one per language and
never mix inside a directory. Documents at the root that GitHub renders
specially keep their conventional shouty names: `README.md`,
`CONTRIBUTING.md`, `AGENTS.md`.

## Git

| Thing | Convention | Example |
|---|---|---|
| Branch | story number, then the slugged feature | `us-102-reject-by-swipe` |
| Commit | `Subject: detail` | `US-102: reject by swipe` |
| PR title | the same as the issue | `US-102 — Reject by swipe` |

## Identifiers from the specification

`En` epics · `US-nnn` stories · `BR-nn` business rules · `Bn` batches ·
`Pn` priority phases.

**Cite them in code where they apply.** A comment saying `# BR-05` above
a rounding is worth more than three lines explaining why the value is
rounded.

<!-- The stack layer appends its own conventions below: models, tables,
     CSS classes, controllers. -->
