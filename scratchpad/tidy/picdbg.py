import sys, math
sys.path[:0] = ["tools", "test"]
import build_quests as B, layout
keys = {q.key for c in B.CHAPTERS for q in c.quests}
B.style_quests()
c = next(c for c in B.CHAPTERS if c.key == sys.argv[1])
raw = []
orig = layout._mirror_pictures
def f(chapter, r, secs):
    raw.extend(r); return orig(chapter, r, secs)
layout._mirror_pictures = f
layout.apply(c, keys)
nodes = [(q.x, q.y, layout._size(q)) for q in c.quests] + [(x, y, 1.0) for _, x, y in c.links]
for im in raw:
    b = layout._mirror_box(im)
    cov = max(layout._box_inter((n[0]-n[2]/2, n[1]-n[2]/2, n[0]+n[2]/2, n[1]+n[2]/2), b)/n[2]**2 for n in nodes)
    print(round(im["x"],2), round(im["y"],2), im["width"], im["height"], im["rotation"], "cov", round(cov,2))
