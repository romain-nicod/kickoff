---

## On Rails: Minitest

Minitest and fixtures — the Rails default. Rails itself is tested with
it, most gems too, and the official documentation speaks the same
language as the code.

```bash
bin/rails test                        # the suite
bin/rails test test/models            # while you work
bin/rails test test/models/venue_test.rb:42
bin/rails test -n /refuses a second/  # by test name
```

⚠️ **RSpec is the majority framework in the wider ecosystem, and it is what
the bootcamp teaches.** Choosing Minitest is a deliberate exception: plain
Ruby instead of a DSL, a suite two to three times faster, no gem to add.

### Where a story's tests land

| The story changes | It gets |
|---|---|
| A business rule, a validation, a scope | `test/models/` — exhaustively, every boundary |
| A computation extracted from a view | `test/helpers/` |
| A service, a generator, a parser | `test/services/` |
| A route's behaviour, a redirect, a status | `test/integration/` |
| The demo journey, once it exists | `test/system/` — one, not ten |

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

### The gate

`bundle exec rspec` fully green, `bundle exec rubocop` with no offence,
`bundle exec brakeman -q` with no warning. All three before a push, and
all three in CI. A project at zero on the three stays there — the day one
offence is tolerated, the count never comes back down.
