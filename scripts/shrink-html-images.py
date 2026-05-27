#!/usr/bin/env python3
"""Extract embedded data:image URIs to assets/ and replace favicon base64 with icon.png."""
import hashlib
import base64
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")
HTML_FILES = [
    "index.html",
    "letters.html",
    "judgments.html",
    "templates.html",
    "widget.html",
]

MIME_EXT = {
    "png": "png",
    "jpeg": "jpg",
    "jpg": "jpg",
    "gif": "gif",
    "webp": "webp",
    "svg+xml": "svg",
}

FAVICON_APPLE = re.compile(
    r'<link\s+rel="apple-touch-icon"\s+href="data:image/[^"]+">',
    re.IGNORECASE,
)
FAVICON_ICON = re.compile(
    r'<link\s+rel="icon"\s+type="image/png"\s+href="data:image/[^"]+">',
    re.IGNORECASE,
)
DATA_URI = re.compile(r"data:image/([^;]+);base64,([A-Za-z0-9+/=]+)")
DEAD_WIDGET_CONST = re.compile(
    r"^const (?:QR_DATA_URI|INVOICE_URI|INVOICE_BARCODE_URI) = \"data:image[^\"]*\";\s*\n?",
    re.MULTILINE,
)


def save_data_uri(mime: str, b64: str) -> str:
    ext = MIME_EXT.get(mime.lower(), "bin")
    raw = base64.b64decode(b64)
    name = f"img-{hashlib.md5(raw).hexdigest()[:12]}.{ext}"
    path = os.path.join(ASSETS, name)
    rel = f"assets/{name}"
    if not os.path.exists(path):
        with open(path, "wb") as f:
            f.write(raw)
    return rel


def process_html(filename: str) -> tuple[int, int]:
    path = os.path.join(ROOT, filename)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    before = len(content.encode("utf-8"))

    if filename == "widget.html":
        content = DEAD_WIDGET_CONST.sub("", content)

    content = FAVICON_APPLE.sub('<link rel="apple-touch-icon" href="icon.png">', content)
    content = FAVICON_ICON.sub('<link rel="icon" type="image/png" href="icon.png">', content)

    seen: dict[str, str] = {}

    def repl(match: re.Match) -> str:
        full = match.group(0)
        if full in seen:
            return seen[full]
        rel = save_data_uri(match.group(1), match.group(2))
        seen[full] = rel
        return rel

    content = DATA_URI.sub(repl, content)

    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    after = len(content.encode("utf-8"))
    return before, after


def pct_smaller(before: int, after: int) -> str:
    if before <= 0:
        return "n/a"
    return f"{100 * (before - after) / before:.1f}% smaller"


def main() -> int:
    os.makedirs(ASSETS, exist_ok=True)
    total_before = total_after = 0
    for name in HTML_FILES:
        p = os.path.join(ROOT, name)
        if not os.path.exists(p):
            print(f"skip {name} (missing)")
            continue
        b, a = process_html(name)
        total_before += b
        total_after += a
        print(f"{name}: {b/1024:.1f} KB -> {a/1024:.1f} KB ({pct_smaller(b, a)})")
    asset_paths = [
        os.path.join(ASSETS, name)
        for name in os.listdir(ASSETS)
        if os.path.isfile(os.path.join(ASSETS, name))
    ]
    asset_kb = sum(os.path.getsize(p) for p in asset_paths) / 1024
    print(f"\nassets/: {len(asset_paths)} files, {asset_kb:.1f} KB total")
    print(
        f"HTML total: {total_before/1024:.1f} KB -> {total_after/1024:.1f} KB "
        f"({pct_smaller(total_before, total_after)})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
