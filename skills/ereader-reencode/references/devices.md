# Device profiles

`width` and `height` are the panel's **native black-and-white resolution**.

On a Kaleido panel, colour renders at **half** that resolution (a colour filter
sits over a monochrome panel). Target the black-and-white figure anyway: line
art — which is most of what a comic or an album is made of — genuinely uses it.

| Profile | Panel | B&W | Colour |
|---|---|---|---|
| `era-color` | PocketBook Era Color, 7", Kaleido 3 | 1264 × 1680 (300 dpi) | 632 × 840 (150 dpi) |
| `inkpad-color-3` | Vivlio / PocketBook InkPad Color 3, 7.8", Kaleido 3 | 1404 × 1872 (300 dpi) | 702 × 936 (150 dpi) |
| `era` | PocketBook Era, 6", monochrome | 1072 × 1448 (300 dpi) | — |

## Why the colour figure matters

It explains a specific failure: a page laid out at 1264 × 1430 showed **a
quarter of itself** on an Era Color, because the reader worked against the
632 × 840 colour surface. The fix was not a smaller image — it was a layout the
reader scales, namely an `<svg>` with a `viewBox` and `preserveAspectRatio`.

## Adding a device

Add an entry to `DEVICES` in `scripts/reencode.py`, or skip the profile
entirely:

```bash
python scripts/reencode.py book.pdf --device era-color --width 1236 --height 1648
```

Find the native resolution in the manufacturer's specification — **verify it,
do not infer it from the screen size**. Getting this wrong is what produced the
quarter-page bug above.
