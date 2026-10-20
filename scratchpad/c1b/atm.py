"""Dump an ATM10 chapter's quest list (ids, pos, size, shape, deps, task items, en_us title) for mirroring."""
import re, sys, pathlib, json

Q = pathlib.Path(r"C:\Users\Grandpawarbucks\curseforge\minecraft\Instances\All the Mods 10 - ATM10\config\ftbquests\quests")


def parse(s):
    i = 0
    n = len(s)

    def ws():
        nonlocal i
        while i < n and s[i] in " \t\r\n,":
            i += 1

    def val():
        nonlocal i
        ws()
        c = s[i]
        if c == "{":
            i += 1
            d = {}
            while True:
                ws()
                if s[i] == "}":
                    i += 1
                    return d
                m = re.compile(r'"((?:[^"\\]|\\.)*)"|([A-Za-z0-9_.+\-]+)').match(s, i)
                k = m.group(1) if m.group(1) is not None else m.group(2)
                i = m.end()
                ws()
                assert s[i] == ":", s[i - 20:i + 20]
                i += 1
                d[k] = val()
        if c == "[":
            i += 1
            ws()
            if re.match(r"[BIL];", s[i:i + 2]):
                i += 2
            out = []
            while True:
                ws()
                if s[i] == "]":
                    i += 1
                    return out
                out.append(val())
        if c == '"':
            m = re.compile(r'"((?:[^"\\]|\\.)*)"').match(s, i)
            i = m.end()
            return m.group(1).encode().decode("unicode_escape") if "\\u" in m.group(1) else m.group(1).replace('\\"', '"')
        m = re.compile(r"[^,\s\]\}]+").match(s, i)
        i = m.end()
        t = m.group(0)
        mm = re.fullmatch(r"(-?[0-9.]+(?:E-?\d+)?)[dfbsLD]?", t)
        if mm:
            return float(mm.group(1))
        return t

    return val()


def lang():
    titles = {}
    for f in (Q / "lang/en_us").rglob("*.snbt"):
        for m in re.finditer(r'quest\.([0-9A-F]{16})\.title: "((?:[^"\\]|\\.)*)"', f.read_text(encoding="utf-8")):
            titles[m.group(1)] = m.group(2)
    return titles


def items_of(t):
    out = []
    it = t.get("item")
    if isinstance(it, dict):
        iid = it.get("id")
        comps = it.get("components", {})
        filt = comps.get("ftbfiltersystem:filter") if isinstance(comps, dict) else None
        if filt:
            out.append("FILTER " + filt)
        else:
            out.append(iid)
    elif isinstance(it, str):
        out.append(it)
    return out


def main(stem):
    d = parse((Q / "chapters" / f"{stem}.snbt").read_text(encoding="utf-8"))
    titles = lang()
    ids = {q["id"] for q in d["quests"]}
    for q in d["quests"]:
        tasks = []
        for t in q.get("tasks", []):
            typ = t.get("type")
            if typ == "item":
                tasks.append(f"{'|'.join(items_of(t))} x{int(t.get('count', 1))}")
            else:
                tasks.append(typ + (":" + str(t.get("dimension") or t.get("entity") or t.get("structure") or "") if typ != "checkmark" else ""))
        deps = q.get("dependencies", [])
        extra = []
        for k in ("size", "shape", "optional", "hide", "dependency_requirement"):
            if k in q:
                extra.append(f"{k}={q[k]}")
        title = titles.get(q["id"], "")
        print(f"{q['id']} ({q['x']:.1f},{q['y']:.1f}) {' '.join(extra)} | {title} | {'; '.join(tasks)} | deps={[ (x if x in ids else 'EXT:'+x) for x in deps]}")
    print("quests:", len(d["quests"]))


if __name__ == "__main__":
    main(sys.argv[1])
