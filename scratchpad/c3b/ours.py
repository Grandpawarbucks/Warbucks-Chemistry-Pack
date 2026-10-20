"""Compact listing of our chapter: key, tasks, deps, flags."""
import importlib, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
ch = importlib.import_module(f"quests.{sys.argv[1]}").CHAPTER
print(ch.key, len(ch.quests), "quests; links", [l[0] for l in ch.links], "mirror", ch.mirror)
for q in ch.quests:
    t = []
    for x in q.tasks:
        if x[0] == "item": t.append(f"{x[1]}" + (f" x{x[2]}" if x[2] != 1 else ""))
        elif x[0] == "filter": t.append(f"{x[1]}" + (f" x{x[2]}" if x[2] != 1 else ""))
        else: t.append("<" + ":".join(str(y) for y in x) + ">")
    fl = []
    if q.optional: fl.append("opt")
    if q.size: fl.append(f"s{q.size}")
    if q.section: fl.append(f"sec={q.section}")
    if q.mirror: fl.append(f"m={q.mirror}")
    print(f"{q.key:24} {' '.join(fl):10} deps={','.join(q.deps)}  :: {' ; '.join(t)}  [{q.title}]")
