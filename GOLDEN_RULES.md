# Golden rules

Each one is something that costs an hour early and a day late. Read them
once at kick-off, then use them as a review checklist: **a blocked pull
request names the rule by its number.**

Rules 1 to 30 hold whatever you are building. Anything after 30 comes
from the stack layer and is specific to {{STACK}}.

---

## 1. Data you cannot get back

**1 — Validations in the code *and* constraints in the database.** A
validation is a message for the user; a `NOT NULL` and a unique index
are what actually protect the data.

**2 — Index every foreign key and every column you filter on.** The
query that is fast on thirty rows is the one that times out on thirty
thousand.

**3 — A shipped migration is never edited.** Correct it with a new one.
Editing one a teammate already ran leaves two divergent schemas and one
long evening.

**4 — Never build a query by string interpolation.** It is an injection,
every time, including "just for this admin page".

**5 — Multiple writes that mean one thing go in a transaction.** Either
both or neither.

**6 — Store durations, amounts and dates with their unit and their
zone.** `wait_minutes`, not `wait`. The day someone stores seconds in
it, the product lies about time.

**7 — Seeds are idempotent.** Everyone re-runs them; nobody wants three
copies of the same row.

---

## 2. Text is data, and it is not always English

**8 — No visible string hard-coded in a view.** Even in a single-locale
product: a string in a template is a string nobody reviews, reuses or
translates. It goes through the translation layer.

**9 — Never render user input as raw markup.** A note, a comment, a
name: escaped by default. If you need markup, sanitise explicitly.

**10 — Formatting rules live in one place.** Rounding, truncating,
pluralising: one function, called from everywhere. Two formatting rules
diverge the week they exist.

---

## 3. What the product promises

**11 — Touch targets 44 px minimum, and no information carried by
colour alone.** Both are cheap now and expensive to retrofit — and both
are the difference between a product that is usable outdoors and one
that is not.

**12 — Measure on the real device and the real network, or do not claim
it.** A localhost measurement proves nothing about a promise made on
speed.

**13 — Every screen has a way out.** Permission denied, empty result,
offline, out of coverage: each one is a state with an action, not a
dead end.

**14 — Never present a hypothesis as measured data.** In the code, in
the README, and in front of whoever is judging the work. An assumed
number that reaches a slide as fact is the fastest way to lose trust.

**15 — Accessibility and performance are acceptance criteria, not a
later pass.** A story that meets its criteria but fails contrast is not
done.

---

## 4. Code that survives

**16 — Use the framework's own idioms.** Its helpers, its routing, its
conventions. Hand-rolling what the framework provides loses the
escaping, the integration and the upgrade path in one go.

**17 — Business logic lives in one layer, and it is not the view.** A
controller finds, delegates and renders. A template decides nothing.

**18 — Comment the *why*, never the *what*.** The code says what it
does. The comment says why it is allowed to — and cites the rule or the
story by number.

**19 — Name things for what they are.** No abbreviation nobody else
uses, no `data`, no `manager`, no `utils`.

**20 — Delete dead code.** Git remembers. Commented-out code is code
nobody dares remove at the end.

**21 — Do not abstract before the third occurrence.** Two similar blocks
are two blocks. A premature abstraction costs more to undo than the
duplication it prevented.

**22 — Handle the error you expect, and no more.** Never swallow an
exception: a silent failure resurfaces at the worst moment, without a
trace.

**23 — No surprise refactor inside a feature pull request.** If a
rewrite is needed, it is its own commit, ideally its own PR, so the
reviewer can read the feature.

---

## 5. Git and review

**24 — Commit often, small, with a clear message.** One intent per
commit, `Subject: detail`.

```
no   fix stuff
yes  US-102: reject by swipe, with the 24 px dead zone
```

**25 — One branch per issue, one PR per branch, under ~400 changed
lines.** A big PR is not reviewed, it is approved.

**26 — Read your own diff before asking someone else to.** Half the
review comments you will get are things you would have caught yourself.

**27 — Push daily.** Work that exists only on your laptop does not exist
for the team, and cannot be picked up if you are ill.

**28 — Every key lives in `.env`, and `.env` is never pushed.** One
mechanism, no exception: an API key, a token, a password, a connection
string, a webhook URL — it goes in `.env`, which `.gitignore` already
covers. In the code you read it through the environment
(`ENV.fetch("STRIPE_KEY")`), never as a literal, and never "just for
this test". Add the variable to `.env.example` **in the same commit**,
with an empty value: that file is how the next person learns it exists.
In production there is no `.env` at all — the values are the host's
secrets.

```ruby
# no  api_key = "sk_live_5f3a…"
# yes api_key = ENV.fetch("STRIPE_KEY")
```

Never force-push a shared branch either. If a key leaks: revoke and
rotate first, clean the history after — revocation is instant and
total, history rewriting is slow and imperfect.

**29 — CI green before you ask for a review.** Asking someone to read
code that does not build spends their time to save yours.

**30 — Say you are stuck within the hour.** Not at tomorrow's standup.
On a short project a day lost is a measurable share of the capacity —
and someone else has probably already hit the same wall.

---

## Files that are not touched casually

| File | Why |
|---|---|
| The design tokens | A value added without review is a design system dead in three weeks |
| The specification | Changing it is a product decision, and the issue scripts must be re-run |
| The database schema | Conflicts are resolved by re-running migrations, never by hand |
| The linter configuration | An exclusion is a team decision, not a way to make your PR green |
| `.gitignore`, `.env.example` | Removing a line from one of them is how a secret reaches the history |

---

## The five that get skipped

**Use the framework's idioms** (16) · **no visible string outside the
translation layer** (8) · **comment the why** (18) · **small commits
with clear messages** (24) · **say you are stuck** (30).

They are also, in that order, the five most common reasons a pull
request gets blocked.
