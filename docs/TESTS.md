# Test strategy

The method is authoritative (§ 4.3 to 4.5); this page says how it applies in this repository.

## In which order

1. Write the test from the acceptance criterion, in its own words, **with its identifier at the start
   of the name**: `test "CA-01 refuses a second vote from the same member"`.
2. Run it and **see it fail**, for the right reason. A test that has never been red has proved
   nothing; for a defect, it is seen red against the faulty code.
3. Write the least code that makes it pass, then tidy up, with the test green.

No separate test plan: the criterion's identifier in the test name is the link back to the issue.

## What is tested

| Level | When |
|---|---|
| Unit | business rules, validations, services: every boundary |
| Integration | every route touched, for every role (anonymous, signed in, administrator), in HTML and in JSON |
| System | as soon as the story touches a page: the journey in a real browser, at the three widths of the UI/UX pass |
| Regression | every defect fixed |
| Security | permissions, CSRF on, injection through the parameters, XSS escaping; no offensive tooling |

A 200 proves nothing about a page: what counts is what the browser drew.

## When

- While developing: the targeted tests.
- Before merging the branch into the recette environment: the full suite, once.
- CI is the referee: **no pull request until it is green.** A script run outside CI does not count as
  a test.
