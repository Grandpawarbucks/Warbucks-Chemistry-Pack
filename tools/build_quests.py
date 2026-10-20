#!/usr/bin/env python3
"""Build the FTB Quests book (pack/config/ftbquests/quests/) from the data in this file.

Format matches FTB Quests 2101.1.36 (checked against its source): data.snbt, chapter_groups.snbt,
chapters/<name>.snbt, and all text in lang/en_us.snbt under keys "<type>.<HEXID>.<key>".
Every item and dimension id is checked against test/ids.tsv (run test/build_id_index.py);
the build fails on any unknown id, so the book can't reference things that don't exist.

Quest positions are computed by tools/layout.py (automatic layout) just before writing, except in chapters
declared with Chapter(..., layout="manual"). Then tools/quest_overrides.json (written by tools/quest_editor.py)
is applied on top: dragged positions and edited title/subtitle/description text.

Every run (build or --check) also runs the cheap checks of tools/quest_audit.py (dependency cycles, unreachable
quests, required-behind-optional warnings, item/entity/biome/structure/dimension id kinds); errors stop the build.
For the full audit (unobtainable items, tier sanity) see tools/quest_audit.py --full.

Usage: python3 tools/build_quests.py               build into pack/config/ftbquests/quests (+ docs/QUESTS.md)
       python3 tools/build_quests.py --check       validate only, write nothing
       python3 tools/build_quests.py --layout-report   per-chapter layout metrics, hand x/y vs automatic layout
       QUEST_OUT=<folder> python3 tools/build_quests.py   build somewhere else (QUESTS.md goes into that folder too)
"""
import hashlib
import os
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from questlib import ROOT, ERRORS as errors, check  # noqa: E402
from quest_data import CHAPTERS, GROUPS, BOOK_TITLE, REWARD_TABLES, ONLY, UNLISTED  # noqa: E402
from quest_data import load_overrides, apply_overrides  # noqa: E402  (tools/quest_overrides.json, quest editor)
import layout  # noqa: E402

if os.environ.get("QUEST_OUT"):
    OUT = pathlib.Path(os.environ["QUEST_OUT"]).resolve()
    DOC = OUT / "QUESTS.md"
else:
    OUT = ROOT / "pack/config/ftbquests/quests"
    DOC = ROOT / "docs/QUESTS.md"
TOP = "top"  # ungrouped chapters: written with group "" so FTB Quests lists them above the first group tab


def hexid(key):
    """Stable 16-hex-digit id from a key (first digit 0-7 so it parses as a signed long)."""
    n = int(hashlib.sha1(key.encode()).hexdigest()[:16], 16) & 0x7FFFFFFFFFFFFFFF
    return f"{n:016X}"


# --- SNBT writer ------------------------------------------------------------------------------
def snbt(v, indent=0):
    pad, inner = "\t" * indent, "\t" * (indent + 1)
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, Long):
        return f"{int(v)}L"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, float):
        return f"{v}d"
    if isinstance(v, str):
        return '"' + v.replace("\\", "\\\\").replace('"', '\\"') + '"'
    if isinstance(v, list):
        if not v:
            return "[ ]"
        return "[\n" + "\n".join(inner + snbt(x, indent + 1) for x in v) + "\n" + pad + "]"
    if isinstance(v, dict):
        if not v:
            return "{ }"
        return "{\n" + "\n".join(f"{inner}{key(k)}: {snbt(x, indent + 1)}" for k, x in v.items()) + "\n" + pad + "}"
    raise TypeError(v)


def key(k):
    """SNBT keys with characters outside [A-Za-z0-9_.+-] (e.g. "ftbfiltersystem:filter") must be quoted."""
    import re
    return k if re.fullmatch(r"[A-Za-z0-9_.+-]+", k) else snbt(k)


class Long(int):
    pass


# --- build ------------------------------------------------------------------------------------
def build():
    keys = {q.key: hexid("quest:" + q.key) for c in CHAPTERS for q in c.quests}
    lang = {"file.0000000000000001.title": BOOK_TITLE}
    for c in CHAPTERS:
        for q in c.quests:
            for d in q.deps:
                if d not in keys:
                    errors.append(f"dependency {d} (from {q.key})")
            for tkey in (q.loot, q.choice):
                if tkey and tkey not in REWARD_TABLES:
                    errors.append(f"reward table {tkey} (from {q.key})")
            # FTB Quests refuses to render "&" before whitespace ("Invalid formatting! ... escape with \&")
            for text in [q.title or "", q.subtitle or "", *q.desc]:
                if re.search(r"(?<!\\)&(\s|$)", text):
                    errors.append(f"bare '&' in text (write 'and' or \\&) (from {q.key}): {text[:60]!r}")
        for lk, _, _ in c.links:
            if lk not in keys:
                errors.append(f"quest link {lk} (in chapter {c.key})")
    if ONLY:  # partial check: deps on quests in chapters that weren't loaded are fine if the key exists somewhere
        known = {k for f in (ROOT / "tools/quests").glob("*.py") for k in re.findall(r'Q\(\s*"([^"]+)"', f.read_text(encoding="utf-8"))}
        errors[:] = [e for e in errors if not (e.startswith(("dependency ", "quest link ")) and e.split()[-3 if e.startswith("dependency") else 2] in known)]
        if "--check" not in sys.argv:
            sys.exit("QUEST_ONLY is for --check only")
    if UNLISTED and not ONLY:
        print("WARNING: chapter files not in LAYOUT (tools/quest_data.py), so not built: " + ", ".join(UNLISTED))
    if errors:
        sys.exit("Unknown ids/dependencies:\n  " + "\n  ".join(sorted(set(errors))))
    dup = [k for k in keys if sum(1 for c in CHAPTERS for q in c.quests if q.key == k) > 1]
    if dup:
        sys.exit("Duplicate quest keys: " + ", ".join(sorted(set(dup))))
    audit()  # tools/quest_audit.py cheap checks: cycles, reachability, ids and their kinds (fails on errors)
    style_quests()  # tools/quest_style.py: shapes and sizes by role, BEFORE the layout (it spaces quests by size)
    if "--layout-report" in sys.argv:
        print(layout.report(CHAPTERS, lambda c: layout.apply(c, set(keys)),
                            before_fn=lambda c: layout.apply_legacy(c, set(keys))))
        return
    if "--check" in sys.argv:
        for c in CHAPTERS:  # the layout must run cleanly on every chapter too
            layout.apply(c, set(keys))
        n_over = overrides()
        print(f"OK: {len(CHAPTERS)} chapters, {len(keys)} quests, all ids and dependencies valid (nothing written)"
              + (f"; {n_over} editor override(s)" if n_over else ""))
        return
    for c in CHAPTERS:
        layout.apply(c, set(keys))
    overrides()

    # Delete the old files but keep the folders: on Windows, OneDrive or Explorer can hold a folder
    # open, and removing it then fails halfway through.
    if OUT.exists():
        for f in sorted(OUT.rglob("*"), reverse=True):
            if f.is_file():
                f.unlink()
    (OUT / "chapters").mkdir(parents=True, exist_ok=True)
    (OUT / "lang").mkdir(exist_ok=True)

    used = [g for g in GROUPS if g != TOP and any(c.group == g for c in CHAPTERS)]
    group_ids = {g: hexid("group:" + g) for g in used}
    group_ids[TOP] = ""  # FTB Quests' default (ungrouped) group: the "group" field is empty
    (OUT / "data.snbt").write_text(snbt({"version": 13, "progression_mode": "flexible"}) + "\n", encoding="utf-8", newline="\n")
    (OUT / "chapter_groups.snbt").write_text(snbt({"chapter_groups": [{"id": group_ids[g]} for g in used]}) + "\n", encoding="utf-8", newline="\n")
    for g in used:
        lang[f"chapter_group.{group_ids[g]}.title"] = GROUPS[g]

    order = {g: 0 for g in GROUPS}
    total = 0
    for c in CHAPTERS:
        cid = hexid("chapter:" + c.key)
        lang[f"chapter.{cid}.title"] = c.title
        lang[f"chapter.{cid}.chapter_subtitle"] = c.subtitle
        quests = []
        for q in c.quests:
            qid = keys[q.key]
            tasks, rewards = [], []
            for i, t in enumerate(q.tasks):
                tid = hexid(f"task:{q.key}:{i}")
                if t[0] == "item":
                    tasks.append({"id": tid, "type": "item", "item": {"id": t[1], "count": 1}, "count": Long(t[2])})
                    if q.consume:
                        tasks[-1]["consume_items"] = True
                elif t[0] == "dimension":
                    tasks.append({"id": tid, "type": "dimension", "dimension": t[1]})
                elif t[0] == "kill":
                    tasks.append({"id": tid, "type": "kill", "entity": t[1], "value": Long(t[2])})
                elif t[0] == "structure":
                    tasks.append({"id": tid, "type": "structure", "structure": t[1]})
                elif t[0] == "biome":
                    tasks.append({"id": tid, "type": "biome", "biome": t[1]})
                elif t[0] == "filter":
                    tasks.append({"id": tid, "type": "item", "item": {"id": "ftbfiltersystem:smart_filter", "count": 1,
                                  "components": {"ftbfiltersystem:filter": t[1]}}, "count": Long(t[2])})
                else:
                    tasks.append({"id": tid, "type": "checkmark"})
            if q.xp:
                rewards.append({"id": hexid(f"reward:{q.key}:xp"), "type": "xp", "xp": q.xp})
            tokens = q.tokens if q.tokens is not None else c.tokens * (2 if (q.size or 1) >= 1.5 else 1)
            if tokens:
                rewards.append({"id": hexid(f"reward:{q.key}:tokens"), "type": "item",
                                "item": {"id": "kubejs:demigod_token", "count": tokens}})
            for kind, tkey in (("random", q.loot), ("choice", q.choice)):
                if tkey:
                    rewards.append({"id": hexid(f"reward:{q.key}:{kind}"), "type": kind,
                                    "table_id": Long(int(hexid("table:" + tkey), 16))})
            for i, (rid, n) in enumerate(q.items):
                rewards.append({"id": hexid(f"reward:{q.key}:{i}"), "type": "item", "item": {"id": rid, "count": n}})
            entry = {"id": qid, "x": float(q.x), "y": float(q.y)}
            if q.shape:
                entry["shape"] = q.shape
            if q.size:
                entry["size"] = float(q.size)
            if q.optional:
                entry["optional"] = True
            if q.hidden:
                entry["hide_until_deps_visible"] = True
            if q.secret:
                entry["invisible"] = True
            if q.any_dep:
                entry["dependency_requirement"] = "one_completed"
            if q.repeat:
                entry["can_repeat"] = True
            if q.locked_hidden:
                entry["hide_until_deps_complete"] = True
            if getattr(q, "hide_lines", False):  # set by the layout (hub fans, long lines between sections)
                entry["hide_dependency_lines"] = True
            if getattr(q, "hide_dependents", False):  # its lines TO its dependents (e.g. a feeder into the spine)
                entry["hide_dependent_lines"] = True
            if getattr(q, "icon", None):
                entry["icon"] = {"id": q.icon, "count": 1}
            if q.deps:
                entry["dependencies"] = [keys[d] for d in q.deps]
            entry["tasks"] = tasks
            if rewards:
                entry["rewards"] = rewards
            quests.append(entry)
            if q.title:
                lang[f"quest.{qid}.title"] = q.title
            if q.subtitle:
                lang[f"quest.{qid}.quest_subtitle"] = q.subtitle
            if q.desc:
                lang[f"quest.{qid}.quest_desc"] = q.desc
            total += 1
        # Banner (tools/build_art.py) above the topmost quest or link (layout.banner); 960x160 art = 6 x 1 grid cells.
        bx, by = layout.banner(c)
        images = [{"id": hexid(f"image:{c.key}:banner"), "x": float(bx), "y": float(by),
                   "width": 6.0, "height": 1.0, "rotation": 0.0, "image": f"warbucks:textures/quests/{c.key}.png"}]
        for h in c.sections:  # section headers (tools/layout.py), art from section_art()
            images.append({"id": hexid(f"image:{c.key}:section:{h['slug']}"), "x": float(h["x"]), "y": float(h["y"]),
                           "width": float(h["w"]), "height": float(h["h"]), "rotation": 0.0,
                           "image": f"warbucks:textures/quests/sections/{c.key}_{h['slug']}.png"})
        if c.key == "welcome":  # the pack logo (1220x360) above the banner
            images.append({"id": hexid("image:welcome:logo"), "x": float(bx + 0.5), "y": float(by - 2.25),
                           "width": 7.0, "height": 2.07, "rotation": 0.0, "image": "warbucks:textures/quests/logo.png"})
        chapter = {"id": cid, "group": group_ids[c.group], "order_index": order[c.group], "filename": c.key,
                   "icon": {"id": c.icon, "count": 1},
                   "default_quest_shape": "rsquare" if c.group == "main" or c.key == "welcome" else "circle",
                   "default_hide_dependency_lines": False,
                   **({"progression_mode": "linear"} if getattr(c, "linear", False) else {}),
                   "quests": quests, "images": images,
                   # size written out: FTB's QuestLink is 1.0 by default whatever quest it shows (the layout uses 1.0)
                   "quest_links": [{"id": hexid(f"link:{c.key}:{lk}"), "linked_quest": keys[lk], "x": float(lx), "y": float(ly),
                                    "size": 1.0} for lk, lx, ly in c.links]}
        order[c.group] += 1
        (OUT / "chapters" / f"{c.key}.snbt").write_text(snbt(chapter) + "\n", encoding="utf-8", newline="\n")

    section_art()
    chapter_banners()
    (OUT / "reward_tables").mkdir(exist_ok=True)
    for i, (tkey, t) in enumerate(REWARD_TABLES.items()):
        tid = hexid("table:" + tkey)
        lang[f"reward_table.{tid}.title"] = t["title"]
        table = {"id": tid, "order_index": i, "loot_size": t.get("loot_size", 1), "use_title": True,
                 "rewards": [{"id": hexid(f"tablereward:{tkey}:{j}"), "item": {"id": item, "count": n},
                              **({"weight": float(w)} if w != 1 else {})}
                             for j, (item, n, w) in enumerate(t["entries"])]}
        (OUT / "reward_tables" / f"{tkey}.snbt").write_text(snbt(table) + "\n", encoding="utf-8", newline="\n")
    (OUT / "lang" / "en_us.snbt").write_text(snbt(lang) + "\n", encoding="utf-8", newline="\n")
    write_doc(total)
    print(f"Reward tables: {len(REWARD_TABLES)}")
    rel = lambda f: f.relative_to(ROOT) if f.is_relative_to(ROOT) else f
    print(f"Built {len(CHAPTERS)} chapters, {total} quests -> {rel(OUT)} (+ {rel(DOC)})")


def style_quests():
    """Shapes and sizes from each quest's role (tools/quest_style.py, if present). Runs after normalize_milestones
    (quest_data) and before the layout."""
    try:
        import quest_style
    except ImportError:
        return
    for c in CHAPTERS:
        quest_style.apply(c)


SECTION_DIR = ROOT / "pack/kubejs/assets/warbucks/textures/quests/sections"
SECTION_PX = 96   # pixels per grid cell


def _font(size):
    """A bold sans font that exists on this machine (Windows Segoe UI, macOS Avenir Next), else Pillow's default."""
    from PIL import ImageFont
    for path, index in (("C:/Windows/Fonts/segoeuib.ttf", 0), ("/System/Library/Fonts/Avenir Next.ttc", 2),
                        ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 0)):
        if os.path.exists(path):
            return ImageFont.truetype(path, size, index=index)
    return ImageFont.load_default(size)


def section_png(title, w_cells, h_cells):
    """One section header: gold title on a transparent strip, a thin cyan rule under it running to the right edge."""
    from PIL import Image, ImageDraw
    w, h = int(round(w_cells * SECTION_PX)), int(round(h_cells * SECTION_PX))
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    size = int(h * 0.66)
    f = _font(size)
    while d.textlength(title, font=f) > w - 12 and size > 12:
        size -= 2
        f = _font(size)
    asc, desc = f.getmetrics()
    ty = max(0, int(h * 0.70) - asc)  # baseline at 70%: descenders stay above the rule
    d.text((7, ty + 2), title, font=f, fill=(0, 0, 0, 150))          # soft shadow
    d.text((5, ty), title, font=f, fill=(242, 181, 68, 255))         # gold, like the chapter banners
    tw = int(d.textlength(title, font=f))
    y = int(h * 0.90)
    d.line([(5, y), (w - 4, y)], fill=(79, 209, 197, 110), width=max(2, h // 40))   # thin cyan rule, full width
    d.line([(5, y), (min(w - 4, tw + 14), y)], fill=(79, 209, 197, 255), width=max(3, h // 28))
    return img


def section_art():
    """Write the section header PNGs (one per section of every chapter) and delete stale ones. Files are only
    rewritten when their bytes change, so packwiz hashes stay stable."""
    try:
        import PIL  # noqa: F401
    except ImportError:
        print("WARNING: Pillow missing: section header PNGs not regenerated (use the repo .venv)")
        return
    import io
    SECTION_DIR.mkdir(parents=True, exist_ok=True)
    want = set()
    for c in CHAPTERS:
        for h in c.sections:
            name = f"{c.key}_{h['slug']}.png"
            want.add(name)
            buf = io.BytesIO()
            section_png(h["title"], h["w"], h["h"]).save(buf, format="PNG", optimize=True)
            f = SECTION_DIR / name
            if not f.exists() or f.read_bytes() != buf.getvalue():
                f.write_bytes(buf.getvalue())
    stale = [f for f in SECTION_DIR.glob("*.png") if f.name not in want]
    for f in stale:
        f.unlink()
    print(f"Section headers: {len(want)} PNGs in {SECTION_DIR.relative_to(ROOT)}" + (f" ({len(stale)} stale removed)" if stale else ""))


BANNER_DIR = ROOT / "pack/kubejs/assets/warbucks/textures/quests"


def chapter_banners():
    """Chapter banners (tools/build_art.py: the page's element tile and colour, the chapter's sidebar title) for
    every chapter outside the Demigod's Path (its tier art is made by build_art.py itself). A chapter split from a
    mod page (only if quest_data.SPLIT_TABS is switched on) renders in its page's style. Files are only rewritten
    when their bytes change; banners of chapters that no longer exist (old split chapters such as
    "mekanism_the_chemical_plant") are deleted."""
    try:
        import build_art
    except ImportError:
        print("WARNING: Pillow missing: chapter banners not regenerated (use the repo .venv)")
        return
    import tempfile
    from types import SimpleNamespace
    todo = [c for c in CHAPTERS if c.group != "main"]
    n = 0
    with tempfile.TemporaryDirectory() as tmp:
        for c in todo:
            # write_banners names the file and picks the tile by key: render as the page, then store as the chapter
            src = getattr(c, "page", None) or c.key
            build_art.write_banners([SimpleNamespace(key=src, title=c.title)], pathlib.Path(tmp))
            data = (pathlib.Path(tmp) / f"{src}.png").read_bytes()
            f = BANNER_DIR / f"{c.key}.png"
            if not f.exists() or f.read_bytes() != data:
                f.write_bytes(data)
                n += 1
    if ONLY:
        return
    keys = {c.key for c in CHAPTERS} | {getattr(c, "page", None) for c in CHAPTERS} - {None}
    # A stale banner is "<chapter or page key>_<slug>.png" that is no chapter's own (logo/background never match).
    stale = [f for f in BANNER_DIR.glob("*.png") if f.stem not in keys and any(f.stem.startswith(k + "_") for k in keys)]
    for f in stale:
        f.unlink()
    print(f"Chapter banners: {len(todo)} chapters ({n} written)" + (f", {len(stale)} stale removed" if stale else ""))


def audit():
    """Run the cheap quest-audit checks (tools/quest_audit.py): errors stop the build, soft warnings are printed."""
    import quest_audit
    errs, warns = quest_audit.cheap_checks(CHAPTERS, REWARD_TABLES, partial=bool(ONLY))
    if warns:
        print(f"Quest audit warnings ({len(set(warns))}):\n" + quest_audit.fmt(warns))
    if errs:
        sys.exit(f"Quest audit errors ({len(set(errs))}):\n" + quest_audit.fmt(errs))


def overrides():
    """Apply tools/quest_overrides.json (quest editor: positions and text) on top of the layout; warn about bad entries."""
    try:
        data = load_overrides()
    except ValueError as e:  # json.JSONDecodeError is a ValueError
        sys.exit(f"tools/quest_overrides.json is not valid: {e}")
    for w in apply_overrides(CHAPTERS, data):
        print("WARNING: " + w)
    return len(data)


def write_doc(total):
    """Readable overview of the whole book, for reviewing without launching the game."""
    import re
    strip = lambda t: re.sub(r"&[0-9a-fk-or]", "", t)
    names = {q.key: (q.title or "") for c in CHAPTERS for q in c.quests}
    used = [g for g in GROUPS if any(c.group == g for c in CHAPTERS)]
    out = [f"# {BOOK_TITLE}", "",
           f"{len(used) - (TOP in used)} categories, {len(CHAPTERS)} chapters, {total} quests. Generated by "
           "`tools/build_quests.py` from `tools/quest_data.py`; don't edit by hand.", "", "## Sidebar", ""]
    for g in used:  # the book's sidebar: categories (FTB chapter groups) and their chapters, with quest counts
        cs = [c for c in CHAPTERS if c.group == g]
        out.append(f"- **{GROUPS[g] or 'Start here (no category)'}** ({sum(len(c.quests) for c in cs)} quests)")
        out += [f"  - {strip(c.title)} ({len(c.quests)})" for c in cs]
    out.append("")
    for g, gname in GROUPS.items():
        if g not in used:
            continue
        out += [f"## {gname or 'Start here (no group, above the tabs)'}", ""]
        for c in [c for c in CHAPTERS if c.group == g]:
            out += [f"### {c.title}", "", "*" + " ".join(c.subtitle) + "*", ""]
            for n, q in enumerate(c.quests, 1):
                tasks = []
                for t in q.tasks:
                    if t[0] == "item":
                        tasks.append(f"{t[2]}x `{t[1]}`" if t[2] > 1 else f"`{t[1]}`")
                    elif t[0] == "dimension":
                        tasks.append(f"visit `{t[1]}`")
                    elif t[0] == "kill":
                        tasks.append(f"kill {t[2]}x `{t[1]}`")
                    elif t[0] in ("structure", "biome"):
                        tasks.append(f"find {t[0]} `{t[1]}`")
                    elif t[0] == "filter":
                        tasks.append(f"{t[2]}x any of `{t[1]}`")
                    else:
                        tasks.append("checkmark")
                title = q.title or (q.tasks[0][1] if q.tasks[0][0] == "item" else q.key)
                deps = ", ".join(names.get(d) or d for d in q.deps)
                out.append(f"{n}. **{strip(title)}**: {'; '.join(tasks)}" + (f" *(after: {deps})*" if deps else ""))
                for line in q.desc:
                    if line:
                        out.append(f"   > {strip(line)}")
            out.append("")
    DOC.write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    build()
