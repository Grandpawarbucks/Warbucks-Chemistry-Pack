"""Automatic quest layout for the FTB Quests book (rules L1-L12 in docs/research/quest_layout_audit.md §4.2).

build_quests.py calls apply(chapter) for every chapter before writing it. Writers don't place x/y any more.
v11 (apply): the chapter is split into SECTIONS (_sections), each laid out as its own small drawing with the
v10 engine below (_apply_once, per connected group), turned top-down for "tree"/"grid" pages, then arranged on
the page by the chapter's style ("spine", "tree", "grid"; see the sections block further down) or shape motif
(v12: "winding", "radial", "molecule"; see the motifs block), with header images (chapter.sections), hidden
lines (q.hide_lines / q.hide_dependents) and a last nudge pass. The v10
whole-chapter drawing described next is still there as apply_legacy (the report's "before" column).
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
            bands = min(G.get("bands", 3), math.ceil(len(fan) / G["fan"]))
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


def apply_legacy(chapter, book_keys=None):
    """The v10 whole-chapter layout (one layered drawing, every line pointing right). Kept for the "before" column
    of --layout-report; apply() now lays chapters out in sections and calls _apply_once per section part."""
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


def _apply_once(chapter, book_keys, fan, bands=3):
    quests = chapter.quests
    byk, idx, parents, children, order = _graph(quests)
    G = {"byk": byk, "idx": idx, "parents": parents, "children": children, "order": order,
         "opt": {k: bool(byk[k].optional) for k in byk}, "fan": fan, "bands": bands}

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


# --- sections and page styles (v11) -------------------------------------------------------------
# apply() splits a chapter into visual SECTIONS (small trees of about 4-14 quests, each under a labelled header
# image), lays each section out with _apply_once, then arranges the sections on the page by the chapter's STYLE:
#   "spine": the chapter's main path runs left to right on y = 0; sections are left-to-right trees in one lane
#            above and one lane below it, each starting next to the spine quest it hangs from.
#   "tree":  mod pages. Sections are top-down trees (root on top, children fanning below), stacked in columns in
#            reading order, so section N+1 starts right under section N.
#   "grid":  collection pages: like "tree", but fans wrap into wider, tighter rows.
# Then hide_lines (FTB hide_dependency_lines) is set on quests whose lines would be clutter (a hub's fan, or a
# long line between two sections) when every dependency stays readable without the line: in the same section,
# in a neighbouring section, or shown here as a quest link. FTB still draws hidden lines on mouse-over.
import re

DEFAULT_STYLE = "tree"
SEC_MIN, SEC_IDEAL, SEC_MAX = 4, 9, 14   # section sizes (quests)
HUB = {"spine": 6, "tree": 6, "grid": 4, "winding": 6, "radial": 99, "molecule": 6}  # dependents that make a
# quest a hub (its fan's lines are hidden; radial pages draw the hub's spokes, they are short)
HEAD_H = 0.75      # section header image height (cells)
HEAD_PAD = 0.25    # header bottom to the top edge of the section's quests
CHAR_W = 0.3       # estimated header text width per character (cells), so a block is at least as wide as its title
GAP = {"spine": (1.5, 1.0), "tree": (1.5, 1.0), "grid": (1.25, 1.0)}   # between section blocks (x, y), edge to edge
ROW_W = {"spine": 7.0, "tree": 10.0, "grid": 8.0}  # inside a block: wrap unconnected groups at this width
PAGE_W, PAGE_H = 26.0, 18.0  # target page size; the column packing aims for it
NEAR_ORDER = 2     # sections this close in reading order count as neighbours (a hidden line between them stays readable)
NEAR_GAP = 3.0     # ... and so do sections whose blocks are at most this far apart
DOWN_PITCH = 0.875 # top-down trees: level pitch = COL x this (1.75 cells), where the spacing allows it
SPINE_Y = 1.5      # spine style: distance from the spine (y = 0) to the near edge of a section block


class _Part:
    """A stand-in chapter (one connected group of a section) for _apply_once."""
    def __init__(self, quests, links=()):
        self.key, self.quests, self.layout = "part", quests, "auto"
        self.links = [(lk, 0.0, 0.0) for lk in links]


def _plain(t):
    return " ".join(re.sub(r"&[0-9a-fk-or]", "", t or "").replace("\\&", "&").split())


def quest_name(q):
    """The name FTB shows for a quest: its title, else the first task's item/target id made readable."""
    if q.title:
        return _plain(q.title)
    for t in q.tasks:
        if t[0] in ("item", "dimension", "structure", "biome", "kill"):
            return t[1].split(":")[-1].replace("_", " ").title()
    return q.key


def _short(t, n=26):
    if len(t) <= n:
        return t
    cut = t[:n + 1].rsplit(" ", 1)[0]
    return (cut if len(cut) >= 8 else t[:n]).rstrip(" ,:;-&")


def slug(t):
    """File-name slug for a section title (lower case only: KubeJS rejects upper case asset names)."""
    return re.sub(r"[^a-z0-9]+", "_", t.lower()).strip("_")[:40] or "section"


def _head_w(title):
    return max(3.0, math.ceil((len(title) * CHAR_W + 0.6) * 2) / 2)


def _sections(chapter, G, spine, style, home, titles):
    """Split a chapter into sections. Returns [{"title", "members" (keys, declaration order), "attach", "root"}].
    - Q(section="Title") wins, and passes down to descendants (through each quest's deepest dependency here)
      that have no section of their own. In spine style the spine itself is never in a section.
    - The rest: in spine style, every branch hanging off a spine quest is a unit; in tree/grid style each spine
      quest with the branches hanging off it is a unit (so the spine runs through the sections in order). Groups
      with no line to the spine are units too. Units over SEC_MAX are split along their own subtrees; small
      neighbouring units are merged (dynamic programming towards SEC_IDEAL quests).
    home: quest key -> chapter key (anchor of groups that start from another chapter); titles: chapter key -> title."""
    byk, idx, parents, order = G["byk"], G["idx"], G["parents"], G["order"]
    depth = {}
    for k in order:
        depth[k] = max((depth[p] + 1 for p in parents[k]), default=0)
    pp = {k: (max(parents[k], key=lambda p: (depth[p], -idx[p])) if parents[k] else None) for k in order}
    sidx = {k: i for i, k in enumerate(spine)}
    on_spine = set(spine) if style == "spine" else set()
    label = {}
    for k in order:
        if k in on_spine:
            continue
        own, p = getattr(byk[k], "section", None), pp[k]
        if own:
            label[k] = own
        elif p is not None and p in label:
            label[k] = label[p]
        elif p in on_spine and getattr(byk[p], "section", None):
            label[k] = byk[p].section

    def attach_of(k):
        """Spine index of the nearest spine quest up k's chain of deepest dependencies (None: no line to the spine)."""
        p = k
        while p is not None and p not in sidx:
            p = pp[p]
        return sidx.get(p) if p is not None else None

    auto = [k for k in order if k not in on_spine and k not in label]
    aset = set(auto)
    tpar = {k: (pp[k] if pp[k] in aset else None) for k in auto}
    heads = [k for k in auto if tpar[k] is None or (style != "spine" and k in sidx)]
    hset = set(heads)
    kids = {k: [] for k in auto}
    for k in auto:
        if tpar[k] is not None and k not in hset:
            kids[tpar[k]].append(k)

    def subtree(r, within=None):
        out, st = set(), [r]
        while st:
            v = st.pop()
            out.add(v)
            st += [c for c in kids[v] if within is None or c in within]
        return out

    def split(root, nodes):
        """A unit over SEC_MAX: the root keeps the child subtrees that fit, the others become their own sections."""
        if len(nodes) <= SEC_MAX:
            return [nodes]
        subs = {c: subtree(c, nodes) for c in kids[root] if c in nodes}
        core, bins, out = {root}, [], []
        for c in sorted(subs, key=lambda c: (-len(subs[c]), idx[c])):
            s = subs[c]
            if len(s) > SEC_MAX:
                out += split(c, s)
            elif len(core) + len(s) <= SEC_MAX or (len(s) <= 2 and len(core) + len(s) <= SEC_MAX + 10) or (
                    style == "radial" and len(s) <= 3 and len(core) + len(s) <= SEC_MAX + 24):
                core |= s  # small leaves stay with their hub (a hub's fan reads best in one block; on a radial page
                #            they ring the hub)
            else:
                b = next((b for b in bins if len(b) + len(s) <= SEC_MAX), None)
                if b is None:
                    bins.append(set(s))
                else:
                    b |= s
        return [core] + bins + out

    def anchor(h):
        if attach_of(h) is not None:
            return "spine"
        ext = [d for d in byk[h].deps if d not in byk]
        if ext:
            return "ch:" + home.get(ext[0], "")
        return "sec:" + label[pp[h]] if pp[h] in label else ""

    def spine_attach(h, members):
        """Spine style: the spine quest a unit hangs from (through deepest deps), else the earliest spine quest any
        of its quests depends on, else None (no line to the spine)."""
        a = attach_of(h)
        if a is None:
            a = min((sidx[d] for m in members for d in parents[m] if d in sidx), default=None)
        if a is None:  # a feeder: sits just before the first spine quest that needs it
            a = min((max(0, sidx[c] - 1) for m in members for c in G["children"][m] if c in sidx), default=None)
        return a

    units = []
    for h in heads:  # parts of a split unit stay next to each other (the split-off parts follow their root)
        for n, part in enumerate(split(h, subtree(h))):
            units.append({"members": part, "attach": spine_attach(h, part) if style == "spine" else None,
                          "anchor": anchor(h), "first": min(idx[k] for k in part), "order": (idx[h], n)})
    # A feeder unit (nothing here leads into it, and it doesn't feed the spine) joins the unit it feeds most, so a
    # prerequisite sits in the same tree as the quest that needs it.
    unit_of = {k: i for i, u in enumerate(units) for k in u["members"]}
    for i, u in enumerate(units):
        if not u["members"] or any(p not in u["members"] for m in u["members"] for p in parents[m]):
            continue
        tgt = [unit_of.get(c, "spine") for m in u["members"] for c in G["children"][m] if c not in u["members"]]
        if tgt and "spine" not in tgt:  # several consumers: it joins the one it feeds most (ties: the earliest)
            j = max(dict.fromkeys(tgt), key=lambda t: (tgt.count(t), -units[t]["order"][0]))
            if j != "spine" and j != i and len(units[j]["members"]) + len(u["members"]) <= SEC_MAX + 2:
                units[j]["members"] |= u["members"]
                units[j]["first"] = min(units[j]["first"], u["first"])
                for k in u["members"]:
                    unit_of[k] = j
                u["members"] = set()
    units = [u for u in units if u["members"]]
    if style == "spine":
        units.sort(key=lambda u: (u["attach"] or 0, u["order"]))  # loose units sit by the start
    else:
        units.sort(key=lambda u: u["order"])

    def group_cost(g):
        n = sum(len(u["members"]) for u in g)
        if len(g) > 1 and n > SEC_MAX:
            return None
        att = [u["attach"] for u in g]
        if style == "spine" and len(g) > 1:
            loose = [u for u in g if u["attach"] is None]
            if loose and len(loose) < len(g) and sum(len(u["members"]) for u in loose) > 2:
                return None  # only a quest or two with no line to the spine may join a spine section
            att = [a for a in att if a is not None] or [None]
            if att[0] is not None and max(att) - min(att) > 3:
                return None
        c = (n - SEC_IDEAL) ** 2 + (60 if n < SEC_MIN else 0)
        return c + 25 * (len({u["anchor"] for u in g}) - 1)

    best, prev = [0.0] + [math.inf] * len(units), [0] * (len(units) + 1)
    for j in range(1, len(units) + 1):
        for i in range(j - 1, -1, -1):
            c = group_cost(units[i:j])
            if c is None:
                break
            if best[i] + c < best[j]:
                best[j], prev[j] = best[i] + c, i
    groups, j = [], len(units)
    while j > 0:
        groups.append(units[prev[j]:j])
        j = prev[j]
    groups.reverse()

    secs = []
    for g in groups:
        mem = set().union(*(u["members"] for u in g))
        att = [u["attach"] for u in g if u["attach"] is not None]
        secs.append({"members": mem, "attach": min(att) if att else None, "title": None,
                     "anchor": g[0]["anchor"], "first": min(idx[k] for k in mem), "order": g[0]["order"]})
    for name in dict.fromkeys(label[k] for k in order if k in label):  # explicit sections, as written
        mem = {k for k in label if label[k] == name}
        att = [a for a in (attach_of(k) for k in mem) if a is not None]
        secs.append({"members": mem, "attach": (min(att) if att else None) if style == "spine" else None,
                     "title": _plain(name), "anchor": "", "first": min(idx[k] for k in mem),
                     "order": (min(idx[k] for k in mem), 0)})
    if style == "spine":
        secs.sort(key=lambda s: (s["attach"] is None, s["attach"] or 0, s["order"]))
    else:
        secs.sort(key=lambda s: s["order"])

    used = {}
    for s in secs:
        mem = s["members"]
        s["members"] = sorted(mem, key=idx.get)
        roots = [k for k in s["members"] if pp[k] not in mem]
        n_kids = {k: sum(1 for c in mem if pp[c] == k) for k in roots}
        s["root"] = min(roots, key=lambda k: (-n_kids[k], idx[k]))
        if not s["title"]:
            if not any(n_kids.values()) and len(roots) >= 3 and s["anchor"].startswith("ch:") and titles.get(s["anchor"][3:]):
                s["title"] = "From " + _plain(titles[s["anchor"][3:]])  # a loose collection: named after where it starts
            else:
                s["title"] = quest_name(byk[s["root"]])
        t = _short(s["title"])
        used[t] = used.get(t, 0) + 1
        s["title"] = t if used[t] == 1 else f"{t} {used[t]}"
    return secs


def _part_layout(quests, links, fans, bands):
    """_apply_once on one connected group (best of the fan widths). Returns {node: (x, y, size)} in L->R form;
    link nodes are ("link", key)."""
    part, best = _Part(quests, links), None
    for fan in fans:
        part.links = [(lk, 0.0, 0.0) for lk in links]
        _apply_once(part, None, fan, bands)
        sc = _score(metrics(part))
        if best is None or sc < best[0]:
            best = (sc, {q.key: (float(q.x), float(q.y), _size(q)) for q in quests},
                    {("link", lk): (float(x), float(y), 1.0) for lk, x, y in part.links})
    return {**best[1], **best[2]}


def _extent(pts):
    return (min(x - s / 2 for x, y, s in pts.values()), min(y - s / 2 for x, y, s in pts.values()),
            max(x + s / 2 for x, y, s in pts.values()), max(y + s / 2 for x, y, s in pts.values()))


def _block(sec, byk, links, style, header):
    """Lay out one section as a block: header strip on top (if any), then its quests. links: {link key: [its
    dependents in this section]}. Adds pos (node -> (x, y, size)), w, h and head (header box x0, y0, x1, y1) to
    the section dict, all relative to the block's top-left corner."""
    keys = sec["members"]
    kset = set(keys)
    comp = {k: k for k in keys}

    def find(k):
        while comp[k] != k:
            comp[k] = comp[comp[k]]
            k = comp[k]
        return k

    for k in keys:  # connected groups inside the section (union-find)
        for d in byk[k].deps:
            if d in kset and d != k:
                comp[find(k)] = find(d)
    groups = {}
    for k in keys:
        groups.setdefault(find(k), []).append(k)
    groups = sorted(groups.values(), key=lambda g: (sec["root"] not in g, -len(g), keys.index(g[0])))
    lgroup = {}
    for lk, ds in links.items():
        cnt = [sum(1 for d in ds if d in g) for g in groups]
        lgroup[lk] = cnt.index(max(cnt))
    fans, bands = (FANS, 3) if style != "grid" else ((5, 4), 6)
    down = style != "spine"
    parts = []
    for gi, g in enumerate(groups):
        pts = _part_layout([byk[k] for k in g], [lk for lk in links if lgroup[lk] == gi], fans, bands)
        if down:
            tight = {n: (y, x * DOWN_PITCH, s) for n, (x, y, s) in pts.items()}
            ok = all(math.hypot(a[0] - b[0], a[1] - b[1]) >= max(MIN_SEP, (a[2] + b[2]) / 2 + 0.5) - 1e-9
                     for i, a in enumerate(tight.values()) for b in list(tight.values())[i + 1:])
            pts = tight if ok else {n: (y, x, s) for n, (x, y, s) in pts.items()}
        x0, y0, x1, y1 = _extent(pts)
        parts.append(({n: (x - x0, y - y0, s) for n, (x, y, s) in pts.items()}, x1 - x0, y1 - y0))
    gx, gy = GAP[style]
    pos, cx, cy, row_h = {}, 0.0, 0.0, 0.0
    width = max([ROW_W[style]] + [w for _, w, _ in parts])
    for pts, w, h in parts:
        if cx > 0 and cx + w > width:  # rows of groups, wrapped at the block width
            cx, cy, row_h = 0.0, cy + row_h + gy * 0.5, 0.0
        pos.update({n: (x + cx, y + cy, s) for n, (x, y, s) in pts.items()})
        cx, row_h = cx + w + gx * 0.5, max(row_h, h)
    x0, y0, x1, y1 = _extent(pos)
    top = HEAD_H + HEAD_PAD if header else 0.0
    pos = {n: (round((x - x0) * 2) / 2, round((y - y0 + top) * 2) / 2, s) for n, (x, y, s) in pos.items()}
    hx0 = 0.0
    if not down:  # spine style: the header starts at the root, so the line from the spine passes left of it
        rx, _, rs = pos[sec["root"]]
        hx0 = max(0.0, rx - rs / 2)
    hw = _head_w(sec["title"])
    x0, y0, x1, y1 = _extent(pos)
    w = max(x1, hx0 + hw) if header else x1
    sec.update(pos=pos, w=w, h=y1, head=(hx0, 0.0, w, HEAD_H) if header else None)
    return sec


def _pack_columns(blocks, style):
    """Tree/grid style: blocks in reading order, top to bottom in columns. Tries every column height and keeps the
    one whose page fits the PAGE_W x PAGE_H target best. Returns {block index: (x, y)}."""
    gx, gy = GAP[style]
    total = sum(b["h"] for b in blocks) + gy * (len(blocks) - 1)
    best = None
    H = max(b["h"] for b in blocks)
    while True:
        cols, cur, ch = [], [], 0.0
        for i, b in enumerate(blocks):
            need = b["h"] + (gy if cur else 0.0)
            if cur and ch + need > H + 1e-9:
                cols.append(cur)
                cur, ch, need = [], 0.0, b["h"]
            cur.append(i)
            ch += need
        cols.append(cur)
        W = sum(max(blocks[i]["w"] for i in c) for c in cols) + gx * (len(cols) - 1)
        Hh = max(sum(blocks[i]["h"] for i in c) + gy * (len(c) - 1) for c in cols)
        sc = max(W / PAGE_W, Hh / PAGE_H) + 0.02 * len(cols)
        if best is None or sc < best[0] - 1e-9:
            best = (sc, cols)
        if H >= total:
            break
        H += 0.5
    at, x = {}, 0.0
    for c in best[1]:
        y = 0.0
        for i in c:
            at[i] = (x, y)
            y += blocks[i]["h"] + gy
        x += max(blocks[i]["w"] for i in c) + gx
    # Rows (reading order left to right, wrapped at a width) instead, when that fits the target page better.
    total_w = sum(b["w"] for b in blocks) + gx * (len(blocks) - 1)
    W = max(b["w"] for b in blocks)
    while True:
        rows, cur, cw = [], [], 0.0
        for i, b in enumerate(blocks):
            need = b["w"] + (gx if cur else 0.0)
            if cur and cw + need > W + 1e-9:
                rows.append(cur)
                cur, cw, need = [], 0.0, b["w"]
            cur.append(i)
            cw += need
        rows.append(cur)
        Hh = sum(max(blocks[i]["h"] for i in r) for r in rows) + gy * (len(rows) - 1)
        Ww = max(sum(blocks[i]["w"] for i in r) + gx * (len(r) - 1) for r in rows)
        sc = max(Ww / PAGE_W, Hh / PAGE_H) + 0.02 * len(rows) + 0.03  # small bias: columns read top-down
        if sc < best[0] - 1e-9:
            best = (sc, None)
            at, y = {}, 0.0
            for r in rows:
                xx = 0.0
                for i in r:
                    at[i] = (xx, y)
                    xx += blocks[i]["w"] + gx
                y += max(blocks[i]["h"] for i in r) + gy
        if W >= total_w:
            break
        W += 0.5
    return at


class _Stub:
    """A quest link standing in as a quest, so _apply_once can lay links out by their quests' own deps."""
    def __init__(self, key, deps):
        self.key, self.deps, self.x, self.y = key, deps, 0.0, 0.0
        self.size, self.optional, self.row, self.any_dep, self.hidden, self.repeat = 1.0, True, None, False, False, False
        self.hide_lines = self.hide_dependents = False


def _link_block(keys, book, down, width):
    """Positions (relative, top-left at 0, 0) for links with no dependents here. Links whose quests depend on each
    other are drawn by FTB with a line between them, so they are laid out as trees (top-down if down), each
    connected group on its own, packed in rows of the given width."""
    ks = set(keys)
    stubs = {k: _Stub(k, [d for d in (book[k].deps if k in book else []) if d in ks and d != k]) for k in keys}
    comp = {k: k for k in keys}

    def find(k):
        while comp[k] != k:
            comp[k] = comp[comp[k]]
            k = comp[k]
        return k

    for k in keys:
        for d in stubs[k].deps:
            comp[find(k)] = find(d)
    groups = {}
    for k in keys:
        groups.setdefault(find(k), []).append(k)
    parts = []
    for g in sorted(groups.values(), key=lambda g: (len(g) == 1, keys.index(g[0]))):
        if len(g) == 1:
            parts.append(({g[0]: (0.5, 0.5)}, 1.0, 1.0))
            continue
        pts = _part_layout([stubs[k] for k in g], [], FANS, 3)
        if down:
            pts = {n: (y, x, s) for n, (x, y, s) in pts.items()}
        x0, y0, x1, y1 = _extent(pts)
        parts.append(({n: (x - x0, y - y0) for n, (x, y, s) in pts.items()}, x1 - x0, y1 - y0))
    out, cx, cy, row_h = {}, 0.0, 0.0, 0.0
    for pts, w, h in parts:
        if cx > 0 and cx + w > width:
            cx, cy, row_h = 0.0, cy + row_h + 0.5, 0.0
        out.update({n: (round((x + cx) * 2) / 2, round((y + cy) * 2) / 2) for n, (x, y) in pts.items()})
        cx, row_h = cx + w + 0.5, max(row_h, h)
    return out


def _free_spot(x, y, taken, lo_x=None):
    """Nearest spot to (x, y) on the 0.5 grid that is at least MIN_SEP from every taken (x, y, size) point."""
    for r in range(0, 80):
        ring = sorted({(a * 0.5, b * 0.5) for a in range(-r, r + 1) for b in range(-r, r + 1) if max(abs(a), abs(b)) == r},
                      key=lambda d: (abs(d[0]) + abs(d[1]), d))
        for dx, dy in ring:
            px, py = x + dx, y + dy
            if lo_x is not None and px > lo_x:
                continue
            if all(math.hypot(px - tx, py - ty) >= max(MIN_SEP, (ts + 1) / 2 + 0.5) for tx, ty, ts in taken):
                return px, py
    return x, y


# --- shape motifs (v12) -------------------------------------------------------------------------
# Three page shapes on top of the v11 sections (STYLES in quest_data.py; each falls back to plain blocks where a
# shape doesn't fit, so a page is never worse than readable):
#   "winding":  spine pages. The spine snakes in rows of 4-7 quests, alternating direction (an S-curve), with a
#               vertical step at each bend (bend quests sit on a rounded corner when the rows are far apart). Sections
#               hang off their spine quest as top-down trees: above a row (pointing up) or below it (pointing down),
#               in the lane between two rows; sections that hang from a bend sit outside the bend.
#   "radial":   hub pages. The hub (the quest most of the page hangs from) sits in the middle with its own section
#               as a radial tree around it (rings of children, staggered when crowded); the other sections are
#               spokes around it, each a short tree pointing outward. Pages with no real hub put their first section
#               in the middle instead.
#   "molecule": chemistry pages. A section whose quests form a tree that fits is drawn as small rings of 5-6
#               quests (benzene-like hexagons, ring order = dependency order) joined by bonds, with short chains
#               (substituents) pointing outward. A ring's closing side isn't a dependency, so FTB draws no line there.
# BLOCK_KIND (quest_data.BLOCKS) can also ask for molecule-shaped sections on a winding page (e.g. t4, t6).
MOTIF_BASE = {"spine": "spine", "tree": "tree", "grid": "grid", "winding": "spine", "radial": "tree", "molecule": "tree"}
WIND_ROWS = (4, 5, 6, 7)   # spine quests per row tried
WIND_PITCH = (2.0, 2.5)    # spine pitch tried (cells)
WIND_GAP = 3.0             # minimum distance between two spine rows
WIND_STEP = 3.0            # bend quests are added so the vertical step has no line longer than this ...
WIND_BEND = 2              # ... but at most this many per bend (the rest of the spine stays in rows)
WIND_TALL = 7.0            # a block taller than this pushes two rows far apart: it prefers an outer lane
BOND = 2.0                 # molecule: bond length (cells)
SPREAD = math.radians(42)  # molecule / radial: angle between sibling branches
RING_R = {6: 2.0, 5: 1.75} # ring radius (centre to quest) for size-1 quests


def _rects_hit(a, b, pad=0.0):
    return a[0] < b[2] + pad and b[0] < a[2] + pad and a[1] < b[3] + pad and b[1] < a[3] + pad


def _flip(pos, axis):
    """Mirror block positions (top-left at 0, 0) on x ("x") or y ("y")."""
    x0, y0, x1, y1 = _extent(pos)
    if axis == "x":
        return {n: (x1 - (x - x0), y, s) for n, (x, y, s) in pos.items()}
    return {n: (x, y1 - (y - y0), s) for n, (x, y, s) in pos.items()}


def _edges_in(pos, byk):
    """Dependency lines between quests of one block: [(a, b)]."""
    return [(d, k) for k in pos if isinstance(k, str) and k in byk
            for d in dict.fromkeys(byk[k].deps) if d in pos and d != k]


def _clean(pos, byk, edges=None):
    """True when no two quests are too close, no line runs through a quest and no two lines cross."""
    items = list(pos.items())
    for i, (a, (ax, ay, as_)) in enumerate(items):
        for b, (bx, by, bs) in items[i + 1:]:
            if math.hypot(ax - bx, ay - by) < max(MIN_SEP, (as_ + bs) / 2 + 0.5) - 1e-9:
                return False
    edges = _edges_in(pos, byk) if edges is None else edges
    segs = [((pos[a][0], pos[a][1]), (pos[b][0], pos[b][1]), a, b) for a, b in edges]
    for p1, p2, a, b in segs:
        for k, (x, y, s) in items:
            if k not in (a, b) and _seg_dist(p1, p2, (x, y)) < 0.5 + (s - 1) / 2:
                return False
    for i in range(len(segs)):
        for j in range(i + 1, len(segs)):
            if _cross(segs[i][:2], segs[j][:2]):
                return False
    return True


def _with_header(sec, pos, byk, header, mode, orient):
    """Normalise a block (top-left at 0, 0) and add its header strip. mode: "top" (above the block; for a
    left-to-right block it starts at the root, so the line into the root passes left of it), "bottom" (below the
    block: the far end of a block that hangs down), "corner" (top left, only as wide as the title: a radial core,
    so the spoke going up passes beside it), "beside" (on the root's row, beside the root: for a block that
    hangs down from a line coming in from above; falls back to "bottom")."""
    x0, y0, x1, y1 = _extent(pos)
    x0, y0 = math.floor(x0 * 2) / 2, math.floor(y0 * 2) / 2  # a grid-aligned shift keeps every gap as it was
    pos = {n: (round((x - x0) * 2) / 2, round((y - y0) * 2) / 2, s) for n, (x, y, s) in pos.items()}
    w, h = _extent(pos)[2:]
    root = sec["root"]
    hb = None
    if header:
        hw = _head_w(sec["title"])
        rx, ry, rs = pos[root]
        if mode == "beside":
            edges = _edges_in(pos, byk)
            for side in (1, -1) if rx <= w / 2 else (-1, 1):
                if side == 1:
                    bx0 = rx + rs / 2 + 0.25
                else:
                    bx0 = rx - rs / 2 - 0.25 - hw
                box = (bx0, ry - 0.5, bx0 + hw, ry - 0.5 + HEAD_H)
                if any(_rects_hit(box, (x - s / 2, y - s / 2, x + s / 2, y + s / 2), 0.15) for n, (x, y, s) in pos.items()):
                    continue
                if any(box[0] < pos[a][0] + (pos[b][0] - pos[a][0]) * t / 12 < box[2]
                       and box[1] < pos[a][1] + (pos[b][1] - pos[a][1]) * t / 12 < box[3]
                       for a, b in edges for t in range(1, 12)):
                    continue
                hb = box
                break
            if hb is None:
                mode = "bottom"
        if mode in ("top", "corner"):
            top = HEAD_H + HEAD_PAD
            pos = {n: (x, y + top, s) for n, (x, y, s) in pos.items()}
            if orient == "right":
                hx0 = max(0.0, rx - rs / 2)
            elif orient == "left":
                hx0 = max(0.0, min(rx + rs / 2, w) - hw)
            else:
                hx0 = 0.0
            hb = (hx0, 0.0, max(w, hx0 + hw) if mode == "top" else hx0 + hw, HEAD_H)
        elif mode == "bottom":
            hb = (0.0, h + HEAD_PAD, max(w, hw), h + HEAD_PAD + HEAD_H)
        # normalise again (a header beside the root may stick out left or above)
        ex0 = min(0.0, hb[0])
        ey0 = min(0.0, hb[1])
        pos = {n: (x - ex0, y - ey0, s) for n, (x, y, s) in pos.items()}
        hb = (hb[0] - ex0, hb[1] - ey0, hb[2] - ex0, hb[3] - ey0)
    x0, y0, x1, y1 = _extent(pos)
    w, h = (max(x1, hb[2]), max(y1, hb[3])) if hb else (x1, y1)
    return {**sec, "pos": pos, "w": w, "h": h, "head": hb, "orient": orient}


def _molecule(keys, byk, idx):
    """Molecule positions for one section (centre-relative, not normalised), or None when it doesn't fit: no
    subtree big enough for a ring, or the drawing isn't clean (quests too close, lines through quests or crossing).
    Each tree of the section: from its root, a subtree of 5+ quests becomes a ring (its first 5-6 quests in
    depth-first order, biggest branch first, so a chain closes into a hexagon; at most 2 of its lines may be
    chords), and smaller ones become short chains pointing outward."""
    kset = set(keys)
    par = {k: [d for d in dict.fromkeys(byk[k].deps) if d in kset and d != k] for k in keys}
    depth = {}

    def dep(k, seen=()):
        if k not in depth:
            depth[k] = 0 if k in seen else max((dep(p, seen + (k,)) + 1 for p in par[k]), default=0)
        return depth[k]

    for k in keys:
        dep(k)
    tp = {k: (max(par[k], key=lambda p: (depth[p], idx[p])) if par[k] else None) for k in keys}
    kids = {k: [] for k in keys}
    for k in sorted(keys, key=idx.get):
        if tp[k] is not None:
            kids[tp[k]].append(k)
    size = {}

    def sz(k):
        if k not in size:
            size[k] = 1 + sum(sz(c) for c in kids[k])
        return size[k]

    for k in keys:
        kids[k].sort(key=lambda c: (-sz(c), idx[c]))
    roots = [k for k in sorted(keys, key=idx.get) if tp[k] is None]

    def pre(r):
        out = [r]
        for c in kids[r]:
            out += pre(c)
        return out

    def ring_of(r):
        if sz(r) < 5:
            return None
        ring = pre(r)[: 6 if sz(r) >= 6 else 5]
        rs = set(ring)
        pos_ = {v: i for i, v in enumerate(ring)}
        chords = sum(1 for v in ring if tp[v] in rs and abs(pos_[v] - pos_[tp[v]]) not in (1, len(ring) - 1))
        return ring if chords <= 2 else None

    if not any(ring_of(k) for k in keys):
        return None
    big = lambda ks: max([float(byk[k].size or 1) for k in ks] + [1.0])

    def build(spread, spin0, bond):
        P = {}

        def grow(r, ang, spin):
            ring = ring_of(r)
            x, y = P[r]
            if ring:
                k = len(ring)
                R = RING_R[k] + 0.5 * (big(ring) - 1)
                cx, cy = x + R * math.cos(ang), y + R * math.sin(ang)
                cx, cy = round(cx * 2) / 2, round(cy * 2) / 2
                base = math.atan2(y - cy, x - cx)
                for i, v in enumerate(ring):
                    if i:
                        a = base + spin * 2 * math.pi * i / k
                        P[v] = (cx + R * math.cos(a), cy + R * math.sin(a))
                rs = set(ring)
                for v in ring:
                    outs = [c for c in kids[v] if c not in rs]
                    av = math.atan2(P[v][1] - cy, P[v][0] - cx)
                    for j, c in enumerate(outs):
                        a = av + (j - (len(outs) - 1) / 2) * spread
                        b_ = bond + 0.5 * (max(big([v]), big([c])) - 1)
                        P[c] = (P[v][0] + b_ * math.cos(a), P[v][1] + b_ * math.sin(a))
                        grow(c, a, -spin)
            else:
                cs = kids[r]
                for j, c in enumerate(cs):
                    a = ang + (j - (len(cs) - 1) / 2) * spread
                    b_ = bond + 0.5 * (max(big([r]), big([c])) - 1)
                    P[c] = (x + b_ * math.cos(a), y + b_ * math.sin(a))
                    grow(c, a, spin)

        out, cx = {}, 0.0
        for n, r in enumerate(roots):  # trees of the section side by side
            P = {r: (0.0, 0.0)}
            grow(r, math.pi / 2, spin0 if n % 2 == 0 else -spin0)
            pts = {k: (round(x * 2) / 2, round(y * 2) / 2, float(byk[k].size or 1)) for k, (x, y) in P.items()}
            x0, y0, x1, y1 = _extent(pts)
            out.update({k: (x - x0 + cx, y - y0, s) for k, (x, y, s) in pts.items()})
            cx += x1 - x0 + 1.5
        return out

    best = None
    for bond in (BOND, BOND + 0.5):
        for spread in (SPREAD, math.radians(55), math.radians(32)):
            for spin in (1, -1):
                pos = build(spread, spin, bond)
                if len(pos) == len(keys) and _clean(pos, byk):
                    x0, y0, x1, y1 = _extent(pos)
                    sc = (x1 - x0) * (y1 - y0) + 4 * abs((x1 - x0) - (y1 - y0))
                    if best is None or sc < best[0]:
                        best = (sc, pos)
        if best:
            break
    return best[1] if best else None


def _shaped_block(sec, byk, idx, links, orient, header, head, kind, grid=False):
    """One section as a block turned to orient ("down": root on top, "up": root at the bottom, "right": root on the
    left, "left": root on the right), shaped as kind ("tree" or "molecule"; a molecule that doesn't fit is a tree).
    Molecule blocks carry no quest links (the page places those beside their quests)."""
    pos = None
    if kind == "molecule":
        pos = _molecule(sec["members"], byk, idx)
        if pos is not None:
            if orient == "up":
                pos = _flip(pos, "y")
            elif orient in ("right", "left"):  # turn it: the root (on top) faces the line coming in from the side
                pos = {n: (y, x, s) for n, (x, y, s) in pos.items()}
                if orient == "left":
                    pos = _flip(pos, "x")
    if pos is None:
        st = "spine" if orient in ("right", "left") else ("grid" if grid else "tree")
        b = _block(dict(sec), byk, links, st, False)
        pos = b["pos"]
        if orient == "up":
            pos = _flip(pos, "y")
        elif orient == "left":
            pos = _flip(pos, "x")
        kind = "tree"
    out = _with_header(sec, pos, byk, header, head, orient)
    out["kind"] = kind
    return out


def _pava_lane(items, gx, zones=()):
    """1-D packing of one lane: items [(key, desired left, width)] -> {key: left}, as close to the desired spots as
    possible (least squares), in order, gx apart. zones: [(x0, x1)] that no block may overlap (a bend's line);
    blocks wanting the left of a zone stay left of it, the others right of it."""
    if not items:
        return {}
    groups = [[]]
    bounds = [(-math.inf, math.inf)]
    zs = sorted(zones)
    if zs:
        edges = [-math.inf] + [v for z in zs for v in z] + [math.inf]
        groups = [[] for _ in range(len(zs) + 1)]
        bounds = [(edges[2 * i], edges[2 * i + 1]) for i in range(len(zs) + 1)]
    for it in items:
        c = it[1] + it[2] / 2
        gi = sum(1 for z in zs if c > (z[0] + z[1]) / 2)
        groups[gi].append(it)
    out = {}
    for (lo, hi), g in zip(bounds, groups):
        if not g:
            continue
        g.sort(key=lambda t: (t[1] + t[2] / 2, str(t[0])))
        seps = [g[i][2] + gx for i in range(len(g) - 1)]
        xs = _pava([t[1] for t in g], [1.0] * len(g), seps)
        shift = 0.0
        if xs[-1] + g[-1][2] > hi - gx:
            shift = hi - gx - (xs[-1] + g[-1][2])
        if xs[0] + shift < lo + gx:
            shift = lo + gx - xs[0]
        for t, x in zip(g, xs):
            out[t[0]] = round((x + shift) * 2) / 2
    return out


def _settle(boxes, fixed, gap):
    """Push overlapping blocks apart: boxes {i: [x0, y0, x1, y1]} (moved in place, away from what they hit, the
    shorter way), fixed: rects that never move (quests, headers). A few rounds; returns True when clean."""
    for _ in range(60):
        moved = False
        ks = sorted(boxes)
        for i in ks:
            b = boxes[i]
            others = [boxes[j] for j in ks if j != i] + fixed
            for o in others:
                if not _rects_hit(b, o, gap - 1e-9):
                    continue
                cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
                ox, oy = (o[0] + o[2]) / 2, (o[1] + o[3]) / 2
                # the smaller push that separates them, moving away from the other box
                dx = (o[2] + gap - b[0]) if cx >= ox else -(b[2] + gap - o[0])
                dy = (o[3] + gap - b[1]) if cy >= oy else -(b[3] + gap - o[1])
                if abs(dx) <= abs(dy):
                    b[0] += dx
                    b[2] += dx
                else:
                    b[1] += dy
                    b[3] += dy
                moved = True
        if not moved:
            return True
    return False


def _place_block(b, ox, oy, P, heads, i):
    b["box"] = (ox, oy, ox + b["w"], oy + b["h"])
    P.update({n: (x + ox, y + oy, s) for n, (x, y, s) in b["pos"].items()})
    if b["head"]:
        hx0, hy0, hx1, hy1 = b["head"]
        heads.append((i, hx0 + ox, hy0 + oy, hx1 + ox, hy1 + oy))


def _page_box(P, heads):
    xs = [x - s / 2 for x, _, s in P.values()] + [x + s / 2 for x, _, s in P.values()] + [h[1] for h in heads] + [h[3] for h in heads]
    ys = [y - s / 2 for _, y, s in P.values()] + [y + s / 2 for _, y, s in P.values()] + [h[2] for h in heads] + [h[4] for h in heads]
    return min(xs), min(ys), max(xs), max(ys)


def _wind_try(spine, secs, byk, mk, L, pitch, gx):
    """One winding layout: rows of L spine quests at the given pitch. mk(i, orient, head) builds section i's block.
    Returns (score, P, blocks {i: block}, heads)."""
    n = len(spine)
    bends = []
    for it in range(5):
        # partition: rows of L quests, joined by bend quests (bends[r] of them between row r and r + 1)
        rows, bq, i = [], [], 0
        while i < n:
            rows.append(list(range(i, min(n, i + L))))
            i += len(rows[-1])
            b = bends[len(rows) - 1] if len(rows) - 1 < len(bends) else 0
            b = min(b, max(0, n - i - 2))  # the next row keeps at least 2 quests
            bq.append(list(range(i, i + b)))
            i += b
        R = len(rows)
        where = {}
        for r, row in enumerate(rows):
            for j, si in enumerate(row):
                where[si] = ("row", r, j)
        for r, b in enumerate(bq):
            for j, si in enumerate(b):
                where[si] = ("bend", r, j)
        X = {}
        right_end = (L - 1) * pitch
        for r, row in enumerate(rows):
            for j, si in enumerate(row):
                X[si] = j * pitch if r % 2 == 0 else right_end - j * pitch
        # lanes: lane r is above row r (lane R: below the last row). A section hangs from its attach quest.
        lane_of, outside, loose, blk, load = {}, {}, [], {}, {}
        for i_, s in enumerate(secs):
            a = s["attach"]
            if a is None:
                loose.append(i_)
                continue
            kind, r, j = where[a]
            if kind == "bend":
                outside.setdefault(r, []).append(i_)
                continue
            best = None
            flat = "right" if r % 2 == 0 else "left"  # sideways, flowing with the row
            for lane, orient in ((r + 1, "down"), (r + 1, flat), (r, "up")):
                b = mk(i_, orient, "top" if orient == "up" else "beside")
                if orient == flat and b["head"] and b["head"][3] > b["pos"][b["root"]][1] + 0.5:
                    continue  # its header didn't fit beside the root: the line from the spine would cross it
                rx = b["pos"][b["root"]][0]
                left = X[a] - rx
                iv = (left - gx, left + b["w"] + gx)
                over = sum(max(0.0, min(iv[1], o[1]) - max(iv[0], o[0])) for o in load.get(lane, []))
                bz = 0.0  # a bend's line runs through a middle lane: blocks must keep clear of it
                if 0 < lane < R:
                    xe = right_end if (lane - 1) % 2 == 0 else 0.0
                    bz = max(0.0, min(iv[1], xe + 2) - max(iv[0], xe - 2))
                cur = max([0.0] + [blk[k]["h"] for k, l in lane_of.items() if l == lane])
                # a taller middle lane pushes two rows apart (a longer bend); the outer lanes cost little
                grow = max(0.0, b["h"] - cur) * (0.6 if 0 < lane < R else 0.1)
                if 0 < lane < R and b["h"] > WIND_TALL:
                    grow += 2.0 * (b["h"] - WIND_TALL)
                cost = over + 2 * bz + grow + (0.01 if orient == "up" else 0.0)
                if best is None or cost < best[0]:
                    best = (cost, lane, b, left)
            _, lane, b, left = best
            lane_of[i_], blk[i_] = lane, b
            b["want"] = left
            load.setdefault(lane, []).append((left - gx, left + b["w"] + gx))
        lefts = {}
        for lane in range(R + 1):  # pack every lane, clear of the bend that runs through it
            its = [(k, blk[k]["want"], blk[k]["w"]) for k, l in lane_of.items() if l == lane]
            zones = []
            if 0 < lane < R:
                r = lane - 1
                xe = right_end if r % 2 == 0 else 0.0
                out_ = (1.0 if bq[r] else 0.0) * (1 if r % 2 == 0 else -1)
                zones = [(min(xe, xe + out_) - 0.75, max(xe, xe + out_) + 0.75)]
            lefts.update(_pava_lane(its, gx, zones))
        H = {lane: max([blk[k]["h"] for k, l in lane_of.items() if l == lane] + [0.0]) for lane in range(R + 1)}
        Y = [0.0]
        for r in range(1, R):
            Y.append(Y[-1] + max(WIND_GAP, H[r] + 2 * SPINE_Y))
        new = [min(WIND_BEND, max(0, math.ceil((Y[r + 1] - Y[r]) / WIND_STEP - 1e-9) - 1)) for r in range(R - 1)]
        new = [max(a, bends[r] if r < len(bends) else 0) for r, a in enumerate(new)]  # only grows: no flip-flop
        if new == bends[:R - 1] or it == 4:
            break
        bends = new
    P, heads, blocks = {}, [], {}
    for r, row in enumerate(rows):
        for si in row:
            P[spine[si]] = (X[si], Y[r], _size(byk[spine[si]]))
    for r, b in enumerate(bq):
        if not b or r + 1 >= R:
            continue
        xe = right_end if r % 2 == 0 else 0.0
        xo = xe + (1.0 if r % 2 == 0 else -1.0)
        for j, si in enumerate(b):
            y = Y[r] + (Y[r + 1] - Y[r]) * (j + 1) / (len(b) + 1)
            X[si] = xo
            P[spine[si]] = (xo, round(y * 2) / 2, _size(byk[spine[si]]))
    for i_, lane in lane_of.items():
        b = blk[i_]
        rx, ry, rs = b["pos"][b["root"]]
        if b["orient"] != "up":  # hangs below row lane - 1
            oy = Y[lane - 1] + SPINE_Y - (ry - rs / 2)
        else:  # stands on row lane
            oy = Y[lane] - SPINE_Y - b["h"]
        blocks[i_] = b
        b["at"] = [lefts[i_], oy]
    for r, ks in outside.items():  # sections hanging from a bend quest: outside the bend, level with that quest
        right = r % 2 == 0
        for i_ in ks:
            b = mk(i_, "right" if right else "left", "top")
            a = secs[i_]["attach"]
            rx, ry, rs = b["pos"][b["root"]]
            ox = X[a] + 0.5 + gx - (rx - rs / 2) if right else X[a] - 0.5 - gx - (rx + rs / 2)
            b["at"] = [ox, P[spine[a]][1] - ry]
            blocks[i_] = b
    fixed = [(x - s / 2, y - s / 2, x + s / 2, y + s / 2) for x, y, s in P.values()]
    boxes = {i_: [b["at"][0], b["at"][1], b["at"][0] + b["w"], b["at"][1] + b["h"]] for i_, b in blocks.items()}
    _settle(boxes, fixed, gx * 0.75)
    for i_, bx in boxes.items():
        _place_block(blocks[i_], bx[0], bx[1], P, heads, i_)
    if loose:  # sections with no line to the spine: shelves below everything
        x0, _, x1, y1 = _page_box(P, heads)
        width = max(x1 - x0, 12.0)
        y, cx, shelf = y1 + gx, 0.0, 0.0
        for i_ in loose:
            b = mk(i_, "down", "top")
            if cx > 0 and cx + b["w"] > width:
                cx, y, shelf = 0.0, y + shelf + gx, 0.0
            blocks[i_] = b
            _place_block(b, x0 + cx, y, P, heads, i_)
            cx, shelf = cx + b["w"] + gx, max(shelf, b["h"])
    x0, y0, x1, y1 = _page_box(P, heads)
    w, h = x1 - x0, y1 - y0
    pull = 0.0  # line length from each spine quest into its section
    for i_, b in blocks.items():
        a = secs[i_]["attach"]
        if a is not None:
            px, py, _ = P[b["root"]]
            pull += math.hypot(px - P[spine[a]][0], py - P[spine[a]][1])
    # long vertical steps at the bends, and a last row of one quest after a bend, read badly
    steps = sum(max(0.0, (Y[r + 1] - Y[r]) / (len(bq[r]) + 1) - WIND_STEP) for r in range(R - 1))
    sc = (max(w / PAGE_W, h / (PAGE_H + 2)) + 0.25 * abs(math.log(max(w, 1) / max(h, 1) / 1.35)) + 0.02 * pull
          + 0.04 * steps + (0.15 if R > 1 and len(rows[-1]) == 1 else 0.0))
    return sc, P, blocks, heads


def _wind_page(spine, secs, byk, mk, gx):
    """The winding motif: the best of WIND_ROWS x WIND_PITCH. Returns (P, blocks, heads)."""
    # A section with no line to the spine but lines to other sections hangs where those sections hang.
    sidx = {k: i for i, k in enumerate(spine)}
    sec_of = {k: i for i, s in enumerate(secs) for k in s["members"]}
    for _ in range(3):
        for s in secs:
            if s["attach"] is not None:
                continue
            mem = set(s["members"])
            mates = {d for m in mem for d in byk[m].deps if d in byk and d not in mem}
            mates |= {k for k in byk if k not in mem and any(d in mem for d in byk[k].deps)}
            ext = {d for m in mem for d in byk[m].deps if d not in byk}  # shown as quest links: near their other users
            if not mates and ext:
                mates = {k for k in byk if k not in mem and ext & set(byk[k].deps)}
            att = sorted(sidx[k] if k in sidx else secs[sec_of[k]]["attach"] for k in mates
                         if k in sidx or (k in sec_of and secs[sec_of[k]]["attach"] is not None))
            if att:
                s["attach"] = att[len(att) // 2]
    best = None
    for L in WIND_ROWS:
        if L > len(spine) + 1 and best is not None:
            break
        for pitch in WIND_PITCH:
            t = _wind_try(spine, secs, byk, mk, L, pitch, gx)
            if best is None or t[0] < best[0] - 1e-9:
                best = t
    return best[1], best[2], best[3]


def _radial_core(sec, byk, idx, spokes, scale=1.0, hub_angles=()):
    """The hub section as a radial tree around its hub (at 0, 0). spokes: {core quest: n} virtual leaves (other
    sections hanging from that quest) that get their own angle, so the lines out to them pass between the core's
    quests. hub_angles: fixed angles for the hub's own spokes (compass slots), else they are spread evenly.
    The hub's children share the circle evenly (branches and spokes get a wider share); a crowded first
    ring alternates two radii; deeper quests fan out around their parent's angle, one ring further out. Each quest
    is placed in turn (by depth, then angle) and stepped outward until it is clear of everything placed before.
    Returns (pos {key: (x, y, size)}, {(core quest, j): angle}) or None if the result isn't clean."""
    keys = sec["members"]
    kset = set(keys)
    par = {k: [d for d in dict.fromkeys(byk[k].deps) if d in kset and d != k] for k in keys}
    hub = sec["hub"]
    depth, unreached = {hub: 0}, set()

    def relax():
        for _ in range(len(keys) + 1):
            ch = False
            for k in keys:
                ds = [depth[p] + 1 for p in par[k] if p in depth]
                if k != hub and k not in unreached and ds and depth.get(k, -1) < max(ds):
                    depth[k], ch = max(ds), True
            if not ch:
                return

    relax()
    while len(depth) < len(keys):  # quests with no line from the hub: placed on the first ring beside it
        un = [k for k in keys if k not in depth]
        k0 = next((k for k in un if not any(p in un for p in par[k])), un[0])
        depth[k0] = 1
        unreached.add(k0)
        relax()
    tp = {}
    for k in keys:
        if k == hub:
            continue
        ps = [p for p in par[k] if p in depth and depth[p] < depth[k]]
        tp[k] = max(ps, key=lambda p: (depth[p], idx[p])) if ps and k not in unreached else hub
    kids = {k: [] for k in keys}
    for k in sorted(tp, key=idx.get):
        kids[tp[k]].append(k)
    virt = {}
    for v, m in spokes.items():
        for j in range(m):
            node = ("spoke", v, j)
            kids.setdefault(v, []).append(node)
            virt[node] = v
    nsub = {}

    def leaves(k):
        if k not in nsub:
            cs = kids.get(k, [])
            nsub[k] = 1 if not cs else sum(leaves(c) for c in cs)
        return nsub[k]

    # the hub's children: spokes spread evenly among the core branches; a branch's share grows with its size
    real = [c for c in kids[hub] if c not in virt]
    sp = [c for c in kids[hub] if c in virt]
    seq = list(real)
    for j, s_ in enumerate(sp):
        seq.insert(round((j + 0.5) * len(real) / max(1, len(sp))) + j, s_)
    share = {c: (2.0 if c in virt else 1.0 + 0.5 * min(3, leaves(c) - 1)) for c in seq}
    tot = sum(share.values()) or 1.0

    def angles(rot):
        out, a = {}, rot
        for c in seq:
            out[c] = a + math.pi * share[c] / tot
            a += 2 * math.pi * share[c] / tot
        return out

    if hub_angles and len(hub_angles) == len(sp):
        # fixed spoke slots; the core's branches fill the arcs between them (half a share of margin each side)
        ang = {c: a for c, a in zip(sp, hub_angles)}
        fa = sorted(a % (2 * math.pi) for a in hub_angles)
        rs_ = [c for c in seq if c not in virt]
        tot_r = sum(share[c] for c in rs_) or 1.0
        unit = 2 * math.pi / (tot_r + 2.0 * len(fa))
        arcs = [(fa[i] + unit, (fa[(i + 1) % len(fa)] + (2 * math.pi if i + 1 == len(fa) else 0.0)) - unit)
                for i in range(len(fa))]
        free = sum(max(0.0, b - a) for a, b in arcs) or 1.0
        acc = 0.0
        for c in rs_:
            t = (acc + share[c] / 2) / tot_r * free  # distance along the free arcs
            acc += share[c]
            for a, b in arcs:
                L_ = max(0.0, b - a)
                if t <= L_ + 1e-9:
                    ang[c] = a + t
                    break
                t -= L_
            else:
                ang[c] = arcs[-1][1]
        seq = rs_ + sp
    else:
        rot = 0.0
        if sp:  # spokes sideways (pages are wider than tall) and away from straight up (the core's header)
            rot = min((sum(abs(math.sin(angles(2 * math.pi * r / 36)[s_])) for s_ in sp), r) for r in range(36))[1]
            rot = 2 * math.pi * rot / 36
        ang = angles(rot)
    n1 = len(real)
    ring1 = max(2.5, n1 * 2.1 / (2 * math.pi))
    stagger = ring1 > 3.75
    if stagger:
        ring1 = max(2.75, n1 * 1.15 / (2 * math.pi))
    ring1 *= scale
    pos = {hub: (0.0, 0.0, _size(byk[hub]))}
    segs = []
    out_ang = {}

    def ok(k, p, parent):
        s = _size(byk[k])
        for j, (x, y, js) in pos.items():
            if math.hypot(x - p[0], y - p[1]) < max(MIN_SEP, (s + js) / 2 + 0.5) + 0.25:
                return False
        for d in [parent]:  # the tree line must be clean (other lines into k may be hidden later, if messy)
            pp = pos[d][:2]
            for j, (x, y, js) in pos.items():
                if j != d and _seg_dist(pp, p, (x, y)) < 0.55 + (js - 1) / 2:
                    return False
            for a, b, ka, kb in segs:
                if d not in (ka, kb) and _cross((a, b), (pp, p)):
                    return False
        for a, b, ka, kb in segs:
            if _seg_dist(a, b, p) < 0.55 + (s - 1) / 2:
                return False
        return True

    tries = sorted(((st, da) for st in range(24) for da in (0.0, 0.12, -0.12, 0.25, -0.25, 0.4, -0.4)),
                   key=lambda t: (t[0] + 8 * abs(t[1]), abs(t[1])))

    def put(k, a, r0, parent):
        for st, da in tries:
            r = r0 + 0.5 * st
            p = (round(r * math.cos(a + da) * 2) / 2, round(r * math.sin(a + da) * 2) / 2)
            if ok(k, p, parent):
                pos[k] = (p[0], p[1], _size(byk[k]))
                for d in dict.fromkeys([parent] + [d for d in par[k] if d in pos and d != k]):
                    segs.append((pos[d][:2], p, d, k))
                ang[k] = a + da
                return r
        return None

    radius = {hub: 0.0}
    alt = 0
    for c in sorted(seq, key=lambda c: ang[c] % (2 * math.pi)):
        if c in virt:
            continue
        r0 = ring1 + (1.75 if stagger and alt % 2 else 0.0)
        alt += 1
        r = put(c, ang[c], r0, hub)
        if r is None:
            return None
        radius[c] = r
    for c in seq:
        if c in virt:
            out_ang[(virt[c], c[2])] = ang[c]
    # deeper levels: around the parent's angle, one ring further out
    frontier = [c for c in seq if c not in virt]
    while frontier:
        nxt = []
        for v in sorted(frontier, key=lambda v: ang[v] % (2 * math.pi)):
            cs = kids.get(v, [])
            if not cs:
                continue
            r0 = radius[v] + 2.25 * scale
            step = 2.1 / r0
            for j, c in enumerate(cs):
                a = ang[v] + (j - (len(cs) - 1) / 2) * step
                ang[c] = a
                if c in virt:
                    out_ang[(virt[c], c[2])] = a
                    continue
                r = put(c, a, r0, v)
                if r is None:
                    return None
                radius[c] = r
                nxt.append(c)
        frontier = nxt
    tree_edges = [(tp[k], k) for k in tp]
    if len(pos) != len(keys) or not _clean(pos, byk, tree_edges):
        return None
    return pos, out_ang


COMPASS = (0.0, math.pi, math.pi / 2, -math.pi / 2, math.pi / 4, 3 * math.pi / 4, -math.pi / 4, -3 * math.pi / 4,
           math.pi / 8, 7 * math.pi / 8, 3 * math.pi / 8, 5 * math.pi / 8, -math.pi / 8, -7 * math.pi / 8,
           -3 * math.pi / 8, -5 * math.pi / 8)  # spoke slots, best first: sideways, down, up, then the diagonals


def _radial_page(secs, byk, idx, mk, header, gx, hub_min=4):
    """The radial motif. Returns (P, blocks, heads)."""
    sec_of = {k: i for i, s in enumerate(secs) for k in s["members"]}
    nk = {}
    for k in byk:
        for d in dict.fromkeys(byk[k].deps):
            if d in byk and d != k:
                nk[d] = nk.get(d, 0) + 1
    hub = max(byk, key=lambda k: (nk.get(k, 0), -idx[k]))
    real_hub = nk.get(hub, 0) >= hub_min
    ci = sec_of[hub] if real_hub else 0
    # each other section follows the section its root hangs from (the core: a spoke from that core quest)
    parent = {}
    for i, s in enumerate(secs):
        if i == ci:
            continue
        ds = [d for d in byk[s["root"]].deps if d in sec_of and sec_of[d] != i]
        if not ds:
            ds = [d for m in s["members"] for d in byk[m].deps if d in sec_of and sec_of[d] != i]
        parent[i] = ds[0] if ds else None
    core_hub = hub if real_hub else secs[ci]["root"]
    hub_sp = [i for i in parent if parent[i] is None or (parent[i] == core_hub)]
    side_sp = {}  # spokes from other core quests
    for i, p in parent.items():
        if i not in hub_sp and sec_of[p] == ci:
            side_sp.setdefault(p, []).append(i)
    # compass slots for the hub's spokes: the biggest sections sideways
    rank = sorted(hub_sp, key=lambda i: (-len(secs[i]["members"]), i))
    slot = {i: COMPASS[n % len(COMPASS)] for n, i in enumerate(rank)}
    hub_list = sorted(hub_sp, key=lambda i: slot[i] % (2 * math.pi))
    P, heads, blocks, angles = {}, [], {}, {}
    core_pos = None
    if real_hub:
        core = dict(secs[ci], hub=hub)
        sp_n = {hub: len(hub_list), **{p: len(l) for p, l in side_sp.items()}}
        for scale in (1.0, 1.2, 1.4):
            got = _radial_core(core, byk, idx, sp_n, scale, hub_angles=[slot[i] for i in hub_list])
            if got:
                core_pos, a = got
                for j, i in enumerate(hub_list):
                    angles[i] = a[(hub, j)]
                for p, l in side_sp.items():
                    for j, i in enumerate(l):
                        angles[i] = a[(p, j)]
                break
    if core_pos is not None:
        cb = _with_header(dict(secs[ci]), core_pos, byk, header, "corner", "down")
        hx, hy, _ = cb["pos"][hub]
        _place_block(cb, -hx, -hy, P, heads, ci)
    else:
        cb = mk(ci, "down", "top")
        _place_block(cb, -cb["w"] / 2, -cb["h"] / 2, P, heads, ci)
        for i in parent:
            if i in hub_sp or i in sum(side_sp.values(), []):
                angles[i] = slot.get(i, 0.0)
    blocks[ci] = cb
    fixed = [(x - s / 2, y - s / 2, x + s / 2, y + s / 2) for x, y, s in P.values()] + [h[1:] for h in heads]
    todo = sorted(angles, key=lambda i: (len(secs[i]["members"]) < 4, angles[i]))
    rest = [i for i in parent if i not in angles]
    for _ in range(len(secs)):  # followers: a section hanging from a spoke section goes on out beyond it
        for i in list(rest):
            p = parent[i]
            if p is not None and sec_of[p] in angles:
                angles[i] = angles[sec_of[p]]
                todo.append(i)
                rest.remove(i)
    for i in rest:
        angles[i] = 0.0
        todo.append(i)
    for i in todo:
        a = angles[i]
        c, s_ = math.cos(a), math.sin(a)
        orient = "right" if c >= 0.7 else "left" if c <= -0.7 else ("down" if s_ > 0 else "up")
        b = mk(i, orient, "bottom" if orient == "down" else "top")
        p = parent.get(i)
        src = P[p][:2] if p is not None and p in P else (0.0, 0.0)
        rects = fixed + [bb["box"] for j, bb in blocks.items() if j != ci and "box" in bb]
        follower = p is not None and sec_of[p] != ci
        best = None
        for da in ((0.0, math.pi / 4, -math.pi / 4, math.pi / 2, -math.pi / 2) if follower else (0.0,)):
            c, s_ = math.cos(a + da), math.sin(a + da)
            orient = "right" if c >= 0.7 else "left" if c <= -0.7 else ("down" if s_ > 0 else "up")
            b = mk(i, orient, "bottom" if orient == "down" else "top")
            rx, ry, rs = b["pos"][b["root"]]
            t = 1.5
            while True:
                px, py = src[0] + t * c, src[1] + t * s_
                box = (px - rx, py - ry, px - rx + b["w"], py - ry + b["h"])
                if not any(_rects_hit(box, r_, gx * 0.75) for r_ in rects) or t > 80:
                    break
                t += 0.5
            # nearest spot; a follower also stays inside the page so far (no growing the page for it)
            allb = rects + [box]
            grow = (max(r_[2] for r_ in allb) - min(r_[0] for r_ in allb)) + (max(r_[3] for r_ in allb) - min(r_[1] for r_ in allb))
            sc = t + 0.5 * grow + abs(da)
            if best is None or sc < best[0]:
                best = (sc, b, box)
        _, b, box = best
        _place_block(b, round(box[0] * 2) / 2, round(box[1] * 2) / 2, P, heads, i)
        blocks[i] = b
    return P, blocks, heads


def page_sections(chapter, style=None):
    """The sections apply() would draw on this chapter, as [{"title", "members" (keys, declaration order), "root",
    "explicit" (title from Q(section=...))}] in reading order. tools/quest_data.py uses it to split a mod page into
    one chapter per section (the "Mod = category" sidebar)."""
    style = style or getattr(chapter, "style", None) or DEFAULT_STYLE
    base = MOTIF_BASE[style]
    byk, idx, parents, children, order = _graph(chapter.quests)
    G = {"byk": byk, "idx": idx, "parents": parents, "children": children, "order": order,
         "opt": {k: bool(byk[k].optional) for k in byk}}
    spine = _spine(set(byk), G)
    secs = _sections(chapter, G, spine, base if base == "spine" else style if style in ("grid", "radial") else "tree",
                     getattr(chapter, "home_of", None) or {}, getattr(chapter, "chapter_titles", None) or {})
    named = {_plain(q.section) for q in chapter.quests if getattr(q, "section", None)}
    for s in secs:
        s["explicit"] = s["title"] in named
    return secs


def apply(chapter, book_keys=None, style=None):
    """Place every quest of an auto-layout chapter, its quest links and its section headers, and set q.hide_lines.
    chapter.sections becomes [{"title", "slug", "x", "y", "w", "h", "members"}] (header centre and size, in cells).
    book_keys = all quest keys in the book (to add entry links). Optional chapter attributes: style ("spine", "tree"
    or "grid", from STYLES in quest_data.py), home_of (quest key -> chapter key) and chapter_titles (chapter key
    -> title), used to name loose groups. Quests in other chapters are never moved."""
    chapter.pruned_deps = getattr(chapter, "pruned_deps", 0) + prune_transitive(chapter.quests)
    chapter.sections = []
    for q in chapter.quests:
        q.hide_lines = q.hide_dependents = False
    if getattr(chapter, "layout", "auto") == "manual" or not chapter.quests:
        return
    style = style or getattr(chapter, "style", None) or DEFAULT_STYLE
    if style not in MOTIF_BASE:
        raise ValueError(f"chapter {chapter.key}: unknown layout style {style!r} ({', '.join(MOTIF_BASE)})")
    chapter.style = style
    base = MOTIF_BASE[style]  # how sections are found and lines hidden: spine (spine, winding) or tree
    quests = chapter.quests
    byk, idx, parents, children, order = _graph(quests)
    G = {"byk": byk, "idx": idx, "parents": parents, "children": children, "order": order,
         "opt": {k: bool(byk[k].optional) for k in byk}}
    spine = _spine(set(byk), G)
    secs = _sections(chapter, G, spine, base if base == "spine" else style if style in ("grid", "radial") else "tree",
                     getattr(chapter, "home_of", None) or {}, getattr(chapter, "chapter_titles", None) or {})
    # Section headers: only where a page has 2+ sections, and never on a chapter split from a mod page (its title
    # in the sidebar names it; chapter.headers = False, set by tools/quest_data.py).
    header = len(secs) + (1 if base == "spine" else 0) > 1 and getattr(chapter, "headers", True)

    # Quest links: the chapter's own plus the entry quest's deps in other chapters.
    links = [lk for lk, _, _ in chapter.links]
    if book_keys is not None:
        for d in byk[spine[0]].deps:
            if d not in byk and d in book_keys and d not in links:
                links.append(d)
    sec_of = {k: i for i, s in enumerate(secs) for k in s["members"]}
    spine_set = set(spine) if base == "spine" else set()
    # A quest whose dependents here are all in ONE section that isn't its own or next to it in reading order gets
    # a quest link inside that section. FTB draws a dependency line from the LAST button of that quest on the page
    # (quest links are added after quests), so its lines then start at the link: short lines, no long fan.
    where = lambda k: "spine" if k in spine_set else sec_of[k]
    shared = getattr(chapter, "shared_quests", None) or set()  # shown as links elsewhere: no hide flags on these
    for d in order:
        ds = {where(c) for c in children[d]}
        if len(ds) == 1 and d not in links and d not in shared:
            t, f = next(iter(ds)), where(d)
            if t != "spine" and f != "spine" and abs(t - f) > 1:
                links.append(d)
    dependents = {lk: [q.key for q in quests if lk in q.deps] for lk in links}
    lsec = {}
    for lk in links:
        votes = {}
        for d in dependents[lk]:
            v = "spine" if d in spine_set else sec_of[d]
            votes[v] = votes.get(v, 0) + 1
        if votes:
            top = max(votes.values())
            lsec[lk] = next(v for v in ["spine"] + list(range(len(secs))) if votes.get(v) == top)
    blinks = [{lk: [d for d in dependents[lk] if sec_of.get(d) == i] for lk in links if lsec.get(lk) == i}
              for i in range(len(secs))]
    motif = style in ("winding", "radial", "molecule")
    if motif:
        kind = getattr(chapter, "block_kind", None) or ("molecule" if style == "molecule" else "tree")
        cache = {}

        def mk(i, orient, head):
            if (i, orient, head) not in cache:
                cache[(i, orient, head)] = _shaped_block(secs[i], byk, idx, blinks[i], orient, header, head, kind)
            return dict(cache[(i, orient, head)])
    else:
        blocks = [_block(s, byk, blinks[i], style, header) for i, s in enumerate(secs)]

    P = {}       # node -> (x, y, size) on the page
    heads = []   # (section index, x0, y0, x1, y1)

    def put(i, ox, oy):
        b = blocks[i]
        b["box"] = (ox, oy, ox + b["w"], oy + b["h"])
        P.update({n: (x + ox, y + oy, s) for n, (x, y, s) in b["pos"].items()})
        if b["head"]:
            hx0, hy0, hx1, hy1 = b["head"]
            heads.append((i, hx0 + ox, hy0 + oy, hx1 + ox, hy1 + oy))

    gx, gy = GAP[base]
    if style == "winding":
        P, bl, heads = _wind_page(spine, secs, byk, mk, gx)
        blocks = [bl[i] for i in range(len(secs))]
    elif style == "radial":
        P, bl, heads = _radial_page(secs, byk, idx, mk, header, gx)
        blocks = [bl[i] for i in range(len(secs))]
    elif style == "molecule":
        blocks = [mk(i, "down", "top") for i in range(len(secs))]
        for i, (ox, oy) in _pack_columns(blocks, "tree").items():
            put(i, ox, oy)
    elif style == "spine":
        # The spine runs left to right at the normal column pitch. Every block wants to sit where its lines to the
        # spine are short: right after the earliest spine quest it depends on, or (a block that only feeds the
        # spine) just left of the earliest spine quest that needs it. Blocks go into the lane above or below the
        # spine, whichever needs the smaller push to the right; nothing overlaps.
        sidx = {k: i for i, k in enumerate(spine)}
        for k in spine:
            P[k] = (sidx[k] * COL, 0.0, _size(byk[k]))
        want = {}
        for i, s in enumerate(secs):
            b, mem = blocks[i], set(s["members"])
            rx = b["pos"][b["root"]][0]
            after = [sidx[d] for m in mem for d in byk[m].deps if d in sidx]
            before = [sidx[c] for c in spine if any(d in mem for d in byk[c].deps)]
            if after:
                want[i] = min(after) * COL + COL - rx
            elif before:
                want[i] = min(before) * COL - COL / 2 - b["w"]
        free, last = {-1: -1e9, 1: -1e9}, 1
        for i in sorted(want, key=lambda i: (want[i], i)):
            b = blocks[i]
            side = min((-1, 1), key=lambda sd: (max(free[sd], want[i]) - want[i], sd == last))
            left = max(free[side], want[i])
            put(i, left, SPINE_Y if side == 1 else -SPINE_Y - b["h"])
            free[side], last = left + b["w"] + gx, side
        # Blocks with no line to the spine but lines to placed blocks: an outer lane on the side where their
        # partners are, centred under / over them.
        lane = {-1: min([y - s / 2 for _, y, s in P.values()] + [0.0]), 1: max([y + s / 2 for _, y, s in P.values()] + [0.0])}
        free2 = {-1: -1e9, 1: -1e9}
        outer = []
        for i, s in enumerate(secs):
            if i in want:
                continue
            mem = set(s["members"])
            mates = [P[k] for k in P if isinstance(k, str) and k not in mem
                     and (any(k in byk[m].deps for m in mem) or any(m in byk[k].deps for m in mem))]
            if mates:
                b = blocks[i]
                side = 1 if sum(y for _, y, _ in mates) >= 0 else -1
                x = max(free2[side], sum(x for x, _, _ in mates) / len(mates) - b["w"] / 2)
                outer.append((i, side, x))
                free2[side] = x + b["w"] + gx
        for i, side, x in outer:
            b = blocks[i]
            put(i, x, lane[1] + gy + 0.5 if side == 1 else lane[-1] - gy - 0.5 - b["h"])
        placed = set(want) | {i for i, _, _ in outer}
        rest = [i for i in range(len(secs)) if i not in placed]
        if rest:  # sections with no line to the spine: shelves under everything else
            left0 = min(x - s / 2 for x, _, s in P.values())
            y = max(yy + s / 2 for _, yy, s in P.values()) + gy + 0.5
            width = max(max(xx for xx, _, _ in P.values()) - left0, PAGE_W)
            cx, shelf = 0.0, 0.0
            for i in rest:
                b = blocks[i]
                if cx > 0 and cx + b["w"] > width:
                    cx, y, shelf = 0.0, y + shelf + gy, 0.0
                put(i, left0 + cx, y)
                cx, shelf = cx + b["w"] + gx, max(shelf, b["h"])
    else:
        for i, (ox, oy) in _pack_columns(blocks, style).items():
            put(i, ox, oy)

    # Links not inside a block: beside their leftmost dependent; links nothing here depends on: a row on top.
    taken = list(P.values())
    for _, a, b, c, d in heads:  # header strips count as taken, sampled every 0.75 cells
        taken += [(a + 0.375 + 0.75 * m, (b + d) / 2, 0.75) for m in range(int((c - a) / 0.75) + 1)]
    for lk in links:
        node = ("link", lk)
        if node in P or not dependents[lk]:
            continue
        d = min(dependents[lk], key=lambda d: (P[d][0], idx[d]))
        if style == "spine" and d in spine_set:
            px, py = _free_spot(P[d][0] - COL, P[d][1], taken, lo_x=P[d][0] - COL)
        elif style == "winding" and d in spine_set:  # upstream of the spine quest (rows alternate direction)
            i = spine.index(d)
            nb = spine[i + 1] if i == 0 and len(spine) > 1 else (spine[i - 1] if i > 0 else None)
            ux, uy = (-1.0, 0.0)
            if nb is not None:
                vx, vy = P[nb][0] - P[d][0], P[nb][1] - P[d][1]
                L_ = math.hypot(vx, vy) or 1.0
                ux, uy = ((-vx / L_, -vy / L_) if i == 0 else (vx / L_, vy / L_))
                ux, uy = (ux, uy) if i == 0 else (-uy, ux)  # mid-spine: beside the line, not on it
            px, py = _free_spot(P[d][0] + COL * ux, P[d][1] + COL * uy, taken)
        else:
            px, py = _free_spot(P[d][0] - 1.0, P[d][1] - 1.5, taken)
        P[node] = (px, py, 1.0)
        taken.append(P[node])
    loose = [lk for lk in links if not dependents[lk]]
    # A loose link whose quest needs another link placed here: FTB draws a line between the two links, so it sits
    # right under that link (a short line) instead of in the block above the page.
    book = getattr(chapter, "book_quests", None) or {}
    moved = True
    while moved:
        moved = False
        for lk in list(loose):
            ds = [("link", d) for d in (book[lk].deps if lk in book else []) if ("link", d) in P]
            if ds:
                dx, dy, _ = P[ds[0]]
                P[("link", lk)] = _free_spot(dx, dy + 1.5, taken) + (1.0,)
                taken.append(P[("link", lk)])
                loose.remove(lk)
                moved = True
    if loose:  # links nothing here depends on: their own small drawing above the page, in dependency order
        top = min([y - s / 2 for _, y, s in P.values()] + [b for _, _, b, _, _ in heads])
        left = min([x - s / 2 for x, _, s in P.values()] + [a for _, a, _, _, _ in heads])
        right = max([x + s / 2 for x, _, s in P.values()] + [c for _, _, _, c, _ in heads])
        pts = _link_block(loose, getattr(chapter, "book_quests", None) or {}, base != "spine", max(right - left, 8.0))
        h = max(y + 0.5 for x, y in pts.values())
        for lk, (x, y) in pts.items():
            P[("link", lk)] = (left + x, top - 1.0 - h + y, 1.0)

    snap = lambda v: round(v * 2) / 2 + 0.0
    for q in quests:
        q.x, q.y = snap(P[q.key][0]), snap(P[q.key][1])
    chapter.links = [(lk, snap(P[("link", lk)][0]), snap(P[("link", lk)][1])) for lk in links]
    for i, a, b, c, d in heads:
        s = secs[i]
        chapter.sections.append({"title": s["title"], "slug": slug(s["title"]), "x": (a + c) / 2, "y": (b + d) / 2,
                                 "w": c - a, "h": d - b, "members": list(s["members"]), "box": blocks[i]["box"]})
    _hide_lines(chapter, style, spine, blocks, sec_of, spine_set)
    for reach in (3.0, 3.0, 8.0):  # lines still through quests: small moves (then wider), then hide lines again
        if reach > 3.0 and not metrics(chapter)["thru"]:
            break
        if not _nudge(chapter, spine_set, reach) and reach <= 3.0:
            continue
        for q in quests:
            q.hide_lines = q.hide_dependents = False
        _hide_lines(chapter, style, spine, blocks, sec_of, spine_set)


def _lines(chapter):
    """Every dependency line FTB 2101 draws on this page: [(source node, target node, hidden)].
    Nodes are quest keys or ("link", key). As in QuestPanel: every quest button AND every quest-link button draws a
    line to each of its quest's dependencies, and a dependency resolves to the LAST button showing that quest (links
    are added after quests, so a link wins). Hidden: hide_dependency_lines on the drawing quest, or
    hide_dependent_lines on the dependency's quest. A link's quest from another chapter is looked up in
    chapter.book_quests (key -> Q, all chapters)."""
    book = getattr(chapter, "book_quests", None) or {}
    byk = {q.key: q for q in chapter.quests}
    quest = lambda k: byk.get(k) or book.get(k)
    btn = {k: k for k in byk}
    btn.update({lk: ("link", lk) for lk, _, _ in chapter.links})
    owners = [(q.key, q) for q in chapter.quests] + [(("link", lk), quest(lk)) for lk, _, _ in chapter.links]
    out = []
    for node, q in owners:
        if q is None:
            continue
        for d in dict.fromkeys(q.deps):
            if d == q.key or d not in btn:
                continue
            dq = quest(d)
            out.append((btn[d], node, bool(getattr(q, "hide_lines", False) or getattr(dq, "hide_dependents", False))))
    return out


def _drawn(chapter):
    """The lines FTB draws here (not hidden): [(source node, target node)]."""
    return [(a, b) for a, b, h in _lines(chapter) if not h]


def _nudge(chapter, fixed, reach=3.0):
    """Last pass: a drawn line that still runs through a quest moves the quest in the way (or the line's end) by
    up to reach cells, keeping MIN_SEP to everything and clear of section headers, when that lowers the number of
    lines through quests. Returns the number of moves."""
    byk = {q.key: q for q in chapter.quests}
    P = {q.key: [float(q.x), float(q.y), _size(q)] for q in chapter.quests}
    P.update({("link", lk): [float(x), float(y), 1.0] for lk, x, y in chapter.links})
    heads = [(h["x"] - h["w"] / 2, h["y"] - h["h"] / 2, h["x"] + h["w"] / 2, h["y"] + h["h"] / 2) for h in chapter.sections]
    edges = _drawn(chapter)
    inc = {}
    for e in edges:
        for n in e:
            inc.setdefault(n, []).append(e)

    def hits(e, k):
        a, b = e
        if k in (a, b) or (isinstance(a, tuple) and a[1] == k):
            return False
        return _seg_dist(P[a][:2], P[b][:2], P[k][:2]) < 0.45 + (P[k][2] - 1) / 2

    def local(k):
        """Lines-through incidents that involve node k (as the quest in the way or as a line end)."""
        n = sum(1 for e in edges if hits(e, k))
        for e in inc.get(k, []):
            n += sum(1 for j in P if hits(e, j))
        return n

    def free(k, x, y):
        s = P[k][2]
        for j, (jx, jy, js) in P.items():
            if j != k and math.hypot(jx - x, jy - y) < max(MIN_SEP, (s + js) / 2 + 0.5) - 1e-9:
                return False
        return all(not (x0 - s / 2 < x < x1 + s / 2 and y0 - s / 2 < y < y1 + s / 2) for x0, y0, x1, y1 in heads)

    moves = 0
    r2 = int(reach * 2)
    steps = sorted({(dx * 0.5, dy * 0.5) for dx in range(-r2, r2 + 1) for dy in range(-r2, r2 + 1)} - {(0.0, 0.0)},
                   key=lambda d: (abs(d[0]) + abs(d[1]), d))
    for _ in range(3):
        bad = [(e, k) for e in edges for k in P if hits(e, k)]
        if not bad:
            break
        for e, k in bad:
            if not hits(e, k):
                continue
            for m in (k, e[1], e[0]):
                if m in fixed or m not in P:
                    continue
                x0, y0 = P[m][0], P[m][1]
                before = local(m)
                done = False
                for dx, dy in steps:
                    x, y = x0 + dx, y0 + dy
                    if not free(m, x, y):
                        continue
                    P[m][0], P[m][1] = x, y
                    if local(m) < before:
                        done = True
                        break
                    P[m][0], P[m][1] = x0, y0
                if done:
                    moves += 1
                    break
    for q in chapter.quests:
        q.x, q.y = P[q.key][0], P[q.key][1]
    chapter.links = [(lk, P[("link", lk)][0], P[("link", lk)][1]) for lk, _, _ in chapter.links]
    return moves


def _hide_lines(chapter, style, spine, blocks, sec_of, spine_set):
    """Set q.hide_lines (FTB hide_dependency_lines) where a line is clutter and the dependency stays readable.
    Clutter: a dependency is a hub (HUB[style] or more dependents here), or a line runs between two sections and
    is long (> MAX_EDGE), runs through a quest or crosses a section header (on every page but "spine", a line
    crossing two or more others too). Readable: every dependency here is in the quest's own section, a neighbouring
    one (next or previous in order, or touching), the spine (spine style), or shown as a quest link; on every page
    but "spine" any line between two sections is readable (sections sit by shape, not reading order). A radial
    page's hub never gets hide_dependents (its spokes stay drawn). A spine step (spine quest N -> N+1) is never hidden, except in tree/grid style
    when it jumps from one section to the next. Lines into a quest that must keep one of its lines are hidden
    from the other end instead (hide_dependents, FTB hide_dependent_lines on the dependency)."""
    qs = chapter.quests
    pos = {q.key: (float(q.x), float(q.y)) for q in qs}
    size = {q.key: _size(q) for q in qs}
    lpos = {lk: (float(x), float(y)) for lk, x, y in chapter.links}
    src = lambda d: lpos.get(d, pos.get(d))  # a quest link here (even of a quest on this page) is where lines start
    nkids = {}
    for q in qs:
        for d in dict.fromkeys(q.deps):
            if d in pos:
                nkids[d] = nkids.get(d, 0) + 1
    sp_next = dict(zip(spine, spine[1:]))
    heads = [(s["x"] - s["w"] / 2, s["y"] - s["h"] / 2, s["x"] + s["w"] / 2, s["y"] + s["h"] / 2) for s in chapter.sections]
    sec = lambda k: "spine" if k in spine_set else sec_of.get(k)
    boxes = {i: b.get("box") for i, b in enumerate(blocks)}

    def near(a, b):
        if a == b or "spine" in (a, b):
            return True
        if a is None or b is None:
            return False
        if abs(a - b) <= NEAR_ORDER:
            return True
        A, B = boxes.get(a), boxes.get(b)
        if not A or not B:
            return False
        return max(A[0] - B[2], B[0] - A[2], 0.0) <= NEAR_GAP and max(A[1] - B[3], B[1] - A[3], 0.0) <= NEAR_GAP

    def messy(p1, p2, a, b, long_counts=True):
        if long_counts and math.dist(p1, p2) > MAX_EDGE:
            return True
        for k, p in list(pos.items()) + [(("link", lk), p) for lk, p in lpos.items()]:
            if k not in (a, b) and _seg_dist(p1, p2, p) < 0.45 + (size.get(k, 1.0) - 1) / 2:
                return True
        for x0, y0, x1, y1 in heads:  # does the line cross a header strip? (sampled)
            for t in range(1, 20):
                x, y = p1[0] + (p2[0] - p1[0]) * t / 20, p1[1] + (p2[1] - p1[1]) * t / 20
                if x0 < x < x1 and y0 < y < y1:
                    return True
        return False

    # A chapter split from a mod page (no headers) is small: a hub's fan is short and IS the page, so it stays drawn
    # unless its line crosses another one; otherwise only messy lines (long, through a quest, crossing two others).
    small = not getattr(chapter, "headers", True)
    hub = 99 if small else HUB[style]
    relaxed = style != "spine"
    # A quest with a quest link on its own page: FTB draws its dependency lines at the link too (every button of
    # the quest draws them), so those would run to the far link. Its own lines are hidden (they show on hover).
    shared = getattr(chapter, "shared_quests", None) or set()
    for q in qs:
        if q.key in lpos and any(d in pos for d in q.deps):
            q.hide_lines = True
    # Every drawn line d -> q (d a quest here, or a quest link of d): clutter? readable without it? a spine step?
    E = {}
    for q in qs:
        for d in dict.fromkeys(q.deps):
            if d == q.key or (d not in pos and d not in lpos):
                continue
            p1 = src(d)
            if d in pos:  # through a quest or a header: always clutter; long: clutter between sections
                a_ = ("link", d) if d in lpos else d
                messy_ = messy(p1, pos[q.key], a_, q.key, long_counts=sec(d) != sec(q.key))
                ok = d in lpos or near(sec(d), sec(q.key))
                # a spine step stays drawn, except in tree/grid style where it jumps to the next section
                step = sp_next.get(d) == q.key and (MOTIF_BASE[style] == "spine" or sec(d) == sec(q.key))
            else:  # a quest from another chapter, shown by its link
                messy_, ok, step = messy(p1, pos[q.key], ("link", d), q.key), True, False
            if relaxed and d in pos and sec(d) != sec(q.key):
                ok = True  # motif pages: sections sit by shape, not in reading order; any line between them may go
            E[(d, q.key)] = {"clutter": messy_ or nkids.get(d, 0) >= hub, "ok": ok, "step": step, "seg": (p1, pos[q.key]),
                             "fan": nkids.get(d, 0) >= HUB[style]}
    if relaxed:  # a line crossing two or more others is clutter too (one other, for a hub's fan on a small chapter)
        segs = list(E.items())
        for i, (key_i, e) in enumerate(segs):
            n = 0
            for key_j, f in segs:
                if key_j != key_i and not ({*key_i} & {*key_j}) and _cross(e["seg"], f["seg"]):
                    n += 1
                    if n >= 2 or (small and e["fan"]):
                        e["clutter"] = True
                        break
    ins, outs = {}, {}
    for (d, k), e in E.items():
        ins.setdefault(k, []).append(e)
        outs.setdefault(d, []).append((k, e))
    # 1. hide_dependency_lines on a quest: one of its lines is clutter, all are readable, none is a spine step.
    for q in qs:
        if q.hide_lines:
            continue
        es = ins.get(q.key, [])
        if q.key not in shared and any(e["clutter"] for e in es) and all(e["ok"] and not e["step"] for e in es):
            q.hide_lines = True
    # 2. hide_dependent_lines on a dependency, for clutter lines still drawn (into a quest that keeps its other
    #    lines, e.g. a feeder into a spine quest): only if every line from it is readable and none is a spine step.
    shut = {q.key for q in qs if q.hide_lines}
    for q in qs:
        if style == "radial" and nkids.get(q.key, 0) >= 6:
            continue  # a radial page's hub keeps its spokes (their far ends hide their own lines instead)
        os_ = outs.get(q.key, [])
        left = [e for k, e in os_ if k not in shut]
        if q.key not in shared and any(e["clutter"] for e in left) and all(e["ok"] and not e["step"] for _, e in os_):
            q.hide_dependents = True


# --- banner (L12) -----------------------------------------------------------------------------
def banner(chapter, with_links=True):
    """Centre (x, y) of the 6 x 1 chapter banner: above the topmost quest, link or section header, left-aligned
    with the chapter. with_links=False gives the old rule (quests only)."""
    pts = [(q.x, q.y, _size(q)) for q in chapter.quests] + ([(x, y, 1.0) for _, x, y in chapter.links] if with_links else [])
    left = min(x - s / 2 for x, _, s in pts)
    top = min(y - s / 2 for _, y, s in pts)
    for h in getattr(chapter, "sections", None) or []:
        left, top = min(left, h["x"] - h["w"] / 2), min(top, h["y"] - h["h"] / 2)
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
    """Layout numbers for one chapter. Lines of quests with hide_lines (FTB hide_dependency_lines) are not drawn,
    so they don't count for crossings, lines through quests, long edges or directions."""
    qs = chapter.quests
    qpos = {q.key: (float(q.x), float(q.y)) for q in qs}
    size = {q.key: _size(q) for q in qs}
    hid = {q.key for q in qs if getattr(q, "hide_lines", False)}
    hid_out = {q.key for q in qs if getattr(q, "hide_dependents", False)}  # FTB hide_dependent_lines
    # FTB also draws a line from a quest link to each quest here that depends on the linked quest.
    # A link to a quest of this same chapter takes over that quest's lines (FTB uses the last button of a quest).
    lpos = {("link", lk): (float(x), float(y)) for lk, x, y in chapter.links}
    pos = {**qpos, **lpos}
    size.update({k: 1.0 for k in lpos})
    # Every button (quest or link) draws its quest's lines, from the last button of each dependency (_lines).
    allL = _lines(chapter)
    hidden_edges = sum(1 for _, _, h in allL if h)
    edges = [(a, b) for a, b, h in allL if not h]
    segs = [(pos[a], pos[b], a, b) for a, b in edges]
    crossings = sum(1 for i in range(len(segs)) for j in range(i + 1, len(segs)) if _cross(segs[i][:2], segs[j][:2]))
    thru = sum(1 for (p1, p2, a, b) in segs for k, p in pos.items()
               if k not in (a, b) and _seg_dist(p1, p2, p) < 0.45 + (size[k] - 1) / 2)
    long_ = sum(1 for (p1, p2, _, _) in segs if math.dist(p1, p2) > MAX_EDGE)
    left = sum(1 for (p1, p2, _, _) in segs if p2[0] < p1[0] - 1e-9 and abs(p2[0] - p1[0]) >= abs(p2[1] - p1[1]))
    right = sum(1 for (p1, p2, _, _) in segs if p2[0] - p1[0] > 1e-9 and abs(p2[0] - p1[0]) >= abs(p2[1] - p1[1]))
    down = sum(1 for (p1, p2, _, _) in segs if p2[1] - p1[1] > abs(p2[0] - p1[0]))
    up = len(segs) - right - down - left
    lens = sorted(math.dist(p1, p2) for p1, p2, _, _ in segs)
    heads = getattr(chapter, "sections", None) or []
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
    on_head = sum(1 for x, y, s in boxes for h in heads
                  if abs(x - h["x"]) < (h["w"] + s) / 2 - 0.05 and abs(y - h["y"]) < (h["h"] + s) / 2 - 0.05)
    xs = [b[0] - b[2] / 2 for b in boxes] + [b[0] + b[2] / 2 for b in boxes]
    ys = [b[1] - b[2] / 2 for b in boxes] + [b[1] + b[2] / 2 for b in boxes]
    xs += [h["x"] - h["w"] / 2 for h in heads] + [h["x"] + h["w"] / 2 for h in heads]
    ys += [h["y"] - h["h"] / 2 for h in heads] + [h["y"] + h["h"] / 2 for h in heads]
    return {"n": len(qs), "w": max(xs) - min(xs), "h": max(ys) - min(ys), "cross": crossings, "thru": thru,
            "long": long_, "left": left, "right": right, "down": down, "up": up, "lines": len(segs),
            "median": lens[len(lens) // 2] if lens else 0.0, "hidden": len(hid | hid_out), "hidden_edges": hidden_edges,
            "sections": len(heads), "overlap": overlaps + on_banner + on_head, "close": close,
            "links": len(chapter.links)}


def report(chapters, apply_fn, before_fn=None):
    """Before/after table for every chapter (nothing is written). apply_fn(chapter) runs the layout; before_fn
    (default: the chapter's x/y as loaded) gives the "before" column, e.g. the v10 layout (apply_legacy)."""
    rows = []
    for c in chapters:
        if before_fn:
            before_fn(c)
        before = metrics(c, old_banner=before_fn is None)
        apply_fn(c)
        after = metrics(c)
        rows.append((c, before, after))
    rows.sort(key=lambda r: (getattr(r[0], "layout", "auto") == "manual", -r[2]["w"] * r[2]["h"], r[0].key))
    head = ("| chapter | style | n | sections | size WxH | crossings | lines thru quests | edges > 6 | "
            "hidden lines | overlaps | lines right/down/up/left % | median line |")
    out = [head, "|" + "---|" * 12]
    keys = ("cross", "thru", "long", "hidden_edges", "overlap", "sections", "lines", "right", "down", "up", "left")
    tot_b = {k: 0 for k in keys}
    tot_a = dict(tot_b)
    pct = lambda m: "/".join(str(round(100 * m[k] / m["lines"])) if m["lines"] else "0" for k in ("right", "down", "up", "left"))
    for c, b, a in rows:
        for k in keys:
            tot_b[k] += b[k]
            tot_a[k] += a[k]
        style = getattr(c, "style", "") if getattr(c, "layout", "auto") != "manual" else "manual"
        out.append(f"| {c.key} | {style} | {a['n']} | {a['sections']} | {b['w']:g}x{b['h']:g} -> {a['w']:g}x{a['h']:g} | "
                   f"{b['cross']}->{a['cross']} | {b['thru']}->{a['thru']} | {b['long']}->{a['long']} | "
                   f"{b['hidden_edges']}->{a['hidden_edges']} | {b['overlap']}->{a['overlap']} | {pct(b)} -> {pct(a)} | "
                   f"{b['median']:.1f}->{a['median']:.1f} |")
    auto = [r for r in rows if getattr(r[0], "layout", "auto") != "manual"]
    med = lambda v: sorted(v)[len(v) // 2] if v else 0
    out.append(f"| **total** | | {sum(r[2]['n'] for r in rows)} | {tot_a['sections']} | median "
               f"{med([r[1]['w'] for r in auto]):g}x{med([r[1]['h'] for r in auto]):g} -> "
               f"{med([r[2]['w'] for r in auto]):g}x{med([r[2]['h'] for r in auto]):g} | {tot_b['cross']}->{tot_a['cross']} | "
               f"{tot_b['thru']}->{tot_a['thru']} | {tot_b['long']}->{tot_a['long']} | {tot_b['hidden_edges']}->{tot_a['hidden_edges']} | "
               f"{tot_b['overlap']}->{tot_a['overlap']} | {pct(tot_b)} -> {pct(tot_a)} | "
               f"{med([r[1]['median'] for r in auto]):.1f}->{med([r[2]['median'] for r in auto]):.1f} |")
    big = [r[0].key for r in auto if r[2]["w"] > PAGE_W + 4 or r[2]["h"] > PAGE_H + 4]
    out += ["", "Size includes section headers and links. Crossings, lines through quests, edges and directions count "
            "only drawn lines (including the lines FTB draws from quest links); hidden lines show on mouse-over. "
            f"Redundant deps dropped (prune_transitive): {sum(getattr(c, 'pruned_deps', 0) for c in chapters)}.",
            f"Pages over {PAGE_W + 4:g} wide or {PAGE_H + 4:g} tall: {', '.join(big) or 'none'}."]
    return "\n".join(out)
