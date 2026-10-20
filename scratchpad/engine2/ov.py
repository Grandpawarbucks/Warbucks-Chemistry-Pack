import sys, os, math
sys.path.insert(0, "tools")
os.chdir(".")
import quest_data as qd, layout as L
keys = {q.key for c in qd.CHAPTERS for q in c.quests}
want = sys.argv[1].split(",")
for c in qd.CHAPTERS:
    if c.key not in want: continue
    L.apply(c, keys)
    bx, by = L.banner(c)
    boxes = [(q.key, q.x, q.y, L._size(q), q.shape) for q in c.quests] + [("link:"+lk, x, y, 1.0, "") for lk, x, y in c.links]
    for i in range(len(boxes)):
        for j in range(i+1, len(boxes)):
            a, b = boxes[i], boxes[j]
            h = (a[3]+b[3])/2
            if abs(a[1]-b[1]) < h and abs(a[2]-b[2]) < h:
                print(c.key, "OV", a, b)
    for a in boxes:
        if abs(a[1]-bx) < 3+a[3]/2 and abs(a[2]-by) < .5+a[3]/2: print(c.key, "BANNER", a, (bx, by))
    print(c.key, L.metrics(c)["thru"], getattr(c, "mirror_stats", None))
