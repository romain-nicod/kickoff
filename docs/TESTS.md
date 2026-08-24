# Test strategy

{{DEV_DAYS}} development days, {{CAPACITY}} points of capacity. A full
test pyramid is not affordable, and pretending otherwise produces
neither tests nor features. So the strategy is **narrow and
deliberate**.

```bash
```

Use the framework's default test tool. Adding a second testing idiom to
a short project costs setup and buys nothing.

## The order: the test first

🔴 **Every story updates the test suite, in the same pull request.** Not
"once it works", not "in the clean-up story" — there is no clean-up
story.

The order is the point:

1. **Write the failing test first**, from the acceptance criterion, in
   its words. Run it. **Watch it fail** — a test that has never failed
   has never proved anything, and the ones that pass on an empty
   implementation are exactly the ones you would not catch later.
2. Write the least code that makes it pass.
3. Then, and only then, tidy it — with the test still green as the net.

Writing the test first is what forces the acceptance criterion to be
testable. A criterion you cannot turn into a failing test is a criterion
that was never precise enough, and finding that out **before** the code
costs an hour; finding it out at the demo costs the demo.

⚠️ **A test written after the code tests the code.** A test written
before tests the story. They look identical in the diff and they are not
the same object.

The exception is honest and narrow: a spike whose point is to find out
whether something is possible. It carries no test, and it is **thrown
away** — the story that follows is written test-first, from scratch.

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

**A business rule gets a test. A screen gets a look.** Test-first for the
rule; the look happens in the verification pass — see
[`QUALITY.md`](QUALITY.md).

When a bug is found in a business rule, the fix comes with the test that
would have caught it. That is the only way the suite grows where it is
worth growing.
