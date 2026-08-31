---
name: ereader-reencode
description: Re-encode illustrated books (PDF or EPUB) so an E Ink reader turns pages without stalling — targets the PocketBook Era Color and the Vivlio InkPad Color 3. Use when the user shares children's books, comics, manga, illustrated documentaries or albums and mentions a liseuse, e-reader, PocketBook, Vivlio, Era Color, InkPad, Kaleido, or complains that pages are slow to load, that a book "rame", "met du temps à charger", "ne s'affiche pas en entier", or asks to "réencoder", "optimiser", "alléger" or "convertir" books for a reader. Also use before copying a new batch of books onto a device.
---

# Re-encoding books for an E Ink reader

## The one thing to understand first

**The bottleneck is not file size, it is decode cost per page.** These pull in
opposite directions, and getting this backwards undoes the whole job.

A source file is small on disk *because it pushes the work onto the reader*. An
Internet Archive scan fits 5 megapixels into 17 KB — as JPEG 2000, decoded by
wavelet transform, with a separate JBIG2 mask to decode and compose on top. The
compression is spectacular; the price is paid on every page turn.

Output files are therefore **often larger on disk and three to ten times cheaper
to display**: baseline JPEG, sized to the panel, one greyscale channel where the
book is monochrome, no mask.

⚠️ **Never "re-optimise" an output file to make it smaller.** That recreates the
problem.

## Workflow

1. **Ask which device** if the user has not said. It changes the target size.
   Run `python scripts/reencode.py --list-devices` to show the profiles.
2. **Look at what was given.** Report the classification before converting, so
   the user can correct you — especially any file detected as `text`.
3. **Run the script**, one command per book when titles matter.
4. **Report** the before/after table and hand back the files.

```bash
python scripts/reencode.py "book.pdf" --device era-color --out reencoded
python scripts/reencode.py "book.pdf" --device inkpad-color-3 \
    --title "Mon ballon" --author "Mario Ramos" --publisher "L'École des loisirs"
```

Requires **Pillow**, plus **PyMuPDF** (or pypdfium2, or pypdf) for PDFs. If a
PDF backend is missing, install PyMuPDF — without one, only EPUBs can be
processed.

## 🔴 Three kinds of book, three treatments

The script decides this itself and prints its verdict. Confusing them breaks
books, so check the verdict before trusting the output.

| Verdict | What it is | What happens |
|---|---|---|
| `OK` | a page-image book — album, comic, manga, illustrated documentary | rebuilt as fixed-layout EPUB, one image per page |
| `REFLOW` | a reflowable EPUB — several images per document | **structure preserved**, oversized images shrunk only |
| `TEXTE` | a novel: images under 50% of the file | 🔴 **copied verbatim, never re-encoded** |

🔴 **A novel must never be turned into images.** It would destroy the text,
search, dictionary and font size control, and multiply its weight by fifty. If
the user insists a novel is "slow", the cause is elsewhere — text EPUBs are not
what stalls an E Ink reader.

⚠️ **A reflowable EPUB must not be rebuilt page by page.** One album came out at
4 pages out of 43 because it carried 43 images across 5 documents.

## Rules that are not negotiable

- **Never enlarge a source.** A book already below the panel's resolution is
  left alone — enlarging adds no detail, only blur and decode cost.
- **Bound both dimensions.** Capping width alone lets tall pages overflow: a
  manga page came out 2043 px tall on a 1680 px panel, wasting a quarter of the
  decoded pixels and 26 MB.
- **Keep colour** unless the panel is monochrome or the book measurably is.
  `--gray auto` measures it. Do not assume.
- **Never modify the originals.** Output goes to a separate directory.
- **`mimetype` first and uncompressed** in the zip, or readers reject the file.
  The script handles this — do not rebuild the archive by hand.

## Details worth knowing

- **Pale colours?** A Kaleido panel renders colour at half resolution and looks
  washed out. Try `--saturate 125` and compare on the device.
- **Too heavy?** `--quality 78` (default 85) is the first lever. Comics are the
  bulk of any library.
- **Filenames with accents**: matching is normalised (NFC/NFD), because macOS
  mixes both and a literal pattern silently skips files.
- **Titles** are guessed from the filename; pass `--title` and `--author` for a
  readable device library.
- **Unknown device?** Use `--width` and `--height` with the panel's native
  black-and-white resolution. See `references/devices.md`.

## Limits to state up front

- **Large files may not survive upload.** A 74 MB comic scan will likely exceed
  the attachment limit. Ask the user to run the script locally in that case —
  it is standalone and needs only Pillow and PyMuPDF.
- The script **cannot fix a bad scan**: crooked pages, missing pages or unreadable
  text in the source stay that way.
