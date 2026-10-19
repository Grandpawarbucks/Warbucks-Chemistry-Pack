"""Automatic quest layout for the FTB Quests book (rules L1-L12 in docs/research/quest_layout_audit.md §4.2).

build_quests.py calls apply(chapter) for every chapter before writing it. Writers don't place x/y any more.
It is a Sugiyama-style layered drawing:
- Column = in-chapter dependency depth x 2, so every dependency line points right. Deps on quests in other
  chapters don't count (those quests are roots of this chapter). Quests then slide to the median column of
  their neighbours (inside the range their deps/dependents allow) to shorten lines.
- The required critical path (longest chain of non-optional quests, ties to bigger milestones) sits on y = 0.
- Inside each column, quests are ordered by the barycentre of their neighbours (12 sweeps, best kept), then
  given y values as close as possible to their neighbours' mean y, so sub-topics form rows beside the spine.
  Required quests keep 2.0 apart, optional ones 1.5, big milestones (size >= 1.5) more.
- Optional quests aim 1.5 cells off their parent's row (outward); they don't sit on the spine.
- Long lines get placeholder points in the columns they cross, so they get room and count as crossings.
- Groups of quests with no line to the spine's group are laid out the same way and packed below it in shelves.
- A last local search moves single quests up or down when that removes crossings or lines through quests.
- Quest links go in a link column at x = -2 (12 per column, then -4 ...), next to the rows that use them.
  The chapter's entry quest gets a link to each of its deps in other chapters automatically.
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


def _place(keys, G, spine):
    """Lay out one connected group of quests. Returns (column per key, y per key), spine on y = 0."""
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
    m = min(depth.values())
    depth = {k: d - m for k, d in depth.items()}

    # Layers with dummy points on long edges, so lines get room and count in the crossing reduction.
    layers, up, down, ends = {}, {}, {}, {}
    real = set(keys)
    for k in order:
        layers.setdefault(depth[k], []).append(k)
        up.setdefault(k, [])
        down.setdefault(k, [])
    for k in order:
        for p in parents[k]:
            prev, gap = p, depth[k] - depth[p]
            for j in range(1, gap):
                d = ("dummy", p, k, j)
                ends[d] = (p, k, j / gap)
                layers.setdefault(depth[p] + j, []).append(d)
                up[d], down[d] = [prev], []
                down[prev].append(d)
                prev = d
            down[prev].append(k)
            up[k].append(prev)
    L = max(layers) + 1
    for c in range(L):
        layers.setdefault(c, [])

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

    def sweep(c, nb):
        keyed = []
        for i, v in enumerate(layers[c]):
            ns = nb[v]
            keyed.append((sum(pos[n] for n in ns) / len(ns) if ns else i, i, v))
        keyed.sort(key=lambda t: (t[0], t[1]))
        layers[c] = [v for _, _, v in keyed]
        for i, v in enumerate(layers[c]):
            pos[v] = i

    renumber()
    best_order, best_x = {c: list(layers[c]) for c in range(L)}, crossings()
    for _ in range(12):
        if best_x == 0:
            break
        for c in range(1, L):
            sweep(c, up)
        for c in range(L - 2, -1, -1):
            sweep(c, down)
        x = crossings()
        if x < best_x:
            best_x, best_order = x, {c: list(layers[c]) for c in range(L)}
    layers = best_order

    # Coordinates: y close to the barycentre of the neighbours, spine pinned to y = 0, separations kept
    # (2.0 between required quests, 1.5 when one is optional, more around big milestones, less for lines).
    def sep(a, b):
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
    return depth, {k: Y[k] for k in keys}


def _repair(G, X, Y, fixed):
    """Local search on the final positions: move single quests up or down inside their column when that removes
    line crossings (weight 3) or lines running through quests (weight 1). Separations are kept."""
    byk, parents, opt = G["byk"], G["parents"], G["opt"]
    keys = list(G["order"])
    edges = [(p, k) for k in keys for p in parents[k]]
    inc = {k: [] for k in keys}
    for e in edges:
        inc[e[0]].append(e)
        inc[e[1]].append(e)
    col = {}
    for k in keys:
        col.setdefault(X[k], []).append(k)

    def seg(e):
        return (X[e[0]], Y[e[0]]), (X[e[1]], Y[e[1]])

    def thru(e, k):
        return k not in e and _seg_dist(*seg(e), (X[k], Y[k])) < 0.45 + (_size(byk[k]) - 1) / 2

    def local(k):
        """Crossings and line-through counts that involve quest k."""
        mine = inc[k]
        c = sum(1 for a in mine for b in edges if b not in mine and _cross(seg(a), seg(b)))
        t = sum(1 for e in edges if thru(e, k))
        t += sum(1 for a in mine for j in keys if thru(a, j))
        return 3 * c + t

    def ok(k, y):
        if opt[k] and y == 0 and any(j in fixed for j in col[X[k]]):
            return False
        for j in col[X[k]]:
            if j == k:
                continue
            need = ROW if not (opt[k] or opt[j]) else MIN_SEP
            need = max(need, (_size(byk[k]) + _size(byk[j])) / 2 + 0.5)
            if abs(Y[j] - y) < need:
                return False
        return True

    for _ in range(3):
        changed = False
        for k in keys:
            if k in fixed:
                continue
            here = local(k)
            if here == 0:
                continue
            y0, best = Y[k], (here, 0.0, Y[k])
            for step in range(1, 9):
                for y in (y0 - step * 0.5, y0 + step * 0.5):
                    if not ok(k, y):
                        continue
                    Y[k] = y
                    score = (local(k), abs(y - y0), y)
                    Y[k] = y0
                    if score < best:
                        best = score
            if best[2] != y0:
                Y[k] = best[2]
                changed = True
        if not changed:
            break


def apply(chapter, book_keys=None):
    """Place every quest of an auto-layout chapter and its quest links. book_keys = all quest keys in the book
    (used to add entry links); quests in other chapters are never moved."""
    if getattr(chapter, "layout", "auto") == "manual" or not chapter.quests:
        return
    quests = chapter.quests
    byk, idx, parents, children, order = _graph(quests)
    G = {"byk": byk, "idx": idx, "parents": parents, "children": children, "order": order,
         "opt": {k: bool(byk[k].optional) for k in byk}}

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
    blocks = []
    for i, ks in enumerate(comps):
        depth, Y = _place(ks, G, spine if i == main else _spine(ks, G))
        blocks.append((i, ks, depth, Y))
    X, Yall = {}, {}
    i, ks, depth, Y = blocks[main]
    for k in ks:
        X[k], Yall[k] = depth[k] * COL, Y[k]
    width = max(max(X.values()), 26.0)
    bottom = max(Yall[k] + _size(byk[k]) / 2 for k in ks)
    rest = sorted((b for b in blocks if b[0] != main), key=lambda b: (-len(b[1]), min(idx[k] for k in b[1])))
    cx, shelf_top, shelf_h = 0.0, None, 0.0
    for i, ks, depth, Y in rest:
        top = min(Y[k] - _size(byk[k]) / 2 for k in ks)
        h = max(Y[k] + _size(byk[k]) / 2 for k in ks) - top
        w = max(depth.values()) * COL
        if shelf_top is None or (cx > 0 and cx + w > width):  # new shelf
            shelf_top = (bottom if shelf_top is None else shelf_top + shelf_h) + 1.5
            cx, shelf_h = 0.0, 0.0
        dy = math.ceil((shelf_top - top) * 2) / 2
        for k in ks:
            X[k], Yall[k] = cx + depth[k] * COL, Y[k] + dy
        cx += w + (COL if len(ks) == 1 else 2 * COL)
        shelf_h = max(shelf_h, h + (dy - (shelf_top - top)))
    _repair(G, X, Yall, set(spine) | {k for k in byk if byk[k].row is not None})
    for q in quests:
        q.x, q.y = X[q.key], Yall[q.key] + 0.0

    # L8: links in a link column at x = -2 (wrapping to -4, -6 ... after LINK_ROWS), next to the rows they serve.
    # The entry quest's deps in other chapters get a link automatically.
    links = [lk for lk, _, _ in chapter.links]
    if book_keys is not None:
        for d in byk[spine[0]].deps:
            if d not in byk and d in book_keys and d not in links:
                links.append(d)
    dependents = {}
    for q in quests:
        for d in q.deps:
            dependents.setdefault(d, []).append(q.y)
    want = sorted(((sum(dependents[lk]) / len(dependents[lk]) if dependents.get(lk) else 0.0), i, lk)
                  for i, lk in enumerate(links))
    placed = []
    for start in range(0, len(want), LINK_ROWS):
        part = want[start:start + LINK_ROWS]
        x = LINK_X - COL * (start // LINK_ROWS)
        ys = _pava([w[0] for w in part], [1.0] * len(part), [MIN_SEP] * (len(part) - 1))
        ys = [round(y * 2) / 2 for y in ys]
        for j in range(1, len(ys)):
            ys[j] = max(ys[j], ys[j - 1] + MIN_SEP)
        placed += [(lk, x, y) for (_, _, lk), y in zip(part, ys)]
    chapter.links = placed


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
    pos = {q.key: (float(q.x), float(q.y)) for q in qs}
    size = {q.key: _size(q) for q in qs}
    edges = [(d, q.key) for q in qs for d in dict.fromkeys(q.deps) if d in pos and d != q.key]
    segs = [(pos[a], pos[b], a, b) for a, b in edges]
    crossings = sum(1 for i in range(len(segs)) for j in range(i + 1, len(segs)) if _cross(segs[i][:2], segs[j][:2]))
    thru = sum(1 for (p1, p2, a, b) in segs for k, p in pos.items()
               if k not in (a, b) and _seg_dist(p1, p2, p) < 0.45 + (size[k] - 1) / 2)
    long_ = sum(1 for (p1, p2, _, _) in segs if math.dist(p1, p2) > MAX_EDGE)
    left = sum(1 for (p1, p2, _, _) in segs if p2[0] <= p1[0])
    boxes = [(x, y, size[k]) for k, (x, y) in pos.items()] + [(float(x), float(y), 1.0) for _, x, y in chapter.links]
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
    return "\n".join(out)
