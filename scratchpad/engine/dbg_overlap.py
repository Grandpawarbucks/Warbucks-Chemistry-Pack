import sys, math, os
sys.path.insert(0, "tools")
keys_arg = sys.argv[1].split(",")
os.environ.setdefault("QUEST_ONLY", sys.argv[1])
from quest_data import CHAPTERS
import layout, quest_style
keys = {q.key for c in CHAPTERS for q in c.quests}
verbose = "-v" in sys.argv
for c in CHAPTERS:
    if c.key not in keys_arg: continue
    quest_style.apply(c)
    layout.apply(c, keys)
    print(c.key, "style", c.style, getattr(c, "mirror_stats", None))
    m = getattr(c, "mirror_matched", {})
    boxes = [(q.key, q.x, q.y, layout._size(q), q.shape, q.key in m) for q in c.quests] + [(("link", lk), x, y, 1.0, "circle", False) for lk, x, y in c.links]
    n = 0
    for i in range(len(boxes)):
        for j in range(i+1, len(boxes)):
            k1,x1,y1,s1,sh1,m1 = boxes[i]; k2,x2,y2,s2,sh2,m2 = boxes[j]
            if layout._overlap_nodes((x1,y1,s1),(x2,y2,s2),sh1,sh2):
                n += 1
                if verbose: print(f"  LINT-OVERLAP {k1}({x1},{y1},{s1},{sh1},{'M' if m1 else 'u'}) {k2}({x2},{y2},{s2},{sh2},{'M' if m2 else 'u'})")
    mt = layout.metrics(c)
    print(f"  lint-overlaps={n} metrics={ {k: mt[k] for k in ('w','h','cross','thru','long','lines','hidden_edges','overlap','close','ortho')} }")
