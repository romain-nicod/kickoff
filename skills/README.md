# Skills

One skill, `project-kickoff`: it applies, with this template, the delivery-by-user-story method
(`/Users/albert/Documents/Claude/ObsiClaud/dev/methode/Méthode - Livraison applicative par user story.md`).
**It lives here, versioned with the templates it uses**: a skill and a template changed in the same
commit cannot diverge.

| Skill | Answers | Triggered by |
|---|---|---|
| **`project-kickoff`** | "Create the repository, the board and the first stories"; "Prepare the deployment" | starting a project, a need to turn into stories, a deployment pull request |

## Installation: a symbolic link, not a copy

`~/.claude/skills/project-kickoff` is a **symbolic link** to this folder in the main clone. Nothing has
to be copied after a change: the skill that loads is the one on the branch checked out in
`code/kickoff`, normally `main`. A working branch in a worktree does not change the skill in service
until it is merged.

On a new machine, from its terminal:

```bash
ls -la ~/.claude/skills/
ln -s /Users/albert/Documents/Claude/code/kickoff/skills/project-kickoff ~/.claude/skills/project-kickoff
ls -l ~/.claude/skills/project-kickoff
```

Expected: a line starting with `l` and ending with
`-> /Users/albert/Documents/Claude/code/kickoff/skills/project-kickoff`. If `ln` answers
"File exists", a folder or a link already carries that name: look at what it holds before anything
else, archive it under `~/.claude/skills-archive/` if it is an old copy, then run `ln` again.

`bin/kickoff` removes `skills/` from the project it creates: the skill's work is done by then.

## Why there is only one

The former `methode-projet` and `methode-wagon` skills are archived under
`~/.claude/skills-archive/` and are not coming back: they carried a second version of the method, which
contradicted it (RSpec, `feat/…` branches, French comments, specifications and test plans outside the
issues). The method is authoritative in the vault note; the Rails idioms that still hold are in
`stacks/rails/` (`GOLDEN_RULES.append.md`, `docs/GEMS.md`).
