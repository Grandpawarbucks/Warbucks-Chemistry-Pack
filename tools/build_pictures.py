#!/usr/bin/env python3
"""Quest-page pictures: the images FTB Quests shows between quests (ATM10 places about a dozen per chapter).

Everything here is drawn by us: item and block textures are read from the mod jars in test/server/mods and
composed into our own pictures (the way JEI renders them), never copied from another pack.
The quest engine (tools/build_quests.py via tools/layout.py) calls `render(slot)` for every picture slot and
`clean(keep)` afterwards. Output: pack/kubejs/assets/warbucks/textures/quests/pictures/<chapter>_<slug>.png.

Kinds (picked from the slot's shape and items unless slot["kind"] says otherwise):
  showcase    3-6 item/block renders in a row, arc or column, framed, with a caption
  machine     one large block render with its name
  multiblock  an isometric diagram of a Modern Industrialization multiblock (assembled + layer by layer); the
              shapes were read from MI's ShapeTemplate builders (javap of MultiblockMachines/EBF/DistillationTower)
              and from our own KubeJS registrations (startup_scripts/aluminum_line.js)
  decor       an element-tile motif (chapters without item context)
  backdrop    a quiet framed panel that quests sit on (tier tint, faint lab grid, no renders, no caption); an
              optional title tab in one corner (slot["tab"] = "tl"/"tr"/"bl"/"br", text = slot["title"])
  label       a low strip with only its title (ATM10 labels its rows this way)
  rule        a thin divider line (ATM10's table lines)
slot["caption"] = "bottom", "top" or None places the caption of the art kinds (no key: bottom when there is a
title); tools/layout.py decides it so that no quest sits on a caption (tools/layout_lint.py checks it).
Style follows tools/build_art.py (navy/teal gradients, cyan + gold, Avenir Next / Segoe UI).
Run: .venv/Scripts/python tools/build_pictures.py --demo   writes samples to test/preview/pictures/ (git-ignored)
"""
import hashlib
import io
import math
import pathlib
import sys

from PIL import Image, ImageDraw, ImageFilter

ROOT = pathlib.Path(__file__).resolve().parent.parent
for p in (ROOT / "tools", ROOT / "test"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import build_quest_preview as bqp  # noqa: E402  (IconCache, Assets, _iso, _tex, _model_chain: the preview's renderer)
from build_art import CYAN, ELEMENTS, GOLD, NAVY, TIER_COLORS, WHITE, element_tile, font, gradient  # noqa: E402

PIC_DIR = ROOT / "pack/kubejs/assets/warbucks/textures/quests/pictures"
DEMO_DIR = ROOT / "test/preview/pictures"
RESOURCE = "warbucks:textures/quests/pictures/"
CELL = 48        # px per quest-grid cell
MAX_SIDE = 1024
MI = "modern_industrialization:"

# ---------------------------------------------------------------- MI multiblock shapes
# (x, y, z) -> block id; x = -1..1 left to right, y up, z = 0 front (controller row) to back.
# "ring" = the 3x3 with its centre left open.


def _layer(y, block, ring=False, centre=None):
    out = {}
    for x in (-1, 0, 1):
        for z in (0, 1, 2):
            if x == 0 and z == 1:
                if ring and centre is None:
                    continue
                if centre is not None:
                    out[(x, y, z)] = centre
                    continue
            out[(x, y, z)] = block
    return out


def _stack(*layers):
    out = {}
    for lay in layers:
        out.update(lay)
    return out


_HEAT, _STEEL, _COIL = MI + "heatproof_machine_casing", MI + "steel_machine_casing", MI + "cupronickel_coil"
_CSS, _SPIPE = MI + "clean_stainless_steel_machine_casing", MI + "stainless_steel_machine_casing_pipe"
_FROST, _FIRE, _BRICKS = MI + "frostproof_machine_casing", MI + "fire_clay_bricks", "minecraft:bricks"
_STPIPE = MI + "steel_machine_casing_pipe"

SHAPES = {
    # ShapeTemplate: heatproof floor, two hollow coil rings, heatproof roof (EBF tier 1 = cupronickel)
    "electric_blast_furnace": dict(title="Electric Blast Furnace", note="3 x 4 x 3  (cupronickel tier)",
                                   blocks=_stack(_layer(0, _HEAT), _layer(1, _COIL, True), _layer(2, _COIL, True), _layer(3, _HEAT))),
    # add3by3Levels(-1, 1, bricks): full floor, then two hollow rings; the controller sits in the middle row
    "coke_oven": dict(title="Coke Oven", note="3 x 3 x 3  vanilla bricks", controller=(0, 1, 0),
                      blocks=_stack(_layer(0, _BRICKS), _layer(1, _BRICKS, True), _layer(2, _BRICKS, True))),
    # add3by3Levels(-1, 2, fire clay bricks)
    "steam_blast_furnace": dict(title="Steam Blast Furnace", note="3 x 4 x 3  fire clay bricks", controller=(0, 1, 0),
                                blocks=_stack(_layer(0, _FIRE), _layer(1, _FIRE, True), _layer(2, _FIRE, True), _layer(3, _FIRE, True))),
    # add3by3(0, steel, hollow) + add3by3(1, steel, hollow)
    "steam_quarry": dict(title="Steam Quarry", note="3 x 2 x 3  steel casing, open centre",
                         blocks=_stack(_layer(0, _STEEL, True), _layer(1, _STEEL, True))),
    # the steam quarry ring plus a pipe frame above it (pipe pillars at the back corners, a bar across the top)
    "electric_quarry": dict(title="Electric Quarry", note="steel casing ring with a pipe frame",
                            blocks=_stack(_layer(0, _STEEL, True), _layer(1, _STEEL, True),
                                          {(-1, y, 1): _STPIPE for y in (2, 3, 4)}, {(1, y, 1): _STPIPE for y in (2, 3, 4)},
                                          {(0, 4, 1): _STPIPE, (0, 3, 1): _STPIPE, (0, 2, 1): _STPIPE})),
    # add3by3LevelsRoofed(-1, 2, frostproof): floor, two rings, roof
    "vacuum_freezer": dict(title="Vacuum Freezer", note="3 x 4 x 3  frostproof casing", controller=(0, 1, 0),
                           blocks=_stack(_layer(0, _FROST), _layer(1, _FROST, True), _layer(2, _FROST, True), _layer(3, _FROST))),
    # one casing ring with a stainless pipe in the centre per level; 4 levels shown (it can be taller)
    "distillation_tower": dict(title="Distillation Tower", note="3 x N x 3  clean stainless casing, pipe core",
                               blocks=_stack(*[_layer(y, _CSS, centre=_SPIPE) for y in range(4)])),
    # ours: startup_scripts/aluminum_line.js (steel floor and anode beam, cupronickel coils round the bath)
    "hall_heroult_cell": dict(title="Hall-Héroult Cell", note="3 x 3 x 3  steel + cupronickel coils", controller=(0, 1, 0),
                              blocks=_stack(_layer(0, _STEEL), _layer(1, _COIL, True), _layer(2, _STEEL))),
}

# MI casing names (model "casing" field) -> block texture
_CASING_TEX = {"bronze": MI + "block/bronze_machine_casing", "steel": MI + "block/steel_machine_casing",
               "lv": MI + "block/basic_machine_hull", "mv": MI + "block/advanced_machine_hull",
               "hv": MI + "block/turbo_machine_hull", "ev": MI + "block/highly_advanced_machine_hull",
               "superconductor": MI + "block/quantum_machine_hull", "firebricks": MI + "block/fire_clay_bricks",
               "bricks": "minecraft:block/bricks"}

# chapters that get element-tile decor when they have no items nearby (and the elements they lean on)
CHAPTER_ELEMENTS = {"welcome": ("H", "He", "Li", "Be", "B", "C"), "tips": ("Ti", "Ar", "Ne", "Kr", "Xe", "Rn"),
                    "start": ("He", "C", "N", "O", "Na", "Cl"), "lab_notes": ("Cl", "Br", "I", "F", "At", "Ts"),
                    "completionist": ("Lr", "No", "Md", "Fm", "Es", "Cf"), "market": ("Au", "Ag", "Pt", "Pd", "Cu", "Sn"),
                    "periodic": ("Og", "Ts", "Lv", "Mc", "Fl", "Nh"), "building": ("Ca", "Si", "Al", "Fe", "Mg", "K")}

_icons = None
_A = None


def _cache():
    global _icons, _A
    if _icons is None:
        _icons = bqp.IconCache()
        _A = _icons.A
    return _icons


def _name(item_id):
    n = bqp.names().get(item_id)
    if n:
        return n
    return item_id.split(":", 1)[-1].split("/")[-1].replace("_", " ").title()


# ---------------------------------------------------------------- textures and renders


def _tex16(name):
    """A 16x16 texture (first animation frame), or None."""
    t = bqp._tex(_A, name)
    return None if t is None else t.resize((16, 16), Image.NEAREST)


def _block_faces(block_id):
    """(top, front, side) 16px faces for a block id, or None when it has no cube model."""
    ns, path = block_id.split(":", 1)
    tex, flat, block, elements = bqp._model_chain(_A, f"{ns}:block/{path}")
    info = bqp._model_chain.info
    if info.get("casing") and isinstance(info.get("default_overlays"), dict):
        return _machine_faces(info["casing"], info["default_overlays"])
    if not tex or flat:
        return None

    def res(k):
        v = tex.get(k)
        for _ in range(6):
            if isinstance(v, str) and v.startswith("#"):
                v = tex.get(v[1:])
        return v

    def pick(*keys):
        for k in keys:
            t = _tex16(res(k))
            if t is not None:
                return t
        return None
    top = pick("top", "up", "end", "all", "texture", "side", "particle")
    if top is None:
        return None
    side = pick("side", "east", "west", "all", "texture", "particle") or top
    front = pick("front", "north", "south", "side", "all", "texture", "particle") or side
    return top, front, side


def _machine_faces(casing, overlays):
    """MI machine: the casing texture with the machine's front/top/side overlays."""
    base = None
    for cand in (_CASING_TEX.get(casing), MI + "block/" + casing, MI + "block/casings/" + casing, "minecraft:block/" + casing):
        if cand:
            base = _tex16(cand)
            if base is not None:
                break
    if base is None:
        base = bqp._casing(casing)
    faces = []
    for k in ("top", "front", "side"):
        f = base.copy()
        t = _tex16(overlays.get(k)) if overlays.get(k) else None
        if t is not None:
            f.alpha_composite(t)
        faces.append(f)
    return tuple(faces)


def _cube(block_id, size):
    faces = _block_faces(block_id)
    if faces is None:
        return None
    return bqp._iso(*faces, S=size)


def _flat(item_id, size):
    """A flat item icon upscaled with nearest-neighbour (pixel art stays crisp), or None."""
    im = _cache().get(item_id)
    if im is None:
        return None
    base = 16 if im.size[0] % 16 == 0 and im.size[0] >= 16 else im.size[0]
    im = im.resize((base, base), Image.NEAREST) if im.size[0] != base else im
    k = max(1, size // base)
    return im.resize((base * k, base * k), Image.NEAREST)


def _render_item(item_id, size):
    """An item drawn at about `size` px: a 3D cube for blocks, a flat sprite for items."""
    ns, path = item_id.split(":", 1) if ":" in item_id else ("minecraft", item_id)
    if ns != "chemlib":
        tex, flat, block, elements = bqp._model_chain(_A, f"{ns}:item/{path}")
        if block and not flat:
            cube = _cube(item_id, size)
            if cube is not None:
                return cube
        elif not tex:  # no item model: a block without an item json (or a KubeJS block)
            cube = _cube(item_id, size)
            if cube is not None:
                return cube
    return _flat(item_id, size)


def _shadow(im, radius, dy):
    """`im` on a soft dark shadow offset downwards."""
    pad = int(radius * 3)
    out = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    a = Image.new("L", out.size, 0)
    a.paste(im.getchannel("A"), (pad, pad + dy))
    a = a.filter(ImageFilter.GaussianBlur(radius)).point(lambda v: int(v * 0.7))
    sh = Image.new("RGBA", out.size, (0, 0, 0, 0))
    sh.putalpha(a)
    out.alpha_composite(sh)
    out.alpha_composite(im, (pad, pad))
    return out, pad


# ---------------------------------------------------------------- panel, caption


def _panel(w, h, color):
    """Rounded, framed panel: tier-coloured gradient into navy, a faint lab grid, gold frame."""
    r = max(8, min(w, h) // 10)
    img = gradient(w, h, tuple(int(c * 0.38) for c in color), NAVY).convert("RGBA")
    d = ImageDraw.Draw(img)
    step = CELL // 2
    for i in range(step, w, step):
        d.line([(i, 0), (i, h)], fill=(255, 255, 255, 9), width=1)
    for i in range(step, h, step):
        d.line([(0, i), (w, i)], fill=(255, 255, 255, 9), width=1)
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse([w * 0.1, h * 0.05, w * 0.9, h * 0.8], fill=color + (46,))
    img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(max(8, min(w, h) // 6))))
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 1, h - 1], radius=r, fill=255)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    out.paste(img, (0, 0), mask)
    d = ImageDraw.Draw(out)
    fw = max(2, min(w, h) // 60)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=r, outline=GOLD + (235,), width=fw)
    d.rounded_rectangle([fw, fw, w - 1 - fw, h - 1 - fw], radius=max(4, r - fw), outline=(0, 0, 0, 110), width=1)
    return out


def _caption(img, text, size, y=None, fill=WHITE, weight=1, margin=10):
    """Centred text, shrunk until it fits; returns its height. y=None puts it along the bottom."""
    if not text:
        return 0
    d = ImageDraw.Draw(img)
    w = img.width
    while size > 9 and d.textlength(text, font=font(size, weight)) > w - 2 * margin:
        size -= 1
    f = font(size, weight)
    tw = d.textlength(text, font=f)
    ty = (img.height - size * 1.45 - margin * 0.6) if y is None else (margin * 0.6) if y == "top" else y
    d.text(((w - tw) / 2 + 1, ty + 1), text, font=f, fill=(0, 0, 0, 160))
    d.text(((w - tw) / 2, ty), text, font=f, fill=fill)
    return int(size * 1.45)


def _size(slot):
    w, h = max(1, int(slot.get("width") or 4)), max(1, int(slot.get("height") or 2))
    k = min(CELL, MAX_SIDE / max(w, h))
    return max(32, int(w * k)), max(32, int(h * k))


# ---------------------------------------------------------------- kinds


def _showcase(w, h, color, items, title, top=False):
    if not items:
        return None  # nothing to show: the caller falls back to element-tile decor
    img = _panel(w, h, color)
    n = len(items)
    cap = max(13, min(26, h // 7)) if title else 0
    cap_h = int(cap * 1.5) + 4 if title else 0
    oy = cap_h if top else 0  # caption along the top: the renders move down
    pad = max(8, min(w, h) // 12)
    vertical = h > w * 1.25 and n > 1
    if vertical:
        avail_h = h - cap_h - 2 * pad
        size = min(w - 2 * pad, avail_h // n - pad // 2)
    else:
        avail_w = w - 2 * pad
        size = min(h - cap_h - 2 * pad, (avail_w - (n - 1) * pad // 2) // n)
    size = max(16, size)
    renders = []
    for it in items:
        r = _render_item(it, size)
        if r is not None:
            renders.append(r)
    if not renders:
        return None
    n = len(renders)
    arc = (not vertical) and n >= 4 and h - cap_h > size * 1.6
    amp = min(size * 0.35, (h - cap_h - size) / 2 - pad / 2) if arc else 0
    for i, r in enumerate(renders):
        if vertical:
            cx = w / 2
            cy = pad + size / 2 + i * (h - cap_h - 2 * pad) / n + ((h - cap_h - 2 * pad) / n - size) / 2
        else:
            slot_w = (w - 2 * pad) / n
            cx = pad + slot_w * (i + 0.5)
            cy = (h - cap_h) / 2
            if arc and n > 1:
                t = 2 * i / (n - 1) - 1
                cy += amp * (t * t * 2 - 1) * 0.5 + amp * 0.25
        cy += oy
        sh, off = _shadow(r, max(2, size // 12), max(2, size // 14))
        img.alpha_composite(sh, (int(cx - r.width / 2 - off), int(cy - r.height / 2 - off)))
    _caption(img, title, cap, y="top" if top else None)
    return img


def _machine(w, h, color, item, title, top=False):
    img = _panel(w, h, color)
    cap = max(13, min(26, h // 7)) if title else 0  # the showcase's caption size (tools/layout_lint.caption_band)
    cap_h = int(cap * 1.5) + 4 if title else 0
    pad = max(8, min(w, h) // 10)
    size = max(16, min(w - 2 * pad, h - cap_h - 2 * pad))
    r = _render_item(item, size)
    if r is None:
        return None
    sh, off = _shadow(r, max(2, size // 12), max(2, size // 14))
    cy = (h - cap_h) / 2 + (cap_h if top else 0)
    img.alpha_composite(sh, (int(w / 2 - r.width / 2 - off), int(cy - r.height / 2 - off)))
    _caption(img, title, cap, y="top" if top else None)
    return img


def _iso_blocks(blocks, S, controller=None, dim_controller=False):
    """Isometric painter's render of {(x,y,z): block} with cubes of size S (origin at the controller)."""
    faces = {}
    for b in set(blocks.values()):
        faces[b] = _block_faces(b)
    xs = [x for x, _, _ in blocks]
    ys = [y for _, y, _ in blocks]
    zs = [z for _, _, z in blocks]
    ax, bx, ay = S * 0.44, S * 0.44, S * 0.235
    # projection: screen x = (x - z) * 0.44 S, screen y = (x + z) * 0.235 S - y * 0.47 S
    px = [(x - z) * ax for x, _, z in blocks]
    py = [(x + z) * ay - y * S * 0.47 for x, y, z in blocks]
    x0, y0 = min(px), min(py)
    W = int(max(px) - x0 + S + 2)
    H = int(max(py) - y0 + S + 2)
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ctrl_img = None
    for (x, y, z), b in sorted(blocks.items(), key=lambda kv: (kv[0][0] + kv[0][1] - kv[0][2], kv[0][1])):
        f = faces.get(b)
        if f is None:
            f = (bqp._casing(b),) * 3
        top, front, side = f
        if controller is not None and (x, y, z) == controller:
            top, front, side = _controller_faces(controller[3]) if len(controller) > 3 else (top, front, side)
        cube = bqp._iso(top, front, side, S=S)
        pos = (int((x - z) * ax - x0 + 1), int((x + z) * ay - y * S * 0.47 - y0 + 1))
        out.alpha_composite(cube, pos)
        if controller is not None and (x, y, z) == controller[:3]:
            ctrl_img = (cube, pos)
    if ctrl_img:  # gold edge round the controller so it stands out
        cube, pos = ctrl_img
        edge = cube.getchannel("A").filter(ImageFilter.FIND_EDGES).point(lambda v: 255 if v > 40 else 0)
        ring = Image.new("RGBA", cube.size, GOLD + (0,))
        ring.putalpha(edge.point(lambda v: int(v * 0.9)))
        out.alpha_composite(ring, pos)
    return out


def _controller_faces(machine_id):
    f = _block_faces(machine_id)
    return f if f is not None else (bqp._casing(machine_id),) * 3


def _multiblock(w, h, color, key, machine_id, title, top=False, bare=False):
    shape = SHAPES[key]
    blocks = dict(shape["blocks"])
    ctrl = tuple(shape.get("controller", (0, 0, 0))) + (machine_id,)
    img = _panel(w, h, color)
    cap = max(12, min(22, h // 9))
    note_sz = max(9, int(cap * 0.6))
    cap_h = 0 if bare else int(cap * 1.4) + int(note_sz * 1.35) + 2
    oy = cap_h if top else 0  # caption along the top: the diagram moves down
    pad = max(6, min(w, h) // 16)
    layers = sorted({y for _, y, _ in blocks})
    stacked = h > w * 1.1  # tall slot: assembled view on top, the layers below it
    # assembled view
    nL = len(layers)
    if stacked:
        main_w, main_h = w - 2 * pad, (h - cap_h - 2 * pad) * 0.46
        row_w, row_h = w - 2 * pad, (h - cap_h - 2 * pad) * 0.52
    else:
        main_w, main_h = (w - 2 * pad) * 0.38, h - cap_h - 2 * pad
        row_w, row_h = (w - 2 * pad) * 0.6, h - cap_h - 2 * pad
    dx = max(x for x, _, _ in blocks) - min(x for x, _, _ in blocks) + 1
    dz = max(z for _, _, z in blocks) - min(z for _, _, z in blocks) + 1
    dy = max(y for _, y, _ in blocks) - min(y for _, y, _ in blocks) + 1
    # footprint in cube units: width (dx+dz)*0.88, height (dx+dz)*0.235 + dy*0.47 + 0.5
    S_main = int(min(main_w / ((dx + dz) * 0.44 + 0.12), main_h / ((dx + dz) * 0.235 + dy * 0.47 + 0.3)))
    S_main = max(10, S_main)
    main = _iso_blocks(blocks, S_main, controller=ctrl)
    # layer row (grid when there are many)
    best = None
    for per_row in sorted({nL, math.ceil(nL / 2), math.ceil(nL / 3)}):  # the grid that gives the biggest slabs wins
        rows = math.ceil(nL / per_row)
        cell_w = row_w / per_row
        lab = max(8, min(int(note_sz * 0.95), int(cell_w / 2.2)))  # "L1".."L9" must fit under each slab
        cell_h = (row_h - lab * 1.4 * rows) / rows
        S_lay = int(min(cell_w / ((dx + dz) * 0.44 + 0.2), cell_h / ((dx + dz - 2) * 0.235 + 1.1)))
        if best is None or S_lay > best[0]:
            best = (S_lay, per_row, rows, cell_w, cell_h, lab)
    S_lay, per_row, rows, cell_w, cell_h, lab = best
    S_lay = max(6, S_lay)
    lay_imgs = []
    for y in layers:
        sub = {(x, 0, z): b for (x, yy, z), b in blocks.items() if yy == y}
        c = ctrl if ctrl[1] == y else None
        c = (c[0], 0, c[2], c[3]) if c else None
        lay_imgs.append(_iso_blocks(sub, S_lay, controller=c))
    if stacked:
        mx, my = pad, pad + oy
        rx, ry = pad, pad + main_h + oy
    else:
        mx, my = pad, pad + oy
        rx, ry = pad + main_w, pad + oy
    sh, off = _shadow(main, max(2, S_main // 6), max(2, S_main // 8))
    img.alpha_composite(sh, (int(mx + main_w / 2 - main.width / 2 - off), int(my + main_h / 2 - main.height / 2 - off)))
    d = ImageDraw.Draw(img)
    fl = font(lab, 2)
    for i, (y, li) in enumerate(zip(layers, lay_imgs)):
        r, cidx = divmod(i, per_row)
        cx = rx + cell_w * (cidx + 0.5)
        cy = ry + (cell_h + lab * 1.4) * r + cell_h / 2
        img.alpha_composite(li, (int(cx - li.width / 2), int(cy - li.height / 2)))
        text = f"L{i + 1}"
        tw = d.textlength(text, font=fl)
        d.text((cx - tw / 2, ry + (cell_h + lab * 1.4) * r + cell_h), text, font=fl, fill=CYAN + (230,))
    if bare:
        return img
    if top:
        _caption(img, title or shape["title"], cap, y=4)
        _caption(img, shape.get("note", ""), note_sz, y=4 + int(cap * 1.35), fill=GOLD + (230,), weight=2)
        return img
    note_y = h - int(note_sz * 1.4) - 5
    _caption(img, shape.get("note", ""), note_sz, y=note_y, fill=GOLD + (230,), weight=2)
    _caption(img, title or shape["title"], cap, y=note_y - int(cap * 1.35))
    return img


def _decor(w, h, color, chapter, slug, title, top=False):
    img = _panel(w, h, color)
    syms = CHAPTER_ELEMENTS.get(chapter)
    if not syms:
        seed = int(hashlib.sha1(f"{chapter}:{slug}".encode()).hexdigest(), 16)
        syms = tuple(ELEMENTS[(seed // (7 ** i)) % len(ELEMENTS)] for i in range(6))
    cap = max(13, min(26, h // 7)) if title else 0
    cap_h = int(cap * 1.5) + 4 if title else 0
    pad = max(8, min(w, h) // 12)
    area_w, area_h = w - 2 * pad, h - cap_h - 2 * pad
    oy = cap_h if top else 0
    ring = area_h >= area_w * 0.75 and min(area_w, area_h) >= 120
    if ring:  # six tiles on a benzene-like ring with bonds
        n = 6
        size = int(min(area_w, area_h) * 0.3)
        rad = min(area_w, area_h) / 2 - size / 2
        cx, cy = w / 2, pad + area_h / 2 + oy
        pts = [(cx + rad * math.cos(math.radians(60 * k - 90)), cy + rad * math.sin(math.radians(60 * k - 90))) for k in range(n)]
        d = ImageDraw.Draw(img)
        d.line(pts + [pts[0]], fill=CYAN + (150,), width=max(2, size // 16), joint="curve")
        for k in range(0, n, 2):  # alternating double bonds
            (x1, y1), (x2, y2) = pts[k], pts[(k + 1) % n]
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            ox, oy = (mx - cx) * 0.12, (my - cy) * 0.12
            d.line([(x1 - ox, y1 - oy), (x2 - ox, y2 - oy)], fill=CYAN + (110,), width=max(1, size // 24))
    else:
        n = max(2, min(len(syms), int(area_w // (area_h * 0.9)) or 1, 6))
        size = int(min(area_h, area_w / n - pad / 2))
        gap = (area_w - n * size) / (n - 1) if n > 1 else 0
        pts = [(pad + size / 2 + i * (size + gap), pad + area_h / 2 + oy) for i in range(n)]
    for (x, y), sym in zip(pts, syms):
        z = ELEMENTS.index(sym) + 1 if sym in ELEMENTS else 0
        tile = element_tile(size, sym, z, "", fill=(12, 30, 40), edge=color)
        sh, off = _shadow(tile, max(2, size // 12), max(2, size // 14))
        img.alpha_composite(sh, (int(x - size / 2 - off), int(y - size / 2 - off)))
    _caption(img, title, cap, y="top" if top else None)
    return img


def _backdrop(w, h, color, px, title=None, corner=None):
    """A quiet frame that quests sit on: tier-tinted navy (semi-transparent), a faint lab grid, a thin tier-coloured
    frame with gold corner marks, nothing in the middle (quests cover it). Optional title tab in one corner.
    px = pixels per cell."""
    r = max(6, int(min(w, h, px * 2) // 8))
    base = gradient(w, h, tuple(int(c * 0.22) for c in color), NAVY).convert("RGBA")
    base.putalpha(150)
    d = ImageDraw.Draw(base)
    step = max(4, int(px // 2))
    for i in range(step, w, step):
        d.line([(i, 0), (i, h)], fill=(255, 255, 255, 12), width=1)
    for i in range(step, h, step):
        d.line([(0, i), (w, i)], fill=(255, 255, 255, 12), width=1)
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 1, h - 1], radius=r, fill=255)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    out.paste(base, (0, 0), mask)
    d = ImageDraw.Draw(out)
    fw = max(2, int(px // 24))
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=r, outline=color + (170,), width=fw)
    k = max(6, int(px * 0.6))  # gold corner marks (big frames only: on a small tile they read as dashes)
    for x, y, sx, sy in () if min(w, h) < 3 * px else ((0, 0, 1, 1), (w - 1, 0, -1, 1), (0, h - 1, 1, -1), (w - 1, h - 1, -1, -1)):
        d.line([(x + sx * fw, y + sy * (r + k)), (x + sx * fw, y + sy * r)], fill=GOLD + (210,), width=fw)
        d.line([(x + sx * (r + k), y + sy * fw), (x + sx * r, y + sy * fw)], fill=GOLD + (210,), width=fw)
    if title and corner:
        _tab(out, title, corner, px)
    return out


def _tab(img, text, corner, px):
    """Title tab inside a backdrop's corner, within the box tools/layout_lint.tab_box gives (0.6 cells high, at
    most 60% of the width and 6 cells, 0.15 cells in from the edges)."""
    W, H = img.size
    tw, th, m = min(0.6 * W, 6.0 * px), 0.6 * px, 0.15 * px
    d = ImageDraw.Draw(img)
    size = max(8, int(th * 0.62))
    while size > 8 and d.textlength(text, font=font(size, 1)) > tw - th * 0.8:
        size -= 1
    f = font(size, 1)
    tl = d.textlength(text, font=f)
    w_ = min(tw, tl + th * 0.8)
    x0 = m if corner[1] == "l" else W - m - w_
    y0 = m if corner[0] == "t" else H - m - th
    d.rounded_rectangle([x0, y0, x0 + w_, y0 + th], radius=int(th / 3), fill=(10, 22, 34, 220),
                        outline=GOLD + (220,), width=max(1, int(th / 18)))
    d.text((x0 + (w_ - tl) / 2, y0 + (th - size * 1.25) / 2), text, font=f, fill=WHITE)


def _label(w, h, color, px, title):
    """A low strip with only its title: the panel look, the text centred and as large as fits (at most 0.6
    cells high, the box tools/layout.py keeps quests away from)."""
    img = _panel(w, h, color)
    if title:
        size = max(10, int(min(h * 0.5, px * 0.55)))
        _caption(img, title, size, y=(h - size * 1.25) / 2, weight=2, margin=max(8, int(px * 0.2)))
    return img


def _rule(w, h, color):
    """A thin line, stretched over the slot: tier colour, fading out at both ends."""
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    horizontal = w >= h
    n = w if horizontal else h
    d = ImageDraw.Draw(img)
    for i in range(n):
        t = i / max(1, n - 1)
        a = int(140 * max(0.0, min(1.0, t / 0.08, (1 - t) / 0.08)))
        if horizontal:
            d.line([(i, 0), (i, h)], fill=color + (a,))
        else:
            d.line([(0, i), (w, i)], fill=color + (a,))
    return img


# ---------------------------------------------------------------- public API


def _pick_kind(slot, items):
    kind = slot.get("kind")
    if kind in ("backdrop", "label", "rule"):
        return kind
    if kind == "machine" and any(i.split(":", 1)[-1] in SHAPES for i in items):
        return "multiblock"  # a multiblock diagram beats a single render
    if kind in ("showcase", "machine", "multiblock", "decor"):
        if kind == "multiblock" and not any(i.split(":", 1)[-1] in SHAPES for i in items):
            kind = "showcase" if items else "decor"
        return kind
    if any(i.split(":", 1)[-1] in SHAPES for i in items):
        return "multiblock"
    if not items:
        return "decor"
    w, h = slot.get("width") or 4, slot.get("height") or 2
    if len(items) == 1 or (w <= 2 and h <= 2):
        return "machine"
    return "showcase"


def _draw(slot):
    _cache()
    chapter, slug = slot.get("chapter", "misc"), slot.get("slug", "picture")
    w, h = _size(slot)
    px = w / max(1e-6, float(slot.get("width") or 4))  # pixels per cell
    color = TIER_COLORS.get(chapter, CYAN)
    title = slot.get("title")
    top = slot.get("caption") == "top"
    placed = "caption" in slot  # tools/layout.py placed the caption (None: no spot clear of quests)
    seen, items = set(), []
    for i in slot.get("nearby_items") or []:
        if i and ":" in i and i not in seen:
            seen.add(i)
            items.append(i)
    kind = _pick_kind(slot, items)
    img = None
    if kind == "backdrop":
        return _backdrop(w, h, color, px, title, slot.get("tab")), kind
    if kind == "rule":
        sw, sh = float(slot.get("width") or 1), float(slot.get("height") or 0.1)
        return _rule(*((512, 8) if sw >= sh else (8, 512)), color), kind
    if kind == "label":
        return _label(w, h, color, px, title), kind
    if placed and not slot.get("caption"):
        title = None
    if kind == "multiblock":
        mid = next(i for i in items if i.split(":", 1)[-1] in SHAPES)
        # with no caption spot the diagram still stands, without its title and note
        img = _multiblock(w, h, color, mid.split(":", 1)[-1], mid, title, top=top, bare=placed and not title)
    elif kind == "machine":
        for it in items:
            img = _machine(w, h, color, it, title if placed else (title or _name(it)), top=top)
            if img is not None:
                break
        if img is None and len(items) > 1:
            kind = "showcase"
    if kind == "showcase" and img is None:
        img = _showcase(w, h, color, items[:6], title, top=top)
        if img is None and items:  # no icons at all: try a wider net before giving up on item art
            img = _showcase(w, h, color, items[6:12], title, top=top)
    if img is None:
        kind = "decor"
        img = _decor(w, h, color, chapter, slug, title, top=top)
    return img, kind


def _png(img):
    buf = io.BytesIO()
    img.save(buf, "PNG", optimize=True)
    return buf.getvalue()


def _write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() == data:
        return False
    path.write_bytes(data)
    return True


LOOSE = {}   # file name -> slot, for pictures rendered but not placed (slot["place"] is False)
LIST_DOC = ROOT / "docs/QUEST_PICTURES.md"


def render(slot):
    """Draw the picture for one slot and return its resource location (see the module docstring). A slot with
    place=False is drawn and kept in the pack for placing by hand in FTB's editor, but returns None, so the book
    writes no image for it (clean() keeps it and lists it in docs/QUEST_PICTURES.md)."""
    img, kind = _draw(slot)
    name = f"{slot.get('chapter', 'misc')}_{slot.get('slug', 'picture')}.png".lower()
    _write(PIC_DIR / name, _png(img))
    _cache().save()
    if slot.get("place") is False:
        LOOSE[name] = dict(slot, drawn=kind)
        return None
    return RESOURCE + name


_DESC = {"showcase": "a row of the section's items", "multiblock": "the multiblock, assembled and layer by layer",
         "machine": "one large render", "decor": "element tiles", "label": "its title only",
         "backdrop": "a quiet frame to put quests on", "rule": "a divider line"}


def _write_list():
    """docs/QUEST_PICTURES.md: every loose picture, for placing by hand."""
    rows = sorted(LOOSE.items(), key=lambda kv: (kv[1].get("chapter", ""), kv[0]))
    out = ["# Quest pictures (for placing by hand)", "",
           "Generated by tools/build_quests.py (tools/build_pictures.py); do not edit. The book places no pictures",
           "(user decision 2026-10-20): each page section has one ready-made picture in",
           "`pack/kubejs/assets/warbucks/textures/quests/pictures/`, shipped with the pack. To use one: open the quest",
           "book in edit mode, right-click an empty spot, Add Image, paste the texture path, and set width/height to the",
           "size below (or any size with the same aspect). Keep it clear of quests (captions sit along the bottom).", "",
           f"{len(rows)} pictures.", "",
           "| Texture | Size (cells) | Chapter | Section | What it shows |", "|---|---|---|---|---|"]
    for name, sl in rows:
        what = _DESC.get(sl.get("drawn"), sl.get("drawn", ""))
        cap = sl.get("title")
        out.append(f"| `{RESOURCE}{name}` | {sl.get('width', 0):g} x {sl.get('height', 0):g} | "
                   f"{sl.get('chapter_title') or sl.get('chapter')} (`{sl.get('chapter')}`) | {sl.get('section') or '-'} | "
                   f"{what}" + (f", captioned \"{cap}\"" if cap else "") + " |")
    LIST_DOC.write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")


def clean(keep):
    """Delete pictures whose file name (or resource location) is not in `keep` or rendered loose this run; then
    rewrite docs/QUEST_PICTURES.md (when anything was rendered loose)."""
    names = {k.rsplit("/", 1)[-1] for k in keep} | set(LOOSE)
    gone = 0
    if PIC_DIR.exists():
        for p in PIC_DIR.glob("*.png"):
            if p.name not in names:
                p.unlink()
                gone += 1
    if LOOSE:
        _write_list()
    return gone


# ---------------------------------------------------------------- demo

DEMO = [
    dict(chapter="mekanism", slug="basics", width=6, height=3, title="The first machines",
         nearby_items=["mekanism:metallurgic_infuser", "mekanism:enrichment_chamber", "mekanism:ingot_osmium"]),
    dict(chapter="t3", slug="ebf", width=7, height=4, nearby_items=["modern_industrialization:electric_blast_furnace",
                                                                    "modern_industrialization:cupronickel_coil"]),
    dict(chapter="t1", slug="coke", width=6, height=3, nearby_items=["modern_industrialization:coke_oven"]),
    dict(chapter="t1", slug="sbf", width=4, height=5, nearby_items=["modern_industrialization:steam_blast_furnace"]),
    dict(chapter="t1", slug="quarry", width=6, height=3, nearby_items=["modern_industrialization:steam_quarry"]),
    dict(chapter="t4", slug="hall", width=6, height=4, nearby_items=["modern_industrialization:hall_heroult_cell"]),
    dict(chapter="t4", slug="tower", width=6, height=4, nearby_items=["modern_industrialization:distillation_tower"]),
    dict(chapter="t3", slug="freezer", width=6, height=3, nearby_items=["modern_industrialization:vacuum_freezer"]),
    dict(chapter="t3", slug="equarry", width=6, height=4, nearby_items=["modern_industrialization:electric_quarry"]),
    dict(chapter="t2", slug="steam", width=5, height=2, title="Steam age", nearby_items=[
        "modern_industrialization:bronze_machine_casing", "modern_industrialization:bronze_boiler",
        "modern_industrialization:bronze_macerator", "modern_industrialization:bronze_drill", "modern_industrialization:bronze_ingot"]),
    dict(chapter="t0", slug="hammer", width=2, height=2, nearby_items=["modern_industrialization:forge_hammer"]),
    dict(chapter="ae2", slug="cells", width=3, height=5, title="Storage", nearby_items=[
        "ae2:controller", "ae2:drive", "ae2:item_storage_cell_1k", "ae2:crafting_terminal"]),
    dict(chapter="welcome", slug="hello", width=4, height=4, title="Welcome, demigod"),
    dict(chapter="tips", slug="banner", width=6, height=2),
    dict(chapter="create", slug="arc", width=8, height=3, title="Kinetics", nearby_items=[
        "create:cogwheel", "create:large_cogwheel", "create:shaft", "create:water_wheel", "create:mechanical_press", "create:andesite_alloy"]),
    dict(chapter="periodic", slug="chem", width=5, height=3, title="Elements", nearby_items=[
        "chemlib:hydrogen", "chemlib:oxygen", "chemlib:sodium_hydroxide", "alchemistry:dissolver", "chemlib:iron_ingot"]),
    dict(chapter="t3", slug="lv", width=6, height=2, title="LV machines", nearby_items=[
        "modern_industrialization:macerator", "modern_industrialization:electrolyzer", "modern_industrialization:chemical_reactor",
        "modern_industrialization:lv_diesel_generator"]),
]


def main():
    if "--demo" in sys.argv:
        _cache()
        DEMO_DIR.mkdir(parents=True, exist_ok=True)
        for slot in DEMO:
            img, kind = _draw(slot)
            name = f"{slot['chapter']}_{slot['slug']}.png"
            _write(DEMO_DIR / name, _png(img))
            print(f"{name:28} {kind:10} {img.width}x{img.height}")
        _cache().save()
        print(f"Samples in {DEMO_DIR}")
        return
    print(__doc__)


if __name__ == "__main__":
    main()
