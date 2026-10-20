import sys
sys.path.insert(0, "tools")
import quest_data as qd
qs = {q.key: (c.key, q) for c in qd.CHAPTERS for q in c.quests}
for k in ["gs_ready","t0_pump","t1_dissolver","t1_steel","t3_ebf","t4_acid","t5_hv","t6_pu","t7_nasa","t7_seed"]:
    c, q = qs[k]; print(k, c, q.title, q.optional, q.tasks[:2])
print(qs["gs_ready"][1].tasks)
