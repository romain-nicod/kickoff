# Prompt library

_One prompt per design deliverable. They are versioned like the rest: a prompt that produced a bad output gets amended here, not rewritten from memory next time._

_Until 27/08/2026 this file was generated from Amorce's prompt-library brick. Amorce is out of the method circuit; this file is now maintained directly here._

## How to use this file

1. Copy the prompt, replace everything between `<` and `>`, send it.
2. Read the **Check before accepting** list before you accept anything.
3. If the output was wrong, fix the prompt **here** and commit it. A prompt is a project asset, not a throwaway message.

These prompts are written for: **An agent that reads the repository (Claude Code, Cursor, Copilot)**.
They point at files by path. The agent is expected to open them itself — if yours cannot, rewrite the openings so they carry the content instead — see the note at the bottom of this file — rather than pasting paths at a tool that cannot follow them.

## Product

### Draft the PRD from a brief

**When:** Day one, before any screen or any table exists.

**Have ready:** `docs/PRD.md` (the template) and whatever brief you have.

```text
Read docs/PRD.md.
Here is the brief for the project:
<paste the brief, however rough>

Fill the template section by section. Follow these rules:
- Section "Problem": evidence only. Where the only evidence is "it seems
  obvious", write it down as a named assumption instead of an argument.
- Section "Outcomes": no target without a baseline. If we have no
  baseline, say so and leave the target empty.
- Section "Non-goals": at least three, and each one something a
  reasonable person would otherwise ask for.
- Section "Functional requirements": number them FR-1, FR-2..., make
  each one testable by someone who did not write it, and link each to
  an outcome above.
- Section "Open decisions": every line gets an owner and a date.

Leave any hole you cannot fill visibly empty. Do not invent a number.
At the end, list what you left empty and what you would need to fill it.
```

**Check before accepting:**
- Every `FR-n` is falsifiable — "the screen is fast" is not, "first result under 3 s on 4G" is.
- No figure appeared that you did not supply. Invented baselines are the single most common failure here.
- The non-goals are things somebody would actually ask for, not straw men.
- The holes are still visible. A PRD with three empty boxes is usable; one with three invented numbers is dangerous.

### Argue against the PRD before committing to it

**When:** Once the PRD reads well — which is exactly when it stops being questioned.

**Have ready:** The filled `docs/PRD.md`.

```text
Read docs/PRD.md.

Argue against it. Do not summarise it, do not improve the wording.
Answer these four questions, with the strongest case you can make:
1. Which stated outcome would still be reached if we built nothing?
2. Which assumption, if false, makes the whole document worthless?
   Rank them by how expensive it would be to discover late.
3. Which functional requirement is there because it is easy to build
   rather than because an outcome needs it?
4. What is the cheapest thing we could ship that would tell us whether
   the problem statement is even true?

Be specific and quote the document. "It could be clearer" is not an answer.
```

**Check before accepting:**
- At least one objection actually changes the document. If everything survives, the exercise was not run honestly.
- The answers quote the PRD rather than paraphrasing it.
- Question 4 produces something buildable this week, not a research programme.

### Turn the requirements into user stories

**When:** Once the PRD holds. Before the board gets populated.

**Have ready:** `docs/PRD.md`, `DOR_DOD.md`, `docs/BACKLOG.md`.

```text
Read docs/PRD.md and DOR_DOD.md.

Write one user story per functional requirement, in this format:
  As a <role>, I can <action>, so that <outcome>.
Then, for each story:
- Acceptance criteria, in Given / When / Then, testable by someone who
  did not write the story.
- The `FR-n` it satisfies, quoted with the exact wording of the PRD.
  Do not rephrase it — nobody will make the connection afterwards.
- The entities it touches, among: the project entities.
- A size: S, M or L. Anything L gets split now, not later.

Then check every story against the Definition of Ready and tell me
which ones fail it, and on which criterion.
```

**Check before accepting:**
- Every `FR-n` in the PRD is covered by at least one story, and no story invents a requirement that is not in it.
- The acceptance criteria say what is observable, not how it is implemented.
- No L remains. An L that survives is a story nobody sized honestly.
- The stories that fail the Definition of Ready are named, not silently fixed.

## Design

### Wireframes derived from the PRD

**When:** After the PRD, before the first view.

**Have ready:** `docs/PRD.md` — the main journey and the `FR-n` list.

```text
Read docs/PRD.md.

Produce wireframes, not a finished design. Rules:
- One artboard per step of the main journey, in the order of the journey.
- Each artboard carries, written on it, the `FR-n` it satisfies. An
  artboard satisfying none of them is an idea we had while drawing:
  either it goes back into the PRD, or it goes away.
- For every screen that loads data, draw its four states: empty,
  loading, error, full. The error state is the one always skipped.
- Mobile width first. Desktop is the second pass, not the first.
- Grey boxes and real labels. No colour, no final copy, no icon set.

List at the end: the screens you drew, the `FR-n` left uncovered, and
any question the PRD did not answer.
```

**Check before accepting:**
- Every artboard names its `FR-n`, and the uncovered ones are listed.
- The four states exist wherever data loads — count them, do not trust the summary.
- Nothing was decided visually that the PRD does not support.
- It still looks like a wireframe. A wireframe that arrives coloured has skipped the step where it was cheap to change.

### Visual identity — palette, type, spacing

**When:** Once the wireframes are stable. Never before: styling a layout that still moves is work done twice.

**Have ready:** The wireframes, and the product's audience from the PRD.

```text
Here is what the product does and who it addresses:
<paste the pitch and the primary segment from the PRD>
Here are the wireframes:
<paste or describe the screens>

Propose a visual identity, delivered as tokens, not as a mood board:
- A palette: one primary, one secondary, one accent, plus the neutral
  ramp. Give every pair its contrast ratio against its background, and
  flag anything under 4.5:1 for body text.
- Type: at most two families, with the scale actually used (body, and
  the heading levels the screens need). No size that no screen uses.
- Spacing: a single scale, and the rule for when each step applies.
- Radius, borders and shadow: one value each unless a screen proves
  otherwise.

Deliver it as CSS custom properties ready to paste into a stylesheet,
named for their role rather than their colour, and say for each choice
which screen made you choose it.

Do not put a single value inline in a template. The style lives in a
stylesheet, always.
```

**Check before accepting:**
- The contrast ratios are given, and the failing ones are flagged rather than quietly kept.
- Every token is justified by a screen. Tokens nobody uses are the reason design systems rot.
- The names say the role (`--color-surface`), not the value (`--color-light-grey`) — otherwise a theme change renames everything.
- Nothing came back as inline style.

### Turn a screen into components

**When:** The first time a pattern appears on a second screen — not on the first.

**Have ready:** The stylesheet and the two screens that share the pattern.

```text
Read the stylesheet and the views concerned.

These two screens share a pattern. Extract it into one component:
- Name it for what it is, not where it first appeared.
- Give it its own stylesheet partial, and say where it gets imported.
- List its variants, and refuse any variant that exists only once.
- Say what stays specific to each screen and must not move into it.

Do not touch anything else in the views. Do not rename anything that
was not part of the pattern.
```

**Check before accepting:**
- The component is genuinely used twice. One usage is not a component, it is a premature abstraction.
- No variant exists for a single call site.
- Nothing outside the two screens changed.

## Data and architecture

### Data schema, as a diagram that diffs

**When:** Before the first migration, then again inside every commit that changes the structure.

**Have ready:** `docs/SCHEMA.md`, and the migration or the stories in hand.

```text
Read docs/SCHEMA.md and the current schema file.
The entities in play: the project entities.

Produce the entity-relationship diagram as a Mermaid `erDiagram` block:
- Every table, its columns, their types, and whether they are required.
- Foreign keys marked FK, and the indexes that exist, marked as such.
- Cardinalities written explicitly, one relation per line.
- Where you are unsure whether a relation is 1-N or N-N, do not pick:
  write it as an open question under the diagram.

Mermaid, never an image: it diffs, it renders in the repository, and a
review can see what changed. A screenshot of a schema is dead the day
it is posted.
```

**Check before accepting:**
- The diagram matches the real schema file, column for column. Where they differ, it is the Markdown that is wrong — never the other way round.
- The uncertain relations came back as questions, not as decisions taken quietly on your behalf.
- It is Mermaid, in the document, not an attached picture.

### Architecture diagram

**When:** At the start, then inside every commit that adds a service, a job or an external dependency.

**Have ready:** `docs/ARCHITECTURE.md`.

```text
Read docs/ARCHITECTURE.md and the dependency manifest.

Produce two Mermaid diagrams and nothing else:
1. Context: the system, the kinds of people who use it, and every
   external system it talks to. One box for our system.
2. Containers: what actually runs — application, database, background
   jobs, storage, third-party services — with what flows between them
   and over which protocol.

Then, under the diagrams, a short table of the external dependencies:
what each one is for, what breaks if it is unavailable, and whether it
holds any personal data.

Only draw what exists today. Something planned goes in a sentence
below, marked as planned — a diagram that shows the intended
architecture stops describing the real one.
```

**Check before accepting:**
- Every box exists in the running system. A drawn-but-unbuilt box is how an architecture document starts lying.
- The failure column is filled for every dependency — that is the column anyone will read during an incident.
- Both diagrams are Mermaid and render in the repository.

### Refresh the living documents after a change

**When:** In the same commit as the migration or the new dependency. Not in an end-of-project pass.

**Have ready:** The diff you are about to commit.

```text
Here is the change I am about to commit:
<paste the diff, or name the migration>

Two documents are living and must never lag behind the code:
`docs/SCHEMA.md` and `docs/ARCHITECTURE.md`.

Tell me which of them this change affects and why, then produce the
updated section — the section only, not the whole file. If neither is
affected, say so plainly rather than finding something to edit.

Then give me the commit message, mentioning the document update.
```

**Check before accepting:**
- It updated a section, not the whole document. A wholesale rewrite hides what actually changed from the review.
- "Neither is affected" is an acceptable answer and you should be suspicious when it never comes.
- The updated document and the code go out in the same commit. A wrong schema is worse than no schema: decisions get made on it.

## Delivery

### Implement one story

**When:** Once the story meets the Definition of Ready, and its tests are written.

**Have ready:** The story, `AGENTS.md`, `CONTRIBUTING.md`.

```text
Read AGENTS.md and CONTRIBUTING.md.
Here is the story:
<paste the story and its acceptance criteria>

Before writing any code:
1. Give me the branch name derived from the story title, following the
   repository convention. One story, one branch.
2. Give me the pseudo-code of the change, step by step, and the list of
   files you will touch. Wait for my go-ahead on that list.

Then implement, under these constraints:
- Stay inside the files listed. Anything else is a separate story.
- No refactoring of code the story does not require, however tempting.
- Style goes in a stylesheet, never inline in a template.
- Use the helpers the project already provides rather than
  hand-rolling markup.
- The tests written for this story must pass, and no existing test
  may break.

If a file you did not list turns out to be necessary, stop and tell me
before touching it.
```

**Check before accepting:**
- The file list was agreed before the code was written. That agreement is the whole point of the pause.
- Nothing outside the list changed — check the diff, not the summary.
- No opportunistic refactor rode along.
- The branch is named after the story, so the pull request is readable six weeks later.

### Open the pull request

**When:** Once the story is done and the checks are green locally.

**Have ready:** The diff, the story, `DOR_DOD.md`.

```text
Read DOR_DOD.md.
Here is the diff:
<paste the diff or the branch name>

Write the pull request description:
- What changed and why, in five lines, for someone who does not have
  the story in mind.
- The story it closes, and the acceptance criteria, each marked as met
  or not met.
- What a reviewer should look at first, and what is deliberately out
  of scope.
- Anything you were unsure about while writing it.

Then walk the Definition of Done and tell me which items are not met.
Do not mark an item met because it is nearly met.
```

**Check before accepting:**
- The unmet Definition-of-Done items are named. A pull request that claims to meet everything usually has not been checked.
- The description is readable without the story open.
- The uncertainties are stated. Those are the lines a reviewer should start from.

## Quality

### Write the tests before the code

**When:** As soon as the story is ready, and before a single line of implementation.

**Have ready:** The story and its acceptance criteria.

```text
Here is the story and its acceptance criteria:
<paste the story>
The entities in play: the project entities.

Write the tests for it, and only the tests. Do not write the
implementation, do not stub it, do not tell me how you would build it.

- One test per acceptance criterion, named after the behaviour rather
  than the method.
- Cover the failure paths too, not only the happy one.
- Use the project's existing factories and helpers; do not invent new
  fixtures where one already exists.

Then run them and show me the failures. They must fail for the right
reason — a test that passes before the feature exists is testing
nothing.
```

**Check before accepting:**
- The tests fail, and the failure message is the one you would expect from a missing feature — not from a typo or a missing constant.
- Every acceptance criterion has its test, and the mapping is obvious from the names.
- No implementation arrived alongside. If it did, the discipline is already gone.
- Failure paths are covered, not just the happy one.

### Document the scenarios, mapped to the tests

**When:** Once a story's tests are green, before the pull request.

**Have ready:** `docs/SCENARIOS.md` and the test file.

```text
Read docs/SCENARIOS.md and the test file for this story.

Add this story's scenarios to the document, in readable English — the
kind someone who does not read code can follow:
- One line per scenario: the situation, the action, the expected result.
- Next to each, the reference of the test that covers it: file and
  example name, exactly as they are written.
- At the end of the section, list any scenario that has no test, and
  any test that covers a scenario not written down.

Do not rewrite the scenarios that are already there.
```

**Check before accepting:**
- Every reference resolves to a test that actually exists — check one or two by hand.
- The gaps in both directions are listed rather than quietly closed.
- It reads as English prose. A scenario document written in test jargon is a duplicate of the test file, and will be maintained like one: not at all.

### Review the change before pushing

**When:** Before every push, and as a full pass once a week.

**Have ready:** The diff.

```text
Here is the change:
<paste the diff, or name the branch>

Review it, and rank what you find by severity. For each finding:
- The file and line.
- What breaks, with the concrete input or state that breaks it. If you
  cannot describe the failing case, say the finding is a hunch and
  mark it as such.
- The smallest fix.

Look in this order: correctness first, then things that will not work
under real data volume, then duplication, then naming. Style comes last
and only where the project has a rule about it.

Do not fix anything yet. Do not suggest refactors the change does not
require.
```

**Check before accepting:**
- Every finding names a failing case, or is explicitly labelled a hunch. Findings without one are how review noise gets built.
- The ranking is by severity, not by the order the files appear in the diff.
- Nothing was fixed unilaterally. You decide what gets acted on.

### Security review

**When:** Once a week, and before anything that touches authentication, uploads, payments or personal data goes out.

**Have ready:** The changes of the week, and the dependency manifest.

```text
Read the changes since the last security pass and the dependency manifest.

Run a security pass over it. Cover, in this order:
- Anything reaching the database or the shell from user input.
- Authorisation: for every action, who is allowed, and where that is
  enforced. Being hidden in the interface does not count.
- Data leaving the system: logs, error pages, redirects, third-party
  calls. Say whether any of it carries personal data.
- Secrets: anything hard-coded, anything in the repository history.
- Uploads and file handling, if any.
- Dependencies with known advisories.

For each finding: what an attacker does, step by step, what they get,
and the smallest fix. Where you are not sure it is exploitable, say so
rather than padding the list.
```

**Check before accepting:**
- Every finding comes with an actual attack path. "This could be unsafe" is not a finding, it is an anxiety.
- The authorisation answers point at where enforcement lives in the code, not at the interface.
- The uncertain items are marked uncertain. A security report that is 90 % padding gets skimmed, which is worse than no report.

---

**Missing a prompt?** Write it here the first time you need it, with its **Check before accepting** list — that list is the part that makes it reusable. A prompt with no acceptance criteria is a wish.

## If your assistant cannot open files

Every prompt above points at a path. When you work with a chat that has no
access to the repository, replace each opening line with the content itself:

| Written here | Send instead |
|---|---|
| `Read docs/PRD.md.` | `Here is the PRD:` then paste it |
| `Read AGENTS.md and CONTRIBUTING.md.` | `Here are the working rules:` then paste them |

A prompt that names a file the assistant cannot open does not fail loudly. It
produces confident invention, and that is much more expensive to notice.
