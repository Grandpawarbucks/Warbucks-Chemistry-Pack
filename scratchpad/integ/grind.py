from book import *
import sys
MAINC = set(qd.LAYOUT["main"]) | {"welcome", "completionist"}
def deps_nonshop(k):
    return [d for d in DEPENDENTS.get(k, []) if HOME[d] not in SHOP]
cands = []
for k, q in QS.items():
    h = HOME[k]
    if h in MAINC or h in SHOP or q.optional: continue
    if (q.size or 1) >= 1.5: continue
    tasks = [t for t in q.tasks if t[0] != "checkmark"]
    n_items = len(tasks)
    maxc = max([t[2] for t in tasks if len(t) > 2 and isinstance(t[2], int)] or [0])
    big = n_items >= 4 or maxc >= 32 or k.startswith("mf_sim_")
    if not big: continue
    dn = deps_nonshop(k)
    cands.append((h, k, n_items, maxc, dn))
for h, k, n, m, dn in sorted(cands):
    print(f"{h:14} {k:26} tasks={n:2} max={m:4} dependents={dn[:4]}")
print(len(cands), "free:", sum(1 for c in cands if not c[4]))
