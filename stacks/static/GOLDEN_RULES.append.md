---

## 6. Static — no build you cannot explain

**31 — Semantic HTML first.** A `<button>` that is a `<div>` loses the
keyboard, the screen reader and the focus ring, and you rebuild all
three by hand, badly.

**32 — One stylesheet per component, an index that only imports.** The
index carries no rule of its own. A single stylesheet where everything
lives is a stylesheet nobody dares edit.

**33 — No hard-coded visual value.** Custom properties for colour, size,
spacing, radius and duration, defined in one file that is not edited in
a feature branch.

**34 — Nesting: one level, never two.** If you need two, the inner thing
wants its own class.

**35 — No framework, no build step, until one is justified in writing.**
A static site that needs npm to render a paragraph has bought tooling it
does not use.

**36 — Every asset is optimised before it is committed.** An image at
its natural size, a font subset to the glyphs actually used. A 3 MB hero
image is the whole performance budget spent on decoration.

**37 — No third-party script on the critical path.** Analytics, fonts,
widgets: deferred, or self-hosted, or absent.

**38 — Progressive enhancement.** The content is readable with
JavaScript disabled or failed. It usually costs nothing and it is the
difference between a slow network and a blank page.

**39 — Relative links, checked in CI.** A broken internal link is the
cheapest bug to prevent and the most embarrassing to demonstrate.

**40 — One page, one purpose, one `<h1>`.** The heading outline is the
document structure, not a font-size picker.
