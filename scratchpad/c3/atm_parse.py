"""Structural dump of an ATM10 chapter (ids, positions, tasks, deps, size/shape). Requirements only, for mirroring."""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
ATM = pathlib.Path(r"C:\Users\Grandpawarbucks\curseforge\minecraft\Instances\All the Mods 10 - ATM10\config\ftbquests\quests")
ids = {}
for line in (ROOT / "test/ids.tsv").read_text(encoding="utf-8").splitlines():
    p = line.split("\t")
    ids[p[0]] = p[1] if len(p) > 1 else ""
ours = "\n".join(p.read_text(encoding="utf-8") for p in (ROOT / "tools/quests").glob("*.py"))
LANG = {}
_lt = (ATM / "lang/en_us.snbt").read_text(encoding="utf-8", errors="replace")
for m in re.finditer(r'quest\.([0-9A-F]{16})\.title: "([^"]*)"', _lt):
    LANG[m.group(1)] = re.sub(r"&[0-9a-fk-or]", "", m.group(2))


def balanced(text, start, open_c, close_c):
    """Return the text inside the bracket at text[start] (exclusive), handling nesting."""
    depth = 0
    for i in range(start, len(text)):
        if text[i] == open_c:
            depth += 1
        elif text[i] == close_c:
            depth -= 1
            if depth == 0:
                return text[start + 1:i]
    return text[start + 1:]


def split_top(body):
    out, depth, start = [], 0, None
    for i, c in enumerate(body):
        if c == "{":
            if depth == 0:
                start = i
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                out.append(body[start:i + 1])
    return out


def parse(stem):
    text = (ATM / "chapters" / f"{stem}.snbt").read_text(encoding="utf-8", errors="replace")
    qi = text.index("\n\tquests: [")
    quests = split_top(balanced(text, qi + len("\n\tquests: "), "[", "]"))
    rows = []
    for q in quests:
        qid = re.search(r'\n\t\t\tid: "([0-9A-F]+)"', q).group(1)
        x = re.search(r'\n\t\t\tx: (-?[\d.]+)', q); y = re.search(r'\n\t\t\ty: (-?[\d.]+)', q)
        size = re.search(r'\n\t\t\tsize: ([\d.]+)', q); shape = re.search(r'\n\t\t\tshape: "(\w+)"', q)
        title = re.search(r'\n\t\t\ttitle: "([^"]*)"', q)
        title = title.group(1) if title else LANG.get(qid, "")
        deps = re.findall(r'"([0-9A-F]{16})"', balanced(q, q.index("dependencies: ") + len("dependencies: "), "[", "]")) if "dependencies:" in q else []
        opt = "optional: true" in q
        tasks = []
        if "\n\t\t\ttasks: [" in q:
            ti = q.index("\n\t\t\ttasks: [") + len("\n\t\t\ttasks: ")
            for t in split_top(balanced(q, ti, "[", "]")):
                ttype = re.search(r'type: "(\w+)"', t).group(1)
                if ttype == "item":
                    im = re.search(r'item: (\{.*?\}|"[^"]*")', t, re.S)
                    its = []
                    cnt = re.search(r'\n\t\t\t\t\tcount: (\d+)', t) or re.search(r'count: (\d+)', t)
                    if im:
                        s = im.group(1)
                        idm = re.search(r'id: "([a-z0-9_]+:[a-z0-9_/]+)"', s) or re.search(r'"([a-z0-9_]+:[a-z0-9_/]+)"', s)
                        if idm:
                            its.append(idm.group(1))
                        its += re.findall(r'item\(([a-z0-9_]+:[a-z0-9_/]+)', s)
                        its += [f"#{x}" for x in re.findall(r'item_tag\(([^)]+)\)', s)]
                        tagm = re.search(r'tag: "([^"]*)"', s)
                        if tagm:
                            its.append(f"#{tagm.group(1)}")
                    tasks.append(("item", its, int(cnt.group(1)) if cnt else 1))
                else:
                    extra = re.search(r'(?:entity|structure|biome|dimension|fluid|stat|tag): "([^"]*)"', t)
                    amt = re.search(r'amount: (\d+)', t)
                    tasks.append((ttype, [extra.group(1)] if extra else [], int(amt.group(1)) if amt else 1))
        rows.append(dict(id=qid, x=x.group(1) if x else "?", y=y.group(1) if y else "?", size=size.group(1) if size else "1",
                         shape=shape.group(1) if shape else "", title=title, deps=deps, tasks=tasks, opt=opt))
    return rows


if __name__ == "__main__":
    rows = parse(sys.argv[1])
    byid = {r["id"]: i for i, r in enumerate(rows)}
    for i, r in enumerate(rows):
        deps = ",".join(f"#{byid.get(d, '?')}" for d in r["deps"])
        print(f"#{i:<3} {r['id']} x={r['x']:>6} y={r['y']:>6} sz={r['size']:<4} {r['shape']:<8} opt={int(r['opt'])} deps=[{deps}] | {r['title']}")
        for ttype, its, cnt in r["tasks"]:
            marks = []
            for it in its:
                if it.startswith("#"):
                    marks.append(it)
                else:
                    have = it in ids
                    inbook = f'"{it}"' in ours or f'"{it.split(":", 1)[1]}"' in ours
                    marks.append(f"{it}{'' if have else ' [MISSING]'}{' [quested]' if have and inbook else ''}")
            print(f"        {ttype} x{cnt}: " + ", ".join(marks))
