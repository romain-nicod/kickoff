# The companion skill

`SKILL.md` is a Claude Code skill. The template holds what does not
change between projects; the skill holds what does — reading a brief,
deriving a backlog, sizing it against a real capacity, naming the rules
specific to the product.

## Install

```bash
mkdir -p ~/.claude/skills/project-kickoff
cp skill/SKILL.md ~/.claude/skills/project-kickoff/SKILL.md
```

Then, in any directory: *"kick off a new project"* — or invoke it by
name.

## Keep the two in sync

The skill points at this template and assumes its file names. If you
rename a document here, grep the skill for it. The rule that keeps them
from diverging: **the skill contains no method text of its own.** It
says which document to fill and what makes it worth reading, never what
the document says.
