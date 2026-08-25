# Definition of Ready · Definition of Done

Two checklists. They are short on purpose: a checklist nobody reads is
worse than no checklist.

This file is the reference. Both lists are copied into the three places
where they are actually ticked:

| Copy | Ticked by |
|---|---|
| `.github/ISSUE_TEMPLATE/user_story.md` | a story opened by hand |
| `DEFINITION_OF_DONE` in `scripts/create_issues.py` | a story generated from the specification |
| `.github/PULL_REQUEST_TEMPLATE.md` | the reviewer, on the diff |

🔴 **A change here is a change in all four, in the same commit.** A
reviewer ticking a shorter list than the story's is exactly how an item
stops existing.

---

## Definition of Ready

A story is **not started** until all seven hold.

- [ ] It has an issue, with its acceptance criteria written down.
- [ ] It carries its epic, priority, batch and complexity labels.
- [ ] Its acceptance criteria are testable by someone who did not write
      it — "the screen is fast" is not, "first result in under 3 s on
      4G" is.
- [ ] The routes it adds or changes are named — verb and path — and they
      fit the seven RESTful actions, or the story says which second
      resource it needs instead.
- [ ] It states a **success criterion**: the outcome that proves the
      story was worth doing, its threshold, and when it is read.
      Acceptance is met the day of the merge; success is read afterwards
      on the running product. If the outcome only exists at epic level,
      the story names the epic measure rather than leaving it blank.
- [ ] Its dependencies are delivered, or explicitly stubbed.
- [ ] The business rules it touches are identified by number and not
      contradicted by the design.

**A story whose acceptance criteria must be rewritten is not ready.**
They change in the specification first, then the issue follows.

---

## Definition of Done

A story is **not Done** until all fifteen hold. Merged is not done.

Two groups, because they fail differently. The first is forgotten under
pressure; the second is forgotten on purpose, "for later", and later
never comes.

### The story does what it promised — 9

- [ ] Every acceptance criterion of the issue is checked, one by one.
- [ ] CI is green.
- [ ] It respects the golden rules — no hard-coded value, business logic
      in the right layer, no string outside the translation layer.
- [ ] `routes` lists exactly the paths the story needed, no more: no route
      without an action, no action without a route, and every view uses the
      named helper rather than a string path.
- [ ] Its error and empty states exist and lead somewhere.
- [ ] Accessibility holds: touch targets, contrast, no information
      carried by colour alone.
- [ ] The journey is walked **on the real target device** *and* **against
      the deployed environment** — not only in a desktop browser at the
      right width, not only on localhost. See
      [`docs/GO_LIVE.md`](docs/GO_LIVE.md): the migration that never ran
      on release is the classic one.
- [ ] Nothing is left from writing it: no debugger breakpoint, no console
      log, no commented-out attempt, no dead code the story replaced.
- [ ] The **verification pass** was asked for and done: every acceptance
      criterion walked through in the running app. A security review too,
      if the story touched auth, input, uploads, money or a third-party
      call — see [`docs/QUALITY.md`](docs/QUALITY.md).

### What the story leaves behind — 6

**In the same commit as the code, never in a pass at the end.**

This is the step other methods call "update the wiki". There is no wiki
here — [`docs/WIKI.md`](docs/WIKI.md) says why, and its content is spread
across four versioned documents that a pull request can review. Spreading
it out is only worth something if the Definition of Done follows it, so
here it is, one line per destination.

- [ ] The **success criterion is instrumented**: whatever it is read from
      exists and produces a number. Done does not mean the threshold is
      met — it means the day it is read, there is something to read.
- [ ] Every **decision** taken along the way is written **with its
      reason**, in [`docs/decisions/`](docs/decisions/). Not what was
      chosen: why, and what was refused.
- [ ] Every **trap paid** is written where the next person will hit it —
      `AGENTS.md`. A trap paid twice was never written down.
- [ ] `docs/SCHEMA.md` and `docs/ARCHITECTURE.md` say what the code now
      does, if the story moved the structure. They are living documents:
      a schema that describes last week's migration is worse than none.
- [ ] `docs/SCENARIOS.md` covers what the story added, in Given / When /
      Then, each scenario naming the test that verifies it — by the
      test's description, never by a line number.
- [ ] `README.md`, `AGENTS.md` and `.env.example` are updated if a
      command, a variable or a URL changed. No key in the code:
      everything is read from the environment (rule 28).
- [ ] **No section this template left blank is still blank.** The check
      is a command, not a reading:

      ```bash
      python3 scripts/check_placeholders.py
      ```

      It names the file and the line. Fill it, or delete the section — a
      heading with nothing under it is worse than no heading. 🔴 No
      other gate can see this: a linter, a test suite and a security
      scan are all silent on an empty stack table.

### The five that get skipped, and why they matter

**The decision without its reason.** Six months later the decision is
still there and the reason is gone, so nobody dares change it and nobody
can defend it. It is the most expensive line in this list to leave
unwritten, and the cheapest to write while it is still fresh.

**Instrumenting the success criterion.** A criterion nobody can read is a
criterion nobody will read. It is written at Ready and forgotten at Done,
and six months later the only thing anyone can say about the feature is
that it shipped.

**The real device, and the deployed environment.** Something that works
with a mouse and fails against the platform's own gestures is a demo that
dies in front of an audience. Something that works on localhost and was
never deployed is the same demo, one step earlier.

**Colour alone.** It is cheap to respect and expensive to retrofit, and
it is the difference between a product a colour-blind user can use and
one they cannot.

**The README in the same commit.** A deployment URL that lives only in
someone's terminal history is a URL that is lost the day that person is
ill.
