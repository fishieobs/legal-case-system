"""
Generate the CLIENTS (客戶管理) app icon in the same series style:
deep-navy rounded background, cute kawaii animal + a representative object,
gold accents. Mascot: koala (warm / relationship) holding a contact card.
Matches generate_icons.py helpers & palette.
"""
from PIL import Image, ImageDraw
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "icons")
os.makedirs(OUT, exist_ok=True)

# ── Palette (shared series) ──
BG      = (5, 10, 24)
GOLD    = (200, 169, 110)
GOLD_DK = (140, 100, 50)
GOLD_LT = (230, 200, 140)
WHITE   = (255, 255, 255)
EYE_W   = (240, 240, 250)
EYE_D   = (30, 28, 45)
PINK_CH = (255, 180, 190)

def new_canvas(size=192):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    r = int(size * 0.175)
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=r, fill=BG)
    d.rounded_rectangle([1, 1, size - 2, size - 2], radius=r - 1, outline=(*GOLD, 30), width=1)
    return img, d

def circle(d, cx, cy, r, fill, outline=None, ow=1):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill, outline=outline, width=ow)

def eyes(d, cx, cy, size=192, gap=14, r=7, iris=(50, 90, 160)):
    er = r
    circle(d, cx - gap, cy, er + 1, EYE_W)
    circle(d, cx + gap, cy, er + 1, EYE_W)
    circle(d, cx - gap, cy, er, iris)
    circle(d, cx + gap, cy, er, iris)
    circle(d, cx - gap, cy, int(er * 0.55), EYE_D)
    circle(d, cx + gap, cy, int(er * 0.55), EYE_D)
    hr = max(1, int(er * 0.3)); ho = int(er * 0.25)
    circle(d, cx - gap - ho, cy - ho, hr, WHITE)
    circle(d, cx + gap - ho, cy - ho, hr, WHITE)

def blush(d, cx, cy, size=192):
    S = size / 192
    bw, bh, gap = int(13 * S), int(7 * S), int(28 * S)
    d.ellipse([cx - gap - bw, cy - bh, cx - gap + bw, cy + bh], fill=(*PINK_CH, 140))
    d.ellipse([cx + gap - bw, cy - bh, cx + gap + bw, cy + bh], fill=(*PINK_CH, 140))

def save_both(img, name):
    img.save(os.path.join(OUT, f"{name}.png"))
    img.resize((512, 512), Image.LANCZOS).save(os.path.join(OUT, f"{name}-512.png"))
    print(f"  ✓  {name}.png  +  {name}-512.png")


# ══════════════════════════════════════════════════════════════════════════
# CLIENTS — Koala with a contact card  (grey-blue fur, gold contact card)
# ══════════════════════════════════════════════════════════════════════════
def make_clients(size=192):
    img, d = new_canvas(size)
    S = size / 192
    cx, cy = size // 2, int(size * 0.38)

    KOALA    = (150, 161, 174)
    KOALA_DK = (104, 115, 130)
    KOALA_LT = (188, 197, 208)
    EAR_IN   = (206, 196, 200)
    NOSE_C   = (58, 54, 66)

    # ── Big fluffy ears (before face) ──
    for ex in [-1, 1]:
        ecx = cx + ex * int(33 * S)
        circle(d, ecx, cy - int(26 * S), int(20 * S), KOALA_DK)   # outer fluff
        circle(d, ecx, cy - int(26 * S), int(15 * S), KOALA)      # inner fur
        circle(d, ecx, cy - int(24 * S), int(8 * S), EAR_IN)      # inner ear
        # little fluff highlight
        circle(d, ecx - int(6 * S), cy - int(32 * S), int(3 * S), KOALA_LT)

    # ── Face ──
    circle(d, cx, cy, int(36 * S), KOALA)
    # cheek fluff highlights
    circle(d, cx - int(30 * S), cy + int(6 * S), int(9 * S), KOALA_LT)
    circle(d, cx + int(30 * S), cy + int(6 * S), int(9 * S), KOALA_LT)

    # ── Signature big koala nose (spoon-shaped) ──
    d.ellipse([cx - int(11 * S), cy + int(2 * S), cx + int(11 * S), cy + int(24 * S)], fill=NOSE_C)
    d.ellipse([cx - int(7 * S), cy + int(1 * S), cx + int(7 * S), cy + int(9 * S)], fill=NOSE_C)
    # nose highlight
    circle(d, cx - int(4 * S), cy + int(7 * S), int(2 * S), (*WHITE, 90))

    # ── Eyes & blush ──
    eyes(d, cx, cy - int(6 * S), size, gap=int(15 * S), r=int(6 * S), iris=(78, 100, 132))
    blush(d, cx, cy + int(6 * S), size)

    # ══ Contact card (bottom centre) ══
    rw, rh = int(66 * S), int(46 * S)
    rx, ry = cx - rw // 2, cy + int(44 * S)
    d.rounded_rectangle([rx, ry, rx + rw, ry + rh], radius=int(5 * S), fill=(246, 246, 250), outline=GOLD_DK, width=max(1, int(1 * S)))
    # gold top bar (like a profile header)
    d.rounded_rectangle([rx, ry, rx + rw, ry + int(11 * S)], radius=int(5 * S), fill=GOLD)
    d.rectangle([rx, ry + int(6 * S), rx + rw, ry + int(11 * S)], fill=GOLD)

    # person avatar (left)
    ax, ay = rx + int(16 * S), ry + int(28 * S)
    circle(d, ax, ay - int(4 * S), int(6 * S), GOLD)                 # head
    d.ellipse([ax - int(9 * S), ay + int(2 * S), ax + int(9 * S), ay + int(16 * S)], fill=GOLD)  # shoulders
    # mask lower corners so shoulders read as a bust
    d.rectangle([ax - int(9 * S), ay + int(9 * S), ax + int(9 * S), ay + int(16 * S)], fill=(246, 246, 250))
    d.ellipse([ax - int(9 * S), ay + int(2 * S), ax + int(9 * S), ay + int(12 * S)], fill=GOLD)

    # info lines (right of avatar)
    lx = rx + int(30 * S)
    for i in range(3):
        ly = ry + int(20 * S) + i * int(8 * S)
        w = rw - int(38 * S) if i < 2 else int((rw - int(38 * S)) * 0.6)
        col = GOLD_DK if i == 0 else (170, 176, 190)
        d.line([lx, ly, lx + w, ly], fill=col, width=max(1, int(2 * S) if i == 0 else int(1 * S)))

    # small gold star (client care accent)
    sx, sy = rx + rw - int(6 * S), ry - int(7 * S)
    for a in (0, 90):
        if a == 0:
            d.line([sx - int(6 * S), sy, sx + int(6 * S), sy], fill=GOLD_LT, width=max(1, int(2 * S)))
        else:
            d.line([sx, sy - int(6 * S), sx, sy + int(6 * S)], fill=GOLD_LT, width=max(1, int(2 * S)))
    circle(d, sx, sy, int(2 * S), GOLD_LT)

    save_both(img, "icon-clients")


if __name__ == "__main__":
    print("Generating clients icon...")
    make_clients()
    print("Done!")
