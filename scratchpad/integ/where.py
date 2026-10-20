from book import *
import hashlib, re, sys
def hexid(key):
    n = int(hashlib.sha1(key.encode()).hexdigest()[:16], 16) & 0x7FFFFFFFFFFFFFFF
    return f"{n:016X}"
rev = {hexid("quest:" + k): k for k in QS}
ch, x0, x1, y0, y1 = sys.argv[1], *map(float, sys.argv[2:6])
t = open(f"../../pack/config/ftbquests/quests/chapters/{ch}.snbt", encoding="utf-8").read()
for m in re.finditer(r'\{\s*(?:[^{}]|\{[^{}]*\})*?\}', t):
    b = m.group(0)
    i = re.search(r'\bid: "([0-9A-F]{16})"', b); x = re.search(r'\n\s*x: (-?[\d.]+)d', b); y = re.search(r'\n\s*y: (-?[\d.]+)d', b)
    lq = re.search(r'linked_quest: "([0-9A-F]{16})"', b)
    if i and x and y and x0 <= float(x.group(1)) <= x1 and y0 <= float(y.group(1)) <= y1:
        k = rev.get(lq.group(1) if lq else i.group(1))
        if k: print("link" if lq else "quest", k, HOME[k], x.group(1), y.group(1), "dependents here:", [d for d in DEPENDENTS.get(k, []) if HOME[d]==ch][:6], "deps:", QS[k].deps)
