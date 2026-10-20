import sys, collections
sys.path.insert(0, "tools")
import quest_data as qd
tot = collections.Counter(); n = collections.Counter()
for c in qd.CHAPTERS:
    for q in c.quests:
        t = q.tokens if q.tokens is not None else c.tokens * (2 if (q.size or 1) >= 1.5 else 1)
        tot[c.key] += t; n[c.key] += 1
print(sum(tot.values()), sum(n.values()))
for c in qd.CHAPTERS:
    print(c.key, getattr(c,'group',None), n[c.key], tot[c.key], c.tokens)
for k in ["start","t0","t1","t2","t3","t4","t5","t6","t7","seed","creation"]:
    c = next(x for x in qd.CHAPTERS if x.key == k)
    caps = [(q.key, q.title, q.size) for q in c.quests if (q.size or 1) >= 2]
    print(k, c.title, caps)
