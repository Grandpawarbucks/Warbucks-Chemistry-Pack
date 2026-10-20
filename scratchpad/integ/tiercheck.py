from book import *
import functools, sys
sys.setrecursionlimit(10000)
TI = {k: i for i, k in enumerate(["start", "t0", "t1", "t2", "t3", "t4", "t5", "t6", "t7", "seed", "creation"])}
@functools.lru_cache(None)
def need(k):
    """highest main tier this quest transitively needs"""
    q = QS[k]
    t = TI.get(HOME[k], -1)
    for d in q.deps:
        t = max(t, need(d))
    return t
names = list(TI)
bad = 0
for k, q in QS.items():
    h = HOME[k]
    for d in q.deps:
        nd = need(d)
        # a main-path quest needing a later tier, or a required quest whose dep is optional
        if h in TI and nd > TI[h]:
            bad += 1; print(f"TIER  {h}:{k} <- {HOME[d]}:{d} needs {names[nd]}")
        if not q.optional and QS[d].optional and h not in SHOP:
            bad += 1; print(f"OPT   {h}:{k} (required) <- {HOME[d]}:{d} (optional)")
print(bad)
