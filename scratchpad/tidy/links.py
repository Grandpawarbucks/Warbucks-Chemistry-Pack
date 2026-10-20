import sys, math
sys.path[:0] = ["tools", "test"]
import build_quests as B, layout
keys = {q.key for c in B.CHAPTERS for q in c.quests}
B.style_quests()
c = next(c for c in B.CHAPTERS if c.key == sys.argv[1])
layout.apply(c, keys)
byk = {q.key: q for q in c.quests}
for lk, x, y in c.links:
    deps = [q.key for q in c.quests if lk in q.deps]
    print(lk, (x, y), [(d, byk[d].x, byk[d].y) for d in deps])
