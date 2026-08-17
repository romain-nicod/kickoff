# Code hygiene

Rules of the daily grind, enforced by CI where a machine can do it and
by review where it cannot.

## What the linter enforces

<!-- The linter, its configuration file, and the two commands. Use the
     ecosystem's default configuration: a short project does not debate
     its style guide. -->

```bash
```

**Adding an exclusion is a team decision**, not a way to make your own
PR green.

## What review enforces

**No hard-coded value that belongs in a token or a constant.** The most
common reason to block a PR, in every project.

**Business logic in the right layer.** A computation in a view, a
threshold in a stylesheet, a rule in the template: the same mistake,
three costumes.

**No dead code, no commented-out code.** Git remembers. A commented
block in a short project is a block nobody dares delete at the end.

**No `TODO` without an issue number.** `# TODO: handle the empty case`
is noise; `# TODO(US-1006): handle the exhausted supply` is a pointer.

**A function does one thing, and its name says which.** If the name
needs `and`, it is two functions.

## Comments

Comment **why**, never what. The code says what.

```
# Bad
# round to 5
# Good
# BR-05: never display a to-the-minute value — the underlying data does
# not exist, so that precision would be a lie.
```

Cite the rule by number. Anyone reading it later can find the full text
in the specification.

## Dependencies

**Adding a dependency is announced** in the team channel before the PR,
with one sentence saying what it replaces. Most of what feels like it
needs a library is twenty lines you already understand.

Never a source whose terms of use forbid the usage, including through a
third-party wrapper.

## Files that are not edited casually

| File | Why |
|---|---|
| Design tokens | A value added without review is a design system dead in three weeks |
| The specification | Changing it is a product decision; the issue scripts must be re-run |
| Reference data | The demonstration rests on it |
| The linter configuration | See above |
