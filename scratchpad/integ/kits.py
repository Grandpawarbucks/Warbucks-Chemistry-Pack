import ast, pathlib
Qd = pathlib.Path(__file__).resolve().parents[2] / "tools/quests"
s = (Qd / "storage.py").read_text(encoding="utf-8")
lines = s.split("\n")
tree = ast.parse(s)
grab = sorted((n.lineno, n.end_lineno) for n in ast.walk(tree) if isinstance(n, ast.Call) and n.args
              and isinstance(n.args[0], ast.Constant) and n.args[0].value in ("sto_if_kits", "sto_if_more_kits"))
chunks = []
for a, b in reversed(grab):
    seg = lines[a-1:b]
    assert seg[-1].rstrip().endswith("),"), seg[-1]
    chunks.insert(0, "\n".join(seg))
    del lines[a-1:b]
(Qd / "storage.py").write_text("\n".join(lines), encoding="utf-8", newline="\n")
g = (Qd / "generators.py").read_text(encoding="utf-8")
i = g.rindex("], links=")
g = g[:i] + "    # ===== Upgrade kits (moved from storage.py 2026-10-20; keys unchanged) ==================\n" + "\n".join(chunks) + "\n" + g[i:]
(Qd / "generators.py").write_text(g, encoding="utf-8", newline="\n")
print(len(chunks))
