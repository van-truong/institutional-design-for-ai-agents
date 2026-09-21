#!/usr/bin/env python3
"""Extract a standalone SVG from an HTML figure and embed its stylesheet."""

from __future__ import annotations

import argparse
from pathlib import Path
import re


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()

    html = args.source.read_text(encoding="utf-8")
    style_match = re.search(r"<style[^>]*>(.*?)</style>", html, re.DOTALL | re.IGNORECASE)
    start_match = re.search(r"<svg\b[^>]*>", html, re.IGNORECASE)
    if not start_match:
        raise SystemExit(f"No <svg> found in {args.source}")
    end = html.find("</svg>", start_match.end())
    if end < 0:
        raise SystemExit(f"No closing </svg> found in {args.source}")

    opening = start_match.group(0)
    if "xmlns=" not in opening:
        opening = opening[:-1] + ' xmlns="http://www.w3.org/2000/svg">'
    stylesheet = style_match.group(1) if style_match else ""
    variables = dict(re.findall(r"--([\w-]+)\s*:\s*([^;}]+)", stylesheet))
    svg_body = html[start_match.end() : end + len("</svg>")]
    for name, value in variables.items():
        token = f"var(--{name})"
        stylesheet = stylesheet.replace(token, value.strip())
        svg_body = svg_body.replace(token, value.strip())
    embedded_style = ""
    if stylesheet:
        embedded_style = (
            '\n<defs><style type="text/css"><![CDATA[\n'
            "text { font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif; }\n"
            f"{stylesheet}\n]]></style></defs>"
        )
    args.destination.parent.mkdir(parents=True, exist_ok=True)
    args.destination.write_text(opening + embedded_style + svg_body + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
