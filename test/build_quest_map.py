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

Another pack's book (e.g. ATM10, All Rights Reserved: LOCAL ONLY, never publish, never copy into the repo):
  .venv\\Scripts\\python.exe test/build_quest_map.py --book "<instance>\\config\\ftbquests\\quests" --out test/preview/compare/atm10 --no-text
    --no-text drops descriptions, subtitles and chapter images (structure and requirements only, like
    tools/quest_compare.py). Names/icons of items our pack lacks come from <instance>\\mods (+ kubejs\\assets), icons
    cached in test/preview/icons_foreign/<instance>; else "Digital Miner (mekanism)" and a "#" glyph.
    Quests are colour-coded against OUR book by their task items: gold GAP (in test/ids.tsv, never in our book),
    teal covered, grey not in our pack (--no-gaps to skip).
  .venv\\Scripts\\python.exe test/build_quest_map.py --compare --book "<instance>\\config\\ftbquests\\quests"
    both maps (test/preview/compare/atm10 + ours) and the side-by-side page test/preview/compare/index.html
    (launch config "quest-compare": http://localhost:8768/). Must be served over http (the panes talk to each other).
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


def load_ids():
    """Every id test/ids.tsv knows (named or not): "is this in our pack?"."""
    f = ROOT / "test/ids.tsv"
    if not f.exists():
        return set()
    return {line.split("\t")[0] for line in f.read_text(encoding="utf-8").splitlines() if line and not line.startswith("#")}


def pretty(rid):
    s = str(rid).lstrip("#").split(":")[-1].split("/")[-1]
    return s.replace("_", " ").strip().title() or str(rid)


# keys of "other" tasks/rewards that can hold another pack's prose: dropped with --no-text
TEXT_KEYS = {"title", "description", "subtitle", "text", "message", "command", "toast"}


class ForeignAssets:
    """build_quest_preview.Assets, but over ANOTHER instance's mod jars (+ its kubejs/assets): names and icons for
    items our pack does not have. Read-only; nothing from it is written outside test/preview."""

    def __init__(self, mods_dir, kjs_assets=None):
        import glob
        import zipfile
        self.kjs = pathlib.Path(kjs_assets) if kjs_assets else None
        self._index = {}
        for j in sorted(glob.glob(str(pathlib.Path(mods_dir) / "*.jar"))):
            try:
                z = zipfile.ZipFile(j)
            except Exception:
                continue
            for n in z.namelist():
                if n.startswith("assets/") and n not in self._index:
                    self._index[n] = z

    def index(self):
        return self._index

    def read(self, path):
        if self.kjs is not None:
            p = self.kjs / path[len("assets/"):]
            if p.exists():
                return p.read_bytes()
        z = self._index.get(path)
        if z is None:
            return None
        try:
            return z.read(path)
        except KeyError:
            return None

    def lang(self):
        """{item id: English name} from every assets/<ns>/lang/en_us.json (jars, then kubejs/assets wins)."""
        out = {}
        srcs = [(k, None) for k in self._index if k.endswith("/lang/en_us.json") and k.count("/") == 3]
        if self.kjs is not None:
            srcs += [(None, p) for p in sorted(self.kjs.glob("*/lang/en_us.json"))]
        for k, p in srcs:
            try:
                raw = p.read_bytes() if p else self._index[k].read(k)
                js = json.loads(raw.decode("utf-8-sig", errors="replace"))
            except Exception:
                continue
            if not isinstance(js, dict):
                continue
            for key, v in js.items():
                parts = key.split(".")
                if len(parts) == 3 and parts[0] in ("item", "block", "fluid", "entity") and isinstance(v, str):
                    rid = f"{parts[1]}:{parts[2]}"
                    if p or rid not in out:
                        out[rid] = re.sub(r"§.", "", v)
        return out


class ForeignIconCache:
    """IconCache for another instance's jars, cached separately (test/preview/icons_foreign/<label>)."""

    def __init__(self, assets, label):
        from build_quest_preview import ICON_VERSION
        self.A = assets
        self.dir = ROOT / "test/preview/icons_foreign" / label
        ver = self.dir / "_version.txt"
        if not ver.exists() or ver.read_text(encoding="utf-8").strip() != ICON_VERSION:
            import shutil
            shutil.rmtree(self.dir, ignore_errors=True)
            self.dir.mkdir(parents=True, exist_ok=True)
            ver.write_text(ICON_VERSION + "\n", encoding="utf-8", newline="\n")
        mf = self.dir / "_missing.txt"
        self.missing = set(mf.read_text(encoding="utf-8").split()) if mf.exists() else set()
        self.new_missing = False

    def get(self, item_id):
        from PIL import Image
        from build_quest_preview import _icon_image
        if not item_id or ":" not in item_id or item_id in self.missing:
            return None
        ns, path = item_id.split(":", 1)
        f = self.dir / ns / (path.replace("/", "__") + ".png")
        if f.exists():
            return Image.open(f).convert("RGBA")
        im = _icon_image(self.A, item_id)
        if im is None:
            self.missing.add(item_id)
            self.new_missing = True
        else:
            f.parent.mkdir(parents=True, exist_ok=True)
            im.save(f)
        return im

    def save(self):
        if self.new_missing:
            (self.dir / "_missing.txt").write_text("\n".join(sorted(self.missing)) + "\n", encoding="utf-8", newline="\n")


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
    def __init__(self, folder, no_text=False, foreign_names=None):
        from layout_lint import read_snbt, _lang
        self.folder = pathlib.Path(folder)
        self.read = read_snbt
        self.lang = _lang(self.folder)
        self.N = load_names()
        self.no_text = no_text          # drop descriptions, subtitles and chapter images (another pack's prose/art)
        self.foreign = foreign_names    # {id: name} from another instance's jars; None for our own book
        self.ids = load_ids() if foreign_names is not None else set()
        self.items = {}       # item id -> name (icons resolved later)
        self.warnings = []

    def L(self, key, default=None):
        v = self.lang.get(key)
        return default if v in (None, "", []) else v

    # names -----------------------------------------------------------
    def name(self, rid, kind="item"):
        n = self._name(rid, kind)
        return re.sub(r"%(?:\d\$)?s", "", n).strip() or pretty(rid)  # lang templates like "%s%sIron Chest"

    def _name(self, rid, kind="item"):
        rid = str(rid)
        N = self.N
        for k in ((kind,) if kind != "item" else ()) + ("item", "block", "fluid", "entity"):
            n = N.get(k, {}).get(rid)
            if n:
                return n
        if self.foreign is not None and ":" in rid and not rid.startswith("#"):
            n = self.foreign.get(rid)
            if n:
                return n
            if rid not in self.ids:  # not in our pack and no lang name: "Digital Miner (mekanism)"
                return f"{pretty(rid)} ({rid.split(':')[0]})"
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
        return {"k": "other", "type": ty, "v": self._extra(t)}

    def _extra(self, t):
        extra = {k: v for k, v in t.items() if k not in ("id", "type") and not (self.no_text and k in TEXT_KEYS)}
        return json.dumps(extra, ensure_ascii=False)[:200]

    def reward(self, r):
        ty = str(r.get("type", "item" if "item" in r else ""))
        if ty == "item":
            iid, cnt, _ = item_of(r.get("item"))
            return {"k": "item", "i": self.use_item(iid), "n": int(r.get("count", cnt) or cnt)}
        if ty in ("xp", "xp_levels"):
            return {"k": ty, "n": int(r.get("xp", r.get("xp_levels", 0)) or 0)}
        if ty in ("random", "choice", "loot", "all_table"):
            return {"k": ty, "t": table_hex(r.get("table_id", 0))}
        if ty == "currency":
            return {"k": "currency", "n": int(r.get("amount", 0) or 0)}
        return {"k": "other", "type": ty, "v": self._extra(r)}

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
                             "sub": [] if self.no_text else as_list(self.L(f"chapter.{cid}.chapter_subtitle", c.get("subtitle"))),
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
                "c": ci, "t": title,
                "st": "" if self.no_text else str(self.L(f"quest.{qid}.quest_subtitle", q.get("subtitle") or "") or ""),
                "d": [] if self.no_text else as_list(self.L(f"quest.{qid}.quest_desc", q.get("description"))),
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
            for im in ([] if self.no_text else c.get("images", []) or []):
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
def build_icons(book, out_png, foreign=None):
    """foreign: a ForeignIconCache, asked for items our own jars have no icon for."""
    from PIL import Image
    from build_quest_preview import IconCache
    cache = IconCache()
    ids = sorted(book.items)
    found = []
    for i in ids:
        im = None
        for c in (cache, foreign):
            if c is None or im is not None:
                continue
            if c is cache and foreign is not None and i not in book.ids:
                continue  # not in our pack: only the other instance's jars can have it
            try:
                im = c.get(i)
            except Exception as e:  # a broken model should not stop the map
                book.warnings.append(f"icon {i}: {e}")
                im = None
        if im is not None:
            found.append((i, im))
    cache.save()
    if foreign is not None:
        foreign.save()
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


# ------------------------------------------------------------------ gaps (another book vs ours)
def _task_items(Q):
    out = []
    for t in Q["tk"]:
        if t["k"] == "item" and t.get("i"):
            out.append(t["i"])
        elif t["k"] == "any":
            out += [i for i in t["i"] if i]
    return list(dict.fromkeys(out))


_RANK = {"": 0, "n": 1, "c": 2, "g": 3}


def mark_gaps(data, ours, ids):
    """tools/quest_compare.py's question, per quest: which of THEIR task items exist in our pack (test/ids.tsv) but
    are never asked for by OUR book's tasks? Adds to `data` (their book):
      q[id].g    "g" gap / "c" covered / "n" not in our pack / "" no item tasks (g > c > n: any gap item wins)
      gap        {item: [status, [[our quest id, "t" task / "r" reward / "i" icon], ...]]}
      gapList    [[chapter index, [[item, first quest id], ...]], ...] in chapter order
      ch[i].gp   distinct gap items; ch[i].pr  [[our chapter file, title, shared items], ...] (pairing hints)
      ours       {"q": {our qid: [title, chapter title]}} for the COVERED links
    Like quest_compare, item tags are not expanded."""
    # like quest_compare, an item anywhere in our book counts (tasks first, then rewards, then quest icons)
    asked = {}
    our_ch_items = [set() for _ in ours["ch"]]
    for qid, Q in ours["q"].items():
        for i in _task_items(Q):
            asked.setdefault(i, []).append([qid, "t"])
            our_ch_items[Q["c"]].add(i)
    for role, get in (("r", lambda Q: [r.get("i") for r in Q["rw"] if r["k"] == "item"]), ("i", lambda Q: [Q["ic"]])):
        for qid, Q in ours["q"].items():
            for i in dict.fromkeys(get(Q)):
                if i and not any(e[0] == qid for e in asked.get(i, [])):
                    asked.setdefault(i, []).append([qid, role])
    gap, used = {}, set()
    their_ch_items = [dict() for _ in data["ch"]]  # chapter -> {item: first quest}
    for ci, ch in enumerate(data["ch"]):
        for n in ch["n"]:  # map order, so lists follow the chapter
            if n[5]:
                continue
            for i in _task_items(data["q"][n[4]]):
                their_ch_items[ci].setdefault(i, n[4])
    for qid, Q in data["q"].items():
        st = ""
        for i in _task_items(Q):
            if i not in gap:
                s_ = "c" if i in asked else ("g" if i in ids else "n")
                gap[i] = [s_, asked.get(i, [])[:12]]
                used.update(e[0] for e in gap[i][1])
            if _RANK[gap[i][0]] > _RANK[st]:
                st = gap[i][0]
        Q["g"] = st
    gap_list = []
    for ci, ch in enumerate(data["ch"]):
        items = their_ch_items[ci]
        gl = [[i, q] for i, q in items.items() if gap[i][0] == "g"]
        ch["gp"] = len(gl)
        if gl:
            gap_list.append([ci, gl])
        mine = set(items)
        scores = [(len(mine & oset), oi) for oi, oset in enumerate(our_ch_items) if mine & oset]
        if not scores:  # nothing shared: fall back to the mod (namespace) they mostly quest on
            ns = {}
            for i in mine:
                ns[i.split(":")[0]] = ns.get(i.split(":")[0], 0) + 1
            top = [k for k, v in sorted(ns.items(), key=lambda kv: -kv[1]) if k != "minecraft"][:1]
            for oi, oset in enumerate(our_ch_items):
                n = sum(1 for i in oset if i.split(":")[0] in top)
                if n:
                    scores.append((n / 1000, oi))
        scores.sort(key=lambda t: (-t[0], t[1]))
        ch["pr"] = [[ours["ch"][oi]["f"], ours["ch"][oi]["t"], int(n)] for n, oi in scores[:3]]
    data["gap"] = gap
    data["gapList"] = gap_list
    data["ours"] = {"q": {qid: [re.sub(r"&[0-9a-fk-or]", "", ours["q"][qid]["t"]), ours["ch"][ours["q"][qid]["c"]]["t"]]
                          for qid in sorted(used)}}
    return {k: sum(1 for v in gap.values() if v[0] == k) for k in "gcn"}


# ------------------------------------------------------------------ main
def build(book_dir, out, no_text=False, jars=None, kjs_assets=None, gaps_vs=None, label=None):
    """Build one map into `out`. With jars (another instance's mods folder), names/icons of items our pack lacks come
    from there; with gaps_vs (our quests folder), the book gets gap marks against it."""
    out = pathlib.Path(out)
    out.mkdir(parents=True, exist_ok=True)
    fa = fnames = None
    if jars:
        print(f"Indexing {jars} ...")
        fa = ForeignAssets(jars, kjs_assets)
        fnames = fa.lang()
        print(f"  {len(fa.index())} assets, {len(fnames)} lang names")
    book = Book(book_dir, no_text=no_text, foreign_names=(fnames or {}) if (jars or gaps_vs) else None)
    data, image_names = book.load()
    if gaps_vs:
        ours, _ = Book(gaps_vs).load()
        n = mark_gaps(data, ours, book.ids or load_ids())
        print(f"Gap marks vs {gaps_vs}: {n['g']} GAP items (in our pack, not in our book), {n['c']} covered, "
              f"{n['n']} not in our pack")
    foreign = ForeignIconCache(fa, label or pathlib.Path(jars).parent.name.replace(" ", "_")) if fa else None
    items, nf, ni = build_icons(book, out / "icons.png", foreign)
    rects, asz = build_images(image_names, book, out / "images.webp")
    data.update({"items": items, "img": rects, "iconCols": ICON_COLS, "iconSize": ICON, "noText": bool(no_text),
                 "built": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")})
    # sanity: a book read while the generator is rewriting it shows up as missing text or tables
    untitled = sum(1 for qid in data["q"] if f"quest.{qid}.title" not in book.lang)
    missing_t = {r["t"] for Q in data["q"].values() for r in Q["rw"] if "t" in r and r["t"] not in data["tables"]}
    if untitled and not gaps_vs:  # other packs often leave titles to FTB (the item's name)
        book.warnings.append(f"{untitled} quests have no title in lang (inline titles, or the book is being rebuilt)")
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
    return data


def _instance_of(book_dir):
    """<instance>/config/ftbquests/quests -> <instance>, if it has a mods folder."""
    p = pathlib.Path(book_dir).resolve()
    inst = p.parent.parent.parent
    return inst if (inst / "mods").is_dir() and p != DEFAULT_BOOK.resolve() else None


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--book", default=str(DEFAULT_BOOK), help="config/ftbquests/quests folder (default: ours)")
    ap.add_argument("--out", default=None, help="output folder (default test/preview/map)")
    ap.add_argument("--no-text", action="store_true",
                    help="drop quest descriptions, subtitles, chapter subtitles and chapter images (another pack's book)")
    ap.add_argument("--jars", help="mods folder for names/icons of items our pack lacks (default: the book's instance)")
    ap.add_argument("--no-gaps", action="store_true", help="another book: skip the gap marks against ours")
    ap.add_argument("--compare", action="store_true",
                    help="side-by-side page: --book (another pack) -> <dir>/atm10 with --no-text and gap marks, our "
                         "book -> <dir>/ours, plus <dir>/index.html")
    ap.add_argument("--compare-dir", default=str(ROOT / "test/preview/compare"))
    args = ap.parse_args()
    theirs = pathlib.Path(args.book).resolve() != DEFAULT_BOOK.resolve()
    inst = _instance_of(args.book) if theirs else None
    jars = args.jars or (str(inst / "mods") if inst else None)
    kjs = str(inst / "kubejs/assets") if inst and (inst / "kubejs/assets").is_dir() else None
    label = inst.name.replace(" ", "_") if inst else None
    if args.compare:
        if not theirs:
            ap.error("--compare needs --book <the other pack's quests folder>")
        cdir = pathlib.Path(args.compare_dir)
        print("== ours ==")
        build(DEFAULT_BOOK, cdir / "ours")
        print("== theirs ==")
        data = build(args.book, cdir / "atm10", no_text=True, jars=jars, kjs_assets=kjs, gaps_vs=DEFAULT_BOOK, label=label)
        title = re.sub(r"&[0-9a-fk-or]", "", data["title"])
        (cdir / "index.html").write_text(COMPARE_PAGE.replace("__THEIRS__", _esc(title)), encoding="utf-8", newline="\n")
        print(f"Compare page: {cdir / 'index.html'}")
        return
    if theirs and not args.no_text:
        print("NOTE: another pack's book: consider --no-text (its descriptions are usually All Rights Reserved)")
    build(args.book, args.out or DEFAULT_OUT, no_text=args.no_text, jars=jars, kjs_assets=kjs,
          gaps_vs=DEFAULT_BOOK if theirs and not args.no_gaps else None, label=label)


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
.gapui{display:none}
body.gaps .gapui{display:inline-block}
.badge{background:#f2b544;color:#2a1d00;border-radius:999px;padding:0 6px;font-size:11px;font-weight:700;line-height:17px;min-width:18px;text-align:center}
.grp>button .badge{margin-left:6px}
#dock{position:absolute;left:12px;bottom:12px;display:flex;flex-wrap:wrap;gap:6px;align-items:center;max-width:calc(100% - 170px);z-index:4}
#dock .lg{display:inline-flex;align-items:center;gap:5px;background:rgba(22,22,28,.85);border:1px solid #3a3a46;color:#d8d8e2;border-radius:999px;padding:2px 9px 2px 5px;font-size:11.5px}
#dock .lg i{width:12px;height:12px;border-radius:3px;display:inline-block;border:2px solid}
#dock .pair{background:rgba(30,30,38,.92);border:1px solid #52d6ff;color:#cfefff;border-radius:6px;padding:4px 9px;font-size:12.5px;cursor:pointer}
#dock .pair:hover{background:#1f3440}
#dock .pair small{color:#8fb7c9;margin-left:4px}
.gs{font-size:12px;margin:2px 0 4px 32px;padding:3px 8px;border-radius:5px;border-left:3px solid}
.gs.g{background:var(--accent-soft);border-color:#d39b2a}
.gs.c{background:rgba(60,143,138,.14);border-color:#3c8f8a}
.gs.n{background:var(--surface-2);border-color:#777;color:var(--muted)}
.gs a{margin-right:4px}
.fo{margin-left:6px;background:none;border:1px solid var(--border);border-radius:5px;padding:1px 6px;font-size:11.5px;color:var(--link);cursor:pointer;white-space:nowrap}
.fo:hover{border-color:var(--link)}
.any .fo{margin-left:2px;padding:0 4px}
.note{font-size:12px;color:var(--muted);background:var(--surface-2);border-radius:6px;padding:6px 9px;margin-top:8px}
.gl-ch{display:flex;align-items:center;gap:8px;margin:16px 0 4px;font-weight:600}
.gl-ch .n{color:var(--muted);font-weight:400;font-size:12px}
#toast{position:absolute;left:50%;top:12px;transform:translateX(-50%);background:rgba(20,20,26,.95);color:#fff;border:1px solid #52d6ff;border-radius:6px;padding:6px 12px;font-size:13px;z-index:12;display:none;max-width:90%;text-align:center}
.ic.none{display:inline-flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;color:var(--muted)}
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
  #dock{max-width:calc(100% - 150px)}
  #dock .lg{display:none}
}
</style></head>
<body>
<div id="app">
<header>
  <button class="btn" id="menuBtn" aria-label="Chapters">&#9776;</button>
  <h1 id="bookTitle">__TITLE__ <small id="stats"></small></h1>
  <button class="btn gapui" id="gapsBtn" title="Every GAP item (in our pack, never asked for by our book), by chapter">Gaps list</button>
  <button class="btn gapui" id="gapOnlyBtn" title="Fade everything but GAP quests; sidebar shows only chapters with gaps">Gaps only</button>
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
  <div id="dock"></div>
  <div id="toast"></div>
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
/* embedded in the compare page (test/preview/compare/index.html): ?side=atm|ours, parent.QCOMPARE does the cross-pane work */
const SIDE = new URLSearchParams(location.search).get("side") || "";
let CMP = null; try{ CMP = (window.parent!==window && window.parent.QCOMPARE) || null; }catch(e){ CMP=null; }
const GAPS = !!D.gap;
if(GAPS) document.body.classList.add("gaps");
let gapsOnly=false;
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
  if(k<0) return '<span class="ic none" style="width:'+px+'px;height:'+px+'px" title="'+esc(id||"")+'">'+(id&&px>=18?'#':'')+'</span>';
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
const LSK="qmap.closed"+(SIDE?"."+SIDE:"");
try{closed=JSON.parse(localStorage.getItem(LSK)||"{}")}catch(e){}
function renderList(){
  const q=$("#q").value.trim().toLowerCase();
  const L=$("#list"); let h="";
  if(q.length>=2){ h=searchHTML(q); }
  else{
    D.groups.forEach((g,gi)=>{
      const chs=g.ch.filter(ci=>!gapsOnly||D.ch[ci].gp>0); if(!chs.length) return;
      const qc=chs.reduce((a,c)=>a+D.ch[c].qc,0), gp=GAPS?chs.reduce((a,c)=>a+(D.ch[c].gp||0),0):0;
      h+='<div class="grp'+(closed[g.id||"_"]?" closed":"")+'" data-g="'+esc(g.id||"_")+'"><button><span class="car">▾</span>'+esc(strip(g.t))+
         (gp?'<span class="badge" title="gap items in this group">'+gp+'</span>':'')+
         '<span class="n">'+chs.length+' ch · '+qc+'</span></button><div class="chs">';
      chs.forEach(ci=>{ const c=D.ch[ci];
        h+='<button class="row'+(ci===cur?" cur":"")+'" data-c="'+ci+'">'+iconHTML(c.ic,22)+'<span class="t">'+esc(c.t)+'</span>'+
           (c.gp?'<span class="badge" title="'+c.gp+' gap items: in our pack, never asked for by our book">'+c.gp+'</span>':'')+'<span class="n">'+c.qc+'</span></button>'; });
      h+='</div></div>';
    });
  }
  L.innerHTML=h;
}
$("#list").addEventListener("click",e=>{
  const g=e.target.closest(".grp>button");
  if(g){ const el=g.parentNode, id=el.dataset.g; el.classList.toggle("closed"); closed[id]=el.classList.contains("closed");
    try{localStorage.setItem(LSK,JSON.stringify(closed))}catch(err){} return; }
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
  HAY[id]={t:strip(Q.t).toLowerCase(), items:items.map(([i,n])=>[i,n,(n+" "+(i||"")).toLowerCase()]),
    rw:Q.rw.filter(r=>r.k==="item"&&r.i).map(r=>r.i)};
}
const ITEMRE=/^[a-z0-9_.\-]+:[a-z0-9_.\/\-]+$/;
function searchHTML(q){
  let h="", chs=[];
  D.ch.forEach((c,ci)=>{ if(c.t.toLowerCase().includes(q)||c.f.toLowerCase().includes(q)) chs.push(ci); });
  if(chs.length){ h+='<div class="sec">Chapters</div>';
    chs.forEach(ci=>{const c=D.ch[ci]; h+='<button class="row" data-c="'+ci+'">'+iconHTML(c.ic,22)+'<span class="t">'+esc(c.t)+'</span><span class="n">'+c.qc+'</span></button>';}); }
  const res=[], exact=ITEMRE.test(q);
  for(const id in HAY){ const H_=HAY[id]; let sc=0, why="";
    if(exact){  // "find in other book": quests that ask for exactly this item (then ones that reward it)
      if(H_.items.some(x=>x[0]===q)){ sc=5; why=itemName(q); }
      else if(H_.rw.indexOf(q)>=0){ sc=1; why=""; }
      if(sc) res.push([sc,id,sc===1?"":why,sc===1]); continue; }
    if(H_.t.startsWith(q)) sc=3; else if(H_.t.includes(q)) sc=2;
    const m=H_.items.find(x=>x[2].includes(q)); if(m){ if(!sc) sc=1; why=m[1]; }
    if(sc) res.push([sc,id,why]); }
  res.sort((a,b)=>b[0]-a[0]||strip(D.q[a[1]].t).localeCompare(strip(D.q[b[1]].t)));
  h+='<div class="sec">Quests ('+res.length+(res.length>200?", first 200":"")+')</div>';
  res.slice(0,200).forEach(([sc,id,why,rwd])=>{ const Q=D.q[id];
    h+='<button class="row" data-q="'+id+'">'+iconHTML(Q.ic,22)+'<span class="t">'+fmt(Q.t)+'<small>'+esc(D.ch[Q.c].t)+(why?' · needs '+esc(why):'')+(rwd?' · rewards it':'')+'</small></span></button>'; });
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
  renderDock();
  if(sel && !keepView && D.q[sel].c!==ci){ $("#panel").classList.remove("open"); sel=null; }  // browsing away: close
  selNode = sel? (nodeOfQuest[sel]!==undefined? nodeOfQuest[sel] : -1) : -1;
  if(!keepView) fit();
  renderList();
  const r=$('#list .row.cur'); if(r) r.scrollIntoView({block:"nearest"});
  draw();
}
function renderDock(){
  let h="";
  const c=D.ch[cur];
  if(CMP && c && c.pr && c.pr.length)
    h+=c.pr.map(p=>'<button class="pair" data-pair="'+esc(p[0])+'" title="Open our chapter in the right-hand pane">compare with → '+esc(strip(p[1]))+
      (p[2]?'<small>'+p[2]+' shared</small>':'<small>same mod</small>')+'</button>').join("");
  if(GAPS) h+='<span class="lg"><i style="background:#5b4512;border-color:#f2b544"></i>GAP</span><span class="lg"><i style="background:#1d3b3b;border-color:#3c8f8a"></i>covered</span>'+
    '<span class="lg"><i style="background:#2b2b30;border-color:#5c5c66"></i>not in our pack</span><span class="lg"><i style="background:#3a3a45;border-color:#a7a7b4"></i>no items</span>';
  $("#dock").innerHTML=h;
}
$("#dock").addEventListener("click",e=>{ const b=e.target.closest("[data-pair]"); if(b&&CMP) CMP.open(SIDE,b.dataset.pair); });
let toastT;
function toast(t){ const el=$("#toast"); el.textContent=t; el.style.display="block"; clearTimeout(toastT); toastT=setTimeout(()=>{el.style.display="none"},3500); }
function bounds(){
  const c=D.ch[cur]; let x0=1e9,y0=1e9,x1=-1e9,y1=-1e9;
  c.n.forEach(n=>{const r=n[2]/2; x0=Math.min(x0,n[0]-r);y0=Math.min(y0,n[1]-r);x1=Math.max(x1,n[0]+r);y1=Math.max(y1,n[1]+r+0.5);});
  c.im.forEach(m=>{ const a=m[4]*Math.PI/180, hw=(Math.abs(Math.cos(a))*m[2]+Math.abs(Math.sin(a))*m[3])/2, hh=(Math.abs(Math.sin(a))*m[2]+Math.abs(Math.cos(a))*m[3])/2;
    x0=Math.min(x0,m[0]-hw);y0=Math.min(y0,m[1]-hh);x1=Math.max(x1,m[0]+hw);y1=Math.max(y1,m[1]+hh); });
  if(x0>x1){x0=y0=-1;x1=y1=1;}
  return [x0,y0,x1,y1];
}
let autoView=false;  // the view is still the automatic fit: refit when the canvas changes size
function fit(){
  if(cur<0) return; const [x0,y0,x1,y1]=bounds(); const top=window.innerWidth<=760?36:56;
  const s=Math.max(4,Math.min(64,Math.min((W-40)/(x1-x0+1),(H-top-30)/(y1-y0+1))));
  view.s=s; view.ox=W/2-(x0+x1)/2*s; view.oy=top+(H-top)/2-(y0+y1)/2*s; autoView=true; draw();
}
function centerOn(n){ autoView=false; const s=Math.max(view.s,36); view.s=s;
  const pw = window.innerWidth>760? Math.min(390,W*0.5) : 0, ph = window.innerWidth>760? 0 : H*0.62;  // keep it clear of the panel
  view.ox=(W-pw)/2-n[0]*s; view.oy=(H-ph)/2+(ph?10:0)-n[1]*s; }
function zoomAt(f,px,py){ autoView=false; const s=Math.max(3,Math.min(180,view.s*f)); f=s/view.s;
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
    const G = GAPS? Q.g : null, faded = gapsOnly && G!=="g" && i!==selNode;
    const dim = Q.opt||isLink||faded;
    ctx.globalAlpha = faded?0.13:(isLink?0.6:(Q.opt?0.55:(G==="n"?0.75:1)));
    shapePath(sh,cx,cy,r);
    ctx.fillStyle= G==="g"?"#5b4512":G==="c"?"#1d3b3b":G==="n"?"#2b2b30":(isLink?"#2c3440":"#3a3a45"); ctx.fill();
    ctx.lineWidth = (i===selNode)?Math.max(2,s*0.1):(G==="g"?ew*1.6:ew);
    ctx.strokeStyle = (i===selNode)?"#ffcc33":(i===hov?"#ffffff":(G==="g"?"#f2b544":G==="c"?"#3c8f8a":G==="n"?"#5c5c66":(Q.fl.indexOf("invisible")>=0?"#8a6ad0":"#a7a7b4")));
    ctx.stroke();
    // icon
    const k=itemIdx(Q.ic), isz=sz*s*0.62;
    if(k>=0&&iconsOK){ ctx.imageSmoothingEnabled = isz<ICS; ctx.drawImage(icons,(k%ICC)*ICS,Math.floor(k/ICC)*ICS,ICS,ICS,cx-isz/2,cy-isz/2,isz,isz); }
    else{ const t0=Q.tk[0]; const g=t0?(KGLYPH[t0.k]||(t0.k==="item"||t0.k==="any"?"#":"")):"";
      if(g&&isz>8){ ctx.fillStyle="#d8d8e0"; ctx.font="700 "+Math.max(7,Math.min(isz*0.42,22))+"px system-ui,sans-serif"; ctx.textAlign="center"; ctx.textBaseline="middle"; ctx.fillText(g,cx,cy); } }
    // quest-link arrow
    if(isLink&&s>=10){ ctx.globalAlpha=1; const ax=cx+r*0.62, ay=cy-r*0.62, a=Math.max(4,s*0.13);
      ctx.fillStyle="#2b6fd6"; ctx.beginPath(); ctx.arc(ax,ay,a*1.25,0,Math.PI*2); ctx.fill();
      ctx.strokeStyle="#fff"; ctx.lineWidth=Math.max(1.2,a*0.32); ctx.beginPath();
      ctx.moveTo(ax-a*.55,ay+a*.55); ctx.lineTo(ax+a*.55,ay-a*.55); ctx.moveTo(ax-a*.1,ay-a*.55); ctx.lineTo(ax+a*.55,ay-a*.55); ctx.lineTo(ax+a*.55,ay+a*.1); ctx.stroke(); }
    // label
    if(lab && !faded){ ctx.globalAlpha= dim?0.7:1;
      ctx.font=(i===selNode?"600 ":"")+fs+"px system-ui,sans-serif"; ctx.textAlign="center"; ctx.textBaseline="top";
      const t=ellip(Q.lb||strip(Q.t), Math.max(sz,1)*s*1.75), ty=cy+r+2;
      ctx.lineWidth=3; ctx.strokeStyle="rgba(10,10,14,0.9)"; ctx.lineJoin="round"; ctx.strokeText(t,cx,ty);
      ctx.fillStyle= i===selNode?"#ffcc33":"#e6e6ee"; ctx.fillText(t,cx,ty); }
    ctx.globalAlpha=1;
  });
}
function resize(){ const r=cv.getBoundingClientRect(), was=W; dpr=window.devicePixelRatio||1; W=r.width; H=r.height;
  cv.width=Math.round(W*dpr); cv.height=Math.round(H*dpr);
  if(W && cur>=0){ if(!was && sel && nodeOfQuest[sel]!==undefined) centerOn(D.ch[cur].n[nodeOfQuest[sel]]);  // was hidden (compare page)
    else if(!was || autoView) fit(); }
  draw(); }
window.addEventListener("resize",resize);
if(window.ResizeObserver) new ResizeObserver(()=>{ const r=cv.getBoundingClientRect(); if(r.width!==W||r.height!==H) resize(); }).observe(cv);  // iframes: size can arrive late

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
    if(drag.moved){ cv.classList.add("drag"); view.ox=drag.ox+dx; view.oy=drag.oy+dy; autoView=false; $("#tip").style.display="none"; draw(); return; } }
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
const findBtn = (id,short) => CMP&&id? '<button class="fo" data-find="'+esc(id)+'" title="Search the other book for quests that use this item">'+(short?'⇄':'⇄ find in other book')+'</button>' : '';
const ROLE={t:"",r:" (reward)",i:" (icon)"};
function gapHTML(id){
  const G=GAPS&&D.gap[id]; if(!G) return "";
  if(G[0]==="g") return '<div class="gs g"><b>GAP</b> · in our pack, but our book never asks for it</div>';
  if(G[0]==="n") return '<div class="gs n"><b>NOT IN PACK</b> · we do not have this mod/item</div>';
  const refs=G[1].map(([q,role])=>{ const o=(D.ours&&D.ours.q[q])||[q,""];
    return (CMP?'<a class="q" data-oq="'+esc(q)+'" title="Show in our book (right pane)">'+fmt(o[0])+'</a>':'<span>'+fmt(o[0])+'</span>')+
      '<small style="color:var(--muted)"> '+esc(o[1])+ROLE[role||"t"]+'</small>'; });
  return '<div class="gs c"><b>COVERED</b> · our book: '+(refs.join(" · ")||"yes")+'</div>';
}
function taskHTML(t){
  const n=t.n>1?'×'+t.n.toLocaleString():'';
  switch(t.k){
    case "item": return '<div class="li">'+iconHTML(t.i)+'<span class="t">'+esc(itemName(t.i))+'<small>'+esc(t.i)+'</small></span><span class="cnt">'+n+'</span>'+findBtn(t.i)+'</div>'+gapHTML(t.i);
    case "any": return '<div class="li">'+glyph("ANY")+'<span class="t">Any of '+t.i.length+' items'+(t.tags&&t.tags.length?' or #'+esc(t.tags.join(", #")):'')+
       '<span class="any">'+t.i.map(i=>{ const G=GAPS&&D.gap[i]; const bc=G?(G[0]==="g"?"#d39b2a":G[0]==="c"?"#3c8f8a":"#777"):"";
         return '<span title="'+esc(i)+(G?' · '+({g:"GAP",c:"covered",n:"not in our pack"}[G[0]]):'')+'"'+(bc?' style="box-shadow:inset 0 -2px 0 '+bc+'"':'')+'>'+iconHTML(i,18)+esc(itemName(i))+findBtn(i,1)+'</span>'; }).join("")+'</span></span><span class="cnt">'+n+'</span></div>';
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
  if(r.k==="currency") return '<div class="li">'+glyph("$")+'<span class="t">Currency</span><span class="cnt">'+r.n.toLocaleString()+'</span></div>';
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
  else if(D.noText) h+='<div class="note">Requirements only: this book\'s descriptions and subtitles are left out.</div>';
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
  const f=e.target.closest("[data-find]"); if(f){ if(CMP) CMP.find(SIDE,f.dataset.find,itemName(f.dataset.find)); return; }
  const o=e.target.closest("[data-oq]"); if(o){ if(CMP) CMP.goOther(SIDE,o.dataset.oq); return; }
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

/* ---------- gaps list ---------- */
function showGaps(){
  if(!GAPS) return;
  const tot=D.gapList.reduce((a,x)=>a+x[1].length,0), distinct=Object.values(D.gap).filter(v=>v[0]==="g").length;
  let h='<div class="hd">'+glyph("GAP")+'<div style="min-width:0;flex:1"><h3>Gap items</h3><div class="where">'+distinct+' items exist in our pack but our book never asks for them · '+
    tot+' entries in '+D.gapList.length+' chapters (an item can sit in several)</div></div><button class="btn x" aria-label="Close">✕</button></div><div class="bd">';
  D.gapList.forEach(([ci,list])=>{ const c=D.ch[ci];
    h+='<div class="gl-ch">'+iconHTML(c.ic,20)+'<a class="q" data-ch="'+ci+'">'+esc(c.t)+'</a><span class="n">'+list.length+'</span></div>';
    h+=list.map(([i,q])=>'<div class="li">'+iconHTML(i,22)+'<span class="t"><a class="q" data-go="'+esc(q)+'">'+esc(itemName(i))+'</a><small>'+esc(i)+'</small></span></div>').join(""); });
  h+='</div>';
  const P_=$("#panel"); P_.innerHTML=h; P_.classList.add("open"); P_.scrollTop=0; sel=null; selNode=-1; draw();
}
$("#gapsBtn").onclick=showGaps;
$("#gapOnlyBtn").onclick=e=>{ gapsOnly=!gapsOnly; e.target.classList.toggle("on",gapsOnly); renderList(); draw(); };

/* ---------- API for the compare page ---------- */
window.QMAP_API={
  goTo:id=>{ if(!D.q[id]) return false; goTo(id); return true; },
  openChapterFile:f=>{ const ci=D.ch.findIndex(c=>c.f===f||c.id===f); if(ci<0) return false; openChapter(ci); return true; },
  findItem:(id,name)=>{  // list every quest that asks for this item in the sidebar, open the first one
    $("#q").value=id; renderList();
    const hits=Object.keys(HAY).filter(q=>HAY[q].items.some(x=>x[0]===id));
    const rw=Object.keys(HAY).filter(q=>HAY[q].rw.indexOf(id)>=0&&hits.indexOf(q)<0);
    const nm=name||itemName(id);
    if(hits.length){ hits.sort((a,b)=>D.q[a].c-D.q[b].c); goTo(hits[0]); toast(nm+": "+hits.length+(hits.length>1?" quests ask":" quest asks")+" for it"+(rw.length?", "+rw.length+" reward it":"")+" (list in the sidebar)"); }
    else if(rw.length){ goTo(rw[0]); toast(nm+": no quest asks for it; "+rw.length+" reward it"); }
    else toast(nm+": not in this book");
    return hits.length;
  },
  chapters:()=>D.ch.map(c=>[c.f,c.t]),
};

/* ---------- start ---------- */
function fromHash(){
  const h=decodeURIComponent(location.hash.slice(1));
  if(h.startsWith("q=")&&D.q[h.slice(2)]){ goTo(h.slice(2)); return true; }
  if(h.startsWith("c=")){ const ci=D.ch.findIndex(c=>c.f===h.slice(2)||c.id===h.slice(2)); if(ci>=0){ openChapter(ci); return true; } }
  return false;
}
window.QMAP_DEBUG={hit:(x,y)=>hit(x,y),state:()=>({cur,view,hov,sel,selNode,drag,ptr:ptr.size,gapsOnly})};
resize();
renderList();
if(!fromHash()) openChapter(0);
window.addEventListener("hashchange",fromHash);
if(CMP&&CMP.ready) CMP.ready(SIDE);
})();
</script>
</body></html>
"""

COMPARE_PAGE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Quest Book Compare</title>
<style>
:root{--bg:#f4f3ef;--surface:#ffffff;--surface-2:#eceae4;--border:#d6d3cb;--text:#1d1c1a;--muted:#6b6862;--accent:#b7791f;--accent-soft:#f5e6c8;--teal:#2c7f7a}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#121216;--surface:#1b1b21;--surface-2:#24242c;--border:#33333d;--text:#e9e9ee;--muted:#9a9aa6;--accent:#f2b544;--accent-soft:#3a2f17;--teal:#52c7bf}}
:root[data-theme="dark"]{--bg:#121216;--surface:#1b1b21;--surface-2:#24242c;--border:#33333d;--text:#e9e9ee;--muted:#9a9aa6;--accent:#f2b544;--accent-soft:#3a2f17;--teal:#52c7bf}
*{box-sizing:border-box}
html,body{height:100%;margin:0}
body{background:var(--bg);color:var(--text);font:14px/1.4 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;overflow:hidden;display:flex;flex-direction:column;height:100dvh}
header{display:flex;align-items:center;gap:10px;padding:0 12px;height:44px;flex:none;background:var(--surface);border-bottom:1px solid var(--border);min-width:0}
header h1{font-size:15px;margin:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;flex:1;min-width:0}
header h1 small{color:var(--muted);font-weight:400;margin-left:8px}
.tabs{display:none;gap:4px}
.tabs button{font:inherit;color:inherit;background:var(--surface-2);border:1px solid var(--border);border-radius:6px;padding:5px 10px;cursor:pointer}
.tabs button.on{background:var(--accent-soft);border-color:var(--accent)}
main{flex:1;min-height:0;display:grid;grid-template-columns:1fr 1fr;gap:0}
.pane{display:flex;flex-direction:column;min-width:0;min-height:0;border-right:1px solid var(--border)}
.pane:last-child{border-right:0}
.lab{flex:none;height:26px;display:flex;align-items:center;gap:8px;padding:0 10px;font-size:12px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;color:var(--muted);background:var(--surface);border-bottom:1px solid var(--border)}
.lab b{color:var(--text)}
.pane.flash .lab{background:var(--accent-soft)}
iframe{flex:1;width:100%;border:0;min-height:0;background:#16161c}
@media (max-width:900px){
  header h1 small{display:none}
  .tabs{display:flex}
  main{grid-template-columns:1fr}
  .pane{display:none;border-right:0}
  .pane.on{display:flex}
}
</style></head>
<body>
<header>
  <h1>__THEIRS__ &harr; our book <small>left: requirements only (local preview, never publish) &middot; right: our generated book</small></h1>
  <div class="tabs" role="tablist"><button id="tab-atm" class="on" role="tab">ATM10</button><button id="tab-ours" role="tab">Ours</button></div>
</header>
<main>
  <section class="pane on" id="pane-atm"><div class="lab"><b>ATM10</b> gold = gap (in our pack, our book never asks) &middot; teal = covered &middot; grey = not in our pack</div>
    <iframe id="f-atm" title="ATM10 quest map" src="atm10/quest-map.html?side=atm"></iframe></section>
  <section class="pane" id="pane-ours"><div class="lab"><b>Ours</b> Warbucks Chemistry</div>
    <iframe id="f-ours" title="Our quest map" src="ours/quest-map.html?side=ours"></iframe></section>
</main>
<script>
(function(){
"use strict";
const other = s => s==="atm" ? "ours" : "atm";
const frame = s => document.getElementById("f-"+s);
const api = s => { try{ return frame(s).contentWindow.QMAP_API || null; }catch(e){ return null; } };
const ready = {atm:false, ours:false}, queue = {atm:[], ours:[]};
function show(s){
  const narrow = window.matchMedia("(max-width:900px)").matches;
  ["atm","ours"].forEach(k=>{ document.getElementById("pane-"+k).classList.toggle("on",k===s); document.getElementById("tab-"+k).classList.toggle("on",k===s); });
  if(narrow){ try{ frame(s).contentWindow.dispatchEvent(new Event("resize")); }catch(e){} }
  const p=document.getElementById("pane-"+s); p.classList.add("flash"); setTimeout(()=>p.classList.remove("flash"),700);
}
function run(s, fn){ show(s); if(ready[s] && api(s)) fn(api(s)); else queue[s].push(fn); }
window.QCOMPARE = {
  ready(s){ ready[s]=true; const q=queue[s].splice(0); q.forEach(fn=>fn(api(s))); },
  find(from, id, name){ run(other(from), a=>a.findItem(id, name)); },
  open(from, file){ run(other(from), a=>a.openChapterFile(file)); },
  goOther(from, qid){ run(other(from), a=>a.goTo(qid)); },
  show,
};
document.getElementById("tab-atm").onclick=()=>show("atm");
document.getElementById("tab-ours").onclick=()=>show("ours");
})();
</script>
</body></html>
"""

if __name__ == "__main__":
    main()
