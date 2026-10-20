"""Dump an ATM10 chapter (requirements only) next to which of our quests ask for each item.
usage: dump.py <stem> [our_chapter_keys,...]"""
import importlib, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from layout_lint import read_snbt  # noqa
ATM = pathlib.Path(r"C:\Users\Grandpawarbucks\curseforge\minecraft\Instances\All the Mods 10 - ATM10\config\ftbquests\quests\chapters")
IDS = {l.split("\t")[0] for l in (ROOT / "test/ids.tsv").read_text(encoding="utf-8").splitlines()}

stem = sys.argv[1]
d = read_snbt(ATM / f"{stem}.snbt")
# our items -> keys (all chapters)
ours = {}
for f in sorted((ROOT / "tools/quests").glob("*.py")):
    if f.stem.startswith("_"):
        continue
    try:
        ch = importlib.import_module(f"quests.{f.stem}").CHAPTER
    except Exception as e:
        print("import fail", f.stem, e); continue
    for q in ch.quests:
        for t in q.tasks:
            ids = []
            if t[0] == "item": ids = [t[1]]
            elif t[0] == "filter": ids = re.findall(r"item\(([^)]+)\)", t[1])
            for i in ids:
                ours.setdefault(i, []).append(f"{ch.key}:{q.key}")

def items_of(task):
    out = []
    it = task.get("item")
    if isinstance(it, dict):
        iid = it.get("id"); comp = it.get("components", {})
        filt = comp.get("ftbfiltersystem:filter") if isinstance(comp, dict) else None
        if filt:
            out += [("F", x) for x in re.findall(r"item\(([a-z0-9_]+:[a-z0-9_/]+)\)", filt)]
            out += [("TAG", x) for x in re.findall(r"item_tag\(([^)]+)\)", filt)]
        else:
            out.append(("I", iid))
    elif isinstance(it, str):
        out.append(("I", it))
    return out

imgs = [(i.get("x", 0), i.get("y", 0), i.get("image", "").split("/")[-1]) for i in d.get("images", [])]
print("IMAGES:")
for x, y, im in sorted(imgs, key=lambda t: (t[1], t[0])):
    print(f"   ({x:6.1f},{y:6.1f}) {im}")
print()
qs = d["quests"]
print(f"{len(qs)} quests; default shape {d.get('default_quest_shape')}")
for q in qs:
    tasks = []
    for t in q.get("tasks", []):
        ty = t.get("type")
        if ty == "item":
            its = items_of(t)
            c = t.get("count", 1)
            tasks.append(" | ".join(f"{k}:{i}{'' if (k=='TAG' or i in IDS) else '!MISSING'}" + (f"[{','.join(ours.get(i, []))}]" if i in ours else "") for k, i in its) + (f" x{c}" if c != 1 else ""))
        else:
            tasks.append(f"<{ty}{':'+str(t.get('dimension') or t.get('entity') or t.get('structure') or t.get('biome') or '') if ty not in ('checkmark',) else ''}>")
    deps = q.get("dependencies", [])
    flags = []
    if q.get("optional"): flags.append("opt")
    if q.get("size"): flags.append(f"size={q['size']}")
    if q.get("shape"): flags.append(f"shape={q['shape']}")
    if q.get("hide_until_deps_visible") or q.get("hide_until_deps_complete"): flags.append("hidden")
    print(f"{q['id']} ({q.get('x',0):5.1f},{q.get('y',0):5.1f}) {' '.join(flags)} deps={','.join(deps) if deps else '-'}")
    for t in tasks:
        print("      ", t)
