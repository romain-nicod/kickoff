# Skills — the method, made executable

Three Claude skills. **They live here because this is where a project
starts**: the day you kick one off, they are already at hand, and Claude
follows the same method the template writes into the repository.

| Skill | Answers | Fires |
|---|---|---|
| **`project-kickoff`** | "Create the repository and populate the board." | Starting a project, turning a brief into issues |
| **`methode-projet`** | "Where are we, which deliverable now, who validates it?" | Before a design deliverable, on any change of structure |
| **`methode-wagon`** | "How do I write this line?" | Before opening the first code file |

🔴 **This repository is the source of truth for all three.** They used to
live in two places — `kickoff/skill/` and `amorce/skills/` — and drifted:
38 lines apart on 24/08/2026, 66 lines on 20/08/2026. One home, one truth.

## Two ways to install, and they do different jobs

**For you, everywhere** — copy them into your personal skill directory:

```bash
cp -R skills/methode-projet skills/methode-wagon skills/project-kickoff ~/.claude/skills/
```

**For a project** — `bin/kickoff` does it for you. It installs
`methode-projet` and `methode-wagon` into the new repository's
`.claude/skills/`, so every session opened in that project picks them up
with no setup, for every person on the team. `project-kickoff` is not
installed there: it has done its job by then.

🔴 **A skill only runs from a `.claude/skills/` directory.** This
repository holds the version, `~/.claude/skills/` holds the executable:
editing one without the other creates a silent divergence. Re-copy after
every change here.

## The three relays

A method rule decided with Romain is written in **three places**, and the
three must agree:

| Where | What it drives |
|---|---|
| **The skills** (here) | How Claude works with him |
| **This template** | What a new project starts from |

🔴 **Two relays since 27/08/2026, not three.** There used to be a third —
Amorce's generators, which served a team — and it was dropped: he works alone,
so serving a tool aimed at hypothetical teams cost something on every pass and
never met a user. Amorce stays online and is not deleted; it simply receives no
new rules. See `~/.claude/CLAUDE.md`, "Les deux relais".

A rule that lives only in the skills applies to Claude alone; a rule that lives
only in the template does not drive Claude. **Both are due, and a pass that
stops before the second says so.**

Which repository is authoritative for what: see
[`KICKOFF.md`](../KICKOFF.md), section "Who is authoritative".

The substance stays in the vault (`ObsiClaud/le-wagon/methode/`): the
skills are its executable form, not a second copy to maintain.
