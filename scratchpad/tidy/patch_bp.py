import pathlib
p = pathlib.Path("tools/build_pictures.py")
s = p.read_text(encoding="utf-8")


def rep(old, new):
    global s
    assert old in s, old[:80]
    s = s.replace(old, new, 1)


rep('''  decor       an element-tile motif (chapters without item context)''',
    '''  decor       an element-tile motif (chapters without item context)
  backdrop    a quiet framed panel that quests sit on (tier tint, faint lab grid, no renders, no caption); an
              optional title tab in one corner (slot["tab"] = "tl"/"tr"/"bl"/"br", text = slot["title"])
  label       a low strip with only its title (ATM10 labels its rows this way)
  rule        a thin divider line (ATM10's table lines)
slot["caption"] = "bottom", "top" or None places the caption of the art kinds (no key: bottom when there is a
title); tools/layout.py decides it so that no quest sits on a caption (tools/layout_lint.py checks it).''')

rep('''    ty = (img.height - size * 1.45 - margin * 0.6) if y is None else y''',
    '''    ty = (img.height - size * 1.45 - margin * 0.6) if y is None else (margin * 0.6) if y == "top" else y''')

rep('''def _showcase(w, h, color, items, title):
    img = _panel(w, h, color)
    n = len(items)
    cap = max(13, min(26, h // 7)) if title else 0
    cap_h = int(cap * 1.5) + 4 if title else 0''',
    '''def _showcase(w, h, color, items, title, top=False):
    img = _panel(w, h, color)
    n = len(items)
    cap = max(13, min(26, h // 7)) if title else 0
    cap_h = int(cap * 1.5) + 4 if title else 0
    oy = cap_h if top else 0  # caption along the top: the renders move down''')

rep('''                cy += amp * (t * t * 2 - 1) * 0.5 + amp * 0.25
        sh, off = _shadow(r, max(2, size // 12), max(2, size // 14))
        img.alpha_composite(sh, (int(cx - r.width / 2 - off), int(cy - r.height / 2 - off)))
    _caption(img, title, cap)
    return img''',
    '''                cy += amp * (t * t * 2 - 1) * 0.5 + amp * 0.25
        cy += oy
        sh, off = _shadow(r, max(2, size // 12), max(2, size // 14))
        img.alpha_composite(sh, (int(cx - r.width / 2 - off), int(cy - r.height / 2 - off)))
    _caption(img, title, cap, y="top" if top else None)
    return img''')

rep('''def _machine(w, h, color, item, title):
    img = _panel(w, h, color)
    cap = max(13, min(28, h // 6)) if title else 0''',
    '''def _machine(w, h, color, item, title, top=False):
    img = _panel(w, h, color)
    cap = max(13, min(26, h // 7)) if title else 0  # the showcase's caption size (tools/layout_lint.caption_band)''')
rep('''    sh, off = _shadow(r, max(2, size // 12), max(2, size // 14))
    img.alpha_composite(sh, (int(w / 2 - r.width / 2 - off), int((h - cap_h) / 2 - r.height / 2 - off)))
    _caption(img, title, cap)
    return img''',
    '''    sh, off = _shadow(r, max(2, size // 12), max(2, size // 14))
    cy = (h - cap_h) / 2 + (cap_h if top else 0)
    img.alpha_composite(sh, (int(w / 2 - r.width / 2 - off), int(cy - r.height / 2 - off)))
    _caption(img, title, cap, y="top" if top else None)
    return img''')

rep('''def _multiblock(w, h, color, key, machine_id, title):''',
    '''def _multiblock(w, h, color, key, machine_id, title, top=False, bare=False):''')
rep('''    cap_h = int(cap * 1.4) + int(note_sz * 1.35) + 2''',
    '''    cap_h = 0 if bare else int(cap * 1.4) + int(note_sz * 1.35) + 2
    oy = cap_h if top else 0  # caption along the top: the diagram moves down''')
rep('''    if stacked:
        mx, my = pad, pad
        rx, ry = pad, pad + main_h
    else:
        mx, my = pad, pad
        rx, ry = pad + main_w, pad''',
    '''    if stacked:
        mx, my = pad, pad + oy
        rx, ry = pad, pad + main_h + oy
    else:
        mx, my = pad, pad + oy
        rx, ry = pad + main_w, pad + oy''')
rep('''    note_y = h - int(note_sz * 1.4) - 5
    _caption(img, shape.get("note", ""), note_sz, y=note_y, fill=GOLD + (230,), weight=2)
    _caption(img, title or shape["title"], cap, y=note_y - int(cap * 1.35))
    return img''',
    '''    if bare:
        return img
    if top:
        _caption(img, title or shape["title"], cap, y=4)
        _caption(img, shape.get("note", ""), note_sz, y=4 + int(cap * 1.35), fill=GOLD + (230,), weight=2)
        return img
    note_y = h - int(note_sz * 1.4) - 5
    _caption(img, shape.get("note", ""), note_sz, y=note_y, fill=GOLD + (230,), weight=2)
    _caption(img, title or shape["title"], cap, y=note_y - int(cap * 1.35))
    return img''')

rep('''def _decor(w, h, color, chapter, slug, title):''',
    '''def _decor(w, h, color, chapter, slug, title, top=False):''')
rep('''    area_w, area_h = w - 2 * pad, h - cap_h - 2 * pad
    ring = area_h''',
    '''    area_w, area_h = w - 2 * pad, h - cap_h - 2 * pad
    oy = cap_h if top else 0
    ring = area_h''')
rep('''        cx, cy = w / 2, pad + area_h / 2
''', '''        cx, cy = w / 2, pad + area_h / 2 + oy
''')
rep('''        pts = [(pad + size / 2 + i * (size + gap), pad + area_h / 2) for i in range(n)]''',
    '''        pts = [(pad + size / 2 + i * (size + gap), pad + area_h / 2 + oy) for i in range(n)]''')
rep('''        img.alpha_composite(sh, (int(x - size / 2 - off), int(y - size / 2 - off)))
    _caption(img, title, cap)
    return img
''', '''        img.alpha_composite(sh, (int(x - size / 2 - off), int(y - size / 2 - off)))
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
    k = max(6, int(px * 0.6))  # gold corner marks
    for x, y, sx, sy in ((0, 0, 1, 1), (w - 1, 0, -1, 1), (0, h - 1, 1, -1), (w - 1, h - 1, -1, -1)):
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
''')

rep('''def _pick_kind(slot, items):
    kind = slot.get("kind")
    if kind in ("showcase", "machine", "multiblock", "decor"):''',
    '''def _pick_kind(slot, items):
    kind = slot.get("kind")
    if kind in ("backdrop", "label", "rule"):
        return kind
    if kind in ("showcase", "machine", "multiblock", "decor"):''')

rep('''    w, h = _size(slot)
    color = TIER_COLORS.get(chapter, CYAN)
    title = slot.get("title")
    seen, items = set(), []''',
    '''    w, h = _size(slot)
    px = w / max(1e-6, float(slot.get("width") or 4))  # pixels per cell
    color = TIER_COLORS.get(chapter, CYAN)
    title = slot.get("title")
    top = slot.get("caption") == "top"
    placed = "caption" in slot  # tools/layout.py placed the caption (None: no spot clear of quests)
    seen, items = set(), []''')

rep('''    kind = _pick_kind(slot, items)
    img = None
    if kind == "multiblock":
        mid = next(i for i in items if i.split(":", 1)[-1] in SHAPES)
        img = _multiblock(w, h, color, mid.split(":", 1)[-1], mid, title)
    elif kind == "machine":
        for it in items:
            img = _machine(w, h, color, it, title or _name(it))''',
    '''    kind = _pick_kind(slot, items)
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
            img = _machine(w, h, color, it, title if placed else (title or _name(it)), top=top)''')
rep('''    if kind == "showcase" and img is None:
        img = _showcase(w, h, color, items[:6], title)
        if img is None and items:  # no icons at all: try a wider net before giving up on item art
            img = _showcase(w, h, color, items[6:12], title)
    if img is None:
        kind = "decor"
        img = _decor(w, h, color, chapter, slug, title)''',
    '''    if kind == "showcase" and img is None:
        img = _showcase(w, h, color, items[:6], title, top=top)
        if img is None and items:  # no icons at all: try a wider net before giving up on item art
            img = _showcase(w, h, color, items[6:12], title, top=top)
    if img is None:
        kind = "decor"
        img = _decor(w, h, color, chapter, slug, title, top=top)''')
p.write_text(s, encoding="utf-8", newline="\n")
print("patched")
