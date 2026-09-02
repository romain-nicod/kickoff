# CLAUDE.md

The substance for this project lives in **[`AGENTS.md`](AGENTS.md)**:
product, absolute rules, stack, architecture, batching, conventions,
known traps. Read it before touching anything.

How we write code: **[`GOLDEN_RULES.md`](GOLDEN_RULES.md)**. A blocked
pull request names the rule by its number.

Reminders that are expensive to forget:

<!-- Copy the ones from AGENTS.md, section 3, that actually get broken.
     The three below are decided for every project — keep them. -->

- 🔴 **Every key lives in `.env`, and `.env` is never pushed** (rule 28).
  `ENV.fetch(...)` in the code, the variable name in `.env.example`, in
  the same commit. No exception for a test or a demo.
- 🔴 **The skeleton comes from `rails-ready`**, our Rails template derived
  from Le Wagon's `minimal.rb` — see `docs/BOILERPLATE.md`. Departing from it is written down in
  `README.md`.
- 🔴 **A green test proves nothing until you have seen it red.** Put the
  broken code back, watch the test fail, then restore the fix. On the
  project this template was hardened against, nine serious defects were
  found and **not one of them by a test**, while the suite stayed green
  from end to end: the tests agreed with each other, and none of them
  agreed with the browser. A regression test was even watched passing
  against the broken code, because the test environment had quietly
  disabled the very thing it claimed to check.

<!-- 🔴 The two bullets below are PLACEHOLDERS. Replace them with the
     traps this project has actually paid for — the ones a newcomer
     breaks in week one. If they are still here at the first pull
     request, nobody has written down what this project costs to get
     wrong, and that is the finding. Delete them rather than leave them
     empty: an empty marker is read as "nothing to say". -->

- 🔴 TO FILL IN — a trap this project has already paid for.
- 🔴 TO FILL IN — the second one.

The reference specification is `docs/`. A story cited in code is cited
by its number (`US-nnn`), a business rule by its own (`BR-nn`).

Two skills are installed in `.claude/skills/` and load on their own:
`methode-projet` (which deliverable now, who validates it) and
`methode-wagon` (how the code is written here). They come from the
`kickoff` template, which is authoritative for them — edit them there,
not here.

🔴 **The long memory of this project lives in the vault**, not in this
repository: the folder named at the top of `AGENTS.md`. Decisions and
their reasons, traps already paid for, state of play. A decision that
changes, changes there.
