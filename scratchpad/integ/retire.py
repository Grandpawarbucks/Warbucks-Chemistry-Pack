"""Retire duplicate quests (keys kept) and re-point their dependents to the kept copy.

usage: python retire.py map.json      (map: {"retired_key": "kept_key", ...})
Edits tools/quests/*.py in place with AST spans (never renames a key).
"""
import ast, json, pathlib, re, sys, io, contextlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
QDIR = ROOT / "tools/quests"
sys.path.insert(0, str(ROOT / "tools"))
with contextlib.redirect_stdout(io.StringIO()):
    import quest_data as qd
QS = {q.key: q for c in qd.CHAPTERS for q in c.quests}
HOME = {q.key: c for c in qd.CHAPTERS for q in c.quests}
SHOPS = {"market", "shop_materials", "shop_gear", "shop_world"}


def ctitle(c):
    return c.title.split(". ", 1)[-1]


def calls_in(path):
    """[(key, node)] for every call whose first positional arg (or f-string prefix) names a quest key."""
    src = path.read_text(encoding="utf-8")
    tree = ast.parse(src)
    out = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and node.args and isinstance(node.args[0], ast.Constant) \
                and isinstance(node.args[0].value, str) and node.args[0].value in QS:
            out.append((node.args[0].value, node))
        elif isinstance(node, ast.Call) and node.args and isinstance(node.args[0], ast.Constant) \
                and isinstance(node.args[0].value, str) and isinstance(node.func, ast.Name) and node.func.id in ("buy", "g", "shop_entry"):
            for pre in ("sg_buy_", "sm_buy_", "sw_buy_", "mk_buy_"):
                if pre + node.args[0].value in QS:
                    out.append((pre + node.args[0].value, node))
    return src, out


def offs(src):
    starts, lines = [0], src.split("\n")
    for line in lines:
        starts.append(starts[-1] + len(line) + 1)
    # ast columns are UTF-8 byte offsets: convert to characters
    return lambda ln, col: starts[ln - 1] + len(lines[ln - 1].encode("utf-8")[:col].decode("utf-8"))


def kw_src(src, node, name, off):
    for k in node.keywords:
        if k.arg == name:
            return src[off(k.value.lineno, k.value.col_offset):off(k.value.end_lineno, k.value.end_col_offset)]
    return None


def first_item(q):
    if q.icon:
        return q.icon
    for t in q.tasks:
        if t[0] == "item":
            return t[1]
        if t[0] == "filter":
            m = re.search(r"item\(([^()]+)\)", t[1])
            if m:
                return m.group(1)
    return None


def retired_call(src, node, off, key, kept):
    q, k = QS[key], QS[kept]
    kc = HOME[kept]
    fn = src[off(node.func.lineno, node.func.col_offset):off(node.func.end_lineno, node.func.end_col_offset)]
    assert fn == "Q", (key, fn)
    title = q.title or key
    xy = [src[off(n.lineno, n.col_offset):off(n.end_lineno, n.end_col_offset)] for n in node.args[1:3]]
    parts = [f'Q("{key}", {xy[0]}, {xy[1]}, [tick()], {json.dumps(title, ensure_ascii=False)}']
    for name in ("section", "secret", "hidden", "row"):
        s = kw_src(src, node, name, off)
        if s:
            parts.append(f"{name}={s}")
    parts.append(f"deps={q.deps!r}")
    parts.append("optional=True, tokens=0, xp=0")
    if q.mirror:
        parts.append(f'mirror="{q.mirror}"')
    ic = first_item(q)
    if ic:
        parts.append(f'icon="{ic}"')
    where = "this page" if kc is HOME[key] else f"the {ctitle(kc)} page"
    parts.append(f'subtitle={json.dumps("Moved: see " + (k.title or kept), ensure_ascii=False)}')
    parts.append("desc=[" + json.dumps(f'&eMoved:&r this step is now "{k.title or kept}" on {where}. Click to dismiss.',
                                       ensure_ascii=False) + "]")
    return ", ".join(parts) + ")"


def main():
    rmap = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
    for r, k in rmap.items():
        assert r in QS, r
        assert k in QS, k
        assert k not in rmap, (r, k)
    edits = {}  # path -> [(start, end, text)]
    done_r, done_d = set(), []
    for path in sorted(QDIR.glob("*.py")):
        if path.name.startswith("_"):
            continue
        src, calls = calls_in(path)
        off = offs(src)
        ed = []
        for key, node in calls:
            a, b = off(node.lineno, node.col_offset), off(node.end_lineno, node.end_col_offset)
            if key in rmap:
                ed.append((a, b, retired_call(src, node, off, key, rmap[key])))
                done_r.add(key)
                continue
            q = QS[key]
            bad = [d for d in q.deps if d in rmap]
            if not bad:
                continue
            text = src[a:b]
            # skip the first argument (the key itself)
            head_end = off(node.args[0].end_lineno, node.args[0].end_col_offset) - a
            head, body = text[:head_end], text[head_end:]
            cur = list(q.deps)
            for d in bad:
                new = rmap[d]
                if new == key:  # the kept copy depended on the retired one: inherit its deps instead
                    repl = [x for x in QS[d].deps if x not in q.deps and x != key]
                    lit = ", ".join(f'"{x}"' for x in repl)
                    if lit:
                        body, n = re.subn(r'"%s"' % re.escape(d), lit, body, count=1)
                    else:
                        body, n = re.subn(r',\s*"%s"|"%s",\s*|"%s"' % ((re.escape(d),) * 3), "", body, count=1)
                elif new in cur:
                    body, n = re.subn(r',\s*"%s"|"%s",\s*' % (re.escape(d), re.escape(d)), "", body, count=1)
                else:
                    body, n = re.subn(r'"%s"' % re.escape(d), f'"{new}"', body, count=1)
                    # shop entries: the dep title follows the dep
                    cur.append(new)
                    if n and path.stem in SHOPS and path.stem != "shop_world":
                        m = re.search(r'"%s",\s*(?:\n\s*)?"([^"]*)"' % re.escape(new), body)
                        if m:
                            body = body[:m.start(1)] + (QS[new].title or new).replace('"', "'") + body[m.end(1):]
                assert n == 1, (path.name, key, d, body[:300])
                done_d.append((key, d, new))
            ed.append((a, b, head + body))
        # links
        for m in re.finditer(r'\("([a-z0-9_]+)", 0, 0\)', src):
            if m.group(1) in rmap and path.stem not in ():
                pass
        if ed:
            edits[path] = (src, ed)
    for path, (src, ed) in edits.items():
        for a, b, t in sorted(ed, reverse=True):
            src = src[:a] + t + src[b:]
        # links=[("retired", x, y)] -> kept (dropped if the kept quest lives on this page)
        for r, k in rmap.items():
            own = HOME[k].key == path.stem
            if own:
                src = re.sub(r',?\s*\("%s", 0, 0\)' % re.escape(r), "", src)
            else:
                src = src.replace(f'("{r}", 0, 0)', f'("{k}", 0, 0)')
        path.write_text(src, encoding="utf-8", newline="\n")
    missing = set(rmap) - done_r
    print(f"retired {len(done_r)}; re-pointed {len(done_d)} deps; missing: {sorted(missing)}")
    for x in done_d:
        print("  ", x)


if __name__ == "__main__":
    main()
