#!/usr/bin/env python3
"""Generate the pack's art: title-screen background + logo (FancyMenu) and quest chapter banners.

Requires Pillow (pip install pillow) and the Avenir Next font that ships with macOS.
Outputs (committed, so other machines don't need Pillow):
  pack/config/fancymenu/assets/background.png   1920x1080 menu / loading background
  pack/config/fancymenu/assets/logo.png         transparent logo: WARBUCKS in real element tiles
  pack/kubejs/assets/warbucks/textures/quests/<chapter>.png   chapter banners (FTB Quests images)
Run: <python with pillow> tools/build_art.py
"""
import math
import pathlib
import random
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
FONT = "/System/Library/Fonts/Avenir Next.ttc"  # index 0 regular, 1 bold, 2 demi bold (macOS)

NAVY, TEAL = (8, 14, 30), (10, 52, 60)
CYAN, GOLD, WHITE = (79, 209, 197), (242, 181, 68), (236, 242, 248)


def font(size, weight=1):
    return ImageFont.truetype(FONT, size, index=weight)


def gradient(w, h, top, bottom):
    img = Image.new("RGB", (w, h), top)
    px = img.load()
    for y in range(h):
        t = y / max(1, h - 1)
        c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        for x in range(w):
            px[x, y] = c
    return img


# (symbol, atomic number, name) for the 118 elements, in periodic-table positions (period, group)
ELEMENTS = "H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe Cs Ba La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu Hf Ta W Re Os Ir Pt Au Hg Tl Pb Bi Po At Rn Fr Ra Ac Th Pa U Np Pu Am Cm Bk Cf Es Fm Md No Lr Rf Db Sg Bh Hs Mt Ds Rg Cn Nh Fl Mc Lv Ts Og".split()


def table_positions():
    """Yield (z, period, group) with lanthanides/actinides on rows 8/9."""
    pos = []
    for z in range(1, 119):
        if z == 1: p, g = 1, 1
        elif z == 2: p, g = 1, 18
        elif z <= 10: p, g = 2, (z - 2 if z <= 4 else z + 8)
        elif z <= 18: p, g = 3, (z - 10 if z <= 12 else z)
        elif z <= 36: p, g = 4, z - 18
        elif z <= 54: p, g = 5, z - 36
        elif z <= 56: p, g = 6, z - 54
        elif z <= 71: p, g = 8, z - 54
        elif z <= 86: p, g = 6, z - 68
        elif z <= 88: p, g = 7, z - 86
        elif z <= 103: p, g = 9, z - 86
        else: p, g = 7, z - 100
        pos.append((z, p, g))
    return pos


def element_tile(size, symbol, z, name="", fill=(14, 40, 52), edge=CYAN, text=WHITE, sub=GOLD):
    """A periodic-table tile: atomic number top-left, symbol centre, name below."""
    tile = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(tile)
    r = size // 9
    d.rounded_rectangle([2, 2, size - 3, size - 3], radius=r, fill=fill + (235,), outline=edge + (255,), width=max(2, size // 40))
    d.text((size * 0.1, size * 0.07), str(z), font=font(int(size * 0.17), 2), fill=sub)
    f = font(int(size * (0.5 if len(symbol) == 1 else 0.44)), 1)
    w = d.textlength(symbol, font=f)
    d.text(((size - w) / 2, size * 0.2), symbol, font=f, fill=text)
    if name:
        fn = font(int(size * 0.12), 0)
        w = d.textlength(name, font=fn)
        d.text(((size - w) / 2, size * 0.76), name, font=fn, fill=text + (200,))
    return tile


def glow(img, radius=18):
    """Soft glow behind an RGBA image."""
    a = img.split()[-1].filter(ImageFilter.GaussianBlur(radius))
    g = Image.new("RGBA", img.size, CYAN + (0,))
    g.putalpha(a.point(lambda v: int(v * 0.8)))
    out = Image.new("RGBA", img.size, (0, 0, 0, 0))
    out.alpha_composite(g)
    out.alpha_composite(img)
    return out


def background(w=1920, h=1080, seed=20261018):
    rnd = random.Random(seed)
    img = gradient(w, h, NAVY, TEAL).convert("RGBA")
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    # stars
    for _ in range(420):
        x, y, s = rnd.randrange(w), rnd.randrange(h), rnd.choice([1, 1, 1, 2])
        d.ellipse([x, y, x + s, y + s], fill=WHITE + (rnd.randrange(40, 160),))
    # faint periodic table across the lower half
    cell, gap = 62, 6
    ox, oy = (w - 18 * (cell + gap)) // 2, int(h * 0.42)
    for z, p, g in table_positions():
        x = ox + (g - 1) * (cell + gap)
        y = oy + (p - 1) * (cell + gap) + (14 if p >= 8 else 0)
        d.rounded_rectangle([x, y, x + cell, y + cell], radius=8, outline=CYAN + (38,), width=2, fill=(20, 70, 80, 22))
        d.text((x + 7, y + 4), str(z), font=font(13, 0), fill=GOLD + (60,))
        sym = ELEMENTS[z - 1]
        fs = font(26, 1)
        d.text((x + (cell - d.textlength(sym, font=fs)) / 2, y + 18), sym, font=fs, fill=WHITE + (55,))
    # molecule lattices (hexagons with nodes) in the upper corners
    for cx, cy, scale in ((230, 230, 70), (1690, 260, 80), (1500, 120, 40), (420, 120, 36)):
        for k in range(6):
            a1, a2 = math.radians(60 * k + 30), math.radians(60 * (k + 1) + 30)
            p1 = (cx + scale * math.cos(a1), cy + scale * math.sin(a1))
            p2 = (cx + scale * math.cos(a2), cy + scale * math.sin(a2))
            d.line([p1, p2], fill=CYAN + (70,), width=3)
            d.ellipse([p1[0] - 6, p1[1] - 6, p1[0] + 6, p1[1] + 6], fill=GOLD + (110,))
    layer = layer.filter(ImageFilter.GaussianBlur(0.6))
    img.alpha_composite(layer)
    # vignette + centre glow
    vig = Image.new("L", (w, h), 0)
    ImageDraw.Draw(vig).ellipse([-w * 0.2, -h * 0.35, w * 1.2, h * 1.1], fill=255)
    vig = vig.filter(ImageFilter.GaussianBlur(160))
    dark = Image.new("RGBA", (w, h), (2, 4, 10, 255))
    img = Image.composite(img, dark, vig)
    return img.convert("RGB")


LOGO_TILES = [("W", 74, "Tungsten"), ("Ar", 18, "Argon"), ("B", 5, "Boron"), ("U", 92, "Uranium"),
              ("C", 6, "Carbon"), ("K", 19, "Potassium"), ("S", 16, "Sulfur")]


def logo():
    size, gap = 150, 14
    w = len(LOGO_TILES) * (size + gap) - gap + 80
    img = Image.new("RGBA", (w, 360), (0, 0, 0, 0))
    for i, (sym, z, name) in enumerate(LOGO_TILES):
        img.alpha_composite(element_tile(size, sym, z, name), (40 + i * (size + gap), 20))
    d = ImageDraw.Draw(img)
    f = font(92, 1)
    word = "CHEMISTRY"
    spaced = " ".join(word)
    tw = d.textlength(spaced, font=f)
    d.text(((w - tw) / 2, 186), spaced, font=f, fill=GOLD)
    f2 = font(34, 2)
    tag = "THE DEMIGOD'S CODEX"
    d.text(((w - d.textlength(tag, font=f2)) / 2, 300), tag, font=f2, fill=CYAN)
    return glow(img, 14)


TIER_COLORS = {"welcome": GOLD, "start": (120, 200, 120), "t0": (205, 127, 50), "t1": (150, 160, 170),
               "t2": (240, 120, 60), "t3": (90, 170, 255), "t4": (190, 230, 90), "t5": (60, 60, 60),
               "t6": (170, 120, 255), "t7": (255, 90, 160)}


def banner(key, title, tag, color, z=0):
    w, h = 960, 160
    img = gradient(w, h, tuple(int(c * 0.35) for c in color), NAVY).convert("RGBA")
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=22, outline=color + (255,), width=4)
    img.alpha_composite(element_tile(128, tag, z, "", fill=(12, 30, 40), edge=color), (16, 16))
    d.text((170, 30), title, font=font(64, 1), fill=WHITE)
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 1, h - 1], radius=22, fill=255)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    out.paste(img, (0, 0), mask)
    return out


def main():
    from quest_data import CHAPTERS  # noqa: E402  (needs test/ids.tsv like the quest build)
    fm = ROOT / "pack/config/fancymenu/assets"
    fm.mkdir(parents=True, exist_ok=True)
    background().save(fm / "background.png", optimize=True)
    logo().save(fm / "logo.png", optimize=True)
    qdir = ROOT / "pack/kubejs/assets/warbucks/textures/quests"
    qdir.mkdir(parents=True, exist_ok=True)
    # Banner tiles: tier chapters show T0-T7; the rest show a real element that fits the chapter.
    tags = {"welcome": ("H", 1), "start": ("He", 2), "t0": ("T0", 0), "t1": ("T1", 1), "t2": ("T2", 2),
            "t3": ("T3", 3), "t4": ("T4", 4), "t5": ("T5", 5), "t6": ("T6", 6), "t7": ("T7", 7),
            "tools": ("Fe", 26), "factory": ("C", 6), "qol": ("Ar", 18), "storage": ("Si", 14),
            "magic": ("Au", 79), "worlds": ("O", 8), "farming": ("N", 7)}
    for c in CHAPTERS:
        title = c.title.split(". ", 1)[-1]
        sym, z = tags.get(c.key, ("Ws", 0))
        banner(c.key, title, sym, TIER_COLORS.get(c.key, CYAN), z).save(qdir / f"{c.key}.png", optimize=True)
    print(f"Wrote background, logo and {len(CHAPTERS)} chapter banners")


if __name__ == "__main__":
    main()
