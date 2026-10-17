#!/usr/bin/env python3
"""Build a reflowable EPUB from the Think Bayes 2 chapter notebooks."""

from __future__ import annotations

import argparse
import html
import json
import re
import uuid
import zipfile
from datetime import date
from pathlib import Path

import markdown


ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = [f"chap{i:02}" for i in range(1, 19)] + ["chap19_v3", "chap20"]


def notebook_markdown(path: Path) -> str:
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
            parts.append(source)
    return "\n\n".join(parts)


def xhtml(title: str, body: str) -> str:
    body = re.sub(
        r"<img\b([^>]*)>",
        lambda match: "[Image: "
        + html.unescape((re.search(r'\balt=[\"\']([^\"\']*)[\"\']', match[1]) or [None, "illustration"])[1])
        + "]",
        body,
        flags=re.IGNORECASE,
    )
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
    for index, name in enumerate(CHAPTERS, start=1):
        path = source / f"{name}.ipynb"
        if not path.is_file():
            raise SystemExit(f"Missing chapter notebook: {path}")
        chapters.append((name, f"Chapter {index}: {name.replace('_', ' ').title()}", notebook_markdown(path)))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    book_id = f"urn:uuid:{uuid.uuid4()}"
    manifest = []
    spine = []
    nav = []
    rendered = []
    for href, title, text in chapters:
        content = markdown.markdown(text, extensions=["fenced_code", "tables", "sane_lists"])
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
    css = "body{font-family:serif;line-height:1.45;margin:5%;}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f2f2f2;padding:.6em;}code{font-family:monospace;}img{max-width:100%;height:auto;}h1,h2,h3{break-after:avoid;}"

    with zipfile.ZipFile(args.output, "w") as epub:
        epub.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        epub.writestr("META-INF/container.xml", '<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="EPUB/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>')
        epub.writestr("EPUB/content.opf", opf)
        epub.writestr("EPUB/nav.xhtml", navigation)
        epub.writestr("EPUB/style.css", css)
        for name, document in rendered:
            epub.writestr(f"EPUB/{name}.xhtml", document)
    print(f"Wrote {args.output} ({args.output.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
