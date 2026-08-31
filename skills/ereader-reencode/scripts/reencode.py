#!/usr/bin/env python3
"""Re-encode illustrated books so an E Ink reader turns pages without stalling.

Standalone: no ImageMagick, no poppler. Uses PyMuPDF when available and falls
back to pypdfium2, then to extracting the PDF's embedded page images.

    python reencode.py INPUT... --device era-color [--out DIR]
    python reencode.py --list-devices

The bottleneck on an E Ink reader is NOT file size, it is decode cost per page.
Source files are small because they push the work onto the reader: JPEG 2000
with JBIG2 masks, or 2000 px JPEGs rescaled by a CSS transform. Output is often
LARGER on disk and far cheaper to render. That trade is the whole point.
"""
import argparse, io, json, os, re, shutil, sys, tempfile, unicodedata, uuid, zipfile
from html import escape

# --- Device profiles -------------------------------------------------------
# width/height are the panel's native BLACK AND WHITE resolution: colour on a
# Kaleido panel renders at half that, but line art still benefits from the full
# figure. Add a profile rather than editing one.
DEVICES = {
    "era-color": {
        "label": "PocketBook Era Color (7\", Kaleido 3)",
        "width": 1264, "height": 1680, "colour": True,
    },
    "inkpad-color-3": {
        "label": "Vivlio / PocketBook InkPad Color 3 (7.8\", Kaleido 3)",
        "width": 1404, "height": 1872, "colour": True,
    },
    "era": {
        "label": "PocketBook Era (6\", monochrome)",
        "width": 1072, "height": 1448, "colour": False,
    },
}

QUALITY = 85
SATURATE = 100          # >100 lifts a pale Kaleido palette, e.g. 125


def log(msg):
    print(msg, flush=True)


# --- Imaging ---------------------------------------------------------------
try:
    from PIL import Image, ImageEnhance
except ImportError:
    sys.exit("Pillow is required: pip install pillow")


def fit(img, box_w, box_h):
    """Shrink to fit inside the panel. Never enlarges — enlarging a source adds
    no detail, only blur and decode cost."""
    w, h = img.size
    if w <= box_w and h <= box_h:
        return img
    scale = min(box_w / w, box_h / h)
    return img.resize((max(1, int(w * scale)), max(1, int(h * scale))),
                      Image.LANCZOS)


def save_jpeg(img, path, gray, box_w, box_h):
    img = fit(img, box_w, box_h)
    if gray:
        img = img.convert("L")
    else:
        img = img.convert("RGB")
        if SATURATE != 100:
            img = ImageEnhance.Color(img).enhance(SATURATE / 100)
    img.save(path, "JPEG", quality=QUALITY, optimize=True, progressive=False)
    return img.size


def is_monochrome(images):
    """Measure colour instead of assuming it. A black-and-white manga genuinely
    gains from greyscale — one channel instead of three, nothing lost."""
    sample = images[len(images) // 4:][:5] or images[:5]
    for im in sample:
        rgb = im.convert("RGB").resize((60, 60))
        px = rgb.load()
        for y in range(60):
            for x in range(60):
                r, g, b = px[x, y]
                if max(r, g, b) - min(r, g, b) > 28:
                    return False
    return True


# --- PDF rendering ---------------------------------------------------------
def pdf_pages(path, box_w, box_h):
    """Yield one PIL image per PDF page, by whichever backend is available."""
    try:
        try:
            import pymupdf as fitz
        except ImportError:
            import fitz  # older PyMuPDF
        doc = fitz.open(path)
        for page in doc:
            rect = page.rect
            zoom = min(box_w / rect.width, box_h / rect.height) if rect.width else 1
            zoom = max(zoom, 0.1)
            pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
            yield Image.open(io.BytesIO(pix.tobytes("png")))
        return
    except ImportError:
        pass
    try:
        import pypdfium2 as pdfium
        doc = pdfium.PdfDocument(path)
        for i in range(len(doc)):
            page = doc[i]
            w, h = page.get_size()
            scale = min(box_w / w, box_h / h) if w else 1
            yield page.render(scale=max(scale, 0.1)).to_pil()
        return
    except ImportError:
        pass
    # Last resort: pull the embedded page images out. Works for scans, which
    # carry exactly one full-page image per page.
    try:
        from pypdf import PdfReader
    except ImportError:
        sys.exit("Install one of: pymupdf, pypdfium2, or pypdf")
    reader = PdfReader(path)
    for page in reader.pages:
        got = None
        for img in page.images:
            try:
                candidate = Image.open(io.BytesIO(img.data))
            except Exception:
                continue
            if got is None or candidate.size[0] * candidate.size[1] > got.size[0] * got.size[1]:
                got = candidate
        if got is not None:
            yield got


# --- EPUB inspection -------------------------------------------------------
def epub_parts(path):
    z = zipfile.ZipFile(path)
    names = z.namelist()
    imgs = [n for n in names if re.search(r"\.(jpe?g|png|gif)$", n, re.I)]
    docs = [n for n in names if re.search(r"\.x?html?$", n, re.I)]
    return z, names, imgs, docs


def classify(path):
    """text | page-image | reflowable — decides the whole treatment.

    Confusing these breaks books. A novel re-encoded as images loses its text,
    search, dictionary and font size, and gets fifty times heavier. A reflowable
    EPUB rebuilt page-by-page loses every image but the first of each document.
    """
    if path.lower().endswith(".pdf"):
        return "page-image"
    try:
        z, names, imgs, docs = epub_parts(path)
    except Exception:
        return "text"
    size = os.path.getsize(path)
    img_bytes = sum(z.getinfo(n).file_size for n in imgs)
    if not imgs or not docs or img_bytes / max(size, 1) < 0.5:
        return "text"
    return "page-image" if 0.8 <= len(docs) / len(imgs) <= 1.6 else "reflowable"


def spine_images(path):
    """Images in reading order, one per spine document."""
    z, names, _, _ = epub_parts(path)
    opf = next((n for n in names if n.endswith(".opf")), None)
    if not opf:
        return z, []
    base = os.path.dirname(opf)
    xml = z.read(opf).decode("utf8", "ignore")
    hrefs = {}
    for item in re.findall(r"<item\b[^>]*>", xml):
        i = re.search(r'id="([^"]+)"', item)
        h = re.search(r'href="([^"]+)"', item)
        if i and h:
            hrefs[i.group(1)] = h.group(1)
    out = []
    for idref in re.findall(r'<itemref[^>]*idref="([^"]+)"', xml):
        page = hrefs.get(idref, "")
        if not page.endswith((".xhtml", ".html", ".htm")):
            continue
        full = os.path.normpath(os.path.join(base, page))
        try:
            html = z.read(full).decode("utf8", "ignore")
        except KeyError:
            continue
        m = re.search(r'<(?:img|image)[^>]*(?:src|xlink:href)="([^"]+)"', html)
        if m:
            src = m.group(1).split("#")[0]
            out.append(os.path.normpath(os.path.join(os.path.dirname(full), src)))
    return z, out


# --- EPUB writing ----------------------------------------------------------
CSS = ("body, div, img, svg { margin:0; padding:0; border-width:0; }\n"
       "body { background-color:#ffffff; text-align:center; }\n")

# The image is carried by an SVG with a viewBox, so the reader fits it to the
# page whatever its size. This is the comic-book EPUB technique, and the only
# layout verified to display correctly end to end.
PAGE = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
\t<head>
\t\t<meta charset="utf-8"/>
\t\t<meta content="width={w},height={h}" name="viewport"/>
\t\t<title>{title} - {n}</title>
\t\t<link href="css/style.css" rel="stylesheet" type="text/css"/>
\t</head>
\t<body>
\t\t<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
\t\t     version="1.1" width="100%" height="100%" viewBox="0 0 {w} {h}"
\t\t     preserveAspectRatio="xMidYMid meet">
\t\t\t<image width="{w}" height="{h}" xlink:href="image/{img}"/>
\t\t</svg>
\t</body>
</html>
"""


def write_epub(images, out_path, meta, gray, box_w, box_h):
    tmp = tempfile.mkdtemp()
    root = os.path.join(tmp, "epub")
    img_dir = os.path.join(root, "OEBPS", "image")
    os.makedirs(img_dir)
    os.makedirs(os.path.join(root, "OEBPS", "css"))
    os.makedirs(os.path.join(root, "META-INF"))
    open(os.path.join(root, "OEBPS", "css", "style.css"), "w").write(CSS)

    dims = []
    for i, im in enumerate(images, 1):
        name = f"page{i:03d}.jpg"
        dims.append(save_jpeg(im, os.path.join(img_dir, name), gray, box_w, box_h))
    if not dims:
        raise RuntimeError("no pages produced")

    for i, (w, h) in enumerate(dims, 1):
        open(os.path.join(root, "OEBPS", f"page{i:03d}.xhtml"), "w").write(
            PAGE.format(w=w, h=h, img=f"page{i:03d}.jpg", n=i,
                        title=escape(meta["title"])))

    uid = f"urn:uuid:{uuid.uuid4()}"
    items, spine = [], []
    for i in range(1, len(dims) + 1):
        cover = ' properties="cover-image"' if i == 1 else ''
        items.append(f'    <item href="page{i:03d}.xhtml" id="x{i:03d}" media-type="application/xhtml+xml"/>')
        items.append(f'    <item href="image/page{i:03d}.jpg" id="i{i:03d}" media-type="image/jpeg"{cover}/>')
        spine.append(f'    <itemref idref="x{i:03d}"/>')
    creators = "".join(f'\n    <dc:creator>{escape(a)}</dc:creator>'
                       for a in meta.get("authors", []))
    orient = "landscape" if dims[0][0] > dims[0][1] else "portrait"
    nl = chr(10)
    open(os.path.join(root, "OEBPS", "content.opf"), "w").write(f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" xmlns:dc="http://purl.org/dc/elements/1.1/" unique-identifier="bookid" version="3.0">
  <metadata>
    <dc:title>{escape(meta['title'])}</dc:title>{creators}
    <dc:publisher>{escape(meta.get('publisher', ''))}</dc:publisher>
    <dc:language>{meta.get('language', 'fr')}</dc:language>
    <dc:identifier id="bookid">{uid}</dc:identifier>
    <meta property="dcterms:modified">2026-01-01T00:00:00Z</meta>
    <meta property="rendition:layout">pre-paginated</meta>
    <meta property="rendition:orientation">{orient}</meta>
    <meta property="rendition:spread">none</meta>
    <meta name="cover" content="i001"/>
  </metadata>
  <manifest>
    <item href="nav.xhtml" id="nav" media-type="application/xhtml+xml" properties="nav"/>
    <item href="toc.ncx" id="ncx" media-type="application/x-dtbncx+xml"/>
    <item href="css/style.css" id="css" media-type="text/css"/>
{nl.join(items)}
  </manifest>
  <spine toc="ncx">
{nl.join(spine)}
  </spine>
</package>
""")
    t = escape(meta["title"])
    open(os.path.join(root, "OEBPS", "nav.xhtml"), "w").write(
        '<?xml version="1.0" encoding="utf-8"?>\n<html xmlns="http://www.w3.org/1999/xhtml" '
        'xmlns:epub="http://www.idpf.org/2007/ops"><head><meta charset="utf-8"/>'
        f'<title>{t}</title></head><body><nav epub:type="toc" id="toc"><ol>'
        f'<li><a href="page001.xhtml">{t}</a></li></ol></nav></body></html>')
    open(os.path.join(root, "OEBPS", "toc.ncx"), "w").write(
        f'<?xml version="1.0" encoding="utf-8"?>\n<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" '
        f'version="2005-1"><head><meta name="dtb:uid" content="{uid}"/></head>'
        f'<docTitle><text>{t}</text></docTitle><navMap><navPoint id="n1" playOrder="1">'
        f'<navLabel><text>{t}</text></navLabel><content src="page001.xhtml"/>'
        f'</navPoint></navMap></ncx>')
    open(os.path.join(root, "META-INF", "container.xml"), "w").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<container version="1.0" '
        'xmlns="urn:oasis:names:tc:opendocument:xmlns:container">\n  <rootfiles>\n'
        '    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>\n'
        '  </rootfiles>\n</container>\n')

    # mimetype MUST be the first entry and stored uncompressed, or readers
    # reject the file.
    with zipfile.ZipFile(out_path, "w") as z:
        z.writestr(zipfile.ZipInfo("mimetype"), "application/epub+zip",
                   compress_type=zipfile.ZIP_STORED)
        for base, _, files in os.walk(root):
            for f in sorted(files):
                full = os.path.join(base, f)
                rel = os.path.relpath(full, root)
                if rel != "mimetype":
                    z.write(full, rel, compress_type=zipfile.ZIP_DEFLATED)
    shutil.rmtree(tmp, ignore_errors=True)
    return len(dims), dims[0]


def shrink_reflowable(src, dst, box_w, box_h):
    """Keep the book's structure, only shrink oversized images."""
    tmp = tempfile.mkdtemp()
    work = os.path.join(tmp, "w")
    with zipfile.ZipFile(src) as z:
        z.extractall(work)
    touched = 0
    for base, _, files in os.walk(work):
        for f in files:
            if not f.lower().endswith((".jpg", ".jpeg", ".png")):
                continue
            full = os.path.join(base, f)
            try:
                im = Image.open(full)
            except Exception:
                continue
            if im.size[0] <= box_w and im.size[1] <= box_h:
                continue
            fit(im, box_w, box_h).convert("RGB").save(
                full if f.lower().endswith((".jpg", ".jpeg")) else full,
                "JPEG" if f.lower().endswith((".jpg", ".jpeg")) else "PNG",
                quality=QUALITY, optimize=True)
            touched += 1
    if not touched:                     # nothing to gain: copy it verbatim
        shutil.rmtree(tmp, ignore_errors=True)
        shutil.copy2(src, dst)
        return 0
    with zipfile.ZipFile(dst, "w") as z:
        if os.path.exists(os.path.join(work, "mimetype")):
            z.writestr(zipfile.ZipInfo("mimetype"), "application/epub+zip",
                       compress_type=zipfile.ZIP_STORED)
        for base, _, files in os.walk(work):
            for f in sorted(files):
                full = os.path.join(base, f)
                rel = os.path.relpath(full, work)
                if rel != "mimetype":
                    z.write(full, rel, compress_type=zipfile.ZIP_DEFLATED)
    shutil.rmtree(tmp, ignore_errors=True)
    return touched


def clean_title(path):
    """Best-effort title from the filename.

    Anna's Archive names carry the title before the first ' -- '. Edition
    markers and ALL-CAPS titles are tidied. Always overridable with --title:
    a filename is a guess, a title given by the caller is not.
    """
    name = os.path.splitext(os.path.basename(path))[0]
    name = unicodedata.normalize("NFC", name)
    name = re.split(r"\s+--\s+", name)[0].strip()
    name = re.sub(r"\s*\((?:French|English)[^)]*\)", "", name, flags=re.I)
    name = re.sub(r"\s*\(LES LUTINS\)|\s*\(A_M_[^)]*\)", "", name, flags=re.I)
    name = re.sub(r"\s{2,}", " ", name).strip(" -_")
    if name and name == name.upper():
        name = name.title()
    return name or os.path.splitext(os.path.basename(path))[0]


def process(path, device, outdir, gray_mode, title=None, authors=None,
            publisher=""):
    prof = DEVICES[device]
    box_w, box_h = prof["width"], prof["height"]
    kind = classify(path)
    title = title or clean_title(path)
    dst = os.path.join(outdir, f"{title}.epub")
    before = os.path.getsize(path) / 1e6

    if kind == "text":
        shutil.copy2(path, dst)
        log(f"  TEXTE      {title[:44]:46s} {before:6.1f} Mo  copie a l'identique")
        return dst

    if kind == "reflowable":
        n = shrink_reflowable(path, dst, box_w, box_h)
        after = os.path.getsize(dst) / 1e6
        how = f"{n} images allegees" if n else "aucune image trop grande, copie"
        log(f"  REFLOW     {title[:44]:46s} {before:6.1f} -> {after:5.1f} Mo  {how}")
        return dst

    if path.lower().endswith(".pdf"):
        images = list(pdf_pages(path, box_w, box_h))
    else:
        z, srcs = spine_images(path)
        images = []
        for s in srcs:
            try:
                images.append(Image.open(io.BytesIO(z.read(s))))
            except Exception:
                continue
    if not images:
        log(f"  ECHEC      {title[:44]} : aucune page lisible")
        return None

    gray = (gray_mode == "yes") or (
        gray_mode == "auto" and (not prof["colour"] or is_monochrome(images)))
    n, (w, h) = write_epub(images, dst, {
        "title": title, "authors": authors or [], "publisher": publisher},
        gray, box_w, box_h)
    after = os.path.getsize(dst) / 1e6
    log(f"  OK         {title[:44]:46s} {before:6.1f} -> {after:5.1f} Mo  "
        f"{n} p  {w}x{h}  {'gris' if gray else 'couleur'}")
    return dst


def main():
    global QUALITY, SATURATE
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", nargs="*")
    ap.add_argument("--device", default="era-color")
    ap.add_argument("--out", default="reencoded")
    ap.add_argument("--gray", choices=["auto", "yes", "no"], default="auto")
    ap.add_argument("--quality", type=int, default=QUALITY)
    ap.add_argument("--saturate", type=int, default=SATURATE,
                    help="e.g. 125 to lift a pale Kaleido palette")
    ap.add_argument("--width", type=int, help="override the profile's width")
    ap.add_argument("--height", type=int, help="override the profile's height")
    ap.add_argument("--title", help="override the title (single input only)")
    ap.add_argument("--author", action="append", default=[],
                    help="author; repeat for several")
    ap.add_argument("--publisher", default="")
    ap.add_argument("--list-devices", action="store_true")
    a = ap.parse_args()

    if a.list_devices:
        for k, v in DEVICES.items():
            print(f"  {k:18s} {v['width']}x{v['height']}  {v['label']}")
        return
    if a.device not in DEVICES:
        sys.exit(f"unknown device '{a.device}'. Run --list-devices.")

    QUALITY, SATURATE = a.quality, a.saturate
    if a.width:
        DEVICES[a.device]["width"] = a.width
    if a.height:
        DEVICES[a.device]["height"] = a.height

    os.makedirs(a.out, exist_ok=True)
    prof = DEVICES[a.device]
    log(f"Cible : {prof['label']} — {prof['width']}x{prof['height']}\n")
    done = 0
    for p in a.inputs:
        if not os.path.isfile(p):
            log(f"  INTROUVABLE {p}")
            continue
        try:
            one = len(a.inputs) == 1
            if process(p, a.device, a.out, a.gray,
                       title=a.title if one else None,
                       authors=a.author, publisher=a.publisher):
                done += 1
        except Exception as e:
            log(f"  ECHEC      {os.path.basename(p)[:44]} : {str(e)[:90]}")
    log(f"\n{done} livre(s) ecrit(s) dans {a.out}/")


if __name__ == "__main__":
    main()
