import json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]
d = json.loads((ROOT / "test/dump/recipe_dump.json").read_text(encoding="utf-8"))
OUT = {}
def walk(v, acc):
    if isinstance(v, dict):
        for k in ("id", "item"):
            if isinstance(v.get(k), str) and ":" in v[k]:
                acc.add(v[k])
        for x in v.values():
            walk(x, acc)
    elif isinstance(v, list):
        for x in v:
            walk(x, acc)
for r in d["recipes"]:
    try:
        j = json.loads(r["json"])
    except Exception:
        continue
    acc = set()
    for k, v in j.items():
        if k in ("result", "results", "output", "outputs", "itemOutput", "item_output"):
            walk(v, acc)
    for a in acc:
        OUT.setdefault(a, []).append(r["id"])
if __name__ == "__main__":
    for q in sys.argv[1:]:
        print(q, OUT.get(q, "NO RECIPE")[:3] if q in OUT else "NO RECIPE")
