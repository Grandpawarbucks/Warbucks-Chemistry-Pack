"""Scratch: dump an ATM10 chapter's structure (ids, positions, tasks, deps, sizes) and check items vs test/ids.tsv.
Structure only (ARR): titles are shown for orientation, never copied."""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from layout_lint import read_snbt, _lang  # noqa: E402

ATM = pathlib.Path(r"C:\Users\Grandpawarbucks\curseforge\minecraft\Instances\All the Mods 10 - ATM10\config\ftbquests\quests")

ids = set()
for line in (ROOT / "test/ids.tsv").read_text(encoding="utf-8").splitlines():
    ids.add(line.split("\t")[0])

# our book's item usage (by key) from tools/quests/*.py
ours = {}
for f in (ROOT / "tools/quests").glob("*.py"):
    txt = f.read_text(encoding="utf-8")
    for m in re.finditer(r'Q\("([a-z0-9_]+)"', txt):
        pass
    for m in re.finditer(r'"([a-z0-9_]+:[a-z0-9_/]+)"', txt):
        ours.setdefault(m.group(1), set()).add(f.stem)
P = "powah:"
for f in (ROOT / "tools/quests").glob("*.py"):
    txt = f.read_text(encoding="utf-8")
    for m in re.finditer(r'P \+ "([a-z0-9_]+)"', txt):
        ours.setdefault("powah:" + m.group(1), set()).add(f.stem)


def item_ids(task):
    it = task.get("item")
    if isinstance(it, str):
        return [it]
    if isinstance(it, dict):
        iid = it.get("id")
        if iid == "ftbfiltersystem:smart_filter":
            comp = it.get("components", {})
            s = str(comp)
            s = comp.get("ftbfiltersystem:filter", "")
            out = re.findall(r'item\(([a-z0-9_]+:[a-z0-9_/]+)\)', s)
            out += ["#" + m for m in re.findall(r'item_tag\(([a-z0-9_]+:[a-z0-9_/]+)\)', s)]
            return out or [s]
        return [iid]
    return []


def main(stem):
    lang = _lang(ATM)
    ch = read_snbt(ATM / "chapters" / f"{stem}.snbt")
    qs = ch.get("quests", [])
    print(f"# {stem}: {len(qs)} quests; chapter title: {lang.get(f'quest.{ch.get('id')}.title', ch.get('title'))}")
    for q in qs:
        qid = q.get("id")
        title = lang.get(f"quest.{qid}.title") or q.get("title") or ""
        tasks = []
        for t in q.get("tasks", []):
            ty = t.get("type", "item")
            if ty == "item":
                its = item_ids(t)
                cnt = t.get("count", 1)
                flags = []
                for i in its:
                    flags.append(i + ("" if (i in ids or i.startswith("#")) else " [MISSING]") + (f" <{','.join(sorted(ours[i]))}>" if i in ours else ""))
                tasks.append(f"item x{cnt}: " + " | ".join(flags))
            else:
                tasks.append(f"{ty}: " + str({k: v for k, v in t.items() if k not in ('id', 'type')})[:80])
        deps = q.get("dependencies", [])
        extra = []
        for k in ("size", "shape", "optional", "invisible", "hide", "hide_until_deps_visible", "min_required_dependencies", "dependency_requirement"):
            if k in q:
                extra.append(f"{k}={q[k]}")
        print(f"{qid} ({q.get('x')},{q.get('y')}) [{title}] deps={deps} {' '.join(extra)}")
        for t in tasks:
            print("    " + t)


if __name__ == "__main__":
    for s in sys.argv[1:]:
        main(s)
        print()
