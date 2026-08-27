# Gems — what we install, what we do not, and why

The decision grid. **Not** the setup steps: those live in
[`rails-ready/docs/CONFIGURATION.md`](https://github.com/ai-gmented-pm/rails-ready/blob/main/docs/CONFIGURATION.md),
and the commented `Gemfile` that ships them is in the same repository.

One rule governs the whole list:

🔴 **A gem whose reason you cannot state is a gem you should not add.**

---

## The three tiers

The tier *is* the decision.

| Tier | Meaning | Where it lives |
|---|---|---|
| **Active** | Every project wants it. Removing one is a choice, written in `README.md` | uncommented in the `Gemfile` |
| **Optional** | Nothing is imposed. A project without accounts must not ship Devise | commented, with its steps |
| **Not picked** | An alternative we weighed and declined, named **with the reason** so nobody re-opens the question | named here only |

---

## Active — installed on every project

| Gem | What it buys you |
|---|---|
| `sprockets-rails` · `sassc-rails` | The SCSS pipeline the `bootstrap` gem requires |
| `bootstrap ~> 5.3` | Grid, components, utilities |
| `autoprefixer-rails` | Browser prefixes, from the Can I Use database |
| `font-awesome-sass ~> 6.1` | Icons callable from a view |
| `simple_form` | `f.input` picks the field type from the column and renders errors, with `aria-invalid` for screen readers |
| `solid_queue` · `solid_cache` · `solid_cable` | Jobs, cache and WebSockets — **in the database, no Redis** |
| `mission_control-jobs` | A dashboard for jobs that fail. Without it, they fail silently |
| `dotenv-rails` | Keys in `.env`, not in the code |
| `pry-byebug` · `pry-rails` | Breakpoints, and a Rails console worth using |
| `httplog` (dev) | Every outgoing HTTP call, logged. The difference between debugging an API call and guessing |
| `hotwire-livereload` (dev) | The browser reloads itself. Pure comfort, missed the day it is gone |
| `faker` (dev/test) | Seed data somebody would believe |
| `rubocop-rails-omakase` · `brakeman` · `bundler-audit` | Style, static security scan, dependency audit |

## Optional — shipped commented

| Gem | Switch it on when | Cost of switching it on by default |
|---|---|---|
| `devise` | The product has accounts | Forces an authentication flow on a project that may not want one |
| `pundit` | Some users may do what others may not | Meaningless without `devise` |
| `pg_search` | Users search text | An index to rebuild and keep in sync |
| `cloudinary` | Users upload files | An external account, and a paid one past the free tier |
| `ruby_llm` | The product calls a language model | An API key, a budget, and authentication in front of it |
| `neighbor` | Search must work on meaning, not words | A PostgreSQL extension, and a vector column tied to one embedding model |

🔴 `devise` and `pundit` are uncommented **together**. Authorization without
authentication has no subject.

## Not picked — and why

| Instead of | We use | Reason |
|---|---|---|
| **Sidekiq** | `solid_queue` | Sidekiq is a good library. It needs **Redis**: one more service to run locally, deploy, monitor and pay for. The database is already there |
| **Redis / Valkey** for Action Cable | `solid_cable` | Same reasoning, same saving |
| **Elasticsearch + `searchkick`** | `pg_search` | Better at scoring, typos and suggestions — and it must run on **every** developer's machine and on the host. Move only when you can name what you are missing |
| **Algolia** | `pg_search` | Excellent and fast, especially on short text. It is a paid external service, and weaker on large documents |
| **Propshaft** | Sprockets | Rails 8's default, but the `bootstrap` gem needs Sprockets. 🔴 They do not coexist |
| **Yarn / a Node toolchain** | Importmap | 🔴 A library is added with `bin/importmap pin`, never `yarn add`. One package does not justify a build chain to maintain |
| **`scaffold`** | Writing the actions you need | The course that teaches it says so itself: demonstrations only. No real project needs all seven CRUD actions at once |

---

## The four settings that matter more than any gem

Full steps in `rails-ready/docs/CONFIGURATION.md`. Listed here because each one
fails **silently** when missed.

| Setting | What it prevents |
|---|---|
| `config.active_job.queue_adapter = :solid_queue` | Jobs running **synchronously without warning** — everything looks fine and nothing is asynchronous |
| Single database for the three `solid_*` gems | Four databases billed where one would do. And the step everyone forgets: removing `config.solid_queue.connects_to` from `production.rb` |
| Solid Queue inside Puma, in development only | A second terminal you must remember to start, and notice you forgot when no job runs |
| The `!.env.example` negation placed **last** in `.gitignore` | Git keeps the last matching rule — Rails 8.1 writes its own `/.env*` partway down, which kills a negation placed above it |

---

## Where each thing lives

| Question | Answer |
|---|---|
| Which gem, and why this one | **here** |
| How to switch it on | `rails-ready/docs/CONFIGURATION.md` |
| The `Gemfile` that ships it | `rails-ready/Gemfile` |
| The generator that installs it | `rails-ready/template.rb` |

🔴 **No copies.** Each subject has one home; the others point at it.
