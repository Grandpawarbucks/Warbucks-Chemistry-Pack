from book import *
import re, sys
for pat in sys.argv[1:]:
    for q in QS.values():
        if HOME[q.key] in SHOP: continue
        its = []
        for t in q.tasks:
            if t[0] == "item": its.append(t[1])
            elif t[0] == "filter": its += re.findall(r"item\(([^()]+)\)", t[1])
        hit = [i for i in its if re.search(pat, i)]
        if hit:
            print(f"{pat:28} {HOME[q.key]:14} {q.key:24} opt={int(bool(q.optional))} asks={its[:8]}")
