"""Dump an ATM10 chapter's quest structure (ids, positions, tasks, deps, shape/size). Reference only (ARR: structure only)."""
import re
import sys
import pathlib

ATM = pathlib.Path(r"C:\Users\Grandpawarbucks\curseforge\minecraft\Instances\All the Mods 10 - ATM10\config\ftbquests\quests\chapters")
text = (ATM / (sys.argv[1] + ".snbt")).read_text(encoding="utf-8", errors="replace")
i = text.index("quests: [")
body = text[i + 9:]
depth = 0
start = None
blocks = []
for j, c in enumerate(body):
    if c == '{':
        if depth == 0:
            start = j
        depth += 1
    elif c == '}':
        depth -= 1
        if depth == 0:
            blocks.append(body[start:j + 1])
    elif c == ']' and depth == 0:
        break

TAB3 = "\n\t\t\t"


def field(b, name, default=""):
    m = re.search(r'(?m)^\s*' + name + r': (.+)$', b)
    return m.group(1).strip() if m else default


def top_field(b, name, default=""):
    m = re.search(r'(?m)^\t\t\t' + name + r': (.+)$', b)
    return m.group(1).strip() if m else default


def task_blocks(b):
    m = re.search(r'(?s)' + TAB3 + r'tasks: \[(.*?)' + TAB3 + r'\]', b)
    if not m:
        m = re.search(r'(?s)' + TAB3 + r'tasks: \[(\{.*?' + TAB3 + r'\})\]', b)
    if not m:
        return []
    tb = m.group(1)
    out = []
    d = 0
    s = None
    for j, c in enumerate(tb):
        if c == '{':
            if d == 0:
                s = j
            d += 1
        elif c == '}':
            d -= 1
            if d == 0:
                out.append(tb[s:j + 1])
    return out


for b in blocks:
    qid = top_field(b, "id").strip('"')
    x = top_field(b, "x", "0").rstrip("d")
    y = top_field(b, "y", "0").rstrip("d")
    shape = top_field(b, "shape", "").strip('"')
    size = top_field(b, "size", "").rstrip("d")
    dm = re.search(r'(?s)' + TAB3 + r'dependencies: \[(.*?)\]', b)
    deps = re.findall(r'"([0-9A-F]{16})"', dm.group(1)) if dm else []
    flags = []
    if top_field(b, "optional"):
        flags.append("opt")
    if top_field(b, "hide_until_deps_visible"):
        flags.append("hidden")
    tasks = []
    for t in task_blocks(b):
        ttype = field(t, "type", "item").strip('"')
        if ttype == "item":
            m = re.search(r'item: (?:\{[^}]*?id: )?"([^"]+)"', t)
            if not m:
                m = re.search(r'id: "([a-z0-9_]+:[a-z0-9_/]+)"', t)
            cnt = field(t, "count", "1").rstrip("L")
            items = re.findall(r'item\(([a-z0-9_:/]+)\)', t)
            tag = re.findall(r'item_tag\(([^)]+)\)', t)
            desc = (m.group(1) if m else "?") + " x" + cnt
            if items:
                desc += " OR[" + ",".join(items) + "]"
            if tag:
                desc += " TAG[" + ",".join(tag) + "]"
        elif ttype == "kill":
            desc = field(t, "entity").strip('"') + " x" + field(t, "value", "1").rstrip("L")
        elif ttype in ("structure", "biome", "dimension", "advancement"):
            desc = field(t, ttype).strip('"')
        elif ttype == "checkmark":
            desc = "tick"
        elif ttype == "observation":
            desc = field(t, "to_observe").strip('"')
        else:
            desc = t.replace("\n", " ").replace("\t", "")[:100]
        tasks.append(f"{ttype}:{desc}")
    print(f"{qid}\t({x},{y})\t{shape or '-'}{'/' + size if size else ''}\t{' '.join(flags)}\tdeps={','.join(deps)}\t| " + " ; ".join(tasks))
print(len(blocks), "quests")
