# CLAUDE.md

The substance for this project lives in **[`AGENTS.md`](AGENTS.md)**:
product, absolute rules, stack, architecture, batching, conventions,
known traps. Read it before touching anything.

How we write code: **[`GOLDEN_RULES.md`](GOLDEN_RULES.md)**. A blocked
pull request names the rule by its number.

Reminders that are expensive to forget:

<!-- Copy the ones from AGENTS.md, section 3, that actually get broken.
     The two below are decided for every project — keep them. -->

- 🔴 **Every key lives in `.env`, and `.env` is never pushed** (rule 28).
  `ENV.fetch(...)` in the code, the variable name in `.env.example`, in
  the same commit. No exception for a test or a demo.
- 🔴 **The skeleton comes from `rails-ready`**, our Rails template derived
  from Le Wagon's `minimal.rb` — see `docs/BOILERPLATE.md`. Departing from it is written down in
  `README.md`.
- 🔴
- 🔴

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
