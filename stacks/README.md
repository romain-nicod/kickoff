# Stack layers

The core of this template assumes nothing about how you build. A layer
adds what is specific: the CI workflow, the extra golden rules, the
naming conventions, the test strategy.

`bin/kickoff` merges the layer named in `kickoff.yml`, then deletes this
directory.

## How a layer works

Two mechanisms, and no third:

**Copy.** Any file in `stacks/<name>/` is copied to the same path at the
root. `stacks/rails/.github/workflows/ci.yml` becomes
`.github/workflows/ci.yml`.

**Append.** A file named `X.append.md` is appended to `X.md` instead of
replacing it. `stacks/rails/GOLDEN_RULES.append.md` adds the Rails rules
after rule 30 of the core file.

That is the whole contract. A layer is a directory and two files.

## Existing layers

| Layer | What it adds |
|---|---|
| `rails` | Rules 31 to 59 (Rails idioms and boilerplate helpers, CSS components and tokens, Hotwire), a CI workflow with PostgreSQL, RuboCop and Brakeman |
| `static` | Rules 31 to 40 (structure, assets, no framework), a CI workflow that lints and checks links |
| `none` | Nothing. The method only. |

## Writing a new one

1. `mkdir stacks/<name>`
2. Add `GOLDEN_RULES.append.md` — start numbering at 31, and only write
   rules that are genuinely specific. A rule that holds anywhere belongs
   in the core file.
3. Add `.github/workflows/ci.yml` — the shortest pipeline that catches
   what a human would miss: lint, security, tests.
4. Optionally append to `docs/CODE_HYGIENE.md`, `docs/NAMING.md`,
   `docs/TESTS.md`.
5. Add a line to the table above.

The test of a good layer: someone starting a project on that stack
changes nothing in the core files.
