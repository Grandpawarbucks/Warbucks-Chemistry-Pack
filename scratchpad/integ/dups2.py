from book import *
MAINC = set(qd.LAYOUT["main"])
by = {}
for q in QS.values():
    if HOME[q.key] in SHOP: continue
    it = only_item(q)
    if it: by.setdefault(it, []).append(q)
cats = {"side": [], "main_opt": [], "main_req": []}
for it, qs in sorted(by.items()):
    if len(qs) < 2: continue
    mains = [q for q in qs if HOME[q.key] in MAINC]
    if not mains: cats["side"].append((it, qs))
    elif all(q.optional for q in mains) : cats["main_opt"].append((it, qs))
    else: cats["main_req"].append((it, qs))
import sys
which = sys.argv[1]
for it, qs in cats[which]:
    print(it, " | ".join(f"{HOME[q.key]}:{q.key}{'(o)' if q.optional else ''}{'[M]' if q.mirror else ''}x{q.tasks[0][2]}<-{len(DEPENDENTS.get(q.key,[]))}" for q in qs))
print({k: len(v) for k, v in cats.items()})
