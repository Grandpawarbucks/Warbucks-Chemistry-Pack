#!/usr/bin/env python3
"""Build the FTB Quests book (pack/config/ftbquests/quests/) from the data in this file.

Format matches FTB Quests 2101.1.36 (checked against its source): data.snbt, chapter_groups.snbt,
chapters/<name>.snbt, and all text in lang/en_us.snbt under keys "<type>.<HEXID>.<key>".
Every item and dimension id is checked against test/ids.tsv (run test/build_id_index.py);
the build fails on any unknown id, so the book can't reference things that don't exist.

Usage: python3 tools/build_quests.py
"""
import hashlib
import pathlib
import shutil
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from questlib import ROOT, ERRORS as errors, check  # noqa: E402
from quest_data import CHAPTERS, GROUPS, BOOK_TITLE, REWARD_TABLES, ONLY  # noqa: E402

OUT = ROOT / "pack/config/ftbquests/quests"
DOC = ROOT / "docs/QUESTS.md"


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
        for lk, _, _ in c.links:
            if lk not in keys:
                errors.append(f"quest link {lk} (in chapter {c.key})")
    if ONLY:  # partial check: deps on quests in chapters that weren't loaded are fine if the key exists somewhere
        import re
        known = {k for f in (ROOT / "tools/quests").glob("*.py") for k in re.findall(r'Q\(\s*"([^"]+)"', f.read_text())}
        errors[:] = [e for e in errors if not (e.startswith(("dependency ", "quest link ")) and e.split()[-3 if e.startswith("dependency") else 2] in known)]
        if "--check" not in sys.argv:
            sys.exit("QUEST_ONLY is for --check only")
    if errors:
        sys.exit("Unknown ids/dependencies:\n  " + "\n  ".join(sorted(set(errors))))
    dup = [k for k in keys if sum(1 for c in CHAPTERS for q in c.quests if q.key == k) > 1]
    if dup:
        sys.exit("Duplicate quest keys: " + ", ".join(sorted(set(dup))))
    if "--check" in sys.argv:
        print(f"OK: {len(CHAPTERS)} chapters, {len(keys)} quests, all ids and dependencies valid (nothing written)")
        return

    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "chapters").mkdir(parents=True)
    (OUT / "lang").mkdir()

    group_ids = {g: hexid("group:" + g) for g in GROUPS}
    (OUT / "data.snbt").write_text(snbt({"version": 13}) + "\n")
    (OUT / "chapter_groups.snbt").write_text(snbt({"chapter_groups": [{"id": group_ids[g]} for g in GROUPS]}) + "\n")
    for g, title in GROUPS.items():
        lang[f"chapter_group.{group_ids[g]}.title"] = title

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
        # Banner (tools/build_art.py) above the chapter's top-left quest; 960x160 art = 6 x 1 grid cells.
        minx = min(q.x for q in c.quests)
        miny = min(q.y for q in c.quests)
        images = [{"id": hexid(f"image:{c.key}:banner"), "x": float(minx + 2.5), "y": float(miny - 2.0),
                   "width": 6.0, "height": 1.0, "rotation": 0.0, "image": f"warbucks:textures/quests/{c.key}.png"}]
        if c.key == "welcome":  # the pack logo (1220x360) under the banner area
            images.append({"id": hexid("image:welcome:logo"), "x": float(minx + 3.0), "y": float(miny - 4.25),
                           "width": 7.0, "height": 2.07, "rotation": 0.0, "image": "warbucks:textures/quests/logo.png"})
        chapter = {"id": cid, "group": group_ids[c.group], "order_index": order[c.group], "filename": c.key,
                   "icon": {"id": c.icon, "count": 1},
                   "default_quest_shape": "rsquare" if c.group == "main" else "circle",
                   "default_hide_dependency_lines": False,
                   "quests": quests, "images": images,
                   "quest_links": [{"id": hexid(f"link:{c.key}:{lk}"), "linked_quest": keys[lk], "x": float(lx), "y": float(ly)}
                                   for lk, lx, ly in c.links]}
        order[c.group] += 1
        (OUT / "chapters" / f"{c.key}.snbt").write_text(snbt(chapter) + "\n")

    (OUT / "reward_tables").mkdir(exist_ok=True)
    for i, (tkey, t) in enumerate(REWARD_TABLES.items()):
        tid = hexid("table:" + tkey)
        lang[f"reward_table.{tid}.title"] = t["title"]
        table = {"id": tid, "order_index": i, "loot_size": t.get("loot_size", 1), "use_title": True,
                 "rewards": [{"id": hexid(f"tablereward:{tkey}:{j}"), "item": {"id": item, "count": n},
                              **({"weight": float(w)} if w != 1 else {})}
                             for j, (item, n, w) in enumerate(t["entries"])]}
        (OUT / "reward_tables" / f"{tkey}.snbt").write_text(snbt(table) + "\n")
    (OUT / "lang" / "en_us.snbt").write_text(snbt(lang) + "\n")
    write_doc(total)
    print(f"Reward tables: {len(REWARD_TABLES)}")
    print(f"Built {len(CHAPTERS)} chapters, {total} quests -> {OUT.relative_to(ROOT)} (+ {DOC.relative_to(ROOT)})")


def write_doc(total):
    """Readable overview of the whole book, for reviewing without launching the game."""
    import re
    strip = lambda t: re.sub(r"&[0-9a-fk-or]", "", t)
    names = {q.key: (q.title or "") for c in CHAPTERS for q in c.quests}
    out = [f"# {BOOK_TITLE}", "",
           f"{len(CHAPTERS)} chapters, {total} quests. Generated by `tools/build_quests.py` from `tools/quest_data.py`; don't edit by hand.", ""]
    for g, gname in GROUPS.items():
        out += [f"## {gname}", ""]
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
    DOC.write_text("\n".join(out) + "\n")


if __name__ == "__main__":
    build()
