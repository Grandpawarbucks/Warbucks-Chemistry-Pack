import sys, os, math
sys.path[:0] = ["tools", "test"]
import build_quests as B, layout
want = sys.argv[1].split(",")
keys = {q.key for c in B.CHAPTERS for q in c.quests}
B.style_quests()
for c in B.CHAPTERS:
    if c.key not in want: continue
    layout.apply(c, keys)
    m = getattr(c, "mirror_matched", {}) or {}
    pos = {q.key: (q.x, q.y, q.size) for q in c.quests}
    for lk, lx, ly in c.links: pos.setdefault(("L", lk), (lx, ly, 1))
    print("==", c.key, c.mirror_stats)
    un = [q for q in c.quests if q.key not in m]
    print(" unmatched", len(un))
    for q in un:
        ls = []
        for d in q.deps:
            if d in pos: 
                p = pos[d]; ls.append(f"{d}:{math.dist(p[:2],(q.x,q.y)):.1f}")
        print(f"   {q.key:32} ({q.x:g},{q.y:g}) hide={getattr(q,'hide_lines',None)} deps {' '.join(ls)}")
    for pic in c.pictures:
        print("  pic", pic["slug"], pic.get("kind"), round(pic["x"],2), round(pic["y"],2), round(pic["width"],2), round(pic["height"],2), pic.get("title"), pic.get("caption"), pic.get("tab"))
    print(" drawn lines > 3 or diagonal > 2:")
    P2 = {q.key: (q.x, q.y) for q in c.quests}
    P2.update({("link", lk): (x, y) for lk, x, y in c.links})
    for a, b in layout._drawn(c):
        L = math.dist(P2[a], P2[b])
        orth = layout._ortho(P2[a], P2[b])
        if L > 3 or (not orth and L > 2):
            ma = "M" if a in m else ("L" if isinstance(a, tuple) else "u")
            mb = "M" if b in m else "u"
            print(f"   {str(a):30}{ma} -> {str(b):28}{mb} {L:5.1f} {'orth' if orth else 'diag'}")
