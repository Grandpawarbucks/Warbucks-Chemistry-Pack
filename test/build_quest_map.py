#!/usr/bin/env python3
"""Build test/preview/map/: an interactive "quest-book map" of the FINAL generated FTB Quests book.

Reads the SNBT the game reads (data.snbt, chapter_groups.snbt, chapters/*.snbt, lang/en_us(.snbt|/), reward_tables/),
so it shows whatever the generator produced, however chapters and groups are arranged.

Output (git-ignored, mod textures must not go in the public repo):
  test/preview/map/quest-map.html   the viewer (vanilla JS, no network)
  test/preview/map/quest-data.js    the book as data (window.QUEST_MAP = {...})
  test/preview/map/icons.png        every item icon in one 32 px sprite sheet
  test/preview/map/images.webp      every chapter image (banners, section art) in one atlas

Viewer: sidebar of chapters by group (search box: chapters, quest titles, item names); canvas with the chapter at
its real FTB positions, shapes and sizes, dependency lines (hidden ones appear on hover), quest links, chapter
images, item icons with the item name under each quest; click a quest for its text, tasks, rewards and links.

Icons come from test/build_quest_preview.py's IconCache (cache in test/preview/icons; needs test/server/mods).
Item, entity, biome, dimension and structure names come from test/ids.tsv.

usage:
  .venv\\Scripts\\python.exe test/build_quest_map.py                     build from pack/config/ftbquests/quests
  .venv\\Scripts\\python.exe test/build_quest_map.py --book <quests dir> --out <dir>
  then: python -m http.server 8767 -d test/preview/map  and open http://localhost:8767/quest-map.html
  (opening quest-map.html straight from disk also works)
"""
import argparse
import datetime
import io
import json
import math
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "test"))

DEFAULT_BOOK = ROOT / "pack/config/ftbquests/quests"
DEFAULT_OUT = ROOT / "test/preview/map"
ICON = 32          # sprite cell size (IconCache icons are 32x32)
ICON_COLS = 64     # sprite sheet is ICON_COLS * ICON px wide
ATLAS_W = 2052     # image atlas width (4 images of IMG_MAX px per shelf)
IMG_MAX = 512      # chapter images wider than this are scaled down (keeps the atlas small for phones)

# quest keys handled explicitly; any other boolean flag that is true is listed as-is in the panel
KNOWN = {"id", "x", "y", "size", "shape", "dependencies", "tasks", "rewards", "icon", "title", "subtitle",
         "description", "optional", "hide_dependency_lines", "hide_dependent_lines", "invisible",
         "hide_until_deps_complete", "hide_until_deps_visible", "can_repeat", "dependency_requirement",
         "min_width", "disable_jei", "hide_text_until_complete", "hide_details_until_startable", "secret"}
FLAG_TEXT = {
    "optional": "Optional", "invisible": "Hidden (invisible until unlocked)", "secret": "Secret",
    "hide_until_deps_complete": "Hidden until its dependencies are complete",
    "hide_until_deps_visible": "Hidden until its dependencies are visible",
    "hide_text_until_complete": "Text hidden until complete",
    "hide_details_until_startable": "Details hidden until startable",
    "can_repeat": "Repeatable", "hide_dependency_lines": "Hides its dependency lines",
    "hide_dependent_lines": "Hides lines to its dependents",
}


# ------------------------------------------------------------------ inputs
def load_names():
    """{kind: {id: name}} from test/ids.tsv (kind: item, block, entity, biome, dimension, structure, fluid)."""
    out = {}
    f = ROOT / "test/ids.tsv"
    if not f.exists():
        return out
    for line in f.read_text(encoding="utf-8").splitlines():
        if line.startswith("#"):
            continue
        i, t, n = (line.split("\t") + ["", ""])[:3]
        if n and not (n.startswith("(") and n.endswith(")")):  # "(KubeJS)" is a placeholder, not a name
            out.setdefault(t, {}).setdefault(i, n)
    # KubeJS items: displayName() in the startup scripts, then any lang file the pack ships
    items = out.setdefault("item", {})
    for js in sorted((ROOT / "pack/kubejs/startup_scripts").glob("*.js")):
        src = js.read_text(encoding="utf-8", errors="replace")
        for m in re.finditer(r"""create\(\s*['"]([a-z0-9_/]+)['"](?:(?!create\().)*?displayName\(\s*['"]([^'"]+)['"]""", src, re.S):
            items.setdefault("kubejs:" + m.group(1), m.group(2))
    for lf in sorted((ROOT / "pack/kubejs/assets").glob("*/lang/en_us.json")):
        try:
            lang = json.loads(lf.read_text(encoding="utf-8"))
        except ValueError:
            continue
        for k, v in lang.items():
            p = k.split(".")
            if len(p) == 3 and p[0] in ("item", "block"):
                items.setdefault(f"{p[1]}:{p[2]}", v)
    return out


def pretty(rid):
    s = str(rid).lstrip("#").split(":")[-1].split("/")[-1]
    return s.replace("_", " ").strip().title() or str(rid)


def table_hex(v):
    """A reward-table reference (long or hex string) -> the table's 16-digit hex id."""
    if isinstance(v, str):
        return v.upper()
    return "%016X" % (int(v) & 0xFFFFFFFFFFFFFFFF)


def item_of(it):
    if isinstance(it, str):
        return it, 1, {}
    if isinstance(it, dict):
        return it.get("id") or it.get("item"), int(it.get("count", 1) or 1), it.get("components") or {}
    return None, 1, {}


def as_list(v):
    if v is None:
        return []
    if isinstance(v, list):
        return [str(x) for x in v]
    return [str(v)]


class Book:
    def __init__(self, folder):
        from layout_lint import read_snbt, _lang
        self.folder = pathlib.Path(folder)
        self.read = read_snbt
        self.lang = _lang(self.folder)
        self.N = load_names()
        self.items = {}       # item id -> name (icons resolved later)
        self.warnings = []

    def L(self, key, default=None):
        v = self.lang.get(key)
        return default if v in (None, "", []) else v

    # names -----------------------------------------------------------
    def name(self, rid, kind="item"):
        rid = str(rid)
        N = self.N
        for k in ((kind,) if kind != "item" else ()) + ("item", "block", "fluid", "entity"):
            n = N.get(k, {}).get(rid)
            if n:
                return n
        return pretty(rid)

    def use_item(self, iid):
        if iid and ":" in str(iid):
            self.items.setdefault(iid, self.name(iid))
        return iid

    # tasks / rewards ---------------------------------------------------
    def task(self, t):
        ty = str(t.get("type", ""))
        if ty == "item":
            iid, _, comp = item_of(t.get("item"))
            n = int(t.get("count", 1) or 1)
            if iid == "ftbfiltersystem:smart_filter":
                f = str(comp.get("ftbfiltersystem:filter", ""))
                ids = re.findall(r"(?<![_a-z])item\(([a-z0-9_.\-]+:[a-z0-9_./\-]+)\)", f)
                tags = re.findall(r"item_tag\(([^)]*)\)", f)
                if tags and not ids:
                    return {"k": "tag", "tag": tags[0], "more": tags[1:], "n": n}
                if ids:
                    return {"k": "any", "i": [self.use_item(i) for i in ids], "tags": tags, "n": n}
                return {"k": "filter", "v": f, "n": n}
            return {"k": "item", "i": self.use_item(iid), "n": n}
        if ty == "kill":
            e = str(t.get("entity", ""))
            egg = e + "_spawn_egg" if ":" in e else None
            self.use_item(egg)
            return {"k": "kill", "e": e, "nm": self.name(e, "entity"), "n": int(t.get("value", 1) or 1), "egg": egg}
        if ty in ("dimension", "biome", "structure"):
            v = str(t.get(ty, ""))
            return {"k": ty, "v": v, "nm": ("any " + v) if v.startswith("#") else self.name(v, ty)}
        if ty == "checkmark":
            return {"k": "check"}
        if ty == "fluid":
            f = str(t.get("fluid", ""))
            return {"k": "fluid", "v": f, "nm": self.name(f, "fluid"), "n": int(t.get("amount", 1000) or 1000)}
        if ty == "xp":
            return {"k": "xp", "n": int(t.get("value", 1) or 1), "lv": bool(t.get("points") is False)}
        extra = {k: v for k, v in t.items() if k not in ("id", "type")}
        return {"k": "other", "type": ty, "v": json.dumps(extra, ensure_ascii=False)[:200]}

    def reward(self, r):
        ty = str(r.get("type", "item" if "item" in r else ""))
        if ty == "item":
            iid, cnt, _ = item_of(r.get("item"))
            return {"k": "item", "i": self.use_item(iid), "n": int(r.get("count", cnt) or cnt)}
        if ty in ("xp", "xp_levels"):
            return {"k": ty, "n": int(r.get("xp", r.get("xp_levels", 0)) or 0)}
        if ty in ("random", "choice", "loot", "all_table"):
            return {"k": ty, "t": table_hex(r.get("table_id", 0))}
        extra = {k: v for k, v in r.items() if k not in ("id", "type")}
        return {"k": "other", "type": ty, "v": json.dumps(extra, ensure_ascii=False)[:200]}

    # whole book --------------------------------------------------------
    def load(self):
        f = self.folder
        data = self.read(f / "data.snbt") if (f / "data.snbt").exists() else {}
        file_shape = data.get("default_quest_shape") or "circle"
        book_title = re.sub(r"&[0-9a-fk-or]", "", str(self.L("file.0000000000000001.title", data.get("title") or "Quest book")))
        groups = [{"id": "", "t": "Top chapters", "ch": []}]
        if (f / "chapter_groups.snbt").exists():
            for g in self.read(f / "chapter_groups.snbt").get("chapter_groups", []):
                gid = g["id"]
                groups.append({"id": gid, "t": str(self.L(f"chapter_group.{gid}.title", g.get("title") or gid)), "ch": []})
        gidx = {g["id"]: i for i, g in enumerate(groups)}

        raw = []
        for p in sorted((f / "chapters").glob("*.snbt")):
            try:
                raw.append((p, self.read(p)))
            except Exception as e:
                self.warnings.append(f"cannot parse {p.name}: {e}")
        raw.sort(key=lambda pc: (gidx.get(pc[1].get("group", ""), len(groups)), int(pc[1].get("order_index", 0) or 0), pc[0].stem))

        quests, chapters, rawq = {}, [], {}
        for ci, (p, c) in enumerate(raw):
            cid = str(c.get("id", p.stem))
            dshape = c.get("default_quest_shape") or file_shape
            dhide = bool(c.get("default_hide_dependency_lines", False))
            for q in c.get("quests", []):
                rawq[q["id"]] = (q, ci, dshape, dhide)
            g = c.get("group", "")
            if g not in gidx:
                if g:
                    self.warnings.append(f"{p.name}: unknown group {g}")
                g = ""
            groups[gidx[g]]["ch"].append(ci)
            chapters.append({"id": cid, "f": str(c.get("filename") or p.stem), "_raw": c,
                             "t": re.sub(r"&[0-9a-fk-or]", "", str(self.L(f"chapter.{cid}.title", c.get("title") or p.stem))),
                             "sub": as_list(self.L(f"chapter.{cid}.chapter_subtitle", c.get("subtitle"))),
                             "ic": self.use_item(item_of(c.get("icon"))[0])})

        dependents = {}
        for qid, (q, ci, dshape, dhide) in rawq.items():
            for d in q.get("dependencies", []) or []:
                if isinstance(d, str):
                    dependents.setdefault(d, []).append(qid)

        for qid, (q, ci, dshape, dhide) in rawq.items():
            tasks = [self.task(t) for t in q.get("tasks", []) or []]
            rewards = [self.reward(r) for r in q.get("rewards", []) or []]
            qicon = item_of(q.get("icon"))[0]
            first = next((t for t in tasks if t["k"] in ("item", "any")), None)
            ticon = (first["i"] if first["k"] == "item" else first["i"][0]) if first else None
            if not ticon:
                ticon = next((t.get("egg") for t in tasks if t["k"] == "kill"), None)
            icon = self.use_item(qicon) or ticon
            # label: the requirement's name (what the quest asks for), else the quest's own icon / title
            lab, more = None, 0
            items = [t for t in tasks if t["k"] in ("item", "any", "tag")]
            if items:
                t0 = items[0]
                lab = (self.name(t0["i"]) if t0["k"] == "item" else
                       "any " + self.name(t0["i"][0]) if t0["k"] == "any" else "any #" + t0["tag"].split(":")[-1])
                more = len(items) - 1
            elif tasks and tasks[0]["k"] in ("kill", "dimension", "biome", "structure", "fluid"):
                lab = tasks[0]["nm"]
            title = str(self.L(f"quest.{qid}.title", q.get("title") or "") or "")
            if not title:
                title = (self.name(ticon) if ticon else lab) or (tasks[0]["k"].title() if tasks else qid)
            if not lab:
                lab = re.sub(r"&[0-9a-fk-or]", "", title)
            if more:
                lab += f" +{more}"
            flags = [k for k in FLAG_TEXT if q.get(k) is True and not (k == "hide_dependency_lines" and dhide)]
            flags += [k for k, v in q.items() if k not in KNOWN and v is True]
            if q.get("dependency_requirement") and q["dependency_requirement"] != "all_completed":
                flags.append("deps: " + str(q["dependency_requirement"]).replace("_", " "))
            quests[qid] = {
                "c": ci, "t": title, "st": str(self.L(f"quest.{qid}.quest_subtitle", q.get("subtitle") or "") or ""),
                "d": as_list(self.L(f"quest.{qid}.quest_desc", q.get("description"))),
                "ic": icon, "lb": lab, "tk": tasks, "rw": rewards,
                "dp": [d for d in q.get("dependencies", []) or [] if isinstance(d, str)],
                "dn": dependents.get(qid, []), "fl": flags,
                "opt": bool(q.get("optional")),
                "_hd": bool(q.get("hide_dependency_lines", dhide)), "_hn": bool(q.get("hide_dependent_lines", False)),
                "_sh": q.get("shape") or dshape, "_sz": float(q.get("size", 1.0) or 1.0),
                "_x": float(q.get("x", 0)), "_y": float(q.get("y", 0)),
            }

        images = []  # (image resource, ) collected for the atlas
        img_idx = {}
        for ci, ch in enumerate(chapters):
            c = ch.pop("_raw")
            nodes = []
            for q in c.get("quests", []):
                Q = quests[q["id"]]
                nodes.append([Q["_x"], Q["_y"], Q["_sz"], Q["_sh"], q["id"], 0])
            for l in c.get("quest_links", []) or []:
                lq = l.get("linked_quest")
                Q = quests.get(lq)
                if Q is None:
                    self.warnings.append(f"{ch['f']}: link to unknown quest {lq}")
                    continue
                nodes.append([float(l.get("x", 0)), float(l.get("y", 0)), float(l.get("size", 1.0) or 1.0),
                              l.get("shape") or Q["_sh"], lq, 1])
            # lines, as FTB 2101's QuestPanel draws them: every quest and quest-link button draws a line to each
            # dependency's button (the LAST button showing that quest wins); hidden if the dependent has
            # hide_dependency_lines or the dependency has hide_dependent_lines.
            btn = {}
            for i, n in enumerate(nodes):
                btn[n[4]] = i
            lines = []
            for i, n in enumerate(nodes):
                Q = quests[n[4]]
                for d in Q["dp"]:
                    a = btn.get(d)
                    if a is None or a == i:
                        continue
                    hidden = Q["_hd"] or quests.get(d, {}).get("_hn", False)
                    lines.append([a, i, 1 if hidden else 0])
            ims = []
            for im in c.get("images", []) or []:
                name = str(im.get("image", ""))
                if name not in img_idx:
                    img_idx[name] = len(images)
                    images.append(name)
                a = im.get("alpha", 255)
                ims.append([float(im.get("x", 0)), float(im.get("y", 0)), float(im.get("width", 1)),
                            float(im.get("height", 1)), float(im.get("rotation", 0) or 0),
                            int(a) if isinstance(a, (int, float)) else 255, img_idx[name], int(im.get("order", 0) or 0)])
            ims.sort(key=lambda r: r[7])
            ch["n"], ch["L"], ch["im"] = nodes, lines, [r[:7] for r in ims]
            ch["qc"] = len(c.get("quests", []))
            ch["oc"] = sum(1 for q in c.get("quests", []) if q.get("optional"))
        for Q in quests.values():
            for k in [k for k in Q if k.startswith("_")]:
                del Q[k]

        tables = {}
        for p in sorted((f / "reward_tables").glob("*.snbt")) if (f / "reward_tables").exists() else []:
            try:
                t = self.read(p)
            except Exception as e:
                self.warnings.append(f"cannot parse reward table {p.name}: {e}")
                continue
            tid = table_hex(t.get("id", p.stem))
            rows = []
            for r in t.get("rewards", []) or []:
                rr = self.reward(r)
                rr["w"] = float(r.get("weight", 1.0) or 1.0)
                rows.append(rr)
            tables[tid] = {"t": str(self.L(f"reward_table.{tid}.title", t.get("title") or p.stem)),
                           "ls": int(t.get("loot_size", 1) or 1), "r": rows}
        return {"title": book_title, "groups": [g for g in groups if g["ch"]], "ch": chapters, "q": quests, "tables": tables}, images


# ------------------------------------------------------------------ atlases
def build_icons(book, out_png):
    from PIL import Image
    from build_quest_preview import IconCache
    cache = IconCache()
    ids = sorted(book.items)
    found = []
    for i in ids:
        try:
            im = cache.get(i)
        except Exception as e:  # a broken model should not stop the map
            book.warnings.append(f"icon {i}: {e}")
            im = None
        if im is not None:
            found.append((i, im))
    cache.save()
    rows = max(1, math.ceil(len(found) / ICON_COLS))
    sheet = Image.new("RGBA", (ICON_COLS * ICON, rows * ICON), (0, 0, 0, 0))
    idx = {}
    for k, (i, im) in enumerate(found):
        if im.size != (ICON, ICON):
            im = im.resize((ICON, ICON), Image.NEAREST if im.size[0] < ICON else Image.LANCZOS)
        sheet.alpha_composite(im, ((k % ICON_COLS) * ICON, (k // ICON_COLS) * ICON))
        idx[i] = k
    sheet.save(out_png, optimize=True)
    items = {i: [book.items[i], idx.get(i, -1)] for i in ids}
    return items, len(found), len(ids)


def build_images(names, book, out_png):
    """Shelf-pack every chapter image into one atlas; returns [[x, y, w, h] | None] per image."""
    from PIL import Image
    from build_quest_preview import Assets
    A = Assets()
    pics = []
    for name in names:
        ns, rest = name.split(":", 1) if ":" in name else ("minecraft", name)
        data = A.read(f"assets/{ns}/{rest}")
        im = None
        if data:
            try:
                im = Image.open(io.BytesIO(data)).convert("RGBA")
                if im.size[1] > im.size[0] * 2 and im.size[1] % im.size[0] == 0:  # animated strip: first frame
                    im = im.crop((0, 0, im.size[0], im.size[0]))
                if im.size[0] > IMG_MAX:  # banners are drawn a few hundred px wide at most
                    im = im.resize((IMG_MAX, max(1, round(im.size[1] * IMG_MAX / im.size[0]))), Image.LANCZOS)
            except Exception:
                im = None
        if im is None:
            book.warnings.append(f"chapter image not found: {name}")
        pics.append(im)
    order = sorted((i for i, p in enumerate(pics) if p is not None), key=lambda i: -pics[i].size[1])
    rects = [None] * len(pics)
    x = y = shelf = 0
    for i in order:
        w, h = pics[i].size
        if x + w > ATLAS_W:
            x, y, shelf = 0, y + shelf + 1, 0
        rects[i] = [x, y, w, h]
        x += w + 1
        shelf = max(shelf, h)
    H = max(1, y + shelf)
    atlas = Image.new("RGBA", (ATLAS_W, H), (0, 0, 0, 0))
    for i in order:
        atlas.alpha_composite(pics[i], tuple(rects[i][:2]))
    atlas.save(out_png, "WEBP", quality=80, method=6)  # painted art: lossy WebP is ~5x smaller than PNG
    return rects, (ATLAS_W, H)


# ------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--book", default=str(DEFAULT_BOOK), help="config/ftbquests/quests folder (default: ours)")
    ap.add_argument("--out", default=str(DEFAULT_OUT), help="output folder (default test/preview/map)")
    args = ap.parse_args()
    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    book = Book(args.book)
    data, image_names = book.load()
    items, nf, ni = build_icons(book, out / "icons.png")
    rects, asz = build_images(image_names, book, out / "images.webp")
    data.update({"items": items, "img": rects, "iconCols": ICON_COLS, "iconSize": ICON,
                 "built": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")})
    # sanity: a book read while the generator is rewriting it shows up as missing text or tables
    untitled = sum(1 for qid in data["q"] if f"quest.{qid}.title" not in book.lang)
    missing_t = {r["t"] for Q in data["q"].values() for r in Q["rw"] if "t" in r and r["t"] not in data["tables"]}
    if untitled:
        book.warnings.append(f"{untitled} quests have no title in lang (book being rebuilt? run again)")
    if missing_t:
        book.warnings.append(f"{len(missing_t)} reward tables are referenced but missing: {sorted(missing_t)[:5]}")
    js = "window.QUEST_MAP=" + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n"
    (out / "quest-data.js").write_text(js, encoding="utf-8", newline="\n")
    (out / "quest-map.html").write_text(PAGE.replace("__TITLE__", _esc(data["title"])), encoding="utf-8", newline="\n")
    for w in book.warnings[:40]:
        print("WARNING: " + w)
    if len(book.warnings) > 40:
        print(f"WARNING: ... and {len(book.warnings) - 40} more")
    nq = len(data["q"])
    print(f"Book: {len(data['groups'])} groups, {len(data['ch'])} chapters, {nq} quests, {len(data['tables'])} reward tables")
    print(f"Icons: {nf}/{ni} items have an icon; images: {sum(1 for r in rects if r)}/{len(rects)} (atlas {asz[0]}x{asz[1]})")
    total = 0
    for fn in ("quest-map.html", "quest-data.js", "icons.png", "images.webp"):
        s = (out / fn).stat().st_size
        total += s
        print(f"  {fn:16} {s / 1024:8.0f} KB")
    print(f"  {'total':16} {total / 1024:8.0f} KB  ->  {out}")


def _esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


PAGE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Quest Book Map</title>
<style>
:root{
  --bg:#f4f3ef;--surface:#ffffff;--surface-2:#eceae4;--border:#d6d3cb;--text:#1d1c1a;--muted:#6b6862;
  --accent:#b7791f;--accent-soft:#f5e6c8;--link:#1f6fb7;--chip:#e8e5dd;--scrim:rgba(0,0,0,.35);
  --desc-bg:#17171d;--desc-text:#e9e9ee;--shadow:0 6px 24px rgba(0,0,0,.18);
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --bg:#121216;--surface:#1b1b21;--surface-2:#24242c;--border:#33333d;--text:#e9e9ee;--muted:#9a9aa6;
  --accent:#f2b544;--accent-soft:#3a2f17;--link:#6fb3ff;--chip:#2a2a33;--scrim:rgba(0,0,0,.55);
  --desc-bg:#101015;--desc-text:#e9e9ee;--shadow:0 6px 24px rgba(0,0,0,.5);}}
:root[data-theme="dark"]{
  --bg:#121216;--surface:#1b1b21;--surface-2:#24242c;--border:#33333d;--text:#e9e9ee;--muted:#9a9aa6;
  --accent:#f2b544;--accent-soft:#3a2f17;--link:#6fb3ff;--chip:#2a2a33;--scrim:rgba(0,0,0,.55);
  --desc-bg:#101015;--desc-text:#e9e9ee;--shadow:0 6px 24px rgba(0,0,0,.5);}
*{box-sizing:border-box}
html,body{height:100%;margin:0}
body{background:var(--bg);color:var(--text);font:14px/1.4 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;overflow:hidden}
button{font:inherit;color:inherit}
#app{display:grid;grid-template-columns:290px 1fr;grid-template-rows:48px 1fr;height:100%;height:100dvh}
header{grid-column:1/-1;display:flex;align-items:center;gap:10px;padding:0 12px;background:var(--surface);border-bottom:1px solid var(--border);min-width:0}
header h1{font-size:15px;margin:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;flex:1;min-width:0}
header h1 small{color:var(--muted);font-weight:400;margin-left:8px}
.btn{background:var(--surface-2);border:1px solid var(--border);border-radius:6px;padding:5px 9px;cursor:pointer;line-height:1.2;white-space:nowrap}
.btn:hover{border-color:var(--accent)}
.btn.on{background:var(--accent-soft);border-color:var(--accent)}
#menuBtn{display:none}
aside{background:var(--surface);border-right:1px solid var(--border);display:flex;flex-direction:column;min-height:0}
.searchbox{padding:10px;border-bottom:1px solid var(--border)}
.searchbox input{width:100%;padding:8px 10px;border-radius:6px;border:1px solid var(--border);background:var(--bg);color:var(--text);font:inherit}
.searchbox input:focus{outline:2px solid var(--accent);outline-offset:-1px}
#list{overflow:auto;flex:1;padding:4px 0 24px}
.grp{border-bottom:1px solid var(--border)}
.grp>button{display:flex;width:100%;align-items:center;gap:6px;padding:8px 10px;background:none;border:0;cursor:pointer;text-align:left;font-weight:600}
.grp>button .n{margin-left:auto;color:var(--muted);font-weight:400;font-size:12px}
.grp>button .car{width:10px;color:var(--muted);transition:transform .15s}
.grp.closed>button .car{transform:rotate(-90deg)}
.grp.closed .chs{display:none}
.row{display:flex;align-items:center;gap:8px;width:100%;padding:5px 10px 5px 18px;background:none;border:0;cursor:pointer;text-align:left;min-height:32px}
.row:hover{background:var(--surface-2)}
.row.cur{background:var(--accent-soft);box-shadow:inset 3px 0 0 var(--accent)}
.row .t{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.row .t small{display:block;color:var(--muted);font-size:11.5px;overflow:hidden;text-overflow:ellipsis}
.row .n{color:var(--muted);font-size:12px}
.sec{padding:8px 10px 4px;font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
.ic{display:inline-block;width:24px;height:24px;flex:none;background-repeat:no-repeat;image-rendering:pixelated;vertical-align:middle}
.ic.none{background:var(--chip);border-radius:4px}
#stage{position:relative;min-width:0;min-height:0;overflow:hidden;background:#16161c}
canvas{display:block;width:100%;height:100%;touch-action:none;cursor:grab}
canvas.drag{cursor:grabbing}canvas.hov{cursor:pointer}
#hud{position:absolute;left:12px;top:10px;max-width:min(560px,calc(100% - 24px));pointer-events:none;color:#ecebf2;text-shadow:0 1px 3px #000}
#hud h2{margin:0;font-size:18px}
#hud div{font-size:12.5px;color:#c4c3cf}
#ctrl{position:absolute;right:12px;bottom:12px;display:flex;gap:6px}
#ctrl .btn{background:rgba(30,30,38,.9);border-color:#44444f;color:#eee}
#tip{position:absolute;pointer-events:none;background:rgba(16,1,16,.94);border:1px solid #5a2a9a;color:#fff;padding:5px 8px;border-radius:4px;font-size:12.5px;max-width:280px;display:none;z-index:5}
#tip small{display:block;color:#b8b8c8}
#panel{position:absolute;top:0;right:0;bottom:0;width:390px;max-width:100%;background:var(--surface);border-left:1px solid var(--border);box-shadow:var(--shadow);overflow:auto;transform:translateX(105%);transition:transform .18s;z-index:10}
#panel.open{transform:none}
#panel .hd{position:sticky;top:0;background:var(--surface);display:flex;gap:10px;align-items:flex-start;padding:12px 12px 10px;border-bottom:1px solid var(--border);z-index:1}
#panel .hd .ic{width:40px;height:40px}
#panel h3{margin:0;font-size:16px;line-height:1.25}
#panel .stl{font-size:12.5px;margin-top:2px}
#panel .where{font-size:12px;color:var(--muted);margin-top:3px}
#panel .x{margin-left:auto}
#panel .bd{padding:10px 12px 30px}
#panel h4{margin:14px 0 6px;font-size:11.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
.chips{display:flex;flex-wrap:wrap;gap:5px}
.chip{background:var(--chip);border-radius:999px;padding:2px 9px;font-size:12px}
.chip.warn{background:var(--accent-soft)}
.desc{background:var(--desc-bg);color:var(--desc-text);border-radius:6px;padding:9px 11px;font-size:13px;line-height:1.5}
.desc p{margin:0 0 6px}.desc p:last-child{margin:0}
.desc hr{border:0;border-top:1px dashed #555;margin:8px 0}
.li{display:flex;gap:8px;align-items:center;padding:4px 0;border-bottom:1px solid var(--surface-2)}
.li:last-child{border-bottom:0}
.li .t{flex:1;min-width:0}
.li .t small{display:block;color:var(--muted);font-size:11.5px;word-break:break-all}
.li .cnt{color:var(--muted);font-variant-numeric:tabular-nums;white-space:nowrap}
.glyph{width:24px;height:24px;flex:none;display:inline-flex;align-items:center;justify-content:center;border-radius:4px;background:var(--chip);font-size:11px;font-weight:700;color:var(--muted)}
a.q{color:var(--link);cursor:pointer;text-decoration:none}a.q:hover{text-decoration:underline}
details.tbl{margin:2px 0 0 32px;font-size:12.5px}
details.tbl summary{cursor:pointer;color:var(--muted)}
.sub{display:flex;flex-direction:column}
.any{display:flex;flex-wrap:wrap;gap:4px;margin-top:3px}
.any span{display:inline-flex;align-items:center;gap:4px;background:var(--chip);border-radius:4px;padding:1px 6px 1px 2px;font-size:12px}
.any .ic{width:18px;height:18px}
.id{color:var(--muted);font-size:11px;margin-top:16px;font-family:ui-monospace,Consolas,monospace}
#scrim{display:none}
@media (max-width:760px){
  #app{grid-template-columns:1fr}
  #menuBtn{display:inline-block}
  header h1 small{display:none}
  aside{position:fixed;left:0;top:48px;bottom:0;width:min(320px,86vw);z-index:20;transform:translateX(-102%);transition:transform .18s;box-shadow:var(--shadow)}
  body.side aside{transform:none}
  body.side #scrim{display:block;position:fixed;inset:48px 0 0 0;background:var(--scrim);z-index:15}
  #panel{top:auto;left:0;width:100%;height:62%;border-left:0;border-top:1px solid var(--border);transform:translateY(105%);border-radius:12px 12px 0 0}
  #panel.open{transform:none}
  #hud h2{font-size:15px}
  #hud div{display:none}
  .hide-sm{display:none}
}
</style></head>
<body>
<div id="app">
<header>
  <button class="btn" id="menuBtn" aria-label="Chapters">&#9776;</button>
  <h1 id="bookTitle">__TITLE__ <small id="stats"></small></h1>
  <button class="btn hide-sm" id="hidBtn" title="Show every dependency line, hidden ones too">Hidden lines</button>
  <button class="btn hide-sm" id="labBtn" title="Item names under quests">Labels</button>
</header>
<aside>
  <div class="searchbox"><input id="q" type="search" placeholder="Search chapters, quests, items" autocomplete="off" aria-label="Search"></div>
  <div id="list"></div>
</aside>
<main id="stage">
  <canvas id="cv"></canvas>
  <div id="hud"><h2 id="chTitle"></h2><div id="chSub"></div></div>
  <div id="ctrl"><button class="btn" id="zin" aria-label="Zoom in">+</button><button class="btn" id="zout" aria-label="Zoom out">&minus;</button><button class="btn" id="fit">Fit</button></div>
  <div id="tip"></div>
  <section id="panel" aria-live="polite"></section>
</main>
</div>
<div id="scrim"></div>
<script src="quest-data.js"></script>
<script>
(function(){
"use strict";
const D = window.QUEST_MAP;
const $ = s => document.querySelector(s);
if(!D){document.body.innerHTML='<p style="padding:20px">quest-data.js did not load.</p>';return;}
const ICS = D.iconSize, ICC = D.iconCols;
const icons = new Image(), atlas = new Image();
let iconsOK=false, atlasOK=false;
icons.onload=()=>{iconsOK=true;draw()}; atlas.onload=()=>{atlasOK=true;draw()};
icons.src="icons.png"; atlas.src="images.webp";

/* ---------- text: FTB / Minecraft formatting codes ---------- */
const COL={0:"#000000",1:"#0000AA",2:"#00AA00",3:"#00AAAA",4:"#AA0000",5:"#AA00AA",6:"#FFAA00",7:"#AAAAAA",
  8:"#555555",9:"#5555FF",a:"#55FF55",b:"#55FFFF",c:"#FF5555",d:"#FF55FF",e:"#FFFF55",f:"#FFFFFF"};
const esc = s => String(s).replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const strip = s => String(s||"").replace(/[&§][0-9a-fk-or]/gi,"");
function fmt(s){
  s=String(s==null?"":s);
  let out="", st={c:null,b:0,i:0,u:0,s:0,k:0}, buf="";
  const flush=()=>{ if(!buf) return; let css="";
    if(st.c) css+="color:"+st.c+";"; if(st.b) css+="font-weight:700;"; if(st.i) css+="font-style:italic;";
    const td=[st.u?"underline":"",st.s?"line-through":""].filter(Boolean).join(" "); if(td) css+="text-decoration:"+td+";";
    if(st.k) css+="filter:blur(2px);";
    out+= css? '<span style="'+css+'">'+esc(buf)+'</span>' : esc(buf); buf=""; };
  for(let i=0;i<s.length;i++){
    const ch=s[i];
    if((ch==="&"||ch==="§") && i+1<s.length && /[0-9a-fk-or]/i.test(s[i+1]) && s[i-1]!=="\\"){
      flush(); const k=s[++i].toLowerCase();
      if(COL[k]){st={c:COL[k],b:0,i:0,u:0,s:0,k:0}}
      else if(k==="r"){st={c:null,b:0,i:0,u:0,s:0,k:0}}
      else if(k==="l")st.b=1; else if(k==="o")st.i=1; else if(k==="n")st.u=1; else if(k==="m")st.s=1; else if(k==="k")st.k=1;
    } else if(ch==="\\" && s[i+1]==="&"){ buf+="&"; i++; }
    else buf+=ch;
  }
  flush(); return out;
}
function textComp(j){ if(typeof j==="string") return j; if(Array.isArray(j)) return j.map(textComp).join("");
  if(j&&typeof j==="object") return (j.text||j.translate||"")+(j.extra?textComp(j.extra):""); return ""; }
function descLine(l){
  const t=l.trim();
  if(t==="{@pagebreak}") return "<hr>";
  if(/^\{image:/.test(t)) return '<p><i style="color:#999">[image: '+esc(t.slice(7,-1).split(" ")[0])+']</i></p>';
  if(t.startsWith("{")||t.startsWith("[")){ try{ return "<p>"+fmt(textComp(JSON.parse(t)))+"</p>"; }catch(e){} }
  if(!t) return '<p style="height:.5em"></p>';
  return "<p>"+fmt(l)+"</p>";
}

/* ---------- lookups ---------- */
const itemName = id => (D.items[id]&&D.items[id][0]) || (id? String(id).split(":").pop().replace(/_/g," ") : "?");
const itemIdx = id => D.items[id]? D.items[id][1] : -1;
function iconHTML(id, px){
  px=px||24; const k=itemIdx(id);
  if(k<0) return '<span class="ic none" style="width:'+px+'px;height:'+px+'px" title="'+esc(id||"")+'"></span>';
  const sc=px/ICS, x=(k%ICC)*ICS*sc, y=Math.floor(k/ICC)*ICS*sc;
  return '<span class="ic" style="width:'+px+'px;height:'+px+'px;background-image:url(icons.png);background-size:'+(ICC*ICS*sc)+'px auto;background-position:-'+x+'px -'+y+'px"></span>';
}
const glyph = (t) => '<span class="glyph">'+esc(t)+'</span>';
const KGLYPH={check:"✓",kill:"KILL",dimension:"DIM",biome:"BIO",structure:"FIND",fluid:"FL",xp:"XP",tag:"#",filter:"F",other:"?"};

/* ---------- state ---------- */
const cv=$("#cv"), ctx=cv.getContext("2d");
let cur=-1, sel=null, selNode=-1, hov=-1, showHidden=false, showLabels=true;
let view={s:40,ox:0,oy:0}, W=0, H=0, dpr=1;
let nodeOfQuest={};  // quest id -> node index in the current chapter (the quest itself, not a link)

/* ---------- sidebar ---------- */
const totalQ=Object.keys(D.q).length;
$("#stats").textContent=D.ch.length+" chapters · "+totalQ+" quests · built "+D.built;
let closed={};
try{closed=JSON.parse(localStorage.getItem("qmap.closed")||"{}")}catch(e){}
function renderList(){
  const q=$("#q").value.trim().toLowerCase();
  const L=$("#list"); let h="";
  if(q.length>=2){ h=searchHTML(q); }
  else{
    D.groups.forEach((g,gi)=>{
      const qc=g.ch.reduce((a,c)=>a+D.ch[c].qc,0);
      h+='<div class="grp'+(closed[g.id||"_"]?" closed":"")+'" data-g="'+esc(g.id||"_")+'"><button><span class="car">▾</span>'+esc(strip(g.t))+
         '<span class="n">'+g.ch.length+' ch · '+qc+'</span></button><div class="chs">';
      g.ch.forEach(ci=>{ const c=D.ch[ci];
        h+='<button class="row'+(ci===cur?" cur":"")+'" data-c="'+ci+'">'+iconHTML(c.ic,22)+'<span class="t">'+esc(c.t)+'</span><span class="n">'+c.qc+'</span></button>'; });
      h+='</div></div>';
    });
  }
  L.innerHTML=h;
}
$("#list").addEventListener("click",e=>{
  const g=e.target.closest(".grp>button");
  if(g){ const el=g.parentNode, id=el.dataset.g; el.classList.toggle("closed"); closed[id]=el.classList.contains("closed");
    try{localStorage.setItem("qmap.closed",JSON.stringify(closed))}catch(err){} return; }
  const r=e.target.closest("[data-c],[data-q]"); if(!r) return;
  if(r.dataset.q) goTo(r.dataset.q); else { openChapter(+r.dataset.c); location.hash="c="+D.ch[+r.dataset.c].f; }
  document.body.classList.remove("side");
});

/* ---------- search ---------- */
const HAY={};
for(const id in D.q){ const Q=D.q[id]; let items=[];
  Q.tk.forEach(t=>{ if(t.k==="item") items.push([t.i,itemName(t.i)]);
    else if(t.k==="any") t.i.forEach(i=>items.push([i,itemName(i)]));
    else if(t.k==="tag") items.push([null,"#"+t.tag]);
    else if(t.nm) items.push([null,t.nm]); });
  HAY[id]={t:strip(Q.t).toLowerCase(), items:items.map(([i,n])=>[i,n,(n+" "+(i||"")).toLowerCase()])};
}
function searchHTML(q){
  let h="", chs=[];
  D.ch.forEach((c,ci)=>{ if(c.t.toLowerCase().includes(q)||c.f.toLowerCase().includes(q)) chs.push(ci); });
  if(chs.length){ h+='<div class="sec">Chapters</div>';
    chs.forEach(ci=>{const c=D.ch[ci]; h+='<button class="row" data-c="'+ci+'">'+iconHTML(c.ic,22)+'<span class="t">'+esc(c.t)+'</span><span class="n">'+c.qc+'</span></button>';}); }
  const res=[];
  for(const id in HAY){ const H_=HAY[id]; let sc=0, why="";
    if(H_.t.startsWith(q)) sc=3; else if(H_.t.includes(q)) sc=2;
    const m=H_.items.find(x=>x[2].includes(q)); if(m){ if(!sc) sc=1; why=m[1]; }
    if(sc) res.push([sc,id,why]); }
  res.sort((a,b)=>b[0]-a[0]||strip(D.q[a[1]].t).localeCompare(strip(D.q[b[1]].t)));
  h+='<div class="sec">Quests ('+res.length+(res.length>200?", first 200":"")+')</div>';
  res.slice(0,200).forEach(([sc,id,why])=>{ const Q=D.q[id];
    h+='<button class="row" data-q="'+id+'">'+iconHTML(Q.ic,22)+'<span class="t">'+fmt(Q.t)+'<small>'+esc(D.ch[Q.c].t)+(why?' · needs '+esc(why):'')+'</small></span></button>'; });
  if(!res.length&&!chs.length) h+='<div class="sec" style="text-transform:none">Nothing matches.</div>';
  return h;
}
let st_; $("#q").addEventListener("input",()=>{clearTimeout(st_);st_=setTimeout(renderList,120)});
$("#q").addEventListener("keydown",e=>{
  if(e.key==="Enter"){ const r=$("#list [data-q],#list [data-c]"); if(r) r.click(); }
  if(e.key==="Escape"){ e.target.value=""; renderList(); }
});

/* ---------- chapter / view ---------- */
function openChapter(ci, keepView){
  cur=ci; const c=D.ch[ci]; nodeOfQuest={};
  c.n.forEach((n,i)=>{ if(!n[5]) nodeOfQuest[n[4]]=i; });
  $("#chTitle").textContent=c.t;
  const g=D.groups.find(g=>g.ch.includes(ci));
  $("#chSub").innerHTML=esc(g?strip(g.t):"")+" · "+c.qc+" quests"+(c.oc?" ("+c.oc+" optional)":"")+(c.sub.length?" · "+fmt(c.sub.join(" ")):"");
  hov=-1;
  if(sel && !keepView && D.q[sel].c!==ci){ $("#panel").classList.remove("open"); sel=null; }  // browsing away: close
  selNode = sel? (nodeOfQuest[sel]!==undefined? nodeOfQuest[sel] : -1) : -1;
  if(!keepView) fit();
  renderList();
  const r=$('#list .row.cur'); if(r) r.scrollIntoView({block:"nearest"});
  draw();
}
function bounds(){
  const c=D.ch[cur]; let x0=1e9,y0=1e9,x1=-1e9,y1=-1e9;
  c.n.forEach(n=>{const r=n[2]/2; x0=Math.min(x0,n[0]-r);y0=Math.min(y0,n[1]-r);x1=Math.max(x1,n[0]+r);y1=Math.max(y1,n[1]+r+0.5);});
  c.im.forEach(m=>{ const a=m[4]*Math.PI/180, hw=(Math.abs(Math.cos(a))*m[2]+Math.abs(Math.sin(a))*m[3])/2, hh=(Math.abs(Math.sin(a))*m[2]+Math.abs(Math.cos(a))*m[3])/2;
    x0=Math.min(x0,m[0]-hw);y0=Math.min(y0,m[1]-hh);x1=Math.max(x1,m[0]+hw);y1=Math.max(y1,m[1]+hh); });
  if(x0>x1){x0=y0=-1;x1=y1=1;}
  return [x0,y0,x1,y1];
}
function fit(){
  if(cur<0) return; const [x0,y0,x1,y1]=bounds(); const top=window.innerWidth<=760?36:56;
  const s=Math.max(4,Math.min(64,Math.min((W-40)/(x1-x0+1),(H-top-30)/(y1-y0+1))));
  view.s=s; view.ox=W/2-(x0+x1)/2*s; view.oy=top+(H-top)/2-(y0+y1)/2*s; draw();
}
function centerOn(n){ const s=Math.max(view.s,36); view.s=s;
  const pw = window.innerWidth>760? Math.min(390,W*0.5) : 0, ph = window.innerWidth>760? 0 : H*0.62;  // keep it clear of the panel
  view.ox=(W-pw)/2-n[0]*s; view.oy=(H-ph)/2+(ph?10:0)-n[1]*s; }
function zoomAt(f,px,py){ const s=Math.max(3,Math.min(180,view.s*f)); f=s/view.s;
  view.ox=px-(px-view.ox)*f; view.oy=py-(py-view.oy)*f; view.s=s; draw(); }

/* ---------- drawing ---------- */
function shapePath(sh,cx,cy,r){
  ctx.beginPath();
  if(sh==="circle"||!sh){ ctx.arc(cx,cy,r,0,Math.PI*2); return; }
  if(sh==="square"){ const k=r*.94; ctx.rect(cx-k,cy-k,2*k,2*k); return; }
  if(sh==="rsquare"){ const k=r*.94, rr=r*.38; if(ctx.roundRect){ctx.roundRect(cx-k,cy-k,2*k,2*k,rr);}else{ctx.rect(cx-k,cy-k,2*k,2*k);} return; }
  let pts=null;
  if(sh==="diamond") pts=[[0,-r],[r,0],[0,r],[-r,0]];
  else if(sh==="pentagon"||sh==="hexagon"||sh==="octagon"){ const [n,st]={pentagon:[5,-90],hexagon:[6,0],octagon:[8,22.5]}[sh];
    pts=[]; for(let i=0;i<n;i++){const a=(st+i*360/n)*Math.PI/180; pts.push([r*Math.cos(a),r*Math.sin(a)]);} }
  else if(sh==="gear"){ pts=[]; const T=10; for(let i=0;i<T*4;i++){ const a=(i*360/(T*4)-4.5)*Math.PI/180, rr=(i%4<2)?r:r*.8; pts.push([rr*Math.cos(a),rr*Math.sin(a)]); } }
  else if(sh==="heart"){ pts=[]; for(let i=0;i<48;i++){const t=2*Math.PI*i/48, x=16*Math.pow(Math.sin(t),3), y=-(13*Math.cos(t)-5*Math.cos(2*t)-2*Math.cos(3*t)-Math.cos(4*t)); pts.push([x*r/17,y*r/17-r*.05]);} }
  else if(sh==="none"){ return; }
  if(!pts){ ctx.arc(cx,cy,r,0,Math.PI*2); return; }
  pts.forEach((p,i)=> i?ctx.lineTo(cx+p[0],cy+p[1]):ctx.moveTo(cx+p[0],cy+p[1])); ctx.closePath();
}
const P = (x,y) => [x*view.s+view.ox, y*view.s+view.oy];
function ellip(t,maxW){ if(ctx.measureText(t).width<=maxW) return t;
  let lo=0,hi=t.length; while(lo<hi){const m=(lo+hi+1)>>1; if(ctx.measureText(t.slice(0,m)+"…").width<=maxW) lo=m; else hi=m-1;}
  return t.slice(0,lo)+"…"; }
function draw(){
  if(!W) return;
  ctx.setTransform(dpr,0,0,dpr,0,0);
  ctx.fillStyle="#16161c"; ctx.fillRect(0,0,W,H);
  if(cur<0) return;
  const c=D.ch[cur], s=view.s;
  // grid
  if(s>=8){ ctx.strokeStyle="rgba(255,255,255,0.045)"; ctx.lineWidth=1; ctx.beginPath();
    const gx0=Math.floor((-view.ox)/s-0.5), gx1=Math.ceil((W-view.ox)/s), gy0=Math.floor((-view.oy)/s-0.5), gy1=Math.ceil((H-view.oy)/s);
    for(let gx=gx0;gx<=gx1;gx++){const X=Math.round((gx+.5)*s+view.ox)+.5; ctx.moveTo(X,0);ctx.lineTo(X,H);}
    for(let gy=gy0;gy<=gy1;gy++){const Y=Math.round((gy+.5)*s+view.oy)+.5; ctx.moveTo(0,Y);ctx.lineTo(W,Y);}
    ctx.stroke(); }
  // images
  c.im.forEach(m=>{ const r=D.img[m[6]], [cx,cy]=P(m[0],m[1]), w=m[2]*s, h=m[3]*s;
    ctx.save(); ctx.translate(cx,cy); ctx.rotate(m[4]*Math.PI/180); ctx.globalAlpha=(m[5]==null?255:m[5])/255;
    if(r&&atlasOK){ ctx.imageSmoothingEnabled=true; ctx.drawImage(atlas,r[0],r[1],r[2],r[3],-w/2,-h/2,w,h); }
    else if(!r){ ctx.setLineDash([4,4]); ctx.strokeStyle="#c55"; ctx.strokeRect(-w/2,-h/2,w,h); ctx.setLineDash([]); }
    ctx.restore(); });
  // lines
  const focus=new Set([hov,selNode].filter(i=>i>=0));
  const lw=Math.max(1.2,s*0.075);
  const later=[];
  c.L.forEach(l=>{ const [a,b,hid]=l, f=focus.has(a)||focus.has(b);
    if(hid&&!f&&!showHidden) return;
    if(f){ later.push(l); return; }
    const A=c.n[a], B=c.n[b], opt=D.q[B[4]].opt;
    ctx.strokeStyle= opt?"rgba(175,175,190,0.35)":"rgba(185,185,198,0.75)"; ctx.lineWidth=lw;
    ctx.setLineDash(hid?[lw*2,lw*2]:[]);
    ctx.beginPath(); ctx.moveTo(...P(A[0],A[1])); ctx.lineTo(...P(B[0],B[1])); ctx.stroke(); });
  later.forEach(([a,b,hid])=>{ const A=c.n[a], B=c.n[b];
    const toFocusDep = focus.has(b); // a is a dependency of the focused quest
    ctx.strokeStyle= toFocusDep? "#ffcc33" : "#52d6ff"; ctx.lineWidth=lw*1.4; ctx.setLineDash(hid?[lw*2.5,lw*2]:[]);
    ctx.beginPath(); ctx.moveTo(...P(A[0],A[1])); ctx.lineTo(...P(B[0],B[1])); ctx.stroke(); });
  ctx.setLineDash([]);
  // quests
  const ew=Math.max(1,s*0.06);
  const lab = showLabels && s>=28;
  const fs = Math.max(9,Math.min(13,s*0.27));
  c.n.forEach((n,i)=>{
    const [x,y,sz,sh,qid,isLink]=n, Q=D.q[qid], [cx,cy]=P(x,y), r=sz*s/2*0.95;
    if(cx+r*3<0||cx-r*3>W||cy+r*3<0||cy-r*3>H) return;
    const dim = Q.opt||isLink;
    ctx.globalAlpha = isLink?0.6:(Q.opt?0.55:1);
    shapePath(sh,cx,cy,r);
    ctx.fillStyle= isLink?"#2c3440":"#3a3a45"; ctx.fill();
    ctx.lineWidth = (i===selNode)?Math.max(2,s*0.1):ew;
    ctx.strokeStyle = (i===selNode)?"#ffcc33":(i===hov?"#ffffff":(Q.fl.indexOf("invisible")>=0?"#8a6ad0":"#a7a7b4"));
    ctx.stroke();
    // icon
    const k=itemIdx(Q.ic), isz=sz*s*0.62;
    if(k>=0&&iconsOK){ ctx.imageSmoothingEnabled = isz<ICS; ctx.drawImage(icons,(k%ICC)*ICS,Math.floor(k/ICC)*ICS,ICS,ICS,cx-isz/2,cy-isz/2,isz,isz); }
    else{ const t0=Q.tk[0]; const g=t0?(KGLYPH[t0.k]||""):"";
      if(g&&isz>8){ ctx.fillStyle="#d8d8e0"; ctx.font="700 "+Math.max(7,Math.min(isz*0.42,22))+"px system-ui,sans-serif"; ctx.textAlign="center"; ctx.textBaseline="middle"; ctx.fillText(g,cx,cy); } }
    // quest-link arrow
    if(isLink&&s>=10){ ctx.globalAlpha=1; const ax=cx+r*0.62, ay=cy-r*0.62, a=Math.max(4,s*0.13);
      ctx.fillStyle="#2b6fd6"; ctx.beginPath(); ctx.arc(ax,ay,a*1.25,0,Math.PI*2); ctx.fill();
      ctx.strokeStyle="#fff"; ctx.lineWidth=Math.max(1.2,a*0.32); ctx.beginPath();
      ctx.moveTo(ax-a*.55,ay+a*.55); ctx.lineTo(ax+a*.55,ay-a*.55); ctx.moveTo(ax-a*.1,ay-a*.55); ctx.lineTo(ax+a*.55,ay-a*.55); ctx.lineTo(ax+a*.55,ay+a*.1); ctx.stroke(); }
    // label
    if(lab){ ctx.globalAlpha= dim?0.7:1;
      ctx.font=(i===selNode?"600 ":"")+fs+"px system-ui,sans-serif"; ctx.textAlign="center"; ctx.textBaseline="top";
      const t=ellip(Q.lb||strip(Q.t), Math.max(sz,1)*s*1.75), ty=cy+r+2;
      ctx.lineWidth=3; ctx.strokeStyle="rgba(10,10,14,0.9)"; ctx.lineJoin="round"; ctx.strokeText(t,cx,ty);
      ctx.fillStyle= i===selNode?"#ffcc33":"#e6e6ee"; ctx.fillText(t,cx,ty); }
    ctx.globalAlpha=1;
  });
}
function resize(){ const r=cv.getBoundingClientRect(); dpr=window.devicePixelRatio||1; W=r.width; H=r.height;
  cv.width=Math.round(W*dpr); cv.height=Math.round(H*dpr); draw(); }
window.addEventListener("resize",resize);

/* ---------- pointer ---------- */
function hit(px,py){ if(cur<0) return -1; const c=D.ch[cur];
  for(let i=c.n.length-1;i>=0;i--){ const n=c.n[i], [cx,cy]=P(n[0],n[1]), r=n[2]*view.s/2;
    if(Math.abs(px-cx)<=r&&Math.abs(py-cy)<=r) return i; } return -1; }
const ptr=new Map(); let drag=null, pinch=null;
cv.addEventListener("pointerdown",e=>{ cv.setPointerCapture(e.pointerId); ptr.set(e.pointerId,[e.offsetX,e.offsetY]);
  if(ptr.size===1) drag={x:e.offsetX,y:e.offsetY,ox:view.ox,oy:view.oy,moved:false};
  if(ptr.size===2){ const [a,b]=[...ptr.values()]; pinch={d:Math.hypot(a[0]-b[0],a[1]-b[1]),s:view.s}; drag=null; } });
cv.addEventListener("pointermove",e=>{
  if(ptr.has(e.pointerId)) ptr.set(e.pointerId,[e.offsetX,e.offsetY]);
  if(pinch&&ptr.size===2){ const [a,b]=[...ptr.values()], d=Math.hypot(a[0]-b[0],a[1]-b[1]);
    zoomAt(pinch.s*d/pinch.d/view.s,(a[0]+b[0])/2,(a[1]+b[1])/2); return; }
  if(drag){ const dx=e.offsetX-drag.x, dy=e.offsetY-drag.y; if(Math.abs(dx)+Math.abs(dy)>4) drag.moved=true;
    if(drag.moved){ cv.classList.add("drag"); view.ox=drag.ox+dx; view.oy=drag.oy+dy; $("#tip").style.display="none"; draw(); return; } }
  if(e.pointerType==="mouse"){ const h=hit(e.offsetX,e.offsetY); if(h!==hov){ hov=h; cv.classList.toggle("hov",h>=0); draw(); }
    const tip=$("#tip");
    if(h>=0){ const n=D.ch[cur].n[h], Q=D.q[n[4]];
      tip.innerHTML=(n[5]?'<small>Link to '+esc(D.ch[Q.c].t)+'</small>':'')+fmt(Q.t)+'<small>'+esc(Q.lb||"")+(Q.opt?' · optional':'')+'</small>';
      tip.style.display="block"; const tx=Math.min(e.offsetX+14,W-tip.offsetWidth-6); tip.style.left=tx+"px"; tip.style.top=(e.offsetY+16)+"px"; }
    else tip.style.display="none"; }
});
function up(e){ const wasDrag=drag&&drag.moved; ptr.delete(e.pointerId);
  if(ptr.size<2) pinch=null;
  if(ptr.size===0){ cv.classList.remove("drag");
    if(drag&&!wasDrag){ const h=hit(e.offsetX,e.offsetY);
      if(h>=0){ const n=D.ch[cur].n[h];
        if(window.innerWidth<=760){ const cy=n[1]*view.s+view.oy; if(cy>H*0.34) view.oy-=cy-H*0.2; }  // keep it above the sheet
        select(n[4],h); }
      else { closePanel(); } }
    drag=null; } }
cv.addEventListener("pointerup",up); cv.addEventListener("pointercancel",up);
cv.addEventListener("pointerleave",()=>{ if(hov>=0){hov=-1;draw();} $("#tip").style.display="none"; });
cv.addEventListener("wheel",e=>{ e.preventDefault(); const k=e.deltaMode===1?40:1; zoomAt(Math.exp(-e.deltaY*k*0.0015),e.offsetX,e.offsetY); },{passive:false});
$("#zin").onclick=()=>zoomAt(1.25,W/2,H/2); $("#zout").onclick=()=>zoomAt(0.8,W/2,H/2); $("#fit").onclick=fit;
$("#hidBtn").onclick=e=>{showHidden=!showHidden; e.target.classList.toggle("on",showHidden); draw();};
$("#labBtn").classList.add("on");
$("#labBtn").onclick=e=>{showLabels=!showLabels; e.target.classList.toggle("on",showLabels); draw();};
$("#menuBtn").onclick=()=>document.body.classList.toggle("side");
$("#scrim").onclick=()=>document.body.classList.remove("side");
document.addEventListener("keydown",e=>{ if(e.target.tagName==="INPUT") return;
  if(e.key==="Escape") closePanel(); else if(e.key==="f") fit(); else if(e.key==="/"){ e.preventDefault(); $("#q").focus(); } });

/* ---------- quest panel ---------- */
function qlink(id){ const Q=D.q[id]; if(!Q) return '<div class="li">'+glyph("?")+'<span class="t">Unknown quest <small>'+esc(id)+'</small></span></div>';
  const other=Q.c!==cur;
  return '<div class="li">'+iconHTML(Q.ic)+'<span class="t"><a class="q" data-go="'+id+'">'+fmt(Q.t)+'</a>'+
    '<small>'+(other?'in '+esc(D.ch[Q.c].t)+' · ':'')+esc(Q.lb||"")+(Q.opt?' · optional':'')+'</small></span></div>'; }
function taskHTML(t){
  const n=t.n>1?'×'+t.n.toLocaleString():'';
  switch(t.k){
    case "item": return '<div class="li">'+iconHTML(t.i)+'<span class="t">'+esc(itemName(t.i))+'<small>'+esc(t.i)+'</small></span><span class="cnt">'+n+'</span></div>';
    case "any": return '<div class="li">'+glyph("ANY")+'<span class="t">Any of '+t.i.length+' items'+(t.tags&&t.tags.length?' or #'+esc(t.tags.join(", #")):'')+
       '<span class="any">'+t.i.map(i=>'<span title="'+esc(i)+'">'+iconHTML(i,18)+esc(itemName(i))+'</span>').join("")+'</span></span><span class="cnt">'+n+'</span></div>';
    case "tag": return '<div class="li">'+glyph("#")+'<span class="t">any '+esc(t.tag)+(t.more&&t.more.length?' or '+esc(t.more.join(", ")):'')+'<small>item tag</small></span><span class="cnt">'+n+'</span></div>';
    case "kill": return '<div class="li">'+(itemIdx(t.egg)>=0?iconHTML(t.egg):glyph("KILL"))+'<span class="t">Kill '+esc(t.nm)+'<small>'+esc(t.e)+'</small></span><span class="cnt">'+n+'</span></div>';
    case "dimension": return '<div class="li">'+glyph("DIM")+'<span class="t">Visit '+esc(t.nm)+'<small>'+esc(t.v)+'</small></span></div>';
    case "biome": return '<div class="li">'+glyph("BIO")+'<span class="t">Find biome: '+esc(t.nm)+'<small>'+esc(t.v)+'</small></span></div>';
    case "structure": return '<div class="li">'+glyph("FIND")+'<span class="t">Find structure: '+esc(t.nm)+'<small>'+esc(t.v)+'</small></span></div>';
    case "check": return '<div class="li">'+glyph("✓")+'<span class="t">Checkmark<small>click to complete</small></span></div>';
    case "fluid": return '<div class="li">'+glyph("FL")+'<span class="t">'+esc(t.nm)+'<small>'+esc(t.v)+'</small></span><span class="cnt">'+t.n+' mB</span></div>';
    case "xp": return '<div class="li">'+glyph("XP")+'<span class="t">Spend '+t.n+(t.lv?' levels':' XP')+'</span></div>';
    case "filter": return '<div class="li">'+glyph("F")+'<span class="t">Matching filter<small>'+esc(t.v)+'</small></span><span class="cnt">'+n+'</span></div>';
    default: return '<div class="li">'+glyph("?")+'<span class="t">'+esc(t.type||t.k)+'<small>'+esc(t.v||"")+'</small></span></div>';
  }
}
function rewardHTML(r){
  const n=r.n>1?'×'+r.n.toLocaleString():'';
  if(r.k==="item") return '<div class="li">'+iconHTML(r.i)+'<span class="t">'+esc(itemName(r.i))+'<small>'+esc(r.i)+'</small></span><span class="cnt">'+n+'</span></div>';
  if(r.k==="xp") return '<div class="li">'+glyph("XP")+'<span class="t">'+r.n+' XP</span></div>';
  if(r.k==="xp_levels") return '<div class="li">'+glyph("LV")+'<span class="t">'+r.n+' levels</span></div>';
  if(["random","choice","loot","all_table"].includes(r.k)){ const T=D.tables[r.t];
    const verb={random:"Random roll",choice:"Choose one",loot:"Loot crate",all_table:"Everything"}[r.k];
    if(!T) return '<div class="li">'+glyph("?")+'<span class="t">'+verb+' from table '+esc(r.t)+' <small>table not found</small></span></div>';
    const tw=T.r.reduce((a,x)=>a+(x.w||0),0)||1;
    return '<div class="li">'+glyph(r.k==="choice"?"PICK":"RNG")+'<span class="t">'+verb+': '+fmt(T.t)+'<small>'+T.r.length+' entries'+(T.ls>1?' · '+T.ls+' rolls':'')+'</small></span></div>'+
      '<details class="tbl"><summary>Show table</summary>'+T.r.map(x=>{ const pc=r.k==="choice"?"":' <span class="cnt">'+(100*(x.w||0)/tw).toFixed(x.w/tw<0.1?1:0)+'%</span>';
        return x.k==="item"? '<div class="li">'+iconHTML(x.i,20)+'<span class="t">'+esc(itemName(x.i))+'</span><span class="cnt">'+(x.n>1?'×'+x.n:'')+'</span>'+pc+'</div>'
             : '<div class="li">'+glyph(x.k.slice(0,3).toUpperCase())+'<span class="t">'+esc(x.k)+' '+(x.n||'')+'</span>'+pc+'</div>'; }).join("")+'</details>'; }
  return '<div class="li">'+glyph("?")+'<span class="t">'+esc(r.type||r.k)+'<small>'+esc(r.v||"")+'</small></span></div>';
}
const FLAGTXT={optional:"Optional",invisible:"Hidden until unlocked",secret:"Secret",hide_until_deps_complete:"Hidden until deps complete",
  hide_until_deps_visible:"Hidden until deps visible",hide_text_until_complete:"Text hidden until complete",
  hide_details_until_startable:"Details hidden until startable",can_repeat:"Repeatable",hide_dependency_lines:"Hides its dependency lines",
  hide_dependent_lines:"Hides lines to dependents"};
function select(id, nodeIdx){
  sel=id; selNode = nodeIdx!==undefined? nodeIdx : (nodeOfQuest[id]!==undefined?nodeOfQuest[id]:-1);
  const Q=D.q[id], P_=$("#panel"), c=D.ch[Q.c];
  let h='<div class="hd">'+iconHTML(Q.ic,40)+'<div style="min-width:0;flex:1"><h3>'+fmt(Q.t)+'</h3>'+(Q.st?'<div class="stl">'+fmt(Q.st)+'</div>':'')+
    '<div class="where"><a class="q" data-ch="'+Q.c+'">'+esc(c.t)+'</a>'+(Q.lb?' · '+esc(Q.lb):'')+'</div></div><button class="btn x" aria-label="Close">✕</button></div><div class="bd">';
  if(nodeIdx!==undefined && D.ch[cur] && D.ch[cur].n[nodeIdx] && D.ch[cur].n[nodeIdx][5])
    h+='<div class="chips" style="margin-bottom:8px"><span class="chip warn">Quest link: this quest lives in '+esc(c.t)+'</span> <a class="q" data-go="'+id+'" data-force="1">Go there</a></div>';
  if(Q.fl.length) h+='<div class="chips">'+Q.fl.map(f=>'<span class="chip'+(f==="optional"?'':' warn')+'">'+esc(FLAGTXT[f]||f.replace(/_/g," "))+'</span>').join("")+'</div>';
  if(Q.d.length) h+='<h4>Description</h4><div class="desc">'+Q.d.map(descLine).join("")+'</div>';
  h+='<h4>Tasks ('+Q.tk.length+')</h4>'+(Q.tk.map(taskHTML).join("")||'<div class="li">None</div>');
  h+='<h4>Rewards</h4>'+(Q.rw.map(rewardHTML).join("")||'<div class="li">None</div>');
  h+='<h4>Needs ('+Q.dp.length+')</h4>'+(Q.dp.map(qlink).join("")||'<div class="li" style="color:var(--muted)">Nothing: a starting quest</div>');
  h+='<h4>Unlocks ('+Q.dn.length+')</h4>'+(Q.dn.map(qlink).join("")||'<div class="li" style="color:var(--muted)">Nothing</div>');
  h+='<div class="id">quest '+esc(id)+' · chapter file '+esc(c.f)+'.snbt</div></div>';
  P_.innerHTML=h; P_.classList.add("open"); P_.scrollTop=0;
  if(location.hash!=="#q="+id) history.replaceState(null,"","#q="+id);
  draw();
}
function closePanel(){ $("#panel").classList.remove("open"); sel=null; selNode=-1; draw(); }
$("#panel").addEventListener("click",e=>{
  if(e.target.closest(".x")) return closePanel();
  const a=e.target.closest("[data-go]"); if(a){ goTo(a.dataset.go, !!a.dataset.force); return; }
  const c=e.target.closest("[data-ch]"); if(c){ openChapter(+c.dataset.ch); }
});
function goTo(id, force){
  const Q=D.q[id]; if(!Q) return;
  if(Q.c!==cur || force){ if(Q.c!==cur) openChapter(Q.c,true); }
  else if(!force && nodeOfQuest[id]===undefined){ openChapter(Q.c,true); }
  const ni=nodeOfQuest[id]; if(ni!==undefined) centerOn(D.ch[cur].n[ni]);
  select(id, ni);
}

/* ---------- start ---------- */
function fromHash(){
  const h=decodeURIComponent(location.hash.slice(1));
  if(h.startsWith("q=")&&D.q[h.slice(2)]){ goTo(h.slice(2)); return true; }
  if(h.startsWith("c=")){ const ci=D.ch.findIndex(c=>c.f===h.slice(2)||c.id===h.slice(2)); if(ci>=0){ openChapter(ci); return true; } }
  return false;
}
window.QMAP_DEBUG={hit:(x,y)=>hit(x,y),state:()=>({cur,view,hov,sel,selNode,drag,ptr:ptr.size})};
resize();
renderList();
if(!fromHash()) openChapter(0);
window.addEventListener("hashchange",fromHash);
})();
</script>
</body></html>
"""

if __name__ == "__main__":
    main()
