import sys, math
sys.path[:0] = ["tools", "test"]
import build_quests as B, layout
keys = {q.key for c in B.CHAPTERS for q in c.quests}
B.style_quests()
tot = 0
for c in B.CHAPTERS:
    layout.apply(c, keys)
    if c.style != "mirror": continue
    m = getattr(c, "mirror_matched", None)
    if m is None: continue
    drawn = layout._drawn(c)
    tied = {n for e in drawn for n in e}
    pos = {q.key: (q.x, q.y) for q in c.quests}
    pos.update({("link", lk): (x, y) for lk, x, y in c.links})
    un = [q for q in c.quests if q.key not in m]
    lone = [q.key for q in un if q.key not in tied]
    longd = [(a, b) for a, b in drawn if math.dist(pos[a], pos[b]) > 4 and not layout._ortho(pos[a], pos[b])]
    tot += len(lone)
    print(f"{c.key:18} unmatched {len(un):3}  lone-unmatched {len(lone):3}  long-diag-drawn {len(longd):3}  {lone[:6]}")
print("total lone unmatched", tot)
