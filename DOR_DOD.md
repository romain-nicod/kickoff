# Definition of Ready · Definition of Done

Two checklists. They are short on purpose: a checklist nobody reads is
worse than no checklist.

---

## Definition of Ready

A story is **not started** until all five hold.

- [ ] It has an issue, with its acceptance criteria written down.
- [ ] It carries its epic, priority, batch and complexity labels.
- [ ] Its acceptance criteria are testable by someone who did not write
      it — "the screen is fast" is not, "first result in under 3 s on
      4G" is.
- [ ] Its dependencies are delivered, or explicitly stubbed.
- [ ] The business rules it touches are identified by number and not
      contradicted by the design.

**A story whose acceptance criteria must be rewritten is not ready.**
They change in the specification first, then the issue follows.

---

## Definition of Done

A story is **not Done** until all seven hold. Merged is not done.

- [ ] Every acceptance criterion of the issue is checked, one by one.
- [ ] CI is green.
- [ ] It respects the golden rules — no hard-coded value, business logic
      in the right layer, no string outside the translation layer.
- [ ] It works **on the real target device**, not only in a desktop
      browser at the right width.
- [ ] Accessibility holds: touch targets, contrast, no information
      carried by colour alone.
- [ ] Its error and empty states exist and lead somewhere.
- [ ] The README or `AGENTS.md` is updated **in the same commit** if a
      command, a variable or a URL changed.

### The three that get skipped, and why they matter

**The real device.** Something that works with a mouse and fails against
the platform's own gestures is a demo that dies in front of an audience.

**Colour alone.** It is cheap to respect and expensive to retrofit, and
it is the difference between a product a colour-blind user can use and
one they cannot.

**The README in the same commit.** A deployment URL that lives only in
someone's terminal history is a URL that is lost the day that person is
ill.
