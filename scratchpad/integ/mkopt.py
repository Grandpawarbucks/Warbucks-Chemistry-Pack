"""Mark quests optional (keys from argv file), checking that no required non-shop quest depends on them."""
import ast, pathlib, sys
from book import *
ROOT = pathlib.Path(__file__).resolve().parents[2]
keys = [k for k in pathlib.Path(sys.argv[1]).read_text().split() if k and not QS[k].optional]
S = set(keys)
for k in keys:
    assert k in QS, k
    assert not QS[k].optional, ("already optional", k)
    blockers = [d for d in DEPENDENTS.get(k, []) if HOME[d] not in SHOP and not QS[d].optional and d not in S]
    assert not blockers, (k, blockers)
byfile = {}
for k in keys:
    byfile.setdefault(HOME[k], []).append(k)
n = 0
for ch, ks in byfile.items():
    p = ROOT / "tools/quests" / f"{ch}.py"
    src = p.read_text(encoding="utf-8")
    lines = src.split("\n"); starts = [0]
    for l in lines: starts.append(starts[-1] + len(l) + 1)
    off = lambda ln, col: starts[ln - 1] + len(lines[ln - 1].encode()[:col].decode())
    eds, found = [], set()
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.Call) and node.args and isinstance(node.args[0], ast.Constant) and node.args[0].value in ks:
            k = node.args[0].value
            assert not any(kw.arg == "optional" or kw.arg is None for kw in node.keywords), (k, "has optional/**kw")
            if node.keywords:
                kw = node.keywords[0]
                # keyword node start = its arg name start (py3.9+: kw has lineno/col_offset)
                eds.append((off(kw.lineno, kw.col_offset), "optional=True, "))
            else:
                eds.append((off(node.end_lineno, node.end_col_offset) - 1, ", optional=True"))
            found.add(k)
    assert found == set(ks), set(ks) - found
    for a, t in sorted(eds, reverse=True):
        src = src[:a] + t + src[a:]
    p.write_text(src, encoding="utf-8", newline="\n")
    n += len(eds)
print("marked optional:", n)
