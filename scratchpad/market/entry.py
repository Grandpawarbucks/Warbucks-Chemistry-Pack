import sys
sys.path.insert(0, "tools")
import quest_data as qd
by = {c.key: c for c in qd.CHAPTERS}
for k in ["start","t0","t1","t2","t3","t4","t5","t6","t7","seed","creation"]:
    c = by[k]; ks = {q.key for q in c.quests}
    ent = [q for q in c.quests if not q.optional and not any(d in ks for d in q.deps)]
    print(k, c.title, [(q.key, q.title, q.deps) for q in ent][:4])
