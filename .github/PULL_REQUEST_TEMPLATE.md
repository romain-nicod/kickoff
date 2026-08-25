Closes #

## What this changes

<!-- Two lines. What a reviewer sees differently after this PR. -->

## Definition of Done

**The story**

- [ ] Every acceptance criterion of the issue is met
- [ ] CI is green
- [ ] No hard-coded value that belongs in a token or a constant
- [ ] Business logic in the right layer, not in the view
- [ ] `routes` lists exactly the paths the story needed, and every view
      uses the named helper rather than a string path
- [ ] Error and empty states exist and lead somewhere
- [ ] Accessibility holds: touch targets, contrast, never colour alone
- [ ] Walked **on the real target device** and **against the deployed
      environment** — not only in a desktop browser, not only locally
- [ ] Nothing left from writing it: no debugger breakpoint, no console
      log, no commented-out attempt, no dead code, no key
- [ ] The **verification pass** was asked for and done — plus a security
      review if this touched auth, input, uploads, money or a
      third-party call

**What it leaves behind** — in this same PR

- [ ] The issue's success criterion is instrumented — whatever it is
      read from exists and produces a number
- [ ] Decisions written **with their reason** in `docs/decisions/`
- [ ] Traps paid written in `AGENTS.md`
- [ ] `docs/SCHEMA.md` / `docs/ARCHITECTURE.md` updated if the structure
      moved
- [ ] `docs/SCENARIOS.md` updated, each scenario naming its test
- [ ] README / `AGENTS.md` / `.env.example` updated if a command, a
      variable or a URL changed

## Golden rules

<!-- Any rule from GOLDEN_RULES.md you knowingly bent, and why. Silence
     means none. -->

## Business rules touched

<!-- BR-nn, or "none". A rule implemented here is cited in the code. -->

## What I could not do

<!-- Honest. A known limitation stated here costs nothing; discovered
     during the demo it costs the demo. -->
