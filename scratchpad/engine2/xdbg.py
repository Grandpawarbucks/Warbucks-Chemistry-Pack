import sys
sys.path.insert(0, "tools")
import quest_data as qd, layout as L
keys = {q.key for c in qd.CHAPTERS for q in c.quests}
want = sys.argv[1]
c = next(c for c in qd.CHAPTERS if c.key == want)
L.apply(c, keys)
print("lone_pen", c.lone_penalty, "atm lone", L.load_mirror(c.mirror)["lone"])
pos = {q.key: (q.x, q.y) for q in c.quests}; pos.update({("link", lk): (x, y) for lk, x, y in c.links})
byk = {q.key: q for q in c.quests}
shared = L._ext_targets(c)
d = L._drawn(c)
for i in range(len(d)):
    for j in range(i+1, len(d)):
        if L._cross((pos[d[i][0]], pos[d[i][1]]), (pos[d[j][0]], pos[d[j][1]])):
            def info(e):
                a, b = e
                return f"{a}->{b} [{'S' if b in shared else ''}{'S' if a in shared else ''}]"
            print(info(d[i]), " X ", info(d[j]))
