# Secrets

**No secret ever enters Git.** Not in a commit, not in a comment, not in
a fixture, not "temporarily to test the deploy".

## One mechanism — golden rule 28

🔴 **Every key lives in `.env`, and `.env` is never pushed.** An API key,
a token, a password, a connection string, a webhook URL: all of them, the
same way, with no exception for "this one is not really a secret".

| | Development | Staging / production |
|---|---|---|
| Where the value is | `.env`, gitignored | the host's secrets |
| How the code reads it | `ENV.fetch("NAME")` | `ENV.fetch("NAME")` |
| What is versioned | `.env.example`, empty values | `.env.example`, empty values |

The code path is identical in both: **there is no `.env` in production**,
and no branch in the code that knows which environment it is in. That is
the whole point of the mechanism — nothing to switch, so nothing to
forget to switch.

On Rails, `dotenv-rails` loads `.env` in development and test:

```ruby
group :development, :test do
  gem "dotenv-rails"
end
```

Check `.gitignore` before adding anything new;
`git check-ignore -v <file>` answers in one line — and it should answer
for `.env` before you write a single key into it.

## `.env.example`

`.env.example` is versioned and lists every variable the app can read,
with no real value. When you add a variable, add it there **in the same
commit** — that file is how the next person finds out it exists, and the
only place they can look, since nobody else's `.env` ever leaves their
machine.

⚠️ It is a template file: it carries variable **names**, never the ones
one particular project happened to need. A `FOO_API_KEY` left behind
from another product is how a team spends an afternoon looking for a key
that was never required.

```bash
cp .env.example .env   # then fill in your own values
```

## Sharing them

Out of band: a password manager, not the team chat, not an email, not a
commit. Whoever sets up the host puts the value in the host's secrets
and tells the others **where it lives**, never what it is.

## If a secret leaks

Immediately, in this order:

1. **Revoke and rotate** at the provider. A key in a Git history is
   compromised — even in a private repository, even after a force push.
2. Replace it in the host's secrets.
3. Then, and only then, consider cleaning the history.

Rotating first is the whole point: history rewriting is slow and
imperfect, revocation is instant and total.

## What is not a secret

Reference data, design tokens, the specification. They live in the
repository on purpose. A private repository is private for intellectual
property, not because it holds credentials — and that distinction is
what keeps the real secrets outside of it.
