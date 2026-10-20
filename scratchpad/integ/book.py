import sys, os, pathlib, io, contextlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
with contextlib.redirect_stdout(io.StringIO()):
    import quest_data as qd
CH = qd.CHAPTERS
HOME = {q.key: c.key for c in CH for q in c.quests}
QS = {q.key: q for c in CH for q in c.quests}
SHOP = {"market", "shop_materials", "shop_gear", "shop_world"}
DEPENDENTS = {}
for q in QS.values():
    for d in q.deps:
        DEPENDENTS.setdefault(d, []).append(q.key)
def only_item(q):
    if len(q.tasks) != 1: return None
    t = q.tasks[0]
    if t[0] == "item": return t[1]
    return None
