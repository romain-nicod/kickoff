# Skills

One Claude skill, `project-kickoff`. **It lives here because this is
where a project starts**: the day you kick one off, it is already at
hand, and Claude follows the method the template writes into the
repository.

| Skill | Answers | Fires |
|---|---|---|
| **`project-kickoff`** | "Create the repository and populate the board." | Starting a project, turning a brief into issues |

## Installing it

Copy it into your personal skill directory:

```bash
cp -R skills/project-kickoff ~/.claude/skills/
```

🔴 **A skill only runs from a `.claude/skills/` directory.** This
repository holds the version, `~/.claude/skills/` holds the executable.
Editing one without the other creates a silent divergence, so re-copy
after every change made here.

`project-kickoff` is not installed into the project it creates: it has
done its job by then.

## Why there is only one

Two method skills sat beside it until 03/09/2026 and were removed. They
restated what this repository's own documents already say, and a rule
written in two places becomes two rules that disagree. The method is in
[`GOLDEN_RULES.md`](../GOLDEN_RULES.md), [`DOR_DOD.md`](../DOR_DOD.md),
[`CONTRIBUTING.md`](../CONTRIBUTING.md) and [`docs/`](../docs/), which is
where a human reads it and where Claude reads it too.
