---

## 6. Rails — write what the framework already wrote

**31 — Use the Rails helpers, always.** `link_to`, `button_to`,
`form_with`, `image_tag`, `t()`. Hand-written HTML for a link loses the
Turbo integration, the escaping and the path helpers in one go.

```erb
<%# no  %> <a href="/venues/<%= venue.id %>">…</a>
<%# yes %> <%= link_to venue.name, venue_path(venue) %>
```

**32 — Named routes, never string paths.** A route that moves then
breaks in one place, not in forty.

**33 — RESTful routes, seven actions.** A need that does not fit `index
show new create edit update destroy` is usually a second resource, not
an eighth action.

**34 — Fat model, skinny controller.** Business logic in the model or a
concern, called from anywhere.

**35 — Strong parameters, no exception.** On every write. Not "for now,
in dev".

**36 — Partials take explicit locals.** A partial reading `@venue`
cannot be reused and cannot be tested.

**37 — Scopes, not repeated `where`.** The third time the same condition
appears, it becomes a scope.

**38 — No `default_scope`.** It applies where you forgot it applied, and
you find out when a count is wrong.

**39 — `find` raises, `find_by` returns nil — pick on purpose.** A
`find_by` whose nil is never handled is a 500 waiting to happen.

**40 — No network call in a callback.** An `after_save` that calls an
API turns a save into a timeout. Callbacks touch the record, nothing
else.

**41 — Kill the N+1 the day you write it.** `includes` when you render a
collection, and read the log: the same query printed thirty times is
thirty queries.

**42 — `pluck` when you only need values, `exists?` when you only need a
yes.** Instantiating a hundred records to count them is a habit that
scales badly.

**43 — Enums, not magic strings.** You get the scopes, the validation
and readable code; a scattered `"bistro"` gets you a typo.

**44 — `jsonb` is for what has no schema yet.** A field you filter or
sort on deserves a column.

**45 — `Time.current`, never `Time.now`.** The app has a time zone; the
server has a guess.

---

## 7. CSS — one file per component, tokens for everything

**46 — One file per component, an index that only imports.**
`components/card.css`, `field.css`… The index carries no rule of its
own. A stylesheet where every component lives together is a stylesheet
nobody dares edit.

**47 — No hard-coded visual value.** Not a colour, a size, a spacing, a
radius or a duration: everything reads a token, and the token file is
never edited in a feature branch.

```css
/* no  */ padding: 24px; color: #FF8A3D;
/* yes */ padding: var(--s-6); color: var(--accent);
```

**48 — Nesting: one level, never two.** Deep nesting produces selectors
nobody can override and specificity nobody can predict. If you need two
levels, the inner thing wants its own class.

```css
/* no  */ .card { .content { .title { … } } }
/* yes */ .card__title { … }
```

**49 — BEM with a project prefix.** `.gm-card`, `.gm-card__content`,
`.gm-card--compact`. A class that describes its look
(`.big-orange-text`) lies the day the design changes.

**50 — No `!important`, no inline `style` for design.** The only
acceptable inline value is one computed from data by the server — and it
gets a comment saying so.

**51 — Mobile first.** Write the small screen, then add what a bigger
one allows. Never the reverse.

**52 — On iOS, `100svh`, never `100vh`.** The Safari address bar makes
`100vh` jump on every scroll.

---

## 8. Hotwire — as little JavaScript as possible

**53 — Turbo first, Stimulus second, custom JS last.** Most of what
feels like it needs JavaScript is a Turbo Frame or a Turbo Stream.

**54 — One Stimulus controller per behaviour, named after the
behaviour.** `swipe_controller.js`, not `card_controller.js`. A
controller is a verb, not a place.

**55 — No inline JS, no jQuery, no global.** Behaviour is attached with
`data-controller` and `data-action`, so the HTML says what it does.

**56 — `touch-action` and scroll locks are scoped to the element that
needs them.** Put them on the document and the whole app stops
scrolling.

**57 — No `console.log`, no `debugger`, no `binding.b` committed.** The
linter catches some of it; the reviewer catches the rest.
