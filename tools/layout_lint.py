#!/usr/bin/env python3
"""Visual lint of the FINAL FTB quest book: reads the generated SNBT (pack/config/ftbquests/quests), not the
Python sources, so it measures exactly what players will see, whatever tools/layout.py does.

Per chapter: quest count, page size (cells) and aspect, overlaps, line crossings, lines through quests, long
lines, line direction mix, quests too close, images over quests (iov: a quest box under art, a label or a caption;
backdrops and rules are meant to sit under quests and don't count), image covers quest (icv: a quest or link CENTRE
inside such a picture), caption covered (ccv: a quest box over a picture's caption, label text or backdrop title
tab), pictures overlapping each other (pov), quests outside every section image's column,
orthogonal line % (horizontal or vertical lines), lone quests (no visible line), shape/size variety, hidden lines, images, deps into other chapters with no quest link. Each chapter gets a
0-100 tidiness score and its worst issues.

usage:
  python tools/layout_lint.py                          lint our book
  python tools/layout_lint.py --chapters t1,t2 -v      a few chapters, every issue
  python tools/layout_lint.py --target 18x14           page-size target in cells (default 18x14, ATM10's median)
  python tools/layout_lint.py --compare "<ATM10>\\config\\ftbquests\\quests"   medians side by side
  python tools/layout_lint.py --strict                 exit 1 if any chapter has overlaps, lines through quests or a
                                                       covered caption (a quest on a header, banner or caption)
  python tools/layout_lint.py --book <quests folder>   lint another book (measure only; other books may be ARR)

Geometry follows FTB Quests: x/y is a quest's centre, a quest of size s is about s cells wide, y grows down,
lines run straight from the dependency (or a quest link to it) to the dependent; image x/y is its centre.
test/build_quest_preview.py --gallery imports this module (parse_snbt, load_book, lint_chapter).
"""
import argparse
import math
import pathlib
import re
import statistics
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUR_BOOK = ROOT / "pack/config/ftbquests/quests"
KJS_ASSETS = ROOT / "pack/kubejs/assets"
ATM10 = pathlib.Path.home() / "curseforge/minecraft/Instances/All the Mods 10 - ATM10/config/ftbquests/quests"

LONG = 6.0          # a line longer than this (cells) is "long"
CLOSE = 1.2         # centres closer than CLOSE * mean size are "too close"
OVERLAP_SLACK = 0.1  # boxes must overlap by more than this (cells) to count as an overlap
THROUGH = 0.42      # a line passing within THROUGH * size of a quest centre goes "through" it
ORTHO = 0.1         # a line with |dx| or |dy| below this (cells) is orthogonal (horizontal or vertical)


# ---------------------------------------------------------------- SNBT
_WS = re.compile(r"(?:\s|,)*")
_BARE = re.compile(r"[A-Za-z0-9_.+\-]+")
_NUM = re.compile(r"^[+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?([bBsSlLfFdD]?)$")


def parse_snbt(text):
    """FTB-style SNBT -> Python (dict / list / str / int / float / bool). Commas are optional."""
    pos = 0
    n = len(text)

    def ws():
        nonlocal pos
        pos = _WS.match(text, pos).end()

    def string(q):
        nonlocal pos
        pos += 1
        out = []
        while True:
            j = pos
            while j < n and text[j] != q and text[j] != "\\":
                j += 1
            out.append(text[pos:j])
            if j >= n:
                raise ValueError("unterminated string")
            if text[j] == "\\":
                c = text[j + 1]
                out.append({"n": "\n", "t": "\t"}.get(c, c))
                pos = j + 2
            else:
                pos = j + 1
                return "".join(out)

    def value():
        nonlocal pos
        ws()
        c = text[pos]
        if c == "{":
            pos += 1
            d = {}
            while True:
                ws()
                if text[pos] == "}":
                    pos += 1
                    return d
                if text[pos] in "\"'":
                    k = string(text[pos])
                else:
                    m = _BARE.match(text, pos)
                    k, pos = m.group(), m.end()
                ws()
                if text[pos] != ":":
                    raise ValueError(f"expected ':' at {pos}")
                pos += 1
                d[k] = value()
        if c == "[":
            pos += 1
            m = re.match(r"\s*[BIL]\s*;", text[pos:pos + 8])
            if m:
                pos += m.end()
            out = []
            while True:
                ws()
                if text[pos] == "]":
                    pos += 1
                    return out
                out.append(value())
        if c in "\"'":
            return string(c)
        m = _BARE.match(text, pos)
        if not m:
            raise ValueError(f"bad token at {pos}: {text[pos:pos + 20]!r}")
        pos = m.end()
        tok = m.group()
        if tok in ("true", "false"):
            return tok == "true"
        nm = _NUM.match(tok)
        if nm:
            suf = nm.group(1).lower()
            body = tok[:-1] if suf else tok
            if suf in ("f", "d") or "." in body or "e" in body.lower():
                return float(body)
            return int(body)
        return tok

    v = value()
    return v


def read_snbt(path):
    return parse_snbt(pathlib.Path(path).read_text(encoding="utf-8", errors="replace"))


# ---------------------------------------------------------------- book model
def _lang(folder):
    """Translation keys -> text: lang/en_us.snbt (one file) or lang/en_us/**.snbt (split, newer FTB)."""
    out = {}
    one = folder / "lang/en_us.snbt"
    files = [one] if one.exists() else sorted((folder / "lang/en_us").rglob("*.snbt"))
    for f in files:
        try:
            d = read_snbt(f)
        except Exception:
            continue
        for k, v in d.items():
            out[k] = v
    return out


def _text(v):
    if isinstance(v, list):
        v = " ".join(str(x) for x in v)
    return re.sub(r"&[0-9a-fk-or]", "", str(v or ""))


def _item_id(it):
    if isinstance(it, str):
        return it
    if isinstance(it, dict):
        return it.get("id") or it.get("item")
    return None


def task_icon(t):
    """(item id or None, short label) for a task: the item FTB would show, or a word for other kinds."""
    ty = t.get("type", "")
    if ty == "item":
        iid = _item_id(t.get("item"))
        if iid == "ftbfiltersystem:smart_filter":
            comp = (t.get("item") or {}).get("components", {})
            f = str(comp.get("ftbfiltersystem:filter", ""))
            m = re.search(r"(?<![_a-z])item\(([a-z0-9_.\-]+:[a-z0-9_./\-]+)\)", f)
            if m:
                return m.group(1), "any"
            m = re.search(r"item_tag\(([^)]*)\)", f)
            return None, "#" + (m.group(1).split(":")[-1].split("/")[-1][:6] if m else "tag")
        return iid, (iid or "?").split(":")[-1][:6]
    if ty == "checkmark":
        return None, "OK"
    label = {"dimension": "dim", "kill": "kill", "structure": "find", "biome": "biome", "xp": "xp",
             "advancement": "adv", "observation": "look", "location": "go", "stat": "stat", "fluid": "fluid",
             "forge_energy": "FE", "custom": "?"}.get(ty, ty[:5])
    if ty == "fluid":
        return None, "fluid"
    return None, label


def load_book(folder):
    """The book in `folder` (a config/ftbquests/quests directory) as plain dicts."""
    folder = pathlib.Path(folder)
    lang = _lang(folder)
    data = read_snbt(folder / "data.snbt") if (folder / "data.snbt").exists() else {}
    file_shape = data.get("default_quest_shape") or "circle"
    groups = []
    if (folder / "chapter_groups.snbt").exists():
        for g in read_snbt(folder / "chapter_groups.snbt").get("chapter_groups", []):
            groups.append({"id": g["id"], "title": _text(lang.get(f"chapter_group.{g['id']}.title") or g.get("title") or g["id"])})
    chapters, where = [], {}
    for f in sorted((folder / "chapters").glob("*.snbt")):
        try:
            c = read_snbt(f)
        except Exception as e:
            print(f"WARNING: cannot parse {f.name}: {e}", file=sys.stderr)
            continue
        cid = c.get("id", f.stem)
        dshape = c.get("default_quest_shape") or file_shape
        dhide = bool(c.get("default_hide_dependency_lines", False))
        quests = []
        for q in c.get("quests", []):
            tasks = q.get("tasks", [])
            iid, label = task_icon(tasks[0]) if tasks else (None, "")
            qicon = _item_id(q.get("icon"))
            title = _text(lang.get(f"quest.{q['id']}.title") or q.get("title") or "")
            quests.append({
                "id": q["id"], "x": float(q.get("x", 0)), "y": float(q.get("y", 0)),
                "size": float(q.get("size", 1.0) or 1.0), "shape": q.get("shape") or dshape,
                "deps": [d for d in q.get("dependencies", []) if isinstance(d, str)],
                "hide_dep": bool(q.get("hide_dependency_lines", dhide)),
                "hide_dependent": bool(q.get("hide_dependent_lines", False)),
                "optional": bool(q.get("optional", False)), "invisible": bool(q.get("invisible", False)),
                "icon": qicon or iid, "label": label,
                "title": title or (iid.split(":")[-1].replace("_", " ") if iid else label) or q["id"],
            })
            where[q["id"]] = cid
        links = [{"id": l.get("id"), "quest": l.get("linked_quest"), "x": float(l.get("x", 0)), "y": float(l.get("y", 0)),
                  "size": l.get("size"), "shape": l.get("shape")} for l in c.get("quest_links", [])]
        images = []
        for im in c.get("images", []):
            images.append({"x": float(im.get("x", 0)), "y": float(im.get("y", 0)), "w": float(im.get("width", 1)),
                           "h": float(im.get("height", 1)), "rot": float(im.get("rotation", 0) or 0),
                           "image": str(im.get("image", "")), "alpha": im.get("alpha", 255),
                           "order": int(im.get("order", 0) or 0)})
        chapters.append({"file": f.stem, "id": cid, "group": c.get("group", ""), "order": int(c.get("order_index", 0)),
                         "title": _text(lang.get(f"chapter.{cid}.title") or c.get("title") or f.stem),
                         "icon": _item_id(c.get("icon")), "quests": quests, "links": links, "images": images})
    order = {g["id"]: i for i, g in enumerate(groups)}
    chapters.sort(key=lambda c: (-1 if not c["group"] else order.get(c["group"], 999), c["order"], c["file"]))
    allq = {q["id"]: q for c in chapters for q in c["quests"]}
    for c in chapters:  # links take the linked quest's look unless they set their own
        for l in c["links"]:
            lq = allq.get(l["quest"], {})
            l["size"] = float(l["size"] or 1.0)  # FTB: a link is size 1 unless it sets its own
            l["shape"] = l["shape"] or lq.get("shape", "circle")
            l["title"] = "link: " + lq.get("title", str(l["quest"]))
            l["icon"], l["label"] = lq.get("icon"), lq.get("label", "")
    return {"folder": folder, "groups": groups, "chapters": chapters, "where": where, "quests": allq}


def chapter_lines(c, book):
    """Visible and hidden dependency lines of a chapter: dicts (a, b, hidden), a = dep node, b = quest node.
    Also returns the cross-chapter deps that have no quest link on this page.
    Mirrors FTB 2101's QuestPanel: every quest button AND every quest-link button draws a line to each of its
    quest's dependencies; a dependency resolves to the LAST button showing that quest (links come after quests, so
    a link wins over the quest itself). hide_dependency_lines on the dependent quest, or hide_dependent_lines on the
    dependency's quest, hide the line."""
    allq = book["quests"]
    btn = {q["id"]: q for q in c["quests"]}
    for l in c["links"]:
        btn[l["quest"]] = l  # last matching button wins
    owners = [(q, q) for q in c["quests"]] + [(l, allq[l["quest"]]) for l in c["links"] if l["quest"] in allq]
    lines, unlinked = [], []
    for node, q in owners:
        for d in q["deps"]:
            a = btn.get(d)
            if a is None:
                if node is q and d in book["where"]:
                    unlinked.append((q, d))
                continue
            aq = allq.get(a.get("quest", a["id"]), a)
            hidden = q["hide_dep"] or aq.get("hide_dependent", False)
            lines.append({"a": a, "b": node, "hidden": hidden})
    return lines, unlinked


# ---------------------------------------------------------------- geometry
def _seg_cross(p1, p2, p3, p4):
    def orient(a, b, c):
        v = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
        return 0 if abs(v) < 1e-9 else (1 if v > 0 else -1)
    o1, o2, o3, o4 = orient(p1, p2, p3), orient(p1, p2, p4), orient(p3, p4, p1), orient(p3, p4, p2)
    return o1 * o2 < 0 and o3 * o4 < 0


def _seg_dist(p, a, b):
    ax, ay = a
    dx, dy = b[0] - ax, b[1] - ay
    L = dx * dx + dy * dy
    t = 0 if L == 0 else max(0.0, min(1.0, ((p[0] - ax) * dx + (p[1] - ay) * dy) / L))
    return math.hypot(p[0] - ax - t * dx, p[1] - ay - t * dy), t


def image_box(im):
    """Axis-aligned bounds (x0, y0, x1, y1) of an image, rotation included."""
    a = math.radians(im["rot"])
    hw = (abs(math.cos(a)) * im["w"] + abs(math.sin(a)) * im["h"]) / 2
    hh = (abs(math.sin(a)) * im["w"] + abs(math.cos(a)) * im["h"]) / 2
    return im["x"] - hw, im["y"] - hh, im["x"] + hw, im["y"] + hh


# ---------------------------------------------------------------- pictures (mirror pages)
# tools/layout.py names every picture after what it is (pack/kubejs/assets/warbucks/textures/quests/pictures/
# <chapter>_<prefix>...png): bg_ backdrop (quests sit on it, no caption), bg<corner>_ backdrop with a title tab in
# that corner, rule_ divider line, lab_ label (the whole picture is its text), cap_ caption along the bottom, capt_
# caption along the top, art_ no caption. Banners and section headers are labels too. Other images (other books)
# count as captioned art with the caption along the bottom.
PIC_PX = 48          # tools/build_pictures.py: px per cell (CELL) and the longest side (MAX_SIDE)
PIC_MAX = 1024


def caption_band(w, h):
    """Height (cells) of the caption strip tools/build_pictures.py draws on a w x h picture: the larger of the
    showcase caption and the multiblock title + note, plus a small margin."""
    k = min(PIC_PX, PIC_MAX / max(w, h, 1e-6))
    hp = h * k
    show = max(13, min(26, hp // 7)) * 1.5 + 8
    cap = max(12, min(22, hp // 9))
    multi = cap * 1.4 + max(9, int(cap * 0.6)) * 1.4 + 9
    return min(h, max(show, multi) / k)


def tab_box(box, corner):
    """The title tab of a backdrop (tools/build_pictures.py draws it inside this box at that corner)."""
    x0, y0, x1, y1 = box
    tw, th = min(0.6 * (x1 - x0), 6.0), 0.6
    xa = x0 + 0.15 if corner[1] == "l" else x1 - 0.15 - tw
    ya = y0 + 0.15 if corner[0] == "t" else y1 - 0.15 - th
    return xa, ya, xa + tw, ya + th


def picture_kind(im, chapter_file):
    """(kind, caption box or None) of an image: kind is backdrop, rule, label or art (see above)."""
    name = im["image"].rsplit("/", 1)[-1]
    box = image_box(im)
    if "/quests/pictures/" in im["image"]:
        stem = name[:-4]
        stem = stem[len(chapter_file) + 1:] if stem.startswith(chapter_file + "_") else stem
        pre = stem.split("_", 1)[0]
        if pre == "bg":
            return "backdrop", None
        if pre.startswith("bg") and len(pre) == 4:
            return "backdrop", tab_box(box, pre[2:])
        if pre == "rule":
            return "rule", None
        if pre == "art":
            return "art", None
        if pre == "lab":
            return "label", box
        if pre in ("cap", "capt") and not im["rot"]:
            band = caption_band(im["w"], im["h"])
            x0, y0, x1, y1 = box
            return "art", ((x0 + 0.1, y1 - band, x1 - 0.1, y1) if pre == "cap" else (x0 + 0.1, y0, x1 - 0.1, y0 + band))
    if "/quests/sections/" in im["image"] or im["image"].endswith(f"/quests/{chapter_file}.png"):
        return "label", box
    if im["rot"]:
        return "art", box
    band = caption_band(im["w"], im["h"])
    x0, y0, x1, y1 = box
    return "art", (x0 + 0.1, y1 - band, x1 - 0.1, y1)


_BOXY = {"square", "rsquare"}


def _overlap(a, b, dx, dy, r):
    """Shape-aware overlap of two quest nodes (r = mean size, i.e. the sum of the half-widths).
    Diamonds tile at half-cell offsets (ATM10 does this), so they use the L1 distance; two square shapes use
    their boxes; everything else (circle, hexagon, octagon, gear, pentagon, mixed pairs) is treated as round."""
    lim = r - OVERLAP_SLACK
    sa, sb = a["shape"], b["shape"]
    if sa == "diamond" and sb == "diamond":
        return dx + dy < lim
    if sa in _BOXY and sb in _BOXY:
        return dx < lim and dy < lim
    return math.hypot(dx, dy) < lim


def _pos(n):
    return (n["x"], n["y"])


def lint_chapter(c, book, target=(18, 14)):
    """Metrics, issues (worst first) and a 0-100 tidiness score for one chapter."""
    nodes = c["quests"] + c["links"]
    lines, unlinked = chapter_lines(c, book)
    vis = [l for l in lines if not l["hidden"]]
    m = {"quests": len(c["quests"]), "links": len(c["links"]), "images": len(c["images"]),
         "lines": len(vis), "hidden": len(lines) - len(vis),
         "hidden_quests": sum(1 for q in c["quests"] if q["hide_dep"]),
         "shapes": len({q["shape"] for q in c["quests"]}), "sizes": len({q["size"] for q in c["quests"]})}
    issues = []  # (weight, text)
    if nodes:
        x0 = min(n["x"] - n["size"] / 2 for n in nodes)
        x1 = max(n["x"] + n["size"] / 2 for n in nodes)
        y0 = min(n["y"] - n["size"] / 2 for n in nodes)
        y1 = max(n["y"] + n["size"] / 2 for n in nodes)
    else:
        x0 = y0 = x1 = y1 = 0
    w, h = x1 - x0, y1 - y0
    m.update(w=round(w, 1), h=round(h, 1), aspect=round(w / h, 2) if h else 0.0, bbox=(x0, y0, x1, y1))

    # overlaps / too close
    ov = close = 0
    for i, a in enumerate(nodes):
        for b in nodes[i + 1:]:
            r = (a["size"] + b["size"]) / 2
            dx, dy = abs(a["x"] - b["x"]), abs(a["y"] - b["y"])
            if _overlap(a, b, dx, dy, r):
                ov += 1
                issues.append((10, f"overlap: '{a['title']}' and '{b['title']}' at ({a['x']:g},{a['y']:g})"))
            elif math.hypot(dx, dy) < CLOSE * r:
                close += 1
                issues.append((1, f"too close: '{a['title']}' and '{b['title']}' ({math.hypot(dx, dy):.2f} cells)"))
    m["overlaps"], m["close"] = ov, close

    # lines: length, direction, long, crossings, through quests
    lengths, dirs = [], {"R": 0, "D": 0, "L": 0, "U": 0}
    long_n = ortho = 0
    for l in vis:
        dx, dy = l["b"]["x"] - l["a"]["x"], l["b"]["y"] - l["a"]["y"]
        L = math.hypot(dx, dy)
        lengths.append(L)
        ortho += abs(dx) < ORTHO or abs(dy) < ORTHO
        if L > 1e-9:
            dirs["R" if dx > 0 else "L"] += abs(dx) >= abs(dy)
            dirs["D" if dy > 0 else "U"] += abs(dy) > abs(dx)
        if L > LONG:
            long_n += 1
            issues.append((2, f"long line ({L:.1f}): '{l['a']['title']}' -> '{l['b']['title']}'"))
    m["median_len"] = round(statistics.median(lengths), 2) if lengths else 0.0
    m["long"], m["dirs"] = long_n, dirs
    m["ortho_n"], m["ortho"] = ortho, round(100 * ortho / len(vis)) if vis else 100
    # quests with no visible line at all (on a page that has lines): they look scattered
    tied = {id(l["a"]) for l in vis} | {id(l["b"]) for l in vis}
    m["lone"] = sum(1 for q in c["quests"] if id(q) not in tied) if lines else 0
    boxes = []
    for l in vis:
        a, b = _pos(l["a"]), _pos(l["b"])
        boxes.append((min(a[0], b[0]), min(a[1], b[1]), max(a[0], b[0]), max(a[1], b[1]), a, b, l))
    cross = 0
    for i, A in enumerate(boxes):
        for B in boxes[i + 1:]:
            if A[2] < B[0] or B[2] < A[0] or A[3] < B[1] or B[3] < A[1]:
                continue
            if {id(A[6]["a"]), id(A[6]["b"])} & {id(B[6]["a"]), id(B[6]["b"])}:
                continue
            if _seg_cross(A[4], A[5], B[4], B[5]):
                cross += 1
                issues.append((3, f"crossing: '{A[6]['a']['title']}'->'{A[6]['b']['title']}' x "
                                  f"'{B[6]['a']['title']}'->'{B[6]['b']['title']}'"))
    m["crossings"] = cross
    through = 0
    for bx0, by0, bx1, by1, a, b, l in boxes:
        for n in nodes:
            if n is l["a"] or n is l["b"]:
                continue
            r = THROUGH * n["size"]
            if n["x"] < bx0 - r or n["x"] > bx1 + r or n["y"] < by0 - r or n["y"] > by1 + r:
                continue
            d, t = _seg_dist(_pos(n), a, b)
            if d < r and 0 < t < 1:
                through += 1
                issues.append((6, f"line through quest: '{l['a']['title']}'->'{l['b']['title']}' crosses '{n['title']}'"))
    m["through"] = through

    # images: backdrops and rules are meant to sit under quests; everything else (art, labels, captions) is not
    img_ov = covers = cap_cov = pic_ov = 0
    kinds = [picture_kind(im, c["file"]) for im in c["images"]]
    for im, (kind, cap) in zip(c["images"], kinds):
        if kind in ("backdrop", "rule"):
            if cap is None:
                continue
        ix0, iy0, ix1, iy1 = image_box(im)
        iname = im["image"].split("/")[-1]
        for n in nodes:
            r = n["size"] / 2 - OVERLAP_SLACK
            nb = (n["x"] - r, n["y"] - r, n["x"] + r, n["y"] + r)
            if kind not in ("backdrop", "rule") and nb[2] > ix0 and nb[0] < ix1 and nb[3] > iy0 and nb[1] < iy1:
                img_ov += 1
                issues.append((4, f"image {iname} covers '{n['title']}'"))
                if ix0 <= n["x"] <= ix1 and iy0 <= n["y"] <= iy1:
                    covers += 1
            if cap and nb[2] > cap[0] and nb[0] < cap[2] and nb[3] > cap[1] and nb[1] < cap[3]:
                cap_cov += 1
                issues.append((5, f"caption covered: {iname} under '{n['title']}'"))
    ours = [(im, k) for im, (k, _) in zip(c["images"], kinds) if "/quests/pictures/" in im["image"] and k != "rule"]
    def within(x, y):  # x lies entirely on y (a label on a backdrop: drawn that way on purpose)
        return x[0] >= y[0] - 0.01 and x[1] >= y[1] - 0.01 and x[2] <= y[2] + 0.01 and x[3] <= y[3] + 0.01
    for i, (a, ka) in enumerate(ours):
        A = image_box(a)
        for b, kb in ours[i + 1:]:
            B = image_box(b)
            if (ka == "backdrop" and within(B, A)) or (kb == "backdrop" and within(A, B)):
                continue
            if min(A[2], B[2]) - max(A[0], B[0]) > 0.05 and min(A[3], B[3]) - max(A[1], B[1]) > 0.05:
                pic_ov += 1
                issues.append((3, f"pictures overlap: {a['image'].split('/')[-1]} and {b['image'].split('/')[-1]}"))
    m["image_overlaps"], m["image_covers"], m["caption_covered"], m["picture_overlaps"] = img_ov, covers, cap_cov, pic_ov
    miss = 0  # images whose texture isn't in our KubeJS assets (only checked for namespaces we ship there)
    for im in c["images"]:
        ns, _, rest = im["image"].partition(":")
        if rest and ns == "warbucks" and (KJS_ASSETS / ns).is_dir() and not (KJS_ASSETS / ns / rest).exists():
            miss += 1
            issues.append((8, f"image texture missing: {im['image']}"))
    m["missing_images"] = miss
    outside = 0
    if len(c["images"]) >= 2:
        cols = [image_box(im) for im in c["images"]]
        for q in c["quests"]:
            if not any(cx0 - 0.01 <= q["x"] <= cx1 + 0.01 for cx0, _, cx1, _ in cols):
                outside += 1
        if outside:
            issues.append((2 * outside / max(1, len(c["quests"])) * 5,
                           f"{outside} quest(s) outside every section image's column"))
    m["outside"] = outside
    m["unlinked"] = len(unlinked)
    for q, d in unlinked[:5]:
        dq = book["quests"].get(d, {})
        issues.append((1, f"dep to another chapter without a link: '{q['title']}' needs '{dq.get('title', d)}'"))

    tw, th = target
    excess = max(0.0, w / tw - 1) + max(0.0, h / th - 1)
    if excess > 0.25:
        issues.append((excess * 3, f"page {w:.0f}x{h:.0f} cells is larger than the {tw}x{th} target"))
    if m["aspect"] and (m["aspect"] > 3 or m["aspect"] < 1 / 3):
        issues.append((3, f"extreme aspect ratio {m['aspect']}"))

    nl = max(1, len(vis))
    nq = max(1, len(c["quests"]))
    pen = (min(40, 10 * ov) + min(30, 5 * through) + min(20, 60 * cross / nl) + min(10, 40 * long_n / nl)
           + min(10, 20 * close / nq) + min(10, 3 * img_ov) + min(10, 4 * cap_cov) + min(6, 2 * pic_ov) + min(10, 4 * miss) + min(10, 10 * outside / nq) + min(5, len(unlinked))
           + min(15, 7.5 * max(0.0, excess - 0.25)) + (3 if m["aspect"] and (m["aspect"] > 3 or m["aspect"] < 1 / 3) else 0))
    m["score"] = max(0, round(100 - pen))
    issues.sort(key=lambda t: -t[0])
    # collapse repeats of the same kind, keep the worst few
    seen, top = {}, []
    for wgt, text in issues:
        kind = text.split(":")[0]
        seen[kind] = seen.get(kind, 0) + 1
        if seen[kind] <= 2:
            top.append(text)
    m["issues"] = top
    m["all_issues"] = [t for _, t in issues]
    return m


def lint_book(folder, target=(18, 14), only=None):
    book = load_book(folder)
    out = []
    for c in book["chapters"]:
        if only and c["file"] not in only:
            continue
        out.append((c, lint_chapter(c, book, target)))
    return book, out


# ---------------------------------------------------------------- reports
def _med(xs):
    xs = list(xs)
    return statistics.median(xs) if xs else 0


def summary(book, results):
    lens = []
    for c, m in results:
        lines, _ = chapter_lines(c, book)
        lens += [math.hypot(l["b"]["x"] - l["a"]["x"], l["b"]["y"] - l["a"]["y"]) for l in lines if not l["hidden"]]
    tot_dirs = {k: sum(m["dirs"][k] for _, m in results) for k in "RDLU"}
    nd = max(1, sum(tot_dirs.values()))
    nlines = max(1, len(lens))
    return {
        "chapters": len(results), "quests": sum(m["quests"] for _, m in results),
        "quests/chapter": _med(m["quests"] for _, m in results),
        "width": _med(m["w"] for _, m in results), "height": _med(m["h"] for _, m in results),
        "aspect": _med(m["aspect"] for _, m in results),
        "line length (all lines)": round(_med(lens), 2),
        "long lines %": round(100 * sum(1 for x in lens if x > LONG) / nlines, 1),
        "crossings/chapter": _med(m["crossings"] for _, m in results),
        "through/chapter": _med(m["through"] for _, m in results),
        "overlaps/chapter": _med(m["overlaps"] for _, m in results),
        "too close/chapter": _med(m["close"] for _, m in results),
        "hidden lines %": round(100 * sum(m["hidden"] for _, m in results)
                                / max(1, sum(m["hidden"] + m["lines"] for _, m in results)), 1),
        "images/chapter": _med(m["images"] for _, m in results),
        "image covers quest (total)": sum(m["image_covers"] for _, m in results),
        "caption covered (total)": sum(m["caption_covered"] for _, m in results),
        "pictures overlapping (total)": sum(m["picture_overlaps"] for _, m in results),
        "shapes/chapter": _med(m["shapes"] for _, m in results),
        "sizes/chapter": _med(m["sizes"] for _, m in results),
        "dirs R/D/L/U %": "/".join(str(round(100 * tot_dirs[k] / nd)) for k in "RDLU"),
        "orthogonal lines %": round(100 * sum(m["ortho_n"] for _, m in results) / nlines, 1),
        "orthogonal %/chapter": _med(m["ortho"] for _, m in results),
        "lone quests (no line)": sum(m["lone"] for _, m in results),
        "tidiness": _med(m["score"] for _, m in results),
    }


def report(book, results, verbose=False, target=(18, 14)):
    lines = []
    hdr = (f"{'chapter':16} {'q':>4} {'W x H':>11} {'asp':>5} {'ovl':>4} {'thru':>4} {'cross':>5} {'long':>4} "
           f"{'close':>5} {'R/D/L/U':>13} {'orth%':>5} {'lone':>4} {'img':>3} {'iov':>3} {'icv':>3} {'ccv':>3} {'pov':>3} {'out':>3} {'shp':>3} {'siz':>3} {'hid':>4} "
           f"{'unl':>3} {'score':>5}")
    lines.append(f"Book: {book['folder']}   target page {target[0]}x{target[1]} cells")
    lines.append(hdr)
    lines.append("-" * len(hdr))
    for c, m in results:
        d = m["dirs"]
        lines.append(f"{c['file'][:16]:16} {m['quests']:4} {m['w']:5.0f} x {m['h']:<4.0f} {m['aspect']:5.2f} {m['overlaps']:4} "
                     f"{m['through']:4} {m['crossings']:5} {m['long']:4} {m['close']:5} "
                     f"{d['R']:>3}/{d['D']}/{d['L']}/{d['U']:<3} {m['ortho']:5} {m['lone']:4} {m['images']:3} {m['image_overlaps']:3} {m['image_covers']:3} {m['caption_covered']:3} {m['picture_overlaps']:3} {m['outside']:3} "
                     f"{m['shapes']:3} {m['sizes']:3} {m['hidden']:4} {m['unlinked']:3} {m['score']:5}")
    lines.append("")
    lines.append("Worst chapters:")
    for c, m in sorted(results, key=lambda r: r[1]["score"])[:8]:
        lines.append(f"  {m['score']:3}  {c['file']} ({c['title']})")
        for t in (m["all_issues"] if verbose else m["issues"][:5]):
            lines.append(f"         - {t}")
    if verbose:
        lines.append("")
        lines.append("All chapters' issues:")
        for c, m in results:
            if m["all_issues"]:
                lines.append(f"  {c['file']} ({m['score']}):")
                lines += [f"     - {t}" for t in m["all_issues"]]
    return "\n".join(lines)


def compare(ours, theirs, name="other"):
    keys = list(ours)
    w = max(len(k) for k in keys)
    out = [f"{'median':{w}}  {'ours':>14}  {name:>14}", "-" * (w + 32)]
    for k in keys:
        a, b = ours[k], theirs.get(k, "")
        fa = f"{a:.2f}".rstrip("0").rstrip(".") if isinstance(a, float) else str(a)
        fb = f"{b:.2f}".rstrip("0").rstrip(".") if isinstance(b, float) else str(b)
        out.append(f"{k:{w}}  {fa:>14}  {fb:>14}")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--book", default=str(OUR_BOOK), help="config/ftbquests/quests folder to lint (default: ours)")
    ap.add_argument("--chapters", help="comma-separated chapter file names")
    ap.add_argument("--target", default="18x14", help="page-size target WxH in cells (default 18x14)")
    ap.add_argument("--compare", nargs="?", const=str(ATM10), help="another book's quests folder (default: ATM10)")
    ap.add_argument("--strict", action="store_true", help="exit 1 when a chapter has overlaps or lines through quests")
    ap.add_argument("-v", "--verbose", action="store_true", help="list every issue")
    ap.add_argument("-o", "--out", help="also write the report to this file")
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    tw, th = (float(v) for v in args.target.lower().split("x"))
    target = (tw, th)
    only = set(args.chapters.split(",")) if args.chapters else None
    book, results = lint_book(args.book, target, only)
    text = report(book, results, args.verbose, target)
    ours = summary(book, results)
    text += "\n\n" + compare(ours, {}, "") if not args.compare else ""
    if args.compare:
        obook, ores = lint_book(args.compare, target)
        name = "ATM10" if "ATM10" in args.compare or "All the Mods" in args.compare else pathlib.Path(args.compare).parent.parent.name[:14]
        text += "\n\n" + compare(ours, summary(obook, ores), name)
    print(text)
    if args.out:
        pathlib.Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        pathlib.Path(args.out).write_text(text + "\n", encoding="utf-8", newline="\n")
    if args.strict:
        bad = [c["file"] for c, m in results if m["overlaps"] or m["through"] or m["caption_covered"]]
        if bad:
            print(f"\nSTRICT: overlaps, lines through quests or covered captions (headers, banners) in: "
                  f"{', '.join(bad)}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
