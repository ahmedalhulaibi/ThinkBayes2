#!/usr/bin/env python3
"""Build a reflowable EPUB from the Think Bayes 2 chapter notebooks."""

from __future__ import annotations

import argparse
from hashlib import sha256
import html
from io import BytesIO
import json
import re
import uuid
import zipfile
from datetime import date
from pathlib import Path

import markdown
from matplotlib.mathtext import math_to_image


ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = [f"chap{i:02}" for i in range(1, 19)] + ["chap19_v3", "chap20"]


MATH_DELIMITERS = re.compile(
    r"(?P<display>\$\$(?P<display_dollar>.+?)\$\$|\\\[(?P<display_bracket>.+?)\\\])"
    r"|(?P<inline>(?<![\\$])\$(?!\$)(?P<inline_dollar>[^$\n]+?)(?<![\\$])\$"
    r"|\\\((?P<inline_paren>.+?)\\\))",
    re.DOTALL,
)
CODE_FENCES = re.compile(r"(```[\s\S]*?```|~~~[\s\S]*?~~~)")


def render_math(text: str, assets: dict[str, bytes], markup: dict[str, str]) -> str:
    def render_segment(segment: str) -> str:
        def replace(match: re.Match[str]) -> str:
            display = bool(match.group("display"))
            expression = next(
                match.group(name)
                for name in ("display_dollar", "display_bracket", "inline_dollar", "inline_paren")
                if match.group(name) is not None
            ).strip()
            if (
                match.group("display_bracket") is not None
                and len(expression.split()) > 1
                and not re.search(r"\\[A-Za-z]+|[=+*/^_<>]", expression)
            ):
                return match.group(0)
            image_name = sha256(expression.encode("utf-8")).hexdigest() + ".png"
            if image_name not in assets:
                image = BytesIO()
                math_to_image(f"${expression}$", image, dpi=180, format="png", color="#000000")
                assets[image_name] = image.getvalue()

            marker = f"EQUATIONTOKEN{image_name[:-4]}{'D' if display else 'I'}TOKEN"
            markup[marker] = (
                f'<img class="math-{"display" if display else "inline"}" '
                f'src="images/{image_name}" alt="{html.escape(expression, quote=True)}" />'
            )
            return marker

        return MATH_DELIMITERS.sub(replace, segment)

    segments = CODE_FENCES.split(text)
    return "".join(segment if index % 2 else render_segment(segment) for index, segment in enumerate(segments))


def notebook_markdown(path: Path, assets: dict[str, bytes], markup: dict[str, str]) -> str:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    parts = []
    for cell in notebook.get("cells", []):
        if cell.get("cell_type") not in {"markdown", "code"}:
            continue
        source = "".join(cell.get("source", []))
        if cell["cell_type"] == "code":
            if source.strip():
                parts.append(f"```python\n{source.rstrip()}\n```")
        elif source.strip():
            parts.append(render_math(source, assets, markup))
    return "\n\n".join(parts)


def xhtml(title: str, body: str) -> str:
    def replace_image(match: re.Match[str]) -> str:
        attributes = match.group(1).rstrip()
        if re.search(r'\bsrc=["\']images/', attributes, re.IGNORECASE):
            return f"<img{attributes if attributes.endswith('/') else attributes + ' /'}>"
        alt = re.search(r'\balt=["\']([^"\']*)["\']', attributes, re.IGNORECASE)
        return "[Image: " + html.unescape(alt.group(1) if alt else "illustration") + "]"

    body = re.sub(r"<img\b([^>]*)>", replace_image, body, flags=re.IGNORECASE)
    return (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<!DOCTYPE html>\n'
        '<html xmlns="http://www.w3.org/1999/xhtml" lang="en">\n'
        "<head><title>" + html.escape(title) + "</title>"
        '<link rel="stylesheet" type="text/css" href="style.css"/></head>\n'
        "<body>\n" + body + "\n</body></html>\n"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-o", "--output", type=Path, default=ROOT / "ThinkBayes2.epub")
    args = parser.parse_args()

    source = ROOT / "notebooks"
    chapters = [("preface", "Preface", (ROOT / "jb/preface.md").read_text(encoding="utf-8"))]
    math_assets: dict[str, bytes] = {}
    math_markup: dict[str, str] = {}
    chapters[0] = (chapters[0][0], chapters[0][1], render_math(chapters[0][2], math_assets, math_markup))
    for index, name in enumerate(CHAPTERS, start=1):
        path = source / f"{name}.ipynb"
        if not path.is_file():
            raise SystemExit(f"Missing chapter notebook: {path}")
        chapters.append(
            (
                name,
                f"Chapter {index}: {name.replace('_', ' ').title()}",
                notebook_markdown(path, math_assets, math_markup),
            )
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    book_id = f"urn:uuid:{uuid.uuid4()}"
    manifest = []
    spine = []
    nav = []
    rendered = []
    for href, title, text in chapters:
        content = markdown.markdown(text, extensions=["fenced_code", "tables", "sane_lists"])
        for marker, equation_markup in math_markup.items():
            content = content.replace(marker, equation_markup)
        rendered.append((href, xhtml(title, content)))
        manifest.append(f'<item id="{href}" href="{href}.xhtml" media-type="application/xhtml+xml"/>')
        spine.append(f'<itemref idref="{href}"/>')
        nav.append(f'<li><a href="{href}.xhtml">{html.escape(title)}</a></li>')

    opf = f'''<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="book-id" xml:lang="en">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:identifier id="book-id">{book_id}</dc:identifier><dc:title>Think Bayes</dc:title><dc:creator>Allen B. Downey</dc:creator><dc:language>en</dc:language><meta property="dcterms:modified">{date.today().isoformat()}T00:00:00Z</meta></metadata>
<manifest><item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/><item id="css" href="style.css" media-type="text/css"/>{''.join(manifest)}</manifest>
<spine>{''.join(spine)}</spine></package>'''
    navigation = xhtml("Contents", "<nav epub:type=\"toc\" xmlns:epub=\"http://www.idpf.org/2007/ops\"><h1>Contents</h1><ol>" + "".join(nav) + "</ol></nav>")
    math_manifest = []
    for index, image_name in enumerate(sorted(math_assets)):
        math_manifest.append(
            f'<item id="math{index}" href="images/{image_name}" media-type="image/png"/>'
        )
    opf = opf.replace("</manifest>", "".join(math_manifest) + "</manifest>")
    css = (
        "body{font-family:serif;line-height:1.45;margin:5%;}"
        "pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f2f2f2;padding:.6em;}"
        "code{font-family:monospace;}img{max-width:100%;height:auto;}"
        "img.math-inline{height:1.15em;vertical-align:-.25em;width:auto;}"
        "img.math-display{display:block;max-height:8em;margin:.8em auto;}"
        "h1,h2,h3{break-after:avoid;}"
    )

    with zipfile.ZipFile(args.output, "w") as epub:
        epub.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        epub.writestr("META-INF/container.xml", '<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="EPUB/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>')
        epub.writestr("EPUB/content.opf", opf)
        epub.writestr("EPUB/nav.xhtml", navigation)
        epub.writestr("EPUB/style.css", css)
        for image_name, image_data in math_assets.items():
            epub.writestr(f"EPUB/images/{image_name}", image_data)
        for name, document in rendered:
            epub.writestr(f"EPUB/{name}.xhtml", document)
    print(f"Wrote {args.output} ({args.output.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
