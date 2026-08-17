# Quality checklist

Transverse checks, run before a batch is called finished. They are not
per-story: they are what an audience and a real user notice immediately.

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
