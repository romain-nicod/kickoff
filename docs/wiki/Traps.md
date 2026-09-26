# Cross-cutting traps

Traps that hit more than one story. Each entry says what happens, and what to do instead. Notes that
belong to a single story stay on its own page.

- `bin/rails test` does not load `test/system`: run `bin/rails test:system` as well, locally and in
  CI.
- Selenium scrolls to a hidden control before clicking it: a system test that clicks first reaches a
  button nobody can see. Measure the layout **before** any click
  (`assert_no_horizontal_overflow`, `assert_reachable_targets`).
- A width compared against `innerWidth` proves nothing on mobile: the layout grows with its own
  overflow. Compare against the emulated width.
