# Test strategy

{{DEV_DAYS}} development days, {{CAPACITY}} points of capacity. A full
test pyramid is not affordable, and pretending otherwise produces
neither tests nor features. So the strategy is **narrow and
deliberate**.

```bash
```

Use the framework's default test tool. Adding a second testing idiom to
a short project costs setup and buys nothing.

## What is tested

**The business rules, exhaustively.** They are pure computation, they
are the product's differentiator, and a bug in them is invisible until a
user is harmed by it. Every threshold, every rounding, every boundary.

**The one edge case the specification argues about.** If a rule needed a
paragraph to explain, it needs a test to survive.

**One end-to-end test on the main journey**, once it exists. It is the
demo path — if it breaks, nothing else matters.

## What is not tested

Views, partials, styles. They are verified by looking at them on the
real device, which is a better test than an assertion on markup that
changes every day.

Gesture and animation code. A pointer-event test costs more to write and
maintain than the manual check it replaces — and the manual check must
happen on the real device anyway.

## The rule

**A business rule gets a test. A screen gets a look.**

When a bug is found in a business rule, the fix comes with the test that
would have caught it. That is the only way the suite grows where it is
worth growing.
