import sys
sys.path.insert(0, "tools")
import quest_data as qd, layout as L
keys = {q.key for c in qd.CHAPTERS for q in c.quests}
c = next(c for c in qd.CHAPTERS if c.key == sys.argv[1])
L.apply(c, keys)
print(c.mirror_stats)
sh = (c.shared_quests or set()) | L._ext_targets(c)
print("links", [(lk, x, y, lk in sh, lk in {q.key for q in c.quests}) for lk, x, y in c.links])
a = L.load_mirror(c.mirror)
print(len(a["links"]), a["links"][:8], "lone", a["lone"])
