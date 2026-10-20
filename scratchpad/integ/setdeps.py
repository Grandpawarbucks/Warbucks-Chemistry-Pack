"""usage: setdeps.py file.py key=dep1,dep2 ...  (replaces the deps= keyword of Q(key, ...))"""
import ast, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]
p = ROOT / "tools/quests" / sys.argv[1]
src = p.read_text(encoding="utf-8")
lines = src.split("\n"); starts = [0]
for l in lines: starts.append(starts[-1] + len(l) + 1)
off = lambda ln, col: starts[ln - 1] + len(lines[ln - 1].encode()[:col].decode())
want = dict(a.split("=", 1) for a in sys.argv[2:])
eds = []
for n in ast.walk(ast.parse(src)):
    if isinstance(n, ast.Call) and n.args and isinstance(n.args[0], ast.Constant) and n.args[0].value in want:
        k = n.args[0].value
        kw = [x for x in n.keywords if x.arg == "deps"]
        assert kw, k
        v = kw[0].value
        new = "[" + ", ".join(f'"{d}"' for d in want[k].split(",") if d) + "]"
        eds.append((off(v.lineno, v.col_offset), off(v.end_lineno, v.end_col_offset), new))
        want[k] = None
assert all(v is None for v in want.values()), want
for a, b, t in sorted(eds, reverse=True):
    src = src[:a] + t + src[b:]
p.write_text(src, encoding="utf-8", newline="\n")
print("ok", len(eds))
