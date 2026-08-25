# Definition of Ready · Definition of Done

Two checklists. They are short on purpose: a checklist nobody reads is
worse than no checklist.

This file is the reference. Both lists are copied into the places where
they are actually ticked — `.github/ISSUE_TEMPLATE/user_story.md` for a
story opened by hand, `DEFINITION_OF_DONE` in `scripts/create_issues.py`
for a story generated from the specification. **A change here is a change
in all three, in the same commit.**

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

A story is **not Done** until all eleven hold. Merged is not done.

- [ ] Every acceptance criterion of the issue is checked, one by one.
- [ ] The **success criterion is instrumented**: whatever it is read from
      exists and produces a number. Done does not mean the threshold is
      met — it means the day it is read, there is something to read.
- [ ] CI is green.
- [ ] It respects the golden rules — no hard-coded value, business logic
      in the right layer, no string outside the translation layer.
- [ ] `routes` lists exactly the paths the story needed, no more: no route
      without an action, no action without a route, and every view uses the
      named helper rather than a string path.
- [ ] It works **on the real target device**, not only in a desktop
      browser at the right width.
- [ ] Accessibility holds: touch targets, contrast, no information
      carried by colour alone.
- [ ] Its error and empty states exist and lead somewhere.
- [ ] No key in the code: everything is read from the environment, and
      any new variable is in `.env.example` (rule 28).
- [ ] The **verification pass** was asked for and done: every acceptance
      criterion walked through in the running app. A security review too,
      if the story touched auth, input, uploads, money or a third-party
      call — see [`docs/QUALITY.md`](docs/QUALITY.md).
- [ ] The README or `AGENTS.md` is updated **in the same commit** if a
      command, a variable or a URL changed.

### The four that get skipped, and why they matter

**Instrumenting the success criterion.** A criterion nobody can read is a
criterion nobody will read. It is written at Ready and forgotten at Done,
and six months later the only thing anyone can say about the feature is
that it shipped.

**The real device.** Something that works with a mouse and fails against
the platform's own gestures is a demo that dies in front of an audience.

**Colour alone.** It is cheap to respect and expensive to retrofit, and
it is the difference between a product a colour-blind user can use and
one they cannot.

**The README in the same commit.** A deployment URL that lives only in
someone's terminal history is a URL that is lost the day that person is
ill.
