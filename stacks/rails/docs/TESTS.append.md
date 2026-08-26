---

## On Rails: RSpec

RSpec, FactoryBot and Capybara. Not Minitest — RSpec is what the team
learnt, and its `describe`/`context`/`it` reads back as the story it
came from.

```bash
bundle exec rspec              # the suite
bundle exec rspec spec/models  # while you work
bundle exec rspec spec/models/venue_spec.rb:42
```

### Where a story's tests land

| The story changes | It gets |
|---|---|
| A business rule, a validation, a scope | `spec/models/` — exhaustively, every boundary |
| A computation extracted from a view | `spec/helpers/` |
| A service, a generator, a parser | `spec/services/` |
| A route's behaviour, a redirect, a status | `spec/requests/` |
| The demo journey, once it exists | `spec/features/` — one, not ten |

⚠️ **Request and feature specs need the routes to exist.** They ask for a
path and click a named helper. That is why routes are written before the
tests, not while you code — see rule 35.

### The name is the acceptance criterion

Written before the code, in the words of the issue. Someone who did not
write the story should recognise it:

```ruby
# no
it "works" do

# yes
it "refuses a booking that starts before the venue opens" do
```

### Four traps already paid for

**`rack_test` does not run Turbo.** A `POST` that returns 200 without
redirecting, or that redirects to the form's own URL, is rejected in the
browser and passes in the suite. Redirect to a **different** URL, and
check the real thing in a real browser.

**FactoryBot, never fixtures**, and a factory carries the **minimum** to
be valid. A factory that sets every attribute makes every test depend on
values it does not care about.

**No real network call.** WebMock is in place; stub REST and GraphQL. A
suite that reaches the internet is a suite that is red on the train.

**`travel_to` for anything time-dependent**, never `sleep`. A test that
sleeps is a test that is flaky on a slow machine and slow on a fast one.

### The guards a suite cannot grow on its own

A green suite tells you the code does what the tests ask. It says nothing
about what nobody thought to ask. Three guards, each written after a
defect walked past a green suite on the first real project:

| Guard | The defect it was born from |
|---|---|
| **Every list folds to cards below `md`** | one list of ten scrolled sideways on a phone, and the guard then found an eleventh nobody had audited |
| **Every locale carries the source's keys, scope by scope** | a translation sat at 56 % for a day and only a person counting could tell |
| **No screen prints `translation missing`** | two lists printed it between their pagination controls, and every refused form printed it in place of an error |

🔴 **A guard that cannot fail is not a guard.** Prove each one by breaking
what it watches, watching it go red, then restoring. A guard written and
never seen to fail is a comment with a `describe` around it.

⚠️ **Walk, do not sample.** The cost of one more path in a guard is a
line; the cost of a missing one is a broken screen in front of a client.
And **paginate before you look**: a three-row list hides every defect
that lives in the second page's controls.

### The pass that finds what the suite cannot

🔴 **Open the thing.** On the first real project, the three worst defects
of a day — a 500 on a button, every validation message replaced by
debug text, an English month name on a translated page — were all found
by opening a screen, and none by a suite of a thousand green examples.

A QA pass that opens a screen and does not **press the button on it** is
a QA pass that has not run. That is not a hypothetical: a pass counted
eleven checkboxes on a backup screen, never clicked Start, and the
button had been returning a 500 in production for two deploys.

### The gate

`bundle exec rspec` fully green, `bundle exec rubocop` with no offence,
`bundle exec brakeman -q` with no warning. All three before a push, and
all three in CI. A project at zero on the three stays there — the day one
offence is tolerated, the count never comes back down.
