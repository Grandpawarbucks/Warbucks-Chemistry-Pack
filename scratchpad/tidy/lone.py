import sys, math
sys.path[:0] = ["tools", "test"]
import build_quests as B, layout
keys = {q.key for c in B.CHAPTERS for q in c.quests}
B.style_quests()
c = next(c for c in B.CHAPTERS if c.key == sys.argv[1])
layout.apply(c, keys)
m = c.mirror_matched
drawn = layout._drawn(c)
tied = {n for e in drawn for n in e}
pos = {q.key: (q.x, q.y) for q in c.quests}
pos.update({("link", lk): (x, y) for lk, x, y in c.links})
for q in c.quests:
    if q.key not in tied:
        ds = [(d, round(math.dist(pos[q.key], pos[d] if d in pos else pos.get(("link", d), (99,99))),1)) for d in q.deps]
        kids = [k.key for k in c.quests if q.key in k.deps]
        print(f"{'M' if q.key in m else 'u'} {q.key:28} ({q.x:g},{q.y:g}) deps={ds} kids={kids[:4]} HL={q.hide_lines} HD={q.hide_dependents}")
