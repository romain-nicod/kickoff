# Quality checklist

What to look at during the UI/UX pass of a story and during the periodic
QA review of the production site. When they run, who runs them and what
they produce is set by the delivery method (§ 4.4, § 4.5, § 6 bis); this
page only lists what to look at.

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

## Use the screen, do not only look at it

- [ ] Every button and link the story touched was **pressed**, and what it
      did was checked
- [ ] At least one form was submitted **wrong**, and its error messages
      read as sentences, in the interface's language

A screen that is only looked at is a screenshot, not a pass. One pass on
the first real project built from this template opened a backup screen,
counted its eleven checkboxes, wrote them down — and never clicked Start:
the button had been answering 500 in production for two deploys. And a
screen shows its error messages only when something is refused: on a
translated interface, every validation message had been replaced by
`Translation missing. Options considered were:`, past a suite of a
thousand green tests.

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

## Demo data

- [ ] The seeds are **plausible**: figures a real business could show,
      dates in the past, months that differ, shares that are not all equal

Implausible demo data does not merely look bad: **it makes a working
feature look broken**, and no test ever asks whether a figure is
plausible. On the first real project built from this template, four of
the defects one QA pass caught were in the seeds — a business losing
money every month, entries dated in the future, three identical months
so every comparison read "unchanged", and five payment methods at
exactly 20 % each.
