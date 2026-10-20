from book import *
import sys, re
for pat in sys.argv[1:]:
    for k, q in QS.items():
        if re.fullmatch(pat, k):
            print(f"{HOME[k]:14} {k:24} opt={int(bool(q.optional))} mir={q.mirror} tasks={[t[:3] for t in q.tasks]} deps={q.deps} <- {[(d, HOME[d], int(bool(QS[d].optional))) for d in DEPENDENTS.get(k, [])]}")
