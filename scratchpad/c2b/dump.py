"""Structural dump of ATM10 chapters (requirements only) with our quest keys that ask for each item."""
import re, sys, pathlib, importlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools")); sys.path.insert(0, str(ROOT / "scratchpad/c3"))
import atm_parse
ours = {}
for f in sorted((ROOT / "tools/quests").glob("*.py")):
    if f.stem.startswith("_"): continue
    try:
        ch = importlib.import_module(f"quests.{f.stem}").CHAPTER
    except Exception as e:
        print("ERR", f.stem, e); continue
    for q in ch.quests:
        for t in q.tasks:
            if t[0] == "item": ours.setdefault(t[1], []).append(q.key)
            elif t[0] == "filter":
                for i in re.findall(r"item\(([^)]+)\)", t[1]): ours.setdefault(i, []).append(q.key + "*")
for stem in sys.argv[1:]:
    rows = atm_parse.parse(stem)
    byid = {r["id"]: i for i, r in enumerate(rows)}
    print(f"===== {stem}: {len(rows)}")
    for i, r in enumerate(rows):
        deps = ",".join(f"#{byid.get(d, '?')}" for d in r["deps"])
        print(f"#{i:<3} {r['id']} ({r['x']},{r['y']}) sz={r['size']} {r['shape']} opt={int(r['opt'])} deps=[{deps}] | {r['title']}")
        for ttype, its, cnt in r["tasks"]:
            marks = []
            for it in its:
                if it.startswith("#"): marks.append(it); continue
                have = it in atm_parse.ids
                marks.append(f"{it}{'' if have else ' [MISSING]'}{' <'+','.join(ours[it])+'>' if it in ours else ''}")
            print(f"        {ttype} x{cnt}: " + ", ".join(marks))
