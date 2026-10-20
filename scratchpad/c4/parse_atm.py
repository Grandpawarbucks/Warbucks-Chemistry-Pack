"""Dump an ATM10 chapter's quest STRUCTURE (ids, positions, tasks, deps, sizes) for mirroring.
Structure only; titles are printed for identification and never copied into our book."""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
ATM = pathlib.Path(r"C:\Users\Grandpawarbucks\curseforge\minecraft\Instances\All the Mods 10 - ATM10\config\ftbquests\quests\chapters")
IDS = {}
for line in (ROOT / "test/ids.tsv").read_text(encoding="utf-8").splitlines():
    p = line.split("\t")
    IDS[p[0]] = p[2] if len(p) > 2 else ""
OURS = set()
for f in (ROOT / "pack/config/ftbquests/quests/chapters").glob("*.snbt"):
    t = f.read_text(encoding="utf-8")
    OURS |= set(re.findall(r'id: "([a-z0-9_]+:[a-z0-9_/]+)"', t))
    OURS |= set(re.findall(r'(?<![_a-z])item\(([a-z0-9_]+:[a-z0-9_/]+)\)', t))


def blocks(text, key):
    """Return the list of top-level '{...}' blocks inside `key: [ ... ]`."""
    i = text.index(key + ": [")
    i = text.index("[", i) + 1
    out, depth, start = [], 0, None
    j = i
    while True:
        c = text[j]
        if c == "{":
            if depth == 0:
                start = j
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                out.append(text[start:j + 1])
        elif c == "]" and depth == 0:
            break
        j += 1
    return out


def field(block, name, default=None):
    m = re.search(r'(?m)^\s*' + name + r': ("?)([^"\n]*)\1\s*$', block)
    return m.group(2) if m else default


def top_level(block):
    """Strip nested {...} and [...] to read the quest's own fields."""
    out, depth = [], 0
    inner = block[1:-1]
    for c in inner:
        if c in "{[":
            depth += 1
        elif c in "}]":
            depth -= 1
        elif depth == 0:
            out.append(c)
    return "".join(out)


def main(stem):
    text = (ATM / f"{stem}.snbt").read_text(encoding="utf-8", errors="replace")
    qs = blocks(text, "quests")
    byid = {}
    rows = []
    for q in qs:
        tl = top_level(q)
        qid = field(tl, "id")
        x = float(field(tl, "x", "0").rstrip("d")); y = float(field(tl, "y", "0").rstrip("d"))
        size = field(tl, "size"); shape = field(tl, "shape")
        title = field(tl, "title", "")
        deps = re.findall(r'"([0-9A-F]{16})"', q[q.find("dependencies"):q.find("]", q.find("dependencies"))] ) if "dependencies" in q else []
        tasks = []
        if "tasks: [" in q:
            for t in blocks(q, "tasks"):
                ttype = field(t, "type", "?")
                cnt = field(t, "count", "1").rstrip("L")
                ids = re.findall(r'id: "([a-z0-9_]+:[a-z0-9_/.-]+)"', t)
                ids = [i for i in ids if not i.startswith("ftbquests:")]
                fid = re.findall(r'item\(([a-z0-9_]+:[a-z0-9_/]+)\)', t)
                tagm = re.findall(r'item_tag\(([a-z0-9_]+:[a-z0-9_/]+)\)', t)
                tag = field(t, "tag", "")
                ent = field(t, "entity", "")
                struct = field(t, "structure", "")
                dimn = field(t, "dimension", "")
                filt = re.search(r'"ftbfiltersystem:filter": "((?:[^"\\]|\\.)*)"', t)
                adv = field(t, "advancement", "")
                if filt:
                    ids = [i for i in ids if i != "ftbfiltersystem:smart_filter"]
                    extra_f = "FILTER<" + filt.group(1).replace('\\"', '"')[:160] + ">"
                    tag = extra_f
                if adv:
                    tag = "ADV " + adv
                tasks.append((ttype, ids or fid or ([("#" + x) for x in tagm] if tagm else []), cnt, tag, ent, struct, dimn))
        rows.append((qid, x, y, size, shape, title, deps, tasks))
        byid[qid] = len(rows)
    for n, (qid, x, y, size, shape, title, deps, tasks) in enumerate(rows, 1):
        d = ",".join(str(byid.get(k, "?")) for k in deps)
        ts = []
        for ttype, ids, cnt, tag, ent, struct, dimn in tasks:
            flags = ""
            for i in ids:
                if i.startswith("#"):
                    flags += f" {i}"
                    continue
                st = "OK" if i in IDS else "MISSING"
                if i in OURS:
                    st += "/asked"
                flags += f" {i}[{st}]"
            extra = tag or ent or struct or dimn
            ts.append(f"{ttype}{flags} x{cnt}" + (f" ({extra})" if extra else ""))
        print(f"{n:3d} {qid} ({x:5.1f},{y:5.1f}) sz={size or '1'} sh={shape or '-'} deps=[{d}] | {' ; '.join(ts)} | ~{title[:40]}")


if __name__ == "__main__":
    for s in sys.argv[1:]:
        print("=" * 20, s)
        main(s)
