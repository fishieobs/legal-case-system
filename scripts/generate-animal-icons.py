#!/usr/bin/env python3
"""Generate cute animal-style PWA icons for each subsystem."""
from __future__ import annotations

import os
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICONS_DIR = os.path.join(ROOT, "icons")
SIZE = 192

BG = "#0a1628"
BG2 = "#142238"
GOLD = "#c8a96e"
WHITE = "#f8fafc"
PINK = "#f9a8d4"
DARK = "#1e293b"


def rounded_square(draw: ImageDraw.ImageDraw, r: int = 28) -> None:
    draw.rounded_rectangle([8, 8, SIZE - 8, SIZE - 8], radius=r, fill=BG2, outline=GOLD, width=3)


def eye(draw: ImageDraw.ImageDraw, x: int, y: int, w: int = 22, h: int = 26) -> None:
    draw.ellipse([x, y, x + w, y + h], fill=WHITE)
    draw.ellipse([x + 5, y + 6, x + w - 2, y + h - 4], fill=DARK)
    draw.ellipse([x + 8, y + 8, x + 12, y + 12], fill=WHITE)


def blush(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    draw.ellipse([x, y, x + 18, y + 10], fill=PINK)


def draw_owl(img: Image.Image) -> None:
    d = ImageDraw.Draw(img)
    rounded_square(d)
    # ears / tufts
    d.polygon([(70, 42), (82, 18), (94, 42)], fill=GOLD)
    d.polygon([(98, 42), (110, 18), (122, 42)], fill=GOLD)
    # body
    d.ellipse([48, 52, 144, 148], fill="#a67c52")
    d.ellipse([56, 60, 136, 140], fill="#c49a6c")
    # belly
    d.ellipse([72, 88, 120, 132], fill="#f5e6d3")
    d.ellipse([58, 68, 134, 128], fill="#f5e6d3")
    eye(d, 78, 82, 20, 24)
    eye(d, 104, 82, 20, 24)
    blush(d, 62, 108)
    blush(d, 118, 108)
    # beak
    d.polygon([(92, 108), (100, 118), (84, 118)], fill=GOLD)
    # scales hint
    d.line([(96, 138), (96, 158)], fill=GOLD, width=3)
    d.arc([78, 148, 114, 168], 20, 160, fill=GOLD, width=3)


def draw_bunny(img: Image.Image) -> None:
    d = ImageDraw.Draw(img)
    rounded_square(d)
    # ears
    d.ellipse([58, 22, 78, 72], fill="#f8bbd0", outline="#f472b6", width=2)
    d.ellipse([114, 22, 134, 72], fill="#f8bbd0", outline="#f472b6", width=2)
    d.ellipse([64, 32, 72, 58], fill=PINK)
    d.ellipse([120, 32, 128, 58], fill=PINK)
    # head
    d.ellipse([52, 58, 140, 146], fill="#fff5f7")
    eye(d, 76, 88, 18, 22)
    eye(d, 106, 88, 18, 22)
    blush(d, 64, 112)
    blush(d, 118, 112)
    # nose
    d.ellipse([92, 108, 100, 116], fill=PINK)
    # envelope
    d.rounded_rectangle([64, 132, 128, 168], radius=6, fill=WHITE, outline=GOLD, width=2)
    d.polygon([(64, 132), (96, 152), (128, 132)], fill=GOLD)


def draw_fox(img: Image.Image) -> None:
    d = ImageDraw.Draw(img)
    rounded_square(d)
    # ears
    d.polygon([(62, 70), (50, 28), (78, 52)], fill="#ea580c")
    d.polygon([(130, 70), (142, 28), (114, 52)], fill="#ea580c")
    # head
    d.ellipse([52, 56, 140, 144], fill="#fb923c")
    d.ellipse([72, 100, 120, 148], fill=WHITE)
    eye(d, 76, 86, 18, 22)
    eye(d, 106, 86, 18, 22)
    blush(d, 64, 110)
    blush(d, 118, 110)
    d.ellipse([90, 112, 102, 120], fill=DARK)
    # book
    d.rounded_rectangle([58, 132, 134, 170], radius=5, fill="#3b82f6", outline=GOLD, width=2)
    d.line([(96, 132), (96, 170)], fill=GOLD, width=2)
    d.line([(70, 148), (122, 148)], fill=WHITE, width=2)


def draw_bear(img: Image.Image) -> None:
    d = ImageDraw.Draw(img)
    rounded_square(d)
    # ears
    d.ellipse([50, 48, 78, 76], fill="#92400e")
    d.ellipse([114, 48, 142, 76], fill="#92400e")
    d.ellipse([58, 56, 70, 68], fill="#d97706")
    d.ellipse([122, 56, 134, 68], fill="#d97706")
    # head
    d.ellipse([48, 62, 144, 148], fill="#b45309")
    d.ellipse([68, 92, 124, 128], fill="#fde68a")
    eye(d, 74, 84, 18, 22)
    eye(d, 104, 84, 18, 22)
    d.ellipse([88, 108, 104, 116], fill=DARK)
    blush(d, 62, 106)
    blush(d, 118, 106)
    # gavel
    d.rectangle([118, 128, 148, 138], fill=GOLD)
    d.rectangle([140, 118, 150, 148], fill="#78716c")
    d.ellipse([112, 132, 124, 144], fill="#57534e")


def draw_cat(img: Image.Image) -> None:
    d = ImageDraw.Draw(img)
    rounded_square(d)
    # ears
    d.polygon([(58, 78), (48, 38), (72, 58)], fill="#94a3b8")
    d.polygon([(134, 78), (144, 38), (120, 58)], fill="#94a3b8")
    # head
    d.ellipse([50, 58, 142, 142], fill="#cbd5e1")
    d.ellipse([68, 88, 124, 132], fill=WHITE)
    eye(d, 74, 84, 18, 22)
    eye(d, 104, 84, 18, 22)
    blush(d, 62, 108)
    blush(d, 118, 108)
    d.ellipse([88, 112, 104, 118], fill=PINK)
    d.line([(88, 118), (82, 122)], fill=PINK, width=2)
    d.line([(104, 118), (110, 122)], fill=PINK, width=2)
    # calendar
    d.rounded_rectangle([54, 132, 138, 174], radius=6, fill=WHITE, outline=GOLD, width=2)
    d.rectangle([54, 132, 138, 146], fill=GOLD)
    d.ellipse([72, 154, 82, 164], fill="#ef4444")
    d.ellipse([96, 154, 106, 164], fill="#22c55e")
    d.ellipse([120, 154, 130, 164], fill="#3b82f6")


ICON_DRAWERS = {
    "icon-cases.png": draw_owl,       # 案件管理 — 貓頭鷹（睿智）
    "icon-letters.png": draw_bunny,   # 信函 — 兔子
    "icon-templates.png": draw_fox,   # 文書範本 — 狐狸
    "icon-judgments.png": draw_bear,  # 判決書 — 小熊
    "icon-widget.png": draw_cat,      # 庭期 — 小貓
}


def save_icon(filename: str, drawer) -> str:
    img = Image.new("RGBA", (SIZE, SIZE), BG)
    drawer(img)
    path = os.path.join(ICONS_DIR, filename)
    img.save(path, "PNG", optimize=True)
    # 512px for manifest / high-DPI
    large = img.resize((512, 512), Image.Resampling.LANCZOS)
    large_path = path.replace(".png", "-512.png")
    large.save(large_path, "PNG", optimize=True)
    return path


def main() -> None:
    os.makedirs(ICONS_DIR, exist_ok=True)
    for name, drawer in ICON_DRAWERS.items():
        p = save_icon(name, drawer)
        kb = os.path.getsize(p) / 1024
        print(f"  {name}: {kb:.1f} KB")
    print(f"\nSaved to {ICONS_DIR}/")


if __name__ == "__main__":
    main()
