"""Quest book visual language: every quest's shape and size come from its ROLE, so the whole book reads alike.

build_quests.py calls apply(chapter) for every chapter BEFORE the automatic layout (tools/layout.py), because the
layout spaces quests by size. The Welcome chapter's "How to Read This Book" quests show one example of each role.

Roles, first match wins:
  role        shape     size  what it means
  capstone    gear      2.0   the chapter's big finish (writer set size >= 1.75)
  section     hexagon   1.5   a section milestone (writer set size 1.25 to 1.75)
  secret      diamond   0.75  secret=True: invisible until done, a hidden discovery
  optional    circle    0.85  optional=True: bonus, never blocks progress
  choice      octagon   1.0   any_dep=True: unlocks when ANY ONE of its lines is done (alternative routes)
  tip         pentagon  0.9   required, but only checkmark tasks: a tip or story beat, click to complete
  main        rsquare   1.0   on the chapter's main path (longest required chain; the layout's y = 0 spine)
  side        square    1.0   any other required step (a branch beside the main path)

Rules:
- Milestones are the only place a writer's own size counts, and only through the size (the two milestone styles are
  fixed; this does the same as layout.normalize_milestones, so it doesn't matter which runs first). Every other
  quest's shape and size are set by its role, whatever the chapter file says.
- Quests with `keep_style = True` (set after construction, see tools/quests/welcome.py) keep their shape and size:
  the legend's examples.
- Manual chapters (the token shop grids, layout="manual") are left alone, as are shop entries anywhere
  (repeat/locked_hidden).
- Sizes never cross 1.5 for non-milestones, so token and loot rewards (doubled for size >= 1.5) don't change.

Standalone check: python tools/quest_style.py   (role counts per chapter, nothing written)
"""
from collections import Counter

STYLE = {
    "capstone": ("gear", 2.0),
    "section": ("hexagon", 1.5),
    "secret": ("diamond", 0.75),
    "optional": ("circle", 0.85),
    "choice": ("octagon", 1.0),
    "tip": ("pentagon", 0.9),
    "main": ("rsquare", 1.0),
    "side": ("square", 1.0),
}
ROLES = list(STYLE)


def _is_tip(q):
    return bool(q.tasks) and all(t[0] == "checkmark" for t in q.tasks)


def _base_role(q):
    """Role from the quest's own fields (everything except main vs side, which needs the whole chapter)."""
    s = float(q.size or 1)
    if s >= 1.75:
        return "capstone"
    if s >= 1.25:
        return "section"
    if q.secret:
        return "secret"
    if q.optional:
        return "optional"
    if q.any_dep:
        return "choice"
    if _is_tip(q):
        return "tip"
    return None  # main or side


def _spine(quests):
    """The chapter's main path: the same longest required chain the layout puts on y = 0 (layout._spine), so the
    rounded squares are exactly the middle row. Falls back to our own longest-chain search if layout changes."""
    try:
        import layout
        byk, idx, parents, children, order = layout._graph(quests)
        G = {"byk": byk, "idx": idx, "parents": parents, "children": children, "order": order,
             "opt": {k: bool(byk[k].optional) for k in byk}}
        return set(layout._spine(set(byk), G))
    except Exception:  # noqa: BLE001  (private API of tools/layout.py; keep working if it moves)
        pass
    byk = {q.key: q for q in quests}
    idx = {q.key: i for i, q in enumerate(quests)}
    req = [q for q in quests if not q.optional]
    best = {}

    def chain(k, seen=()):
        if k in best:
            return best[k]
        q = byk[k]
        ps = [d for d in q.deps if d in byk and not byk[d].optional and d not in seen and d != k]
        if not ps:
            best[k] = ((1, float(q.size or 1), -idx[k]), None)
        else:
            p = max(ps, key=lambda p: (chain(p, seen + (k,))[0], -idx[p]))
            (n, s, st), _ = chain(p, seen + (k,))
            best[k] = ((n + 1, s + float(q.size or 1), st), p)
        return best[k]

    if not req:
        return set()
    end = max((q.key for q in req), key=lambda k: (chain(k)[0], -idx[k]))
    out = set()
    while end:
        out.add(end)
        end = best[end][1]
    return out


def roles(chapter):
    """{quest key: role} for one chapter (manual chapters and shop entries: None = left as written)."""
    manual = getattr(chapter, "layout", "auto") == "manual"
    out, pending = {}, []
    for q in chapter.quests:
        if manual or q.repeat or q.locked_hidden or getattr(q, "keep_style", False):
            out[q.key] = None
            continue
        r = _base_role(q)
        out[q.key] = r
        if r is None:
            pending.append(q)
    if pending:
        # Sizes first (tips shrink to 0.9), then the spine: the layout's spine tie-break looks at sizes too.
        for q in chapter.quests:
            r = out[q.key]
            if r is not None:
                q.size = STYLE[r][1]
        spine = _spine(chapter.quests)
        for q in pending:
            out[q.key] = "main" if q.key in spine else "side"
    return out


def apply(chapter):
    """Set every quest's shape and size from its role (see the module docstring). Returns Counter of roles."""
    count = Counter()
    rs = roles(chapter)
    for q in chapter.quests:
        r = rs[q.key]
        if r is None:
            count["kept"] += 1
            continue
        q.shape, q.size = STYLE[r]
        count[r] += 1
    return count


def legend_rows():
    """(role, shape, size) in display order, for the Welcome legend and docs."""
    return [(r, *STYLE[r]) for r in ROLES]


if __name__ == "__main__":
    import pathlib
    import sys
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    sys.stdout.reconfigure(encoding="utf-8")
    from quest_data import CHAPTERS
    total = Counter()
    cols = ROLES + ["kept"]
    print(f"{'chapter':16}" + "".join(f"{c:>9}" for c in cols))
    for c in CHAPTERS:
        n = apply(c)
        total.update(n)
        print(f"{c.key:16}" + "".join(f"{n.get(k, 0):9}" for k in cols))
    print(f"{'TOTAL':16}" + "".join(f"{total.get(k, 0):9}" for k in cols))
    print("shapes:", dict(Counter(q.shape for c in CHAPTERS for q in c.quests).most_common()))
