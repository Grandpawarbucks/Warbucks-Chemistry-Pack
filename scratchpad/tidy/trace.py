import sys, math
sys.path[:0] = ["tools", "test"]
import build_quests as B, layout
keys = {q.key for c in B.CHAPTERS for q in c.quests}
B.style_quests()
watch = sys.argv[2].split(",")
of = layout._finish
def f(chapter, P, *a, **k):
    print("before finish:", {w: P.get(w) for w in watch})
    return of(chapter, P, *a, **k)
layout._finish = f
c = next(c for c in B.CHAPTERS if c.key == sys.argv[1])
layout.apply(c, keys)
byk = {q.key: q for q in c.quests}
print("after:", {w: (byk[w].x, byk[w].y, byk[w].hide_lines, byk[w].hide_dependents, byk[w].deps) for w in watch})
