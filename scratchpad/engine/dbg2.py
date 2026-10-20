import sys, os
sys.path.insert(0, "tools")
os.environ.setdefault("QUEST_ONLY", "create")
from quest_data import CHAPTERS
import layout, quest_style
keys = {q.key for c in CHAPTERS for q in c.quests}
c = next(c for c in CHAPTERS if c.key == "create")
quest_style.apply(c)
byk = {q.key: q for q in c.quests}
for k in ("cr_crank", "cr_steam", "cr_piston", "cr_drill"):
    q = byk[k]; print(k, q.size, q.shape, q.optional, q.deps, [t[:2] for t in q.tasks])
atm = layout.load_mirror("create")
layout.apply(c, keys)
m = c.mirror_matched
for k in ("cr_crank", "cr_steam", "cr_piston", "cr_drill"):
    q = byk[k]; a = atm["quests"][m[k]]; print(k, "->", m[k], a["x"], a["y"], a["size"], a["shape"], "| ours", q.x, q.y, q.size, q.shape)
