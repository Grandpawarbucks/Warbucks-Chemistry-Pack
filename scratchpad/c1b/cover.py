"""For an ATM10 chapter: which quests are mirrored (any tools/quests file), and which of our quests ask for its items."""
import re, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from atm import parse, Q, items_of  # noqa

ROOT = pathlib.Path(__file__).resolve().parents[2]
src = {p.stem: p.read_text(encoding="utf-8") for p in (ROOT / "tools/quests").glob("*.py")}
mirrors = {}
for stem, s in src.items():
    for m in re.finditer(r'Q\("([^"]+)"(.*?)(?=\n    Q\(|\Z)', s, re.S):
        mm = re.search(r'mirror="([0-9A-Fa-f]{16})"', m.group(2))
        if mm:
            mirrors.setdefault(mm.group(1).upper(), []).append(f"{stem}:{m.group(1)}")
ids = set(l.split("\t")[0] for l in (ROOT / "test/ids.tsv").read_text(encoding="utf-8").splitlines())

stem = sys.argv[1]
d = parse((Q / "chapters" / f"{stem}.snbt").read_text(encoding="utf-8"))
for q in d["quests"]:
    its = []
    for t in q.get("tasks", []):
        if t.get("type") == "item":
            for x in items_of(t):
                its += re.findall(r"item\(([a-z0-9_]+:[a-z0-9_/]+)\)", x) or [x]
    have = [i for i in its if i in ids]
    users = set()
    for i in have:
        for st, s in src.items():
            for m in re.finditer(r'Q\("([^"]+)"[^\n]*' + re.escape('"' + i + '"'), s):
                users.add(f"{st}:{m.group(1)}")
    print(q["id"], "MIRRORED " + ",".join(mirrors[q["id"]]) if q["id"] in mirrors else "--", "| items", its, "| have", len(have), "| used by", sorted(users))
