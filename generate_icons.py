"""
Generate animal-court-style app icons for the legal case system.
Matching existing style: dark navy bg, cute pixel-art animals, gold accents.
"""
from PIL import Image, ImageDraw, ImageFilter
import math, os

OUT = os.path.join(os.path.dirname(__file__), "icons")
os.makedirs(OUT, exist_ok=True)

# ── Palette ────────────────────────────────────────────────────────────────
BG       = (5,  10,  24)        # deep navy background
BG_GRAD  = (10, 22,  48)        # slightly lighter for gradient feel
GOLD     = (200,169,110)
GOLD_DK  = (140,100, 50)
GOLD_LT  = (230,200,140)
WHITE    = (255,255,255)
BLACK    = ( 20, 20, 30)
PINK_CH  = (255,180,190)        # cheek blush
EYE_W    = (240,240,250)
EYE_D    = ( 30, 28, 45)        # pupil

# ── Helpers ────────────────────────────────────────────────────────────────
def new_canvas(size=192):
    img = Image.new("RGBA", (size, size), (0,0,0,0))
    d = ImageDraw.Draw(img)
    r = int(size * 0.175)         # corner radius ≈ 17 % of size
    d.rounded_rectangle([0,0,size-1,size-1], radius=r, fill=BG)
    # subtle inner glow ring
    d.rounded_rectangle([1,1,size-2,size-2], radius=r-1, outline=(*GOLD,30), width=1)
    return img, d

def circle(d, cx, cy, r, fill, outline=None, ow=1):
    d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=fill, outline=outline, width=ow)

def eyes(d, cx, cy, size=192, gap=None, r=None, iris=None):
    """Draw two cute eyes centered at (cx,cy)."""
    S = size / 192
    er  = r    or int(7*S)
    gap = gap  or int(14*S)
    iris_c = iris or (50, 90, 160)
    # whites
    circle(d, cx-gap, cy, er+1, EYE_W)
    circle(d, cx+gap, cy, er+1, EYE_W)
    # iris
    circle(d, cx-gap, cy, er,   iris_c)
    circle(d, cx+gap, cy, er,   iris_c)
    # pupil
    circle(d, cx-gap, cy, int(er*0.55), EYE_D)
    circle(d, cx+gap, cy, int(er*0.55), EYE_D)
    # highlight
    hr = max(1, int(er*0.3))
    hl_off = int(er*0.25)
    circle(d, cx-gap-hl_off, cy-hl_off, hr, WHITE)
    circle(d, cx+gap-hl_off, cy-hl_off, hr, WHITE)

def blush(d, cx, cy, size=192):
    S = size/192
    bw, bh = int(13*S), int(7*S)
    gap = int(28*S)
    d.ellipse([cx-gap-bw, cy-bh, cx-gap+bw, cy+bh], fill=(*PINK_CH, 140))
    d.ellipse([cx+gap-bw, cy-bh, cx+gap+bw, cy+bh], fill=(*PINK_CH, 140))

def nose(d, cx, cy, size=192, color=(80,40,40)):
    S = size/192
    nr, nl = int(5*S), int(4*S)
    d.ellipse([cx-nr, cy-nl, cx+nr, cy+nl], fill=color)

def mouth(d, cx, cy, size=192, color=(80,40,40)):
    S = size/192
    mw, mh = int(8*S), int(4*S)
    d.arc([cx-mw, cy, cx+mw, cy+mh*2], 0, 180, fill=color, width=max(1,int(2*S)))

def save_both(img, name):
    """Save 192 and 512 versions."""
    path192 = os.path.join(OUT, f"{name}.png")
    img.save(path192)
    img512 = img.resize((512,512), Image.LANCZOS)
    path512 = os.path.join(OUT, f"{name}-512.png")
    img512.save(path512)
    print(f"  ✓  {name}.png  +  {name}-512.png")


# ══════════════════════════════════════════════════════════════════════════
# 1.  DEADLINE  —  Tortoise with hourglass  (deep green shell, gold timer)
# ══════════════════════════════════════════════════════════════════════════
def make_deadline(size=192):
    img, d = new_canvas(size)
    S = size/192
    cx, cy = size//2, int(size*0.42)

    SHELL    = ( 30,  100,  58)
    SHELL_DK = ( 18,   65,  36)
    SHELL_LT = ( 60,  130,  80)
    SKIN     = ( 95,  165, 100)
    SKIN_DK  = ( 60,  115,  68)

    # ── Shell (dome behind head) ──
    sw, sh = int(54*S), int(38*S)
    # main dome
    d.ellipse([cx-sw, cy-int(10*S), cx+sw, cy+sh], fill=SHELL)
    # hex pattern on dome
    for dx, dy in [(-20, 5),(0,-4),(20, 5),(-10,18),(10,18)]:
        hx2, hy2 = cx+int(dx*S), cy+int(dy*S)
        hr = int(10*S)
        d.regular_polygon((hx2, hy2, hr), 6, rotation=30, fill=SHELL_DK)
    # shell highlight rim
    d.arc([cx-sw+int(4*S), cy-int(10*S), cx+sw-int(4*S), cy+int(20*S)],
          200, 340, fill=SHELL_LT, width=max(1,int(2*S)))

    # ── Head (bigger, front and center) ──
    hr2 = int(34*S)
    circle(d, cx, cy-int(22*S), hr2, SKIN)

    # ── Feet ──
    fr = int(13*S)
    circle(d, cx-int(50*S), cy+int(20*S), fr, SKIN_DK)
    circle(d, cx+int(50*S), cy+int(20*S), fr, SKIN_DK)
    circle(d, cx-int(32*S), cy+int(40*S), int(10*S), SKIN_DK)
    circle(d, cx+int(32*S), cy+int(40*S), int(10*S), SKIN_DK)

    # ── Face ──
    eyes(d, cx, cy-int(26*S), size, gap=int(13*S), r=int(7*S), iris=(40,120,60))
    nose(d, cx, cy-int(16*S), size, color=SKIN_DK)
    blush(d, cx, cy-int(20*S), size)
    mouth(d, cx, cy-int(14*S), size, color=SKIN_DK)

    # ── Hourglass (centred, bottom) ──
    hx, hy = cx, cy+int(60*S)
    hw, hh = int(14*S), int(18*S)
    # frame bars
    d.rounded_rectangle([hx-hw-int(2*S), hy-hh-int(3*S),
                          hx+hw+int(2*S), hy-hh+int(3*S)], radius=int(2*S), fill=GOLD_LT)
    d.rounded_rectangle([hx-hw-int(2*S), hy+hh-int(3*S),
                          hx+hw+int(2*S), hy+hh+int(3*S)], radius=int(2*S), fill=GOLD_LT)
    # sand top triangle
    d.polygon([hx-hw, hy-hh+int(3*S), hx+hw, hy-hh+int(3*S), hx, hy-int(2*S)], fill=GOLD)
    # sand bottom triangle (mostly empty — time running out)
    d.polygon([hx-int(5*S), hy+int(2*S), hx+int(5*S), hy+int(2*S),
               hx, hy+hh-int(3*S)], fill=GOLD)
    # falling sand dot
    for i in range(3):
        circle(d, hx, hy-int(2*S)+i*int(4*S), int(1*S), GOLD_LT)

    save_both(img, "icon-deadline")


# ══════════════════════════════════════════════════════════════════════════
# 2.  CHECKLIST  —  Beaver with clipboard
# ══════════════════════════════════════════════════════════════════════════
def make_checklist(size=192):
    img, d = new_canvas(size)
    S = size/192
    cx, cy = size//2, int(size*0.40)

    FUR    = (130,  82,  40)
    FUR_DK = ( 90,  55,  22)
    MUZZLE = (210, 170, 120)
    TOOTH  = (240, 235, 200)
    CLIP_W = (220, 220, 230)
    CLIP_G = (100, 110, 130)
    CHECK  = ( 50, 200,  80)

    # Rounded ears
    for ex in [-1, 1]:
        circle(d, cx+ex*int(28*S), cy-int(34*S), int(16*S), FUR_DK)
        circle(d, cx+ex*int(28*S), cy-int(34*S), int(10*S), FUR)

    # Face
    circle(d, cx, cy, int(36*S), FUR)
    # Muzzle
    d.ellipse([cx-int(18*S), cy+int(6*S), cx+int(18*S), cy+int(26*S)], fill=MUZZLE)
    # Teeth (two buck teeth)
    d.rectangle([cx-int(9*S), cy+int(20*S), cx-int(2*S), cy+int(30*S)], fill=TOOTH)
    d.rectangle([cx+int(2*S), cy+int(20*S), cx+int(9*S), cy+int(30*S)], fill=TOOTH)
    d.line([cx-int(1*S),cy+int(20*S), cx+int(1*S),cy+int(31*S)], fill=FUR, width=max(1,int(2*S)))

    eyes(d, cx, cy-int(6*S), size, gap=int(13*S), r=int(6*S), iris=(90,50,20))
    nose(d, cx, cy+int(5*S), size, color=FUR_DK)
    blush(d, cx, cy-int(2*S), size)

    # Clipboard body
    bx, by = cx-int(34*S), cy+int(38*S)
    bw, bh = int(68*S), int(54*S)
    d.rounded_rectangle([bx, by, bx+bw, by+bh], radius=int(4*S), fill=CLIP_W, outline=CLIP_G, width=max(1,int(2*S)))
    # Clip at top
    cx2 = bx+bw//2
    d.rounded_rectangle([cx2-int(10*S), by-int(6*S), cx2+int(10*S), by+int(6*S)], radius=int(3*S), fill=CLIP_G)
    # Checklist lines
    lx = bx+int(8*S)
    for i, (done, label) in enumerate([(True,""), (True,""), (False,""), (False,"")]):
        ly = by+int(12*S)+i*int(10*S)
        # check box
        bsz = int(7*S)
        d.rectangle([lx, ly-bsz//2, lx+bsz, ly+bsz//2], outline=CLIP_G, width=max(1,int(1*S)))
        if done:
            d.line([lx+int(1*S), ly, lx+int(3*S), ly+int(3*S)], fill=CHECK, width=max(1,int(2*S)))
            d.line([lx+int(3*S), ly+int(3*S), lx+bsz-int(1*S), ly-int(2*S)], fill=CHECK, width=max(1,int(2*S)))
        # text line
        d.line([lx+bsz+int(4*S), ly, bx+bw-int(8*S), ly], fill=CLIP_G, width=max(1,int(1*S)))

    save_both(img, "icon-checklist")


# ══════════════════════════════════════════════════════════════════════════
# 3.  JUDICIAL SEARCH  —  Raccoon with magnifying glass
# ══════════════════════════════════════════════════════════════════════════
def make_judicial_search(size=192):
    img, d = new_canvas(size)
    S = size/192
    cx, cy = size//2, int(size*0.38)

    GREY    = (165, 175, 185)
    GREY_DK = ( 80,  88, 100)
    MASK    = ( 38,  40,  55)
    WHITE_F = (225, 228, 232)
    LENS_C  = (180, 218, 245)
    HANDLE  = (140,  90,  40)

    # Ears
    for ex in [-1, 1]:
        circle(d, cx+ex*int(28*S), cy-int(34*S), int(17*S), GREY_DK)
        circle(d, cx+ex*int(28*S), cy-int(34*S), int(10*S), GREY)

    # Face base
    circle(d, cx, cy, int(37*S), GREY)

    # White muzzle patch
    d.ellipse([cx-int(19*S), cy+int(2*S), cx+int(19*S), cy+int(22*S)], fill=WHITE_F)

    # Raccoon eye masks — two separate patches, one per eye
    mask_r = int(14*S)
    d.ellipse([cx-int(28*S), cy-int(20*S), cx-int(4*S),  cy+int(2*S)], fill=MASK)
    d.ellipse([cx+int(4*S),  cy-int(20*S), cx+int(28*S), cy+int(2*S)], fill=MASK)

    eyes(d, cx, cy-int(10*S), size, gap=int(13*S), r=int(6*S), iris=(60,90,170))
    nose(d, cx, cy+int(5*S),  size, color=GREY_DK)
    blush(d, cx, cy+int(2*S), size)
    mouth(d, cx, cy+int(12*S), size, color=GREY_DK)

    # Magnifying glass (bottom-right, larger)
    mx, my = cx+int(34*S), cy+int(55*S)
    mr = int(22*S)
    # lens outer ring (gold)
    circle(d, mx, my, mr+int(3*S), GOLD_DK)
    circle(d, mx, my, mr, GOLD)
    # lens glass
    circle(d, mx, my, mr-int(3*S), LENS_C)
    # glass highlight
    circle(d, mx-int(6*S), my-int(6*S), int(6*S), (*WHITE, 100))
    # handle
    ang = math.radians(130)
    hx1 = int(mx + math.cos(ang)*(mr+int(2*S)))
    hy1 = int(my + math.sin(ang)*(mr+int(2*S)))
    hx2 = int(mx + math.cos(ang)*(mr+int(18*S)))
    hy2 = int(my + math.sin(ang)*(mr+int(18*S)))
    d.line([hx1,hy1, hx2,hy2], fill=HANDLE, width=max(4,int(6*S)))

    save_both(img, "icon-judicial-search")


# ══════════════════════════════════════════════════════════════════════════
# 4.  TAX  —  Pig with gold coins
# ══════════════════════════════════════════════════════════════════════════
def make_tax(size=192):
    img, d = new_canvas(size)
    S = size/192
    cx, cy = size//2, int(size*0.40)

    PINK     = (245, 148, 158)
    PINK_LT  = (255, 190, 196)
    PINK_DK  = (210, 100, 115)
    COIN_Y   = (220, 180,  40)
    COIN_DK  = (170, 130,  20)

    # Ears
    for ex in [-1, 1]:
        circle(d, cx+ex*int(30*S), cy-int(30*S), int(15*S), PINK)
        circle(d, cx+ex*int(30*S), cy-int(30*S), int(9*S),  PINK_LT)

    # Face
    circle(d, cx, cy, int(36*S), PINK)
    # Snout
    circle(d, cx, cy+int(13*S), int(17*S), PINK_DK)
    # Nostrils
    circle(d, cx-int(6*S), cy+int(14*S), int(4*S), (*BG, 200))
    circle(d, cx+int(6*S), cy+int(14*S), int(4*S), (*BG, 200))

    eyes(d, cx, cy-int(8*S), size, gap=int(13*S), r=int(6*S), iris=(180, 60, 80))
    blush(d, cx, cy-int(4*S), size)

    # Coin stack (bottom centre)
    for i in range(4):
        iy = cy + int((58-i*9)*S)
        cr_x, cr_y = int(28*S), int(8*S)
        d.ellipse([cx-cr_x, iy-cr_y, cx+cr_x, iy+cr_y],
                  fill=COIN_Y if i%2==0 else COIN_DK,
                  outline=COIN_DK, width=max(1,int(1*S)))
        # ¥ / $ symbol on top coin
        if i == 3:
            d.text((cx, iy), "¥", fill=COIN_DK, anchor="mm") if hasattr(d,'text') else None

    # Gold sparkles
    for sx, sy in [(-int(35*S), int(44*S)), (int(40*S), int(48*S)), (-int(42*S), int(60*S))]:
        cx2, cy2 = cx+sx, cy+sy
        for a in [0, 90]:
            r2 = math.radians(a)
            d.line([cx2-int(5*S),cy2, cx2+int(5*S),cy2], fill=GOLD_LT, width=max(1,int(1*S)))
            d.line([cx2,cy2-int(5*S), cx2,cy2+int(5*S)], fill=GOLD_LT, width=max(1,int(1*S)))
        circle(d, cx2, cy2, int(2*S), GOLD_LT)

    save_both(img, "icon-tax")


# ══════════════════════════════════════════════════════════════════════════
# 5.  COURT NAV  —  Dog with compass / map
# ══════════════════════════════════════════════════════════════════════════
def make_court_nav(size=192):
    img, d = new_canvas(size)
    S = size/192
    cx, cy = size//2, int(size*0.38)

    TAN     = (210, 160,  80)
    TAN_DK  = (150, 100,  40)
    CREAM   = (240, 215, 170)
    MAP_Y   = (220, 190, 120)
    MAP_DK  = (160, 130,  70)
    RED     = (220,  60,  50)

    # Floppy ears: drawn BEFORE face so they appear behind it
    # Each ear is a tall rounded rectangle hanging down from head level
    for ex in [-1, 1]:
        ex2 = ex * int(34*S)
        d.rounded_rectangle(
            [cx+ex2-int(16*S), cy-int(26*S),
             cx+ex2+int(16*S), cy+int(38*S)],
            radius=int(12*S), fill=TAN_DK)
        # lighter inner ear stripe
        d.rounded_rectangle(
            [cx+ex2-int(8*S), cy-int(20*S),
             cx+ex2+int(8*S), cy+int(30*S)],
            radius=int(8*S), fill=TAN)

    # Face
    circle(d, cx, cy, int(34*S), TAN)
    # Muzzle
    d.ellipse([cx-int(18*S), cy+int(6*S), cx+int(18*S), cy+int(22*S)], fill=CREAM)
    # Nose (wider)
    d.ellipse([cx-int(9*S), cy+int(2*S), cx+int(9*S), cy+int(10*S)], fill=TAN_DK)

    eyes(d, cx, cy-int(8*S), size, gap=int(13*S), r=int(6*S), iris=(100, 65, 20))
    blush(d, cx, cy, size)
    mouth(d, cx, cy+int(13*S), size, color=TAN_DK)

    # Map/compass (bottom)
    mx, my = cx, cy+int(54*S)
    mw, mh = int(38*S), int(28*S)
    # folded map
    d.rounded_rectangle([mx-mw, my-mh, mx+mw, my+mh], radius=int(4*S), fill=MAP_Y, outline=MAP_DK, width=max(1,int(2*S)))
    # map fold lines
    d.line([mx, my-mh, mx, my+mh], fill=MAP_DK, width=max(1,int(1*S)))
    d.line([mx-mw, my, mx+mw, my], fill=MAP_DK, width=max(1,int(1*S)))
    # compass rose (simple cross + circle)
    d.line([mx-int(8*S), my-int(4*S), mx+int(8*S), my-int(4*S)], fill=MAP_DK, width=max(1,int(1*S)))
    d.line([mx, my-int(12*S), mx, my+int(4*S)], fill=MAP_DK, width=max(1,int(1*S)))
    # north arrow (red)
    d.polygon([mx, my-int(12*S), mx-int(4*S), my-int(4*S), mx+int(4*S), my-int(4*S)], fill=RED)
    circle(d, mx, my-int(4*S), int(3*S), MAP_DK)
    # location pin
    px, py = mx+int(18*S), my-int(10*S)
    circle(d, px, py, int(5*S), RED, outline=(150,30,30), ow=1)
    d.polygon([px-int(4*S), py+int(1*S), px+int(4*S), py+int(1*S), px, py+int(9*S)], fill=RED)

    save_both(img, "icon-court")


# ══════════════════════════════════════════════════════════════════════════
# 6.  CHECKLIST alt name: also save as icon-checklist  (already done above)
#     Extra: TAX alt name icon-tax
# ══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("Generating icons...")
    make_deadline()
    make_checklist()
    make_judicial_search()
    make_tax()
    make_court_nav()
    print("Done! All icons saved to icons/")
