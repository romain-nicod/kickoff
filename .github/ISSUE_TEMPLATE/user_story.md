---
name: User story
about: A new user capability, discovered along the way
title: "US-nnn — "
labels: ''
---

### User story

As a <who>, I want <what>, so that <why>.

### Acceptance criteria

- [ ] 1.
- [ ] 2.
- [ ] 3.

### Definition of Ready

<!-- Before the first line of code. -->

- [ ] Acceptance criteria are testable by someone else
- [ ] The routes it adds or changes are named, verb and path
- [ ] Dependencies are delivered, or explicitly stubbed

### Deliverables to produce or update

**Design**

- [ ] **Wireframe** of every screen touched, with its four states: empty,
      loading, error, full. Mobile first, since Bootstrap is. Link it here.
- [ ] **Clickable prototype** — only when the interaction is not obvious:
      several steps, drag and drop, a frame that updates without a reload.
      A plain CRUD does not need one.
- [ ] **Design system** — does Bootstrap already have the component? Card,
      Modal, Navbar, Alert, Badge, Form. If it does, use it. A genuinely new
      component is added to the design system **before** it is coded, named
      in BEM, with its SCSS variable if the colour or the spacing is new.
- [ ] **Data schema** — tables and columns with their types, associations,
      an index on every foreign key and every searched field, constraints
      (`null: false`, unique, default). Files go through Active Storage,
      never a `photo_url` column. Say what happens to the child when the
      parent is destroyed.

**Prepare**

- [ ] **RSpec specs**, one `it` per acceptance criterion, written before the
      code and red for the right reason. The specs this story makes wrong are
      updated in the same story, not later.
- [ ] **`docs/SCENARIOS.md`** — each behaviour in Given / When / Then, naming
      the example that verifies it by the example's description, never by a
      line number.
- [ ] **Pseudocode** — numbered steps as comments inside the method, before
      any real code. They stay in the shipped code. A step that does not fit
      on one line deserves its own method.
- [ ] **Branch** from an up-to-date `main`, named from the story title:
      `<type>/<entity>-<action>` — `feat/recipe-list`, `fix/recipe-validation`.
      If the title yields no clear entity and action, the naming is not the
      problem: the story is too vague or too big.

**Code**

- [ ] **One vertical slice at a time**: migration → model → route →
      controller → view → Stimulus, checked in the browser before the next
      slice. Not the four routes, then the four actions, then the four views:
      at the first error, twelve pieces are suspect instead of three.
      The idioms are in `GOLDEN_RULES.md`, not repeated here.

### Definition of Done

- [ ] Its error and empty states exist and lead somewhere
