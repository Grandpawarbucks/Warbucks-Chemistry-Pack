"""Dump an ATM10 chapter's structure (ids, positions, tasks, deps) with our-pack availability."""
import sys, re, pathlib, collections
ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import layout_lint
BOOK = pathlib.Path(r"C:\Users\Grandpawarbucks\curseforge\minecraft\Instances\All the Mods 10 - ATM10\config\ftbquests\quests")
IDS = {l.split("\t")[0] for l in (ROOT / "test/ids.tsv").read_text(encoding="utf-8").splitlines()}
# our quests: key -> ids mentioned
OURS = collections.defaultdict(list)
for f in (ROOT / "tools/quests").glob("*.py"):
    txt = f.read_text(encoding="utf-8")
    for m in re.finditer(r'Q\("([a-z0-9_]+)"(.*?)(?=\n\s*Q\(|\Z)', txt, re.S):
        body = m.group(2)
        tasks = body.split('"', 1)[0]
        for iid in re.findall(r'(?:item|anyof|anytag)\((?:\[)?"([a-z0-9_.\-]+:[a-z0-9_./\-]+)"', body):
            OURS[iid].append(f"{f.stem}:{m.group(1)}")
        for iid in re.findall(r'anyof\(\[([^\]]*)\]', body):
            for i in re.findall(r'"([^"]+)"', iid):
                OURS[i].append(f"{f.stem}:{m.group(1)}")

def item_of(it):
    return layout_lint._item_id(it)

def tasks_of(q):
    out = []
    for t in q.get("tasks", []):
        ty = t.get("type")
        if ty == "item":
            iid = item_of(t.get("item"))
            cnt = t.get("count", 1)
            if iid == "ftbfiltersystem:smart_filter":
                f = str((t.get("item") or {}).get("components", {}).get("ftbfiltersystem:filter", ""))
                out.append(("F", f, cnt))
            else:
                out.append(("I", iid, cnt))
        elif ty == "checkmark":
            out.append(("C",))
        else:
            v = t.get("entity") or t.get("dimension") or t.get("structure") or t.get("biome") or t.get("advancement") or ""
            out.append((ty, v, t.get("value", t.get("count", ""))))
    return out

def mark(iid):
    if iid in IDS:
        o = sorted(set(OURS.get(iid, [])))
        return "+" + ("[" + ",".join(o[:3]) + "]" if o else "")
    return "-"

stem = sys.argv[1]
c = layout_lint.read_snbt(BOOK / "chapters" / f"{stem}.snbt")
qs = c.get("quests", [])
idx = {str(q["id"]): i for i, q in enumerate(qs)}
print(stem, "quests", len(qs), "default shape", c.get("default_quest_shape"))
for i, q in enumerate(qs):
    deps = [idx.get(str(d), str(d)[:6]) for d in q.get("dependencies", [])]
    ts = tasks_of(q)
    parts = []
    for t in ts:
        if t[0] == "I":
            parts.append(f"{t[1]}x{t[2]}{mark(t[1])}")
        elif t[0] == "F":
            ids = re.findall(r"item\(([a-z0-9_.\-]+:[a-z0-9_./\-]+)\)", t[1])
            tags = re.findall(r"item_tag\(([^)]*)\)", t[1])
            parts.append("ANY(" + " ".join(f"{x}{mark(x)}" for x in ids) + (" tags:" + ",".join(tags) if tags else "") + f")x{t[2]}")
        elif t[0] == "C":
            parts.append("CHECK")
        else:
            parts.append(f"{t[0]}:{t[1]}:{t[2]}")
    flags = ""
    if q.get("optional"): flags += " opt"
    if q.get("invisible"): flags += " inv"
    if q.get("dependency_requirement"): flags += " " + str(q.get("dependency_requirement"))
    print(f"{i:3d} {q['id']} ({q.get('x',0):g},{q.get('y',0):g}) s={q.get('size',1):g} {q.get('shape','')}{flags} deps={deps} :: {' | '.join(parts)}")
