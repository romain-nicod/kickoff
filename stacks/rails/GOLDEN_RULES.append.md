---

## 6. Rails — write what the framework already wrote

**31 — Use the Rails helpers, always.** `link_to`, `button_to`,
`form_with`, `image_tag`, `t()`. Hand-written HTML for a link loses the
Turbo integration, the escaping and the path helpers in one go.

```erb
<%# no  %> <a href="/venues/<%= venue.id %>">…</a>
<%# yes %> <%= link_to venue.name, venue_path(venue) %>
```

**32 — Use the helpers the boilerplate already installed**, before you
write a tag or a URL by hand. `minimal` ships them and the answer is
usually yes:

| Instead of writing | Use | From |
|---|---|---|
| a `<div class="form-group">` and its label | `simple_form_for`, `f.input`, `f.association` | simple_form |
| an inline `<svg>` or an icon font tag | `icon("regular", "star")` | font-awesome-sass |
| an `<img>` with a hand-built Cloudinary URL | `cl_image_tag` | cloudinary |
| an `<img>` pointing at a blob path | `image_tag object.photo` | Active Storage |
| `session[:user_id]` and a `User.find` | `current_user`, `user_signed_in?` | devise |
| an `if current_user.admin?` in a view | `policy(object).update?` | pundit |

A tag written by hand where a gem provides one loses the escaping, the
Bootstrap classes and the error states — and it drifts the day the gem is
upgraded. When you write a form outside this list, say so and offer the
idiomatic version; do not decide it silently.

**33 — A view displays, it never computes.** The moment a template does
arithmetic, formats a date, picks a label or branches on three
conditions, it becomes a helper in `app/helpers/`, named after what it
answers. A helper can be read on its own and tested on its own; an
expression buried in ERB can be neither.

```erb
<%# no  %> <%= "#{(venue.distance / 80.0).ceil} min walk" %>
<%# yes %> <%= walking_time(venue) %>
```

**34 — Named routes, never string paths.** A route that moves then
breaks in one place, not in forty.

**35 — RESTful routes, seven actions — and you write them before the
code.** A need that does not fit `index show new create edit update
destroy` is usually a second resource, not an eighth action.

Write them first, flat, in `config/routes.rb`, and read `bin/rails
routes` before opening a controller. A route is a **decision about how
the domain is cut**, not plumbing: written first, it makes the second
resource visible while there is still time to discuss it. Written while
you code, it takes the shape of the controller you already had in mind,
and shows you nothing.

`resources ... only: [...]` — declare what the story uses, nothing else.
One level of nesting, never two.

**36 — Fat model, skinny controller.** Business logic in the model or a
concern, called from anywhere.

**37 — Strong parameters, no exception.** On every write. Not "for now,
in dev".

**38 — Partials take explicit locals.** A partial reading `@venue`
cannot be reused and cannot be tested.

**39 — Scopes, not repeated `where`.** The third time the same condition
appears, it becomes a scope.

**40 — No `default_scope`.** It applies where you forgot it applied, and
you find out when a count is wrong.

**41 — `find` raises, `find_by` returns nil — pick on purpose.** A
`find_by` whose nil is never handled is a 500 waiting to happen.

**42 — No network call in a callback.** An `after_save` that calls an
API turns a save into a timeout. Callbacks touch the record, nothing
else.

**43 — Kill the N+1 the day you write it.** `includes` when you render a
collection, and read the log: the same query printed thirty times is
thirty queries.

**44 — `pluck` when you only need values, `exists?` when you only need a
yes.** Instantiating a hundred records to count them is a habit that
scales badly.

**45 — Enums, not magic strings.** You get the scopes, the validation
and readable code; a scattered `"bistro"` gets you a typo.

**46 — `jsonb` is for what has no schema yet.** A field you filter or
sort on deserves a column.

**47 — `Time.current`, never `Time.now`.** The app has a time zone; the
server has a guess.

---

## 7. CSS — one file per component, tokens for everything

**48 — One file per component, an index that only imports.**
`components/card.css`, `field.css`… The index carries no rule of its
own. A stylesheet where every component lives together is a stylesheet
nobody dares edit.

**49 — No hard-coded visual value.** Not a colour, a size, a spacing, a
radius or a duration: everything reads a token, and the token file is
never edited in a feature branch.

```css
/* no  */ padding: 24px; color: #FF8A3D;
/* yes */ padding: var(--s-6); color: var(--accent);
```

**50 — Nesting: one level, never two.** Deep nesting produces selectors
nobody can override and specificity nobody can predict. If you need two
levels, the inner thing wants its own class.

```css
/* no  */ .card { .content { .title { … } } }
/* yes */ .card__title { … }
```

**51 — BEM with a project prefix.** `.gm-card`, `.gm-card__content`,
`.gm-card--compact`. A class that describes its look
(`.big-orange-text`) lies the day the design changes.

**52 — No `!important`, no inline `style` for design.** The only
acceptable inline value is one computed from data by the server — and it
gets a comment saying so.

**53 — Mobile first.** Write the small screen, then add what a bigger
one allows. Never the reverse.

**54 — On iOS, `100svh`, never `100vh`.** The Safari address bar makes
`100vh` jump on every scroll.

---

## 8. Hotwire — as little JavaScript as possible

**55 — Turbo first, Stimulus second, custom JS last.** Most of what
feels like it needs JavaScript is a Turbo Frame or a Turbo Stream.

**56 — One Stimulus controller per behaviour, named after the
behaviour.** `swipe_controller.js`, not `card_controller.js`. A
controller is a verb, not a place.

**57 — No inline JS, no jQuery, no global.** Behaviour is attached with
`data-controller` and `data-action`, so the HTML says what it does.

**58 — `touch-action` and scroll locks are scoped to the element that
needs them.** Put them on the document and the whole app stops
scrolling.

**59 — No `console.log`, no `debugger`, no `binding.b` committed.** The
linter catches some of it; the reviewer catches the rest.

## Green in the suite, dead on the screen

🔴 **Three things a running Rails server never picks up**, and they share
one tell: the suite is green and the browser is broken, because the test
process boots fresh on every run and the server does not.

| What changed | What you see |
|---|---|
| A new directory under `app/` | every page 500 — autoload paths are computed at boot |
| A file in `config/initializers/` | the feature silently does nothing; initializers run once |
| A gem added to the `Gemfile` | `undefined method` on something the gem provides |

**When something works in test and not in the browser, the first
question is: how long has this server been running?**

Found three times in two days on the first real project built from this
template.

## The 44 px touch floor, held by one rule

**60 — A design system that states a minimum touch size holds it in ONE
CSS rule, never by picking `btn-lg` on the buttons somebody remembers.**

```scss
// @media (pointer: coarse) — a FINGER, not a narrow window. A tablet at
// 900 px is touched; a laptop dragged down to 500 px is not.
@media (pointer: coarse) {
  .btn, .form-control, .form-select { min-height: 44px; }
  .btn { min-width: 44px; }   // an icon-only button has no text to widen it
}
```

⚠️ **Bootstrap's own default `.btn` is 38 px**, so a project that never
writes `btn-sm` is still under a 44 px floor. Measured on the first real
project: fourteen `btn-sm` across nine views at **31 px**, including the
theme toggle in the bar of every single page — eleven months of "we
respect the rule" and nothing anywhere enforced it.

## A French — or any non-English — interface

**61 — No I18n fallback to the source language.** A fallback turns a
missing translation into a source-language string that looks deliberate
and that nobody ever finds. Without one, the screen says
`translation missing` in bold, and a guard makes sure it never has to.

**62 — Count every locale against the source SCOPE BY SCOPE.** Comparing
`fr.yml` to `en.yml` is not enough: gems ship their own
`devise.en.yml`, `simple_form.en.yml`, `kaminari`'s
`views.pagination.*`. Those keys exist in the source locale and in no
other, so a naive count calls the translation complete while every
reset-password subject line stays English.

**63 — A key missing from BOTH locales passes every count.** The only
thing that sees it is a spec that opens the screens and reads what is on
them — paginated, and with a form submitted wrong.

### Four traps, each certain, each on the first project that translated

| Trap | Why it is invisible |
|---|---|
| **ERB escapes `'` to `&#39;` and `&` to `&amp;`** | `expect(response.body).to include(I18n.t(…))` stops matching. The diff prints the whole document and never points at the entity. Compare against an **unescaped** helper. ⚠️ This bites in English too: "Clients & prospects". |
| **Rails keeps `errors.messages.*` inside its own gems, source language only** | Every validation on every form prints `Translation missing. Options considered were:` **to the reader**. `rails-i18n` supplies the rest. |
| **`strftime("%B")` asks the C library** and answers in English whatever the locale | No locale file can change it. `I18n.l` is the only thing that translates a month or a day name. |
| **A translated string written into a DATABASE column** | The column becomes bilingual by date and stays that way for ever. Store a **code**, translate on display. |

🔴 **All four were found by opening something. None was found by a green
suite.**
