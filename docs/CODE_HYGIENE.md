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

**Aim for lines under 80 columns.** An objective, not a dogma — but the
default, and the exceptions are named rather than accumulated.

Three reasons, and the third is the one that matters:

- Two files fit side by side on one screen, and a diff reads in two
  columns without wrapping.
- A projected screen — a livecode, a demo, a review on someone else's
  laptop — cuts around there. A line that wraps on the projector is a
  line nobody in the room follows.
- **A line that will not fit is usually a line doing too much.** Three
  chained calls, a nested ternary, a condition with four clauses: the
  width is the symptom, the structure is the problem. Extract the
  variable, name the intermediate result, split the condition — the code
  gets shorter *and* readable, which is not the usual trade.

```ruby
# no
render json: venues.select { |v| v.open_at?(Time.current) && v.distance < radius }.map { |v| serialize(v) }

# yes
open_nearby = venues.select { |venue| venue.open_at?(Time.current) && venue.distance < radius }
render json: open_nearby.map { |venue| serialize(venue) }
```

Legitimate exceptions: a long URL, a string you must not break, a
generated file. You do not reformat working code to satisfy the limit —
that is a refactor nobody asked for. It applies to what you write now.

**A function does one thing, and its name says which.** If the name
needs `and`, it is two functions.

## Not repeating yourself — and knowing when to stop

**One thing per file, one thing per function.** If you need "and" to
describe it, it is two things.

**DRY is about decisions, not characters.** Before factoring out two
pieces that look alike, ask one question:

> If this rule changes, will I *always* have to change both, in the same
> way?

Yes: it is the same decision written twice — factor it out. No: they
resemble each other by accident. Leave them apart. Merging them couples
two things that are going to diverge, and that is how a codebase ends up
with a boolean parameter threaded through everything.

**Rule of three.** Two occurrences are tolerated; you factor out at the
third. With two, the shape of the abstraction is a guess — and a wrong
abstraction costs more than a copy, because everyone works around it
instead of deleting it. The cost is asymmetric: removing a copy takes
five minutes, undoing an abstraction that ten files depend on takes a
day.

**No `utils` or `helpers` catch-all file.** A file whose responsibility
is "miscellaneous" is the exact opposite of a single responsibility.
Name the file after what it does.

### Moving a value into a configuration file

Do it when all three answers are yes:

1. Does the value change **without the code changing**? (a prompt, a
   threshold, a list of labels, an API URL)
2. Do you want to change it **without reading the surrounding code**?
3. Is there **more than one**, or will there be?

A single value read in a single place stays in the code, named as a
constant. A configuration file with one entry is one more file to open
and nothing else.

Three guard rails whenever you do extract:

- **One place reads the file** and hands the values to the rest of the
  code. Scattered reads are the same value with several truths.
- **Every entry has a default**, and a **clear failure** when it is
  missing or malformed — otherwise you traded a visible bug for a silent
  one.
- The code that uses a value says where it comes from.

🔴 **The stopping test, in both cases: can you still explain one
behaviour by opening two files?** If it takes four, the extraction cost
more than it returned, whatever theory justified it.

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
