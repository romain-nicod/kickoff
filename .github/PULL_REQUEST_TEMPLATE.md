<!-- PR title = story title. One pull request per story, opened when everything is green.
     For a deployment pull request, see .github/PULL_REQUEST_TEMPLATE/deployment.md. -->

Closes #<!-- the story -->
Closes #<!-- every [Task] of the story, one line per task -->
Depends on: #<!-- a single line, only if the story depends on another issue; otherwise delete it -->

<!-- The body only names its own story, its [Task] issues and, where there is one,
     its dependency. No list of other pull requests or issues for context. -->

## ⚠️ After pulling this branch

<!-- Tick what the reviewer has to run for the application to work on their machine.
     Delete the section when nothing applies. -->

- [ ] `bundle install` — the Gemfile changed
- [ ] `bin/rails db:migrate` — new migration
- [ ] `bin/rails db:seed` — the demonstration data changed
- [ ] new variable in `.env` — its name is in `.env.example`, say where to find the value
- [ ] other:

## What this changes

<!-- What Romain will see working, not the list of files. Three lines. -->

-

## Files impacted

<!-- One line per file: WHY it changes, not what it contains. -->

-

## Test instructions

<!-- The exact commands, then the real results on the last commit. -->

```bash
bin/rails test
bin/rails test:system
bin/rubocop
bin/brakeman --no-pager
bundle exec bundler-audit --update
bin/importmap audit
```

| Check | Result | Commit |
|---|---|---|
| `bin/rails test` | <!-- n tests, n assertions, 0 failures --> | `<sha>` |
| `bin/rails test:system` | | `<sha>` |
| Lint and security | | `<sha>` |
| CI | <!-- link --> | `<sha>` |
| Recette (port 3100) | <!-- merged in on DD/MM, journey tested --> | `<sha>` |

Journey to follow on the recette environment:

1.

## UI/UX

<!-- If the story touches a page: screenshots at 1512×982, 1280×800 and 390×844, with
     long data. No horizontal scrolling, targets ≥ 44 px, contrast, no visible text in
     the wrong language, empty states and errors that lead somewhere.
     Otherwise: "not applicable". -->

## Idiomatic QA

<!-- Diff read through: Rails conventions, native helpers, no over-factoring,
     intent comments in English, nothing left dead. -->

- [ ] Whole diff read

## Definition of Done

Tracked in the story's issue: the boxes are ticked there, not here.

## Deployment notes

<!-- Migration, variable, task to run, switch to turn on, order to respect.
     Carried over into the "À savoir" section of CHANGELOG.md at the next deployment.
     Otherwise: "none". -->
