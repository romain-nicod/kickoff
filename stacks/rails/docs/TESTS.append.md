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
