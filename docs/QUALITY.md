# Quality checklist

Transverse checks, run before a batch is called finished. They are not
per-story: they are what an audience and a real user notice immediately.

---

## Two passes before a story ships

🔴 **A story is not handed over on the word of the person who wrote it.**
Two passes run before it leaves — a verification pass and a security
review — and both are **asked for explicitly**, never assumed to have
happened.

| Pass | Answers | Runs on |
|---|---|---|
| **Verification** | Does it actually do what the story promised, in the running app? | Every story, before the PR is opened |
| **Security review** | Does it open something that was closed? | Every story that touches auth, input, uploads, money or a third-party call — **and every week regardless** |

### The verification pass

Not "the tests are green". The app is **running**, and each acceptance
criterion of the issue is walked through in it, one by one, out loud:

- [ ] Every acceptance criterion exercised in the running app, not only in a test
- [ ] The empty, error and loading states reached on purpose, not by accident
- [ ] Checked on the real target device, not a desktop browser at the right width
- [ ] The console clean, and the server log free of the same query printed thirty times

A green suite proves the code does what the test says. It says nothing
about whether the test says what the story says.

### The security review

`/security-review` on the diff, plus the stack's own tools (`brakeman`,
`bundler-audit` on Rails) — and read what they print rather than
counting on the exit code. The questions that matter, on any stack:

- [ ] Any new key read from `ENV`, none in the code (rule 28)
- [ ] Strong parameters on every write, no exception "for now"
- [ ] No user input rendered as raw markup
- [ ] No query built by string interpolation
- [ ] Authorisation checked server-side, not only hidden in the view

**Cadence.** Before any story that touches the list above, and **at
least once a week** on the accumulated diff even when no story did — a
week of small changes is exactly where an opening appears that no single
diff shows.

### Who decides

**The agent decides and asks — it does not wait to be told.** Whoever
works on the story (Claude included) names, at the end of the work,
which of the two passes is due and asks for it. Silence is not a pass:
a story handed over without either is a story nobody checked.

---

## Accessibility — non-negotiable

- [ ] Text contrast at least **4.5:1** everywhere
- [ ] Touch targets at least **44 px**
- [ ] **No information carried by colour alone** — position, shape, or a
      word does the work
- [ ] `prefers-reduced-motion` respected: ambient animation stops,
      meaningful transitions stay
- [ ] Every interactive element is reachable and labelled

## Performance

| Metric | Budget | How to check |
|---|---|---|
| First meaningful screen | | Real device, real network |
| Page weight | | Network tab |
| Total JavaScript | | Network tab |
| Main query | | Server logs |

**Measured on the real device over a real network.** A localhost
measurement proves nothing about a promise made on speed.

## Real device — the check nobody does

- [ ] Installed or opened the way a user will open it
- [ ] The layout survives the platform's own chrome appearing and
      disappearing
- [ ] The main gesture does not fight a system gesture
- [ ] Readable in the real conditions of use

## No dead end

Every failure state offers a way out, not an apology:

- [ ] Permission denied
- [ ] Empty result
- [ ] Outside the supported scope
- [ ] Offline
- [ ] Nothing left to show

## Errors

- [ ] The message says **what to do**, not only what is wrong
- [ ] No modal for something a line of text can carry
- [ ] The form keeps what the user typed

## Honesty

- [ ] No number displayed with more precision than the data supports
- [ ] No value shown without a source, when the source is what makes it
      credible
- [ ] No hypothesis presented as a measurement
