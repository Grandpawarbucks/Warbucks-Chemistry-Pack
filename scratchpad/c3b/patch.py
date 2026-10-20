"""Patch Q(...) calls in a chapter file in place.

usage: patch.py <chapter.py> <spec.py>
spec.py defines:
  EDIT = {key: {"tasks": "<src>", "<kwarg>": "<src>", ...}}  replace/append keyword args (tasks = 4th positional)
  MOVE_OUT = [keys]          remove these Q calls from this file; their source is written to <spec>.moved.txt
  INSERT = "<src>"           text inserted before the closing ']' of the quest list
  INSERT_FILE = "<path>"     (optional) extra text file inserted too (e.g. quests moved from another chapter)
"""
import ast, pathlib, runpy, sys

path = pathlib.Path(sys.argv[1])
spec = runpy.run_path(sys.argv[2])
src = path.read_bytes()
text = src.decode("utf-8")
tree = ast.parse(text)
lines = src.split(b"\n")
starts = [0]
for ln in lines[:-1]:
    starts.append(starts[-1] + len(ln) + 1)


def off(lineno, col):
    return starts[lineno - 1] + col


edits = []  # (start, end, bytes)
EDIT = spec.get("EDIT", {})
MOVE = set(spec.get("MOVE_OUT", []))
seen = set()
moved = []
chapter_call = None
for node in ast.walk(tree):
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "Chapter":
        chapter_call = node
    if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "Q"):
        continue
    if not node.args or not isinstance(node.args[0], ast.Constant):
        continue
    key = node.args[0].value
    if key in MOVE:
        s, e = off(node.lineno, node.col_offset), off(node.end_lineno, node.end_col_offset)
        # swallow the trailing comma
        j = e
        while src[j:j + 1] in (b" ", b"\t"):
            j += 1
        if src[j:j + 1] == b",":
            e = j + 1
        # swallow leading indentation
        i = s
        while i > 0 and src[i - 1:i] in (b" ",):
            i -= 1
        if src[i - 1:i] == b"\n":
            s = i
            if src[e:e + 1] == b"\n":
                e += 1
        moved.append(src[s:e].decode("utf-8"))
        edits.append((s, e, b""))
        seen.add(key)
        continue
    if key not in EDIT:
        continue
    seen.add(key)
    ch = dict(EDIT[key])
    if "tasks" in ch:
        t = ch.pop("tasks")
        if len(node.args) > 3:
            a = node.args[3]
        else:
            a = next(k.value for k in node.keywords if k.arg == "tasks")
        edits.append((off(a.lineno, a.col_offset), off(a.end_lineno, a.end_col_offset), t.encode("utf-8")))
    if "title" in ch and len(node.args) > 4:
        a = node.args[4]
        edits.append((off(a.lineno, a.col_offset), off(a.end_lineno, a.end_col_offset), ch.pop("title").encode("utf-8")))
    if "deps_add" in ch:
        kw = next(k for k in node.keywords if k.arg == "deps")
        cur = ast.literal_eval(kw.value)
        ch["deps"] = repr(cur + [d for d in ch.pop("deps_add") if d not in cur])
    append = []
    for name, val in ch.items():
        kw = next((k for k in node.keywords if k.arg == name), None)
        if kw is not None:
            edits.append((off(kw.value.lineno, kw.value.col_offset), off(kw.value.end_lineno, kw.value.end_col_offset), val.encode("utf-8")))
        else:
            append.append(f"{name}={val}")
    if append:
        e = off(node.end_lineno, node.end_col_offset) - 1  # before ')'
        edits.append((e, e, (", " + ", ".join(append)).encode("utf-8")))

missing = (set(EDIT) | MOVE) - seen
if missing:
    sys.exit(f"keys not found: {sorted(missing)}")

ins = spec.get("INSERT", "")
if spec.get("INSERT_FILE"):
    ins = pathlib.Path(spec["INSERT_FILE"]).read_text(encoding="utf-8") + ins
if ins:
    lst = chapter_call.args[5]
    e = off(lst.end_lineno, lst.end_col_offset) - 1  # the ']'
    # back up over whitespace before ']'
    edits.append((e, e, ("\n" + ins.rstrip() + "\n").encode("utf-8")))

edits.sort(key=lambda t: t[0], reverse=True)
out = src
for s, e, b in edits:
    out = out[:s] + b + out[e:]
path.write_bytes(out)
if moved:
    pathlib.Path(sys.argv[2] + ".moved.txt").write_text("".join(moved), encoding="utf-8", newline="\n")
print(f"patched {path.name}: {len(EDIT)} edited, {len(MOVE)} moved out, insert {len(ins)} chars")
