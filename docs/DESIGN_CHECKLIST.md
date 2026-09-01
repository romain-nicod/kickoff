# Design checklist — everything a system design must produce

<!-- 🔴 A TEMPLATE. Copy it, fill the Status column, and keep it up to date in
     the same commit as the work. A line left blank is a question nobody asked. -->

**What this is:** the exhaustive list of what has to exist before a line of
product code is written, split into the **visual system** and the **technical
system**. Two different documents, two different reviewers, one checklist.

**Status column:** ✅ produced · 🔄 partial · ❌ missing · 🚫 out of scope, with
the reason. Fill it; do not delete rows.

🔴 **A line marked ❌ is a decision waiting to be made by default.** Nobody
decides "no empty state" — it is discovered on the day of deployment, when the
feed is empty.

---

## 🔴 Before drawing anything: the Le Wagon UI Kit already covers a third of it

**https://uikit.lewagon.com/documentation** ships thirteen components with their
HTML, their ERB **and** their CSS, on Bootstrap.
They are not redrawn — they are **cited**, and only the project-specific
variant gets designed.

| UI Kit component | Its classes | What you do with it |
|---|---|---|
| `button` | `btn btn-flat` · `btn-ghost` · `btn-gradient` | 🔴 `btn-flat` = primary, `btn-ghost` = secondary. `btn-gradient` only if the design admits gradients |
| `alert` | `flash flash-success` · `flash-warning` · `flash-danger` | inline alerts and toasts |
| `navbar` | `navbar navbar-lewagon` | the navigation bars derive from it |
| `footer` | — | taken as is |
| `search_form` | `simple_form search` + `btn-flat` | note it already pairs a field **with its button** |
| `avatar` | `avatar` · `avatar-large` · `avatar-bordered` | profile pictures, if the product has any |

| `card_product` / `card_trip` | `card-product` | a content card usually derives from `card_trip` |
| `notification` | — | unread markers |
| `tabs` | `nav nav-pills` | back-office sections |
| `banner`, `card_category`, `cards_grid` | — | marketing layouts |

⚠️ **What the UI Kit does not cover, and which therefore has to be designed:**
every form control beyond the search field, state badges, the data table, the
modal, and **all the system states**. That is where the design effort belongs —
not on a button that already exists.

### Icons — check the licence before the look

The boilerplate ships `font-awesome-sass`, and Font Awesome **Free** is indeed
free — but its icons are **CC BY 4.0**, which requires attribution, and the
fuller sets are paid. Weigh that before adopting a set.

| Candidate | Licence | Verdict |
|---|---|---|
| **Bootstrap Icons** | **MIT** | the safe default on a Bootstrap project — nothing to attribute |
| Lucide | ISC | very clean, but a second visual family alongside Bootstrap |
| Heroicons, Phosphor, Feather | MIT | fine, same objection |
| Font Awesome Free | CC BY 4.0 + paid tiers | attribution required, and the tiering invites a paid dependency |

🔴 **Serve them locally, never from a CDN.** A page that fetches an icon from a
third party tells that third party who is reading it.

---

## A · Visual system — the design system

### A1. Foundations

| # | Element | What it answers | Status |
|---|---|---|---|
| A1.1 | **Palette** | every colour, named by usage, in both themes |  |
| A1.2 | **Measured contrasts** | text ≥ 4.5:1, large text and UI ≥ 3:1 |  |
| A1.3 | **Type families** | how many, how loaded, fallback stack |  |
| A1.4 | **Type scale** | one line per role: size, weight, line-height |  |
| A1.5 | **Spacing scale** | a progression, not case-by-case values |  |
| A1.6 | **Radii, shadows, borders** | including "zero", which is a decision |  |
| A1.7 | **Motion** | durations, easing, and what never moves |  |
| A1.8 | **Breakpoints** | how many, and what changes at each |  |
| A1.9 | **Grid** | columns, gutter, max reading width, **and how edges are drawn** |  |
| A1.9b | **Tonal ramps** | not five flat tokens but a 100→900 step per role, so a hover or a disabled state derives instead of being invented |  |
| A1.10 | **Iconography** | which set, which sizes, stroke or solid, and the rule for labelling |  |
| A1.11 | **Elevation** | the layers — page, sticky, dropdown, modal, toast — as **named steps**, not raw z-index numbers scattered in the CSS |  |
| A1.12 | **Focus ring** | its exact look, on every interactive element |  |
| A1.13 | **Imagery treatment** | 🔴 how photographs are cropped, which ratios exist, what a missing image looks like, whether figures get a caption. **On any product that shows photographs this is a foundation, not a detail** |  |
| A1.14 | **The "Don't" list** | the explicit prohibitions: what someone will reasonably try and must not do |  |

### A2. Atomic components — each in **all** its states

The states are: **rest · hover · focus (keyboard) · active · disabled · loading**,
plus **error** where a value is entered.

| # | Component | Status |
|---|---|---|
| A2.1 | **Button — primary** |  |
| A2.2 | **Button — secondary** |  |
| A2.3 | **Button — quiet / text-only** |  |
| A2.4 | **Button — destructive** |  |
| A2.5 | **Button — icon only** |  |
| A2.6 | **Link** — inline, and the visited state |  |
| A2.7 | **Text input** |  |
| A2.8 | **Textarea** |  |
| A2.9 | **Select / dropdown** |  |
| A2.10 | **Checkbox** |  |
| A2.11 | **Radio group** |  |
| A2.12 | **File drop zone** |  |
| A2.13 | **Badge / pill** |  |
| A2.14 | **Avatar or account marker** |  |
| A2.15 | **Segmented control** |  |
| A2.16 | **Tag** — distinct from a filter chip: a tag labels, a chip filters |  |

### A3. Molecular components

| # | Component | Status |
|---|---|---|
| A3.1 | **Navigation bar — signed out** |  |
| A3.2 | **Navigation bar — reader** |  |
| A3.3 | **Navigation bar — admin** |  |
| A3.4 | **Footer** |  |
| A3.5 | **Article card** |  |
| A3.6 | **Data table** — header, row, empty row, actions |  |
| A3.7 | **Modal** |  |
| A3.8 | **Toast** |  |
| A3.9 | **Inline alert** |  |
| A3.10 | **Pagination or endless scroll marker** |  |
| A3.11 | **Comment thread** |  |
| A3.12 | **Slideshow / carousel** |  |

### A4. System states — the ones nobody draws until the day they appear

| # | State | Status |
|---|---|---|
| A4.1 | **Empty** — no article yet |  |
| A4.2 | **Loading** |  |
| A4.3 | **No results** after a search |  |
| A4.4 | **Network failure** while writing |  |
| A4.5 | **403** — a reader on an admin URL |  |
| A4.6 | **404** |  |
| A4.7 | **500** |  |
| A4.8 | **Offline / poor connection** |  |

### A5. Editorial rules

| # | Element | Status |
|---|---|---|
| A5.1 | **Tone** — tu/vous, and it holds everywhere |  |
| A5.2 | **Action labels** — verb + object |  |
| A5.3 | **Error messages** — what happened, what to do |  |
| A5.4 | **Dates, numbers, currencies** — one format |  |
| A5.5 | **Empty-state copy** |  |

### A6. The deliverables themselves — what ships, as files

| # | Deliverable | Why it exists | Status |
|---|---|---|---|
| A6.1 | **One stylesheet** — the token sheet (`:root` variables, ramps, base type) plus the component layer, linked from every page | a second stylesheet is a second truth |  |
| A6.2 | **A machine-readable theme** (`theme.json`) — the parameters everything else derives from | lets the system be regenerated, and diffed |  |
| A6.3 | **A reference sheet per foundation** — type, colour, layout, icons, imagery — each at real size | a hex code is not reviewable; a swatch is |  |
| A6.4 | **A reference sheet per component family** | same reason |  |
| A6.5 | **A starter template** consuming the system the intended way | proves the system works before the product does |  |
| A6.6 | **A readme** — how to use the system, and its don'ts | without it the system is read by guessing |  |

---

## B · Technical system — the system design

| # | Element | What it answers | Status |
|---|---|---|---|
| B1 | **Context diagram** | who and what talks to the system |  |
| B2 | **Data model** | tables, columns, relations, indexes, deletion |  |
| B3 | **Routes** | written before the code; a need that does not fit the seven verbs is a second resource |  |
| B4 | **The one request that matters** | the path that must be right, step by step |  |
| B5 | **Authentication** | who signs in, how, and what is deliberately absent |  |
| B6 | **Authorisation** | who may do what, enforced where |  |
| B7 | **File storage** | where bytes land, who may read them |  |
| B8 | **Background jobs** | what is asynchronous, and what happens if it fails |  |
| B9 | **E-mail** | relay, sender, and what an e-mail may never contain |  |
| B10 | **Search** | engine, index, degradation |  |
| B11 | **Cache** | what is cached, and what must never be |  |
| B12 | **Business rules** | numbered, citable from the code |  |
| B13 | **Environments and deploy** | how it ships, how it rolls back |  |
| B14 | **Observability** | how you find out it is broken from abroad |  |
| B15 | **Backup and restore** | and the date of the last real restore |  |
| B16 | **Schema evolution** | migration plus backfill, in the same PR |  |
| B17 | **What is deliberately not built** | with what replaces it |  |

---

## Where this list comes from

Three sources, and it is worth saying which:

1. **What a real project turned out to need** — the states and components its
   wireframes actually used, discovered by drawing them.
2. **The Le Wagon UI Kit** — thirteen components already built on Bootstrap.
3. **A published design-system structure**, compared on 01/09/2026 for its
   **scope** rather than its aesthetic. That comparison alone surfaced six
   rows that were missing: tonal ramps, imagery treatment, elevation steps, a
   machine-readable theme, a starter template and an explicit "Don't" list
   (A1.9b, A1.11, A1.13, A1.14, A2.15 and all of A6).

🔴 **Compare the scope of this list against a system you did not write, once
per project.** It is the cheapest way to find the row you had no reason to
think of — and it takes twenty minutes.

## How to read this list

**Do not fill everything.** A line that does not apply is marked 🚫 with its
reason — that is a decision, and it is written down. What is forbidden is
leaving a line blank: a blank line is a question nobody asked.

**Order matters.** A1 before A2 before A3: a button cannot be drawn before the
palette and the spacing scale exist. B2 before B3 before B4.

**The two halves have different reviewers.** The visual system is validated by
looking; the technical system by reading. Do not merge them into one document —
they are not read the same way.
