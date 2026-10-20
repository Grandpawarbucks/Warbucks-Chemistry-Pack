from book import *
by = {}
for q in QS.values():
    if HOME[q.key] in SHOP: continue
    it = only_item(q)
    if it: by.setdefault(it, []).append(q)
n = 0
for it, qs in sorted(by.items()):
    if len(qs) < 2: continue
    live = [q for q in qs if not (q.optional and q.tasks and False)]
    n += 1
    print(it)
    for q in qs:
        deps_on = DEPENDENTS.get(q.key, [])
        print(f"   {HOME[q.key]:16} {q.key:24} opt={int(bool(q.optional))} mir={q.mirror or '-':16} n={q.tasks[0][2]} deps={q.deps} <- {[(d, HOME[d], int(bool(QS[d].optional))) for d in deps_on]}")
print(n)
