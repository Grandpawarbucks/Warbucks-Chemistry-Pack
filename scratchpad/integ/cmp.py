import json, collections
b = json.load(open("before.json")); a = json.load(open("after.json"))
ret = [k for k in a if a[k]["tick"] and not b[k]["tick"]]
newopt = [k for k in a if a[k]["opt"] and not b[k]["opt"]]
grind = [k for k in newopt if k not in ret]
print("retired", len(ret), "newly optional total", len(newopt), "grind (non-retired)", len(grind))
print(sorted(grind))
print("required before", sum(not v["opt"] for v in b.values()), "after", sum(not v["opt"] for v in a.values()))
moved = [k for k in a if a[k]["ch"] != b[k]["ch"]]
print("moved", collections.Counter((b[k]["ch"], a[k]["ch"]) for k in moved))
print("missing keys", set(b) - set(a), set(a) - set(b))
print("quests with changed deps", sum(1 for k in a if a[k]["deps"] != b[k]["deps"]))
