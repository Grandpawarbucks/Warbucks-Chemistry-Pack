"""Automatic quest layout for the FTB Quests book (rules L1-L12 in docs/research/quest_layout_audit.md §4.2).

build_quests.py calls apply(chapter) for every chapter before writing it. Writers don't place x/y any more.
FTB draws every dependency as one straight line (also from a quest link to its dependents here), so the goal
is lines that don't run through other quests, cross little and stay short. It is a Sugiyama-style drawing:
- Redundant deps are dropped first (prune_transitive: A -> B -> C plus A -> C loses A -> C; what the player
  must do doesn't change).
- Column = in-chapter dependency depth x 2, so every dependency line points right. Deps on quests in other
  chapters don't count (those quests are roots of this chapter). Quests then slide to the median column of
  their neighbours (inside the range their deps/dependents allow) to shorten lines. A quest with many
  children that hang only on it spreads them over up to 3 columns (a wedge, not one tall column).
- The required critical path (longest chain of non-optional quests, ties to bigger milestones) sits on y = 0,
  starting in the middle of each column so hubs on it fan out both ways.
- Inside each column, quests are ordered to cut crossings: alternating median / barycentre sweeps plus
  adjacent swaps ("transpose"), 24 rounds, best kept. Then they get y values close to their neighbours' mean,
  so sub-topics form rows beside the spine. Required quests keep 2.0 apart, optional ones 1.5, big milestones
  (size >= 1.5) more. Optional quests aim 1.5 cells off their parent's row (outward), never on the spine.
- Long lines get placeholder points in the columns they cross, so they get room and count as crossings.
- Groups of quests with no line to the spine's group are laid out the same way and packed below it in shelves.
- Quest links take part in all of this: a link sits one column left of its leftmost dependent (x = -2, the
  link column, when that is column 0). Links nothing here depends on stack in the link column above the rest.
  The chapter's entry quest gets a link to each of its deps in other chapters automatically.
- A last local search moves single quests (up/down, and to other columns their deps allow) or swaps two in a
  column when that removes lines through quests (weight 6 in _repair) or crossings (3), then shortens long
  lines where that is free.
- The whole thing runs once per fan width in FANS; the tidiest result (_score) is kept.
- Chapter(..., layout="manual") keeps hand-written x/y. Q(..., row=N) pins a quest to y = 2N.

normalize_milestones() is separate: it runs for every chapter (manual ones too) when the data is loaded.
Everything here is deterministic (ties are broken by declaration order).
"""
import math

COL = 2.0          # column pitch (x per dependency level)
ROW = 2.0          # row pitch for required rows
OPT = 1.5          # optional offset from the parent's row
MIN_SEP = 1.5      # minimum centre distance between two quests
LINK_ROWS = 12     # links per link column before wrapping to the next one (x = -4, -6 ...)
LINK_X = -2.0      # link column
MAX_EDGE = 6.0     # edges longer than this are flagged in the report
FANS = (4, 2, 8)   # fan widths tried: a quest with more single-parent children spreads them over columns


# --- milestone styling (L9) -------------------------------------------------------------------
def normalize_milestones(chapter):
    """Exactly two milestone styles: capstone = size 2.0 gear, section milestone = size 1.5 hexagon."""
    for q in chapter.quests:
        s = q.size or 1
        if s >= 1.75:
            q.size, q.shape = 2.0, "gear"
        elif s >= 1.25:
            q.size, q.shape = 1.5, "hexagon"


# --- graph helpers ----------------------------------------------------------------------------
def _graph(quests):
    byk = {q.key: q for q in quests}
    idx = {q.key: i for i, q in enumerate(quests)}
    parents = {q.key: [] for q in quests}
    for q in quests:
        for d in q.deps:
            if d in byk and d != q.key and d not in parents[q.key]:
                parents[q.key].append(d)
    # Topological order (Kahn, ties by declaration). A cycle would be a data bug; its back edges are dropped.
    indeg = {k: len(p) for k, p in parents.items()}
    children = {k: [] for k in byk}
    for k, ps in parents.items():
        for p in ps:
            children[p].append(k)
    order, ready = [], sorted((k for k, n in indeg.items() if n == 0), key=idx.get)
    seen = set()
    while len(order) < len(quests):
        if not ready:  # cycle: break it at the earliest remaining quest
            k = min((k for k in byk if k not in seen), key=idx.get)
            parents[k] = [p for p in parents[k] if p in seen]
            ready = [k]
        k = ready.pop(0)
        if k in seen:
            continue
        seen.add(k)
        order.append(k)
        for c in children[k]:
            indeg[c] -= 1
            if indeg[c] == 0 and c not in seen:
                ready.append(c)
        ready.sort(key=idx.get)
    children = {k: [] for k in byk}
    for k, ps in parents.items():
        for p in ps:
            children[p].append(k)
    for k in children:
        children[k].sort(key=idx.get)
    return byk, idx, parents, children, order


def _size(q):
    return float(q.size or 1)


def prune_transitive(quests):
    """Drop dependencies that other dependencies already imply (A -> B -> C plus A -> C: the A -> C line goes).
    FTB draws one straight line per dependency, so these shortcut lines only add clutter; what the player must
    do is unchanged. Only in-chapter chains count, and only when the implication is certain:
    - the quest itself needs ALL its deps (not any_dep) and isn't hidden (hide_until_deps_visible looks at the
      deps' visibility, which a chain doesn't imply);
    - every quest on the chain needs all its deps (an any_dep quest with 2+ deps implies none of them);
    - no repeatable quest on the chain or as the dropped dep (a repeat resets its completion).
    Mutates q.deps in place (idempotent) and returns the number of deps dropped."""
    byk = {q.key: q for q in quests}
    deps = {q.key: [d for d in dict.fromkeys(q.deps) if d in byk and d != q.key] for q in quests}
    memo = {}

    def implied(k, stack=()):
        """In-chapter quests that must be complete whenever k is complete."""
        if k in memo:
            return memo[k]
        q = byk[k]
        out = set()
        if k not in stack and not q.repeat and not (q.any_dep and len(q.deps) > 1):
            for d in deps[k]:
                if not byk[d].repeat:
                    out.add(d)
                    out |= implied(d, stack + (k,))
        memo[k] = out
        return out

    n = 0
    for q in quests:
        if q.any_dep or q.hidden or len(deps[q.key]) < 2:
            continue
        drop = {a for a in deps[q.key] if not byk[a].repeat
                and any(a in implied(b) for b in deps[q.key] if b != a)}
        if drop:
            q.deps = [d for d in q.deps if d not in drop]
            n += len(drop)
    return n


# --- the layout -------------------------------------------------------------------------------
def _median(vals):
    s = sorted(vals)
    n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2


def _pava(desired, weights, seps):
    """Weighted least squares y close to desired, subject to y[i+1] - y[i] >= seps[i] (pool adjacent violators)."""
    off = [0.0]
    for s in seps:
        off.append(off[-1] + s)
    blocks = []  # [value, weight, count]
    for d, w, o in zip(desired, weights, off):
        blocks.append([d - o, w, 1])
        while len(blocks) > 1 and blocks[-2][0] > blocks[-1][0]:
            v2, w2, n2 = blocks.pop()
            v1, w1, n1 = blocks.pop()
            blocks.append([(v1 * w1 + v2 * w2) / (w1 + w2), w1 + w2, n1 + n2])
    z = []
    for v, _, n in blocks:
        z += [v] * n
    return [zi + o for zi, o in zip(z, off)]


def _spine(keys, G):
    """L3: longest chain of required quests among keys (all of them if none is required); ties go to the
    chain with the bigger milestones, then to the one declared first."""
    byk, idx, parents, order, opt = G["byk"], G["idx"], G["parents"], G["order"], G["opt"]
    pool = [k for k in order if k in keys and not opt[k]] or [k for k in order if k in keys]
    inpool = set(pool)
    best = {}  # key -> ((length, sizes, -start idx), predecessor) of the best chain ending at key
    for k in pool:
        cand = [p for p in parents[k] if p in inpool]
        if cand:
            p = max(cand, key=lambda p: (best[p][0], -idx[p]))
            (n, s, st), _ = best[p]
            best[k] = ((n + 1, s + _size(byk[k]), st), p)
        else:
            best[k] = ((1, _size(byk[k]), -idx[k]), None)
    end = max(pool, key=lambda k: (best[k][0], -idx[k]))
    spine = []
    while end:
        spine.append(end)
        end = best[end][1]
    return spine[::-1]


def _place(keys, G, spine, links=()):
    """Lay out one connected group of quests. Returns (column per key, y per key), spine on y = 0.
    links: [(link node, [quests here that depend on it])]. Each link sits one column left of its leftmost
    dependent (column -1 = the link column when that is column 0), and its lines take part in the crossing
    reduction. The columns and y values returned include the links."""
    byk, idx, parents, children, opt = G["byk"], G["idx"], G["parents"], G["children"], G["opt"]
    order = [k for k in G["order"] if k in keys]
    spine_set = set(spine)

    # L2: column = longest in-chapter path from a root.
    depth = {}
    for k in order:
        depth[k] = max((depth[p] + 1 for p in parents[k]), default=0)
    # Shorter lines: every non-spine quest moves to the median column of its neighbours, inside the range its
    # deps and dependents allow (it always stays right of its deps and left of its dependents).
    for _ in range(4):
        for k in list(reversed(order)) + order:
            if k in spine_set:
                continue
            lo = max((depth[p] + 1 for p in parents[k]), default=0)
            hi = min((depth[c] - 1 for c in children[k]), default=None)
            if hi is None:
                depth[k] = lo
                continue
            want = round(_median([depth[p] + 1 for p in parents[k]] + [depth[c] - 1 for c in children[k]]))
            depth[k] = min(max(want, lo), hi)
    # Big fans: a quest with more than FAN children that hang only on it spreads them over up to 3 columns
    # (round robin; their own dependents move right with them), so the fan is a short wedge instead of one
    # tall column whose far lines graze the quests beside them.
    for h in order:
        fan = [c for c in children[h] if c not in spine_set and parents[c] == [h] and depth[c] == depth[h] + 1]
        if len(fan) > G["fan"]:
            bands = min(3, math.ceil(len(fan) / G["fan"]))
            for i, c in enumerate(fan):
                depth[c] = depth[h] + 1 + i % bands
            for k in order:
                depth[k] = max([depth[k]] + [depth[p] + 1 for p in parents[k]])
    m = min(depth.values())
    depth = {k: d - m for k, d in depth.items()}

    # Layers with dummy points on long edges, so lines get room and count in the crossing reduction.
    layers, up, down, ends = {}, {}, {}, {}
    real = set(keys)
    lnodes = {ln for ln, _ in links}
    off = 1 if links else 0
    lay = {k: depth[k] + off for k in order}
    lay.update({ln: max(0, min(lay[k] for k in ks) - 1) for ln, ks in links})
    for k in [ln for ln, _ in links] + order:
        layers.setdefault(lay[k], []).append(k)
        up.setdefault(k, [])
        down.setdefault(k, [])
    edges_in = [(p, k) for k in order for p in parents[k]] + [(ln, k) for ln, ks in links for k in ks]
    for p, k in edges_in:
        prev, gap = p, lay[k] - lay[p]
        for j in range(1, gap):
            d = ("dummy", p, k, j)
            ends[d] = (p, k, j / gap)
            layers.setdefault(lay[p] + j, []).append(d)
            up[d], down[d] = [prev], []
            down[prev].append(d)
            prev = d
        down[prev].append(k)
        up[k].append(prev)
    L = max(layers) + 1
    for c in range(L):
        layers.setdefault(c, [])
        # Start with the spine in the middle of its column: siblings tie in the sweeps and keep this order, so
        # a hub on the spine fans out both up and down instead of hanging everything below the spine.
        sp = [v for v in layers[c] if v in spine_set]
        if sp:
            others = [v for v in layers[c] if v not in spine_set]
            h = (len(others) + 1) // 2
            layers[c] = others[:h] + sp + others[h:]

    # L6: crossing reduction: barycentre sweeps (Sugiyama), keep the best ordering.
    pos = {}

    def renumber():
        for c in range(L):
            for i, v in enumerate(layers[c]):
                pos[v] = i

    def crossings():
        total = 0
        for c in range(L - 1):
            es = sorted((pos[u], pos[v]) for u in layers[c] for v in down[u])
            for i in range(len(es)):
                for j in range(i + 1, len(es)):
                    if es[i][0] < es[j][0] and es[i][1] > es[j][1]:
                        total += 1
        return total

    def sweep(c, nb, median):
        keyed = []
        for i, v in enumerate(layers[c]):
            ns = sorted(pos[n] for n in nb[v])
            if not ns:
                key = i
            elif median:  # weighted median (Gansner et al.): the middle neighbour, or a skewed mean of the two middles
                m = len(ns) // 2
                if len(ns) % 2:
                    key = ns[m]
                elif len(ns) == 2:
                    key = (ns[0] + ns[1]) / 2
                else:
                    left, right = ns[m - 1] - ns[0], ns[-1] - ns[m]
                    key = (ns[m - 1] * right + ns[m] * left) / (left + right) if left + right else (ns[m - 1] + ns[m]) / 2
            else:
                key = sum(ns) / len(ns)
            keyed.append((key, i, v))
        keyed.sort(key=lambda t: (t[0], t[1]))
        layers[c] = [v for _, _, v in keyed]
        for i, v in enumerate(layers[c]):
            pos[v] = i

    def pair_cross(u, v):
        """Crossings between the lines of u and v (both in one layer) when u is placed above v."""
        n = 0
        for nb in (up, down):
            for a in nb[u]:
                for b in nb[v]:
                    if pos[a] > pos[b]:
                        n += 1
        return n

    def transpose():
        """Swap neighbours in a layer while that removes crossings (the 'transpose' step of dot)."""
        for _ in range(8):
            better = False
            for c in range(L):
                vs = layers[c]
                for i in range(len(vs) - 1):
                    u, v = vs[i], vs[i + 1]
                    if pair_cross(v, u) < pair_cross(u, v):
                        vs[i], vs[i + 1] = v, u
                        pos[u], pos[v] = i + 1, i
                        better = True
            if not better:
                break

    renumber()
    best_order, best_x = {c: list(layers[c]) for c in range(L)}, crossings()
    for it in range(24):
        if best_x == 0:
            break
        median = it % 2 == 0
        if it % 4 < 2:
            for c in range(1, L):
                sweep(c, up, median)
            for c in range(L - 2, -1, -1):
                sweep(c, down, median)
        else:
            for c in range(L - 2, -1, -1):
                sweep(c, down, median)
            for c in range(1, L):
                sweep(c, up, median)
        transpose()
        x = crossings()
        if x < best_x:
            best_x, best_order = x, {c: list(layers[c]) for c in range(L)}
        elif x > best_x and it % 6 == 5:  # restart from the best ordering found so far
            layers.update({c: list(best_order[c]) for c in range(L)})
            renumber()
    layers = best_order

    # Coordinates: y close to the barycentre of the neighbours, spine pinned to y = 0, separations kept
    # (2.0 between required quests, 1.5 when one is optional, more around big milestones, less for lines).
    def sep(a, b):
        if a in lnodes or b in lnodes:
            return MIN_SEP if (a in lnodes and b in lnodes) or a in real or b in real else 1.0
        if a in real and b in real:
            base = ROW if not (opt[a] or opt[b]) else MIN_SEP
            return max(base, (_size(byk[a]) + _size(byk[b])) / 2 + 0.5)
        if a in real or b in real:
            return _size(byk[a if a in real else b]) / 2 + 0.5
        return 0.5

    Y = {}
    for c in range(L):
        vs = layers[c]
        Y.update(zip(vs, _pava([0.0] * len(vs), [1.0] * len(vs), [sep(a, b) for a, b in zip(vs, vs[1:])])))

    def desired(v, mode):
        if v in spine_set:
            return 0.0, 1e6
        if v in lnodes:
            return (sum(Y[n] for n in down[v]) / len(down[v]) if down[v] else Y[v]), 1.0
        if v not in real:
            p, k, t = ends[v]
            return Y[p] + (Y[k] - Y[p]) * t, 0.5
        q = byk[v]
        if q.row is not None:
            return ROW * q.row, 100.0
        ns = up[v] if mode == "up" else down[v] if mode == "down" else up[v] + down[v]
        if not ns:
            ns = up[v] + down[v]
        if not ns:
            return Y[v], 0.2
        target = sum(Y[n] for n in ns) / len(ns)
        if opt[v] and up[v] and mode != "down":  # L5: optional quests sit 1.5 off their parent's row
            py = sum(Y[n] for n in up[v]) / len(up[v])
            sgn = -1 if py < 0 else 1 if py > 0 else (-1 if Y[v] <= 0 else 1)
            target = py + sgn * OPT
        return target, 1.0

    for mode in ("up", "down", "up", "both", "up", "down", "up"):
        for c in (range(L) if mode != "down" else range(L - 1, -1, -1)):
            vs = layers[c]
            if vs:
                ds = [desired(v, mode) for v in vs]
                Y.update(zip(vs, _pava([d for d, _ in ds], [w for _, w in ds], [sep(a, b) for a, b in zip(vs, vs[1:])])))

    # Snap to the 0.5 grid without breaking separations: walk out from the spine (or the quest nearest y = 0).
    for c in range(L):
        vs = layers[c]
        if not vs:
            continue
        anchor = next((i for i, v in enumerate(vs) if v in spine_set), None)
        if anchor is None:
            anchor = min(range(len(vs)), key=lambda i: (abs(Y[vs[i]]), i))
        Y[vs[anchor]] = round(Y[vs[anchor]] * 2) / 2
        for i in range(anchor + 1, len(vs)):
            Y[vs[i]] = max(round(Y[vs[i]] * 2) / 2, math.ceil((Y[vs[i - 1]] + sep(vs[i - 1], vs[i])) * 2 - 1e-9) / 2)
        for i in range(anchor - 1, -1, -1):
            Y[vs[i]] = min(round(Y[vs[i]] * 2) / 2, math.floor((Y[vs[i + 1]] - sep(vs[i], vs[i + 1])) * 2 + 1e-9) / 2)
    depth.update({ln: lay[ln] - off for ln in lnodes})
    return depth, {k: Y[k] for k in list(keys) + list(lnodes)}


def _repair(keys, parents, children, size, opt, X, Y, fixed, xfixed=()):
    """Local search on the final positions (quests and quest links). A quest may move up or down in its column
    and to another column (still right of all its deps and left of all its dependents) when that lowers
        6 x lines through quests + 3 x line crossings + 0.15 x the length of its own lines.
    FTB draws each dependency as one straight line, so a line through an unrelated quest is the worst clutter.
    A second phase then pulls quests closer to their neighbours when that costs no crossing or line-through.
    Separations are kept; `fixed` (spine, pinned rows) never moves, `xfixed` (links) only moves up and down.
    Deterministic (declaration order, a fixed number of passes)."""
    edges = [(p, k) for k in keys for p in parents[k]]
    inc = {k: [] for k in keys}
    for e in edges:
        inc[e[0]].append(e)
        inc[e[1]].append(e)
    tol = {k: 0.45 + (size[k] - 1) / 2 for k in keys}
    col = {}
    for k in keys:
        col.setdefault(X[k], []).append(k)

    box = {}  # edge -> (min x, max x, min y, max y), kept up to date by move()

    def rebox(e):
        ax, ay, bx, by = X[e[0]], Y[e[0]], X[e[1]], Y[e[1]]
        box[e] = (ax if ax < bx else bx, bx if ax < bx else ax, ay if ay < by else by, by if ay < by else ay)

    for e in edges:
        rebox(e)

    def bad(k):
        """6 x lines through quests + 3 x crossings that involve quest k (as a line end or as the quest hit)."""
        n = 0
        for a in inc[k]:
            ax0, ax1, ay0, ay1 = box[a]
            pa, pb = (X[a[0]], Y[a[0]]), (X[a[1]], Y[a[1]])
            for e in edges:
                bx0, bx1, by0, by1 = box[e]
                if ax1 <= bx0 or bx1 <= ax0 or ay1 < by0 or by1 < ay0 or k == e[0] or k == e[1]:
                    continue
                if _cross((pa, pb), ((X[e[0]], Y[e[0]]), (X[e[1]], Y[e[1]]))):
                    n += 3
            for j in keys:
                px, py, t = X[j], Y[j], tol[j]
                if px < ax0 - t or px > ax1 + t or py < ay0 - t or py > ay1 + t or j == a[0] or j == a[1]:
                    continue
                if _seg_dist(pa, pb, (px, py)) < t:
                    n += 6
        px, py, t = X[k], Y[k], tol[k]
        for e in edges:
            bx0, bx1, by0, by1 = box[e]
            if px < bx0 - t or px > bx1 + t or py < by0 - t or py > by1 + t or k == e[0] or k == e[1]:
                continue
            if _seg_dist((X[e[0]], Y[e[0]]), (X[e[1]], Y[e[1]]), (px, py)) < t:
                n += 6
        return n

    def length(k):
        return sum(math.hypot(X[a] - X[b], Y[a] - Y[b]) for a, b in inc[k])

    def ok(k, x, y):
        here = col.get(x, ())
        if opt[k] and y == 0 and any(j in fixed for j in here):
            return False
        for j in here:
            if j == k:
                continue
            need = ROW if not (opt[k] or opt[j]) else MIN_SEP
            need = max(need, (size[k] + size[j]) / 2 + 0.5)
            if abs(Y[j] - y) < need:
                return False
        return True

    def move(k, x, y):
        if x != X[k]:
            col[X[k]].remove(k)
            col.setdefault(x, []).append(k)
        X[k], Y[k] = x, y
        for e in inc[k]:
            rebox(e)

    def columns(k, reach):
        x0 = X[k]
        if k in xfixed:
            return [x0]
        lo = max((X[p] + COL for p in parents[k]), default=x0 - reach * COL)
        hi = min((X[c] - COL for c in children[k]), default=x0 + reach * COL)
        lo, hi = max(lo, x0 - reach * COL, 0.0), min(hi, x0 + reach * COL)
        xs, x = [], lo
        while x <= hi + 1e-9:
            xs.append(x)
            x += COL
        return xs or [x0]

    def search(k, b0, reach, ysteps, shorter_only):
        """Best (score, tie, x, y) for k. shorter_only: only spots with shorter lines and no worse bad()."""
        x0, y0 = X[k], Y[k]
        L0 = length(k)
        ns = [n for e in inc[k] for n in e if n != k]
        ym = round(sum(Y[n] for n in ns) / len(ns) * 2) / 2 if ns else y0
        best = (b0 + 0.15 * L0, 0.0, x0, y0)
        for x in columns(k, reach):
            ys = {y0 + 0.5 * s for s in range(-ysteps, ysteps + 1)} | {ym + 0.5 * s for s in range(-ysteps, ysteps + 1)}
            for y in sorted(ys):
                if (x == x0 and y == y0) or not ok(k, x, y):
                    continue
                move(k, x, y)
                Ln = length(k)
                if (shorter_only and Ln > L0 - 0.5) or 0.15 * Ln >= best[0] + 1e-9:
                    move(k, x0, y0)
                    continue
                bn = bad(k)
                move(k, x0, y0)
                if shorter_only and bn > b0:
                    continue
                score = (bn + 0.15 * Ln, abs(x - x0) + abs(y - y0), x, y)
                if score < best:
                    best = score
        return best

    for _ in range(6):  # phase 1: remove lines through quests and crossings
        changed = False
        for k in keys:
            if k in fixed:
                continue
            b0 = bad(k)
            if b0 == 0:
                continue
            best = search(k, b0, 3, 10, False)
            if (best[2], best[3]) != (X[k], Y[k]) and best[0] < b0 + 0.15 * length(k) - 1e-9:
                move(k, best[2], best[3])
                changed = True
                continue
            # No single move helps: try swapping places with another quest of the same column.
            x, yk = X[k], Y[k]
            here = b0 + 0.15 * length(k)
            best_j, best_gain = None, 1e-9
            for j in col[x]:
                if j == k or j in fixed or abs(Y[j] - yk) > 8:
                    continue
                yj = Y[j]
                before = here + bad(j) + 0.15 * length(j)
                move(k, x, yj)
                move(j, x, yk)
                if ok(k, x, yj) and ok(j, x, yk):
                    gain = before - (bad(k) + bad(j) + 0.15 * (length(k) + length(j)))
                    if gain > best_gain:
                        best_j, best_gain = j, gain
                move(k, x, yk)
                move(j, x, yj)
            if best_j is not None:
                yj = Y[best_j]
                move(k, x, yj)
                move(best_j, x, yk)
                changed = True
        if not changed:
            break
    for _ in range(3):  # phase 2: shorten long lines where that costs nothing
        changed = False
        for k in keys:
            if k in fixed or not inc[k] or max(math.hypot(X[a] - X[b], Y[a] - Y[b]) for a, b in inc[k]) <= MAX_EDGE:
                continue
            best = search(k, bad(k), 2, 24, True)
            if (best[2], best[3]) != (X[k], Y[k]):
                move(k, best[2], best[3])
                changed = True
        if not changed:
            break


def _score(m):
    """How messy a finished layout looks (lower is better): lines through quests are the worst."""
    return 6 * m["thru"] + 3 * m["cross"] + m["long"] + 0.01 * m["h"]


def apply(chapter, book_keys=None):
    """Place every quest of an auto-layout chapter and its quest links. book_keys = all quest keys in the book
    (used to add entry links); quests in other chapters are never moved. The layout runs once per fan width in
    FANS and keeps the tidiest result (_score of metrics())."""
    chapter.pruned_deps = getattr(chapter, "pruned_deps", 0) + prune_transitive(chapter.quests)
    if getattr(chapter, "layout", "auto") == "manual" or not chapter.quests:
        return
    links0, best = list(chapter.links), None
    for fan in FANS:
        chapter.links = list(links0)
        _apply_once(chapter, book_keys, fan)
        sc = _score(metrics(chapter))
        if best is None or sc < best[0]:
            best = (sc, [(q.x, q.y) for q in chapter.quests], list(chapter.links))
    for q, (x, y) in zip(chapter.quests, best[1]):
        q.x, q.y = x, y
    chapter.links = best[2]


def _apply_once(chapter, book_keys, fan):
    quests = chapter.quests
    byk, idx, parents, children, order = _graph(quests)
    G = {"byk": byk, "idx": idx, "parents": parents, "children": children, "order": order,
         "opt": {k: bool(byk[k].optional) for k in byk}, "fan": fan}

    # Connected groups of quests (lines inside the chapter). The one holding the chapter's spine is laid out
    # first with its spine on y = 0; every other group is laid out the same way on its own and packed below it
    # in shelves, so unrelated topics sit side by side instead of in one tall stack.
    spine = _spine(set(byk), G)
    comp, comps = {}, []
    for k in order:
        if k in comp:
            continue
        stack, members = [k], []
        comp[k] = len(comps)
        while stack:
            v = stack.pop()
            members.append(v)
            for n in parents[v] + children[v]:
                if n not in comp:
                    comp[n] = len(comps)
                    stack.append(n)
        comps.append(set(members))
    main = comp[spine[0]]
    # Links (see L8 below) known before the layout: the chapter's own plus the entry quest's deps elsewhere.
    links = [lk for lk, _, _ in chapter.links]
    if book_keys is not None:
        for d in byk[spine[0]].deps:
            if d not in byk and d in book_keys and d not in links:
                links.append(d)
    dependents = {}
    for q in quests:
        for d in dict.fromkeys(q.deps):
            if d not in byk:
                dependents.setdefault(d, []).append(q.key)
    blocks = []
    for i, ks in enumerate(comps):
        cl = [(("link", lk), [k for k in dependents.get(lk, []) if k in ks]) for lk in links]
        depth, Y = _place(ks, G, spine if i == main else _spine(ks, G), [t for t in cl if t[1]])
        blocks.append((i, ks, depth, Y))

    # L8: a link sits one column left of its leftmost dependent, at the height the layout gave it, so its lines
    # are short (column -1 = the link column at x = -2 when the dependent is in column 0). A link used by
    # several groups goes with the group holding most of its dependents. Links nothing here depends on go in
    # the link column (12 per column, then x = -4 ...). FTB draws a dependency line from a link to every quest
    # of this chapter that depends on the linked quest, so links take part in the final repair too.
    X, Yall, link_at = {}, {}, {}

    def put(ks, depth, Y, cx, dy):
        for k in ks:
            X[k], Yall[k] = cx + depth[k] * COL, Y[k] + dy
        for k in depth:
            if isinstance(k, tuple):
                n = sum(1 for d in dependents[k[1]] if d in ks)
                if k[1] not in link_at or n > link_at[k[1]][0]:
                    link_at[k[1]] = (n, cx + depth[k] * COL, Y[k] + dy)

    i, ks, depth, Y = blocks[main]
    put(ks, depth, Y, 0.0, 0.0)
    width = max(max(X.values()), 26.0)
    bottom = max(Yall[k] + _size(byk[k]) / 2 for k in ks)
    rest = sorted((b for b in blocks if b[0] != main), key=lambda b: (-len(b[1]), min(idx[k] for k in b[1])))
    cx, shelf_top, shelf_h = 0.0, None, 0.0
    for i, ks, depth, Y in rest:
        own = [k for k in depth if isinstance(k, tuple) or k in ks]
        top = min(Y[k] - (_size(byk[k]) if k in byk else 1.0) / 2 for k in own)
        h = max(Y[k] + (_size(byk[k]) if k in byk else 1.0) / 2 for k in own) - top
        left = min(depth[k] for k in own)  # -1 when a link sits left of the group
        w = (max(depth.values()) - left) * COL
        if shelf_top is None or (cx > 0 and cx + w > width):  # new shelf
            shelf_top = (bottom if shelf_top is None else shelf_top + shelf_h) + 1.5
            cx, shelf_h = 0.0, 0.0
        dy = math.ceil((shelf_top - top) * 2) / 2
        put(ks, depth, Y, cx - (left * COL if cx > 0 else 0.0), dy)
        cx += w + (COL if len(own) == 1 else 2 * COL)
        shelf_h = max(shelf_h, h + (dy - (shelf_top - top)))
    placed = [(lk, link_at[lk][1], link_at[lk][2]) for lk in links if lk in link_at and link_at[lk][0] == len(dependents[lk])]
    for lk in links:  # dependents in several groups: left of the leftmost one, in the nearest free spot
        if lk not in link_at or link_at[lk][0] == len(dependents[lk]):
            continue
        x = max(LINK_X, min(X[d] for d in dependents[lk]) - COL)
        y0 = round(sum(Yall[d] for d in dependents[lk]) / len(dependents[lk]) * 2) / 2
        taken = [(Yall[k], _size(byk[k])) for k in order if X[k] == x] + [(yy, 1.0) for _, xx, yy in placed if xx == x]
        y = next(y0 + sg * j * 0.5 for j in range(400) for sg in (1, -1)
                 if all(abs(y0 + sg * j * 0.5 - ty) >= max(MIN_SEP, (ts + 1) / 2 + 0.5) for ty, ts in taken))
        placed.append((lk, x, y))
    loose = [lk for lk in links if lk not in link_at]
    for start in range(0, len(loose), LINK_ROWS):
        part = loose[start:start + LINK_ROWS]
        x = LINK_X - COL * (start // LINK_ROWS)
        y = min([Yall[k] for k in order] + [y for _, xx, y in placed if xx == x])  # stack upwards, clear of the rest
        placed += [(lk, x, y - MIN_SEP * (j + 1)) for j, lk in enumerate(part)]

    # Final repair on quests and links together (links only move up and down in their column).
    lks = {lk for lk, _, _ in placed}
    nodes = list(order) + [("link", lk) for lk, _, _ in placed]
    par = {k: list(parents[k]) + [("link", d) for d in dict.fromkeys(byk[k].deps) if d not in byk and d in lks]
           for k in order}
    chi = {k: list(children[k]) for k in order}
    for lk, x, y in placed:
        par[("link", lk)], chi[("link", lk)] = [], list(dependents.get(lk, []))
        X[("link", lk)], Yall[("link", lk)] = x, y
    size = {k: _size(byk[k]) for k in order}
    size.update({("link", lk): 1.0 for lk in lks})
    optf = dict(G["opt"])
    optf.update({("link", lk): True for lk in lks})  # links keep MIN_SEP apart
    _repair(nodes, par, chi, size, optf, X, Yall, set(spine) | {k for k in byk if byk[k].row is not None},
            {("link", lk) for lk in lks})
    for q in quests:
        q.x, q.y = X[q.key], Yall[q.key] + 0.0
    chapter.links = [(lk, x, Yall[("link", lk)] + 0.0) for lk, x, _ in placed]


# --- banner (L12) -----------------------------------------------------------------------------
def banner(chapter, with_links=True):
    """Centre (x, y) of the 6 x 1 chapter banner: above the topmost quest or link, left-aligned with the chapter.
    with_links=False gives the old rule (quests only), used for the "before" column of the report."""
    pts = [(q.x, q.y, _size(q)) for q in chapter.quests] + ([(x, y, 1.0) for _, x, y in chapter.links] if with_links else [])
    left = min(x - s / 2 for x, _, s in pts)
    top = min(y - s / 2 for _, y, s in pts)
    return left + 3.0, top - 1.5


# --- metrics (--layout-report) ----------------------------------------------------------------
def _orient(a, b, c):
    v = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    return 0 if abs(v) < 1e-9 else (1 if v > 0 else -1)


def _cross(e1, e2):
    """Proper crossing of two segments that share no endpoint."""
    a, b = e1
    c, d = e2
    if {a, b} & {c, d}:
        return False
    return _orient(a, b, c) * _orient(a, b, d) < 0 and _orient(c, d, a) * _orient(c, d, b) < 0


def _seg_dist(a, b, p):
    (x1, y1), (x2, y2), (px, py) = a, b, p
    dx, dy = x2 - x1, y2 - y1
    L = dx * dx + dy * dy
    t = 0 if L == 0 else max(0.0, min(1.0, ((px - x1) * dx + (py - y1) * dy) / L))
    return math.hypot(px - (x1 + t * dx), py - (y1 + t * dy))


def metrics(chapter, old_banner=False):
    qs = chapter.quests
    qpos = {q.key: (float(q.x), float(q.y)) for q in qs}
    size = {q.key: _size(q) for q in qs}
    # FTB also draws a line from a quest link to each quest here that depends on the linked quest.
    lpos = {("link", lk): (float(x), float(y)) for lk, x, y in chapter.links if lk not in qpos}
    pos = {**qpos, **lpos}
    size.update({k: 1.0 for k in lpos})
    edges = [(d, q.key) for q in qs for d in dict.fromkeys(q.deps) if d in qpos and d != q.key]
    edges += [(("link", d), q.key) for q in qs for d in dict.fromkeys(q.deps) if ("link", d) in lpos]
    segs = [(pos[a], pos[b], a, b) for a, b in edges]
    crossings = sum(1 for i in range(len(segs)) for j in range(i + 1, len(segs)) if _cross(segs[i][:2], segs[j][:2]))
    thru = sum(1 for (p1, p2, a, b) in segs for k, p in pos.items()
               if k not in (a, b) and _seg_dist(p1, p2, p) < 0.45 + (size[k] - 1) / 2)
    long_ = sum(1 for (p1, p2, _, _) in segs if math.dist(p1, p2) > MAX_EDGE)
    left = sum(1 for (p1, p2, _, _) in segs if p2[0] <= p1[0])
    boxes = [(x, y, size[k]) for k, (x, y) in qpos.items()] + [(float(x), float(y), 1.0) for _, x, y in chapter.links]
    overlaps = close = 0
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            (x1, y1, s1), (x2, y2, s2) = boxes[i], boxes[j]
            h = (s1 + s2) / 2
            if abs(x1 - x2) < h and abs(y1 - y2) < h:
                overlaps += 1
            elif math.hypot(x1 - x2, y1 - y2) < MIN_SEP:
                close += 1
    bx, by = banner(chapter, with_links=not old_banner)
    on_banner = sum(1 for x, y, s in boxes if abs(x - bx) < 3 + s / 2 and abs(y - by) < 0.5 + s / 2)
    xs = [b[0] for b in boxes]
    ys = [b[1] for b in boxes]
    return {"n": len(qs), "w": max(xs) - min(xs), "h": max(ys) - min(ys), "cross": crossings, "thru": thru,
            "long": long_, "left": left, "overlap": overlaps + on_banner, "close": close, "links": len(chapter.links)}


def report(chapters, apply_fn):
    """Before/after table for every chapter (nothing is written). apply_fn(chapter) runs the layout."""
    rows = []
    for c in chapters:
        before = metrics(c, old_banner=True)
        apply_fn(c)
        after = metrics(c)
        rows.append((c, before, after))
    bad = lambda m: m["cross"] * 2 + m["thru"] + m["long"] * 2 + m["overlap"] * 5 + m["left"]
    rows.sort(key=lambda r: (-bad(r[1]), r[0].key))
    head = ("| chapter | layout | n | extent WxH before->after | crossings | lines thru quests | edges > 6 | "
            "edges pointing left | overlaps (incl. banner) | closer than 1.5 | links |")
    out = [head, "|" + "---|" * 11]
    tot_b = {k: 0 for k in ("cross", "thru", "long", "left", "overlap", "close")}
    tot_a = dict(tot_b)
    for c, b, a in rows:
        for k in tot_b:
            tot_b[k] += b[k]
            tot_a[k] += a[k]
        out.append(f"| {c.key} | {getattr(c, 'layout', 'auto')} | {a['n']} | {b['w']:g}x{b['h']:g}->{a['w']:g}x{a['h']:g} | "
                   f"{b['cross']}->{a['cross']} | {b['thru']}->{a['thru']} | {b['long']}->{a['long']} | "
                   f"{b['left']}->{a['left']} | {b['overlap']}->{a['overlap']} | {b['close']}->{a['close']} | {b['links']}->{a['links']} |")
    out.append(f"| **total** | | {sum(r[2]['n'] for r in rows)} | | {tot_b['cross']}->{tot_a['cross']} | "
               f"{tot_b['thru']}->{tot_a['thru']} | {tot_b['long']}->{tot_a['long']} | {tot_b['left']}->{tot_a['left']} | "
               f"{tot_b['overlap']}->{tot_a['overlap']} | {tot_b['close']}->{tot_a['close']} | |")
    out += ["", "Crossings and lines through quests include the lines FTB draws from quest links. "
            f"Redundant deps dropped (prune_transitive): {sum(getattr(c, 'pruned_deps', 0) for c in chapters)}."]
    return "\n".join(out)
