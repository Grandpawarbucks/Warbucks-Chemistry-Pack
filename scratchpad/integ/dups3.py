# quests whose whole task set (items incl. anyof members, and kills etc) is identical to another quest's
from book import *
import re
def sig(q):
    s = []
    for t in q.tasks:
        if t[0] == "filter":
            s.append(("anyof", tuple(sorted(re.findall(r"item\(([^()]+)\)", t[1]))) or t[1]))
        elif t[0] == "checkmark": return None
        else: s.append((t[0], t[1]))
    return tuple(sorted(map(str, s))) if s else None
by = {}
for q in QS.values():
    if HOME[q.key] in SHOP: continue
    s = sig(q)
    if s and not (len(s) == 1 and s[0][0] == "item"): by.setdefault(s, []).append(q)
for s, qs in by.items():
    if len(qs) > 1:
        print(str(s)[:100], " | ".join(f"{HOME[q.key]}:{q.key}{'(o)' if q.optional else ''}{'[M]' if q.mirror else ''}<-{len(DEPENDENTS.get(q.key,[]))}" for q in qs))
