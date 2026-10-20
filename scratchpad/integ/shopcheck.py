from book import *
import re, sys
def asked(q):
    s = set()
    for t in q.tasks:
        if t[0] == "item": s.add(t[1])
        elif t[0] == "filter": s |= set(re.findall(r"item\(([^()]+)\)", t[1]))
    s |= {i for i, _ in q.items}
    return s
def loose(q):  # tag asks, kills, dimensions, biomes, structures: "yields" by design
    return any(t[0] in ("kill", "dimension", "biome", "structure") or (t[0] == "filter" and "item_tag(" in t[1]) for t in q.tasks)
ASKERS = {}
for q in QS.values():
    if HOME[q.key] in SHOP: continue
    for i in asked(q) - {i for i, _ in q.items}:
        ASKERS.setdefault(i, []).append(q.key)
bad = 0
for c in CH:
    if c.key not in SHOP: continue
    for q in c.quests:
        if not q.items: continue
        have = set()
        lz = False
        for d in q.deps:
            have |= asked(QS[d]); lz |= loose(QS[d])
        miss = [i for i, _ in q.items if i not in have]
        if miss and not lz:
            bad += 1
            print(f"{q.key:28} deps={q.deps} missing={miss}")
            if "-v" in sys.argv:
                for m in miss: print(f"      {m}: {ASKERS.get(m, [])[:6]}")
print("violations", bad)
