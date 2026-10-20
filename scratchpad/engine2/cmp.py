import sys, copy
sys.path.insert(0, "tools")
import quest_data as qd, layout as L
keys = {q.key for c in qd.CHAPTERS for q in c.quests}
want = sys.argv[1].split(",")
styles = sys.argv[2].split(",")
for c in qd.CHAPTERS:
    if c.key not in want: continue
    for st in styles:
        c2 = copy.deepcopy(c)
        c2.style = st
        L.apply(c2, keys, style=st)
        m = L.metrics(c2)
        o = round(100*m["ortho"]/m["lines"]) if m["lines"] else 100
        print(c.key, st, {k: m[k] for k in ("w","h","cross","thru","long","overlap","hidden_edges","lines")}, "orth", o, getattr(c2,"mirror_stats",None) and c2.mirror_stats.get("matched"))
