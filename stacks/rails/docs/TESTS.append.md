## Rails: Minitest and Capybara

Minitest and fixtures, Rails' own default. A project found on RSpec moves to Minitest.

```bash
bin/rails test                               # unit and integration
bin/rails test:system                        # browser: bin/rails test does not run these
bin/rails test test/models/vote_test.rb:42   # while developing
bin/rails test -n "/CA-01/"                  # the tests of one criterion
```

### Where a story's tests go

| The story changes | It gets |
|---|---|
| a business rule, a validation, a scope | `test/models/`, every boundary |
| a computation taken out of a view | `test/helpers/` |
| a service, a parser | `test/services/` |
| a route: status, redirection, permissions per role, HTML and JSON | `test/integration/` |
| a page | `test/system/`, at the three widths |

### System tests

`test/application_system_test_case.rb` drives headless Chrome through Selenium, and provides:

- `WIDTHS` and `resize_viewport(width)`: the exact CSS widths of the UI/UX pass, 1512, 1280 and
  390 px;
- `assert_no_horizontal_overflow(width)`: no horizontal scrolling, neither on the page nor inside an
  element;
- `assert_reachable_targets(width, selector)`: every control is visible and at least 44 px.

```ruby
test "CA-02 the vote list fits every screen" do
  WIDTHS.each do |width|
    resize_viewport(width)
    visit votes_path
    assert_no_horizontal_overflow(width)
    assert_reachable_targets(width, "main a.btn, main button")
  end
end
```

The `capybara` and `selenium-webdriver` gems belong to the `:test` group of the `Gemfile`;
`python3 scripts/after_rails_new.py` names the one that is missing.

### Traps already paid for

- **`rack_test` does not run Turbo.** A `POST` answering 200 without redirecting passes an integration
  test and fails in the browser: redirect, and check it in a system test.
- **Fixtures, not FactoryBot**: a fixture carries the minimum that makes it valid.
- **No real network call** in the suite: stub the HTTP client.
- **`travel_to`** for anything that depends on time, never `sleep`.
- If the parallel suite is flaky or slow on a machine, `PARALLEL_WORKERS=1`, and the reason in
  `AGENTS.md`.

### The guards a suite does not give itself

A green suite says the code does what the tests ask, and nothing about what nobody thought of asking.
Three guards, each written after a defect went through a green suite on the first real project:

| Guard | The defect it comes from |
|---|---|
| **No list overflows at 390 px** | one list in ten scrolled sideways on a phone, and the guard found an eleventh nobody had checked |
| **Every locale carries the keys of the source, scope by scope** | a translation stayed at 56 % for a whole day, and only somebody counting could see it |
| **No screen shows `translation missing`** | two lists showed it between their pagination controls, and every rejected form showed it instead of the error |

- 🔴 **A guard that cannot fail is not a guard.** Break what it watches, see it red, then put it back:
  that is the method's "seen red", applied to guards.
- ⚠️ **Walk them all, do not sample.** One more path in a guard costs a line; one forgotten path costs a
  broken screen in front of a client. And **paginate before looking**: a list of three rows hides every
  defect that lives in the controls of the second page.

### The gate

`bin/rails test`, `bin/rails test:system`, `bin/rubocop`, `bin/brakeman --no-pager`,
`bundle exec bundler-audit --update` and `bin/importmap audit`: green locally, then in CI, before
opening the pull request.
