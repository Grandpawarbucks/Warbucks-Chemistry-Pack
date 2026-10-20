"""Dump an ATM10 chapter's quest STRUCTURE (ids, positions, task item ids/counts, deps, shape/size).
Requirements only: never prints their text. Usage: parse_atm.py <chapter stem>"""
import re, sys, pathlib

ATM = pathlib.Path(r"C:\Users\Grandpawarbucks\curseforge\minecraft\Instances\All the Mods 10 - ATM10\config\ftbquests\quests\chapters")
ROOT = pathlib.Path(__file__).resolve().parents[2]
IDS = {l.split("\t")[0] for l in (ROOT / "test/ids.tsv").read_text(encoding="utf-8").splitlines()}


def list_blocks(text, start):
    """Elements (as raw text) of the [ ... ] list that starts at text[start] == '['."""
    depth = 0; s = None; out = []
    for k in range(start + 1, len(text)):
        c = text[k]
        if c == "{":
            if depth == 0:
                s = k
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                out.append(text[s:k + 1])
        elif c == "]" and depth == 0:
            break
    return out


def base(block):
    m = re.search(r"\n(\t+)[a-z_]+: ", block)
    return len(m.group(1)) if m else 0


def fld(block, name, default=None):
    tabs = base(block)
    m = re.search(rf"\n\t{{{tabs}}}{name}: (.+)", block)
    return m.group(1).strip() if m else default


def main():
    stem = sys.argv[1]
    text = ATM.joinpath(stem + ".snbt").read_text(encoding="utf-8", errors="replace")
    qs = []
    for b in list_blocks(text, text.index("\n\tquests: [") + len("\n\tquests: ")):
        qid = fld(b, "id").strip('"')
        x = float(fld(b, "x", "0").rstrip("d")); y = float(fld(b, "y", "0").rstrip("d"))
        shape = fld(b, "shape", '""').strip('"'); size = fld(b, "size", "1").rstrip("d")
        opt = fld(b, "optional", "false")
        depf = fld(b, "dependencies", "")
        if depf == "[":
            m = re.search(rf"\n\t{{{base(b)}}}dependencies: \[(.*?)\]", b, re.S); depf = m.group(1)
        deps = re.findall(r'"([0-9A-F]{16})"', depf)
        tasks = []
        m = re.search(rf"\n\t{{{base(b)}}}tasks: \[", b)
        for t in (list_blocks(b, m.end() - 1) if m else []):
            ttype = fld(t, "type", '""').strip('"')
            if ttype == "item":
                itm = fld(t, "item")
                if itm and itm.startswith("{") and itm.endswith("}"):
                    body = itm
                elif itm and itm.startswith("{"):
                    bt = base(t)
                    m2 = re.search(rf"\n\t{{{bt}}}item: \{{(.*?)\n\t{{{bt}}}\}}", t, re.S); body = m2.group(1)
                else:
                    body = f"id: {itm}"
                iid = re.search(r'id: "([^"]+)"', body); iid = iid.group(1) if iid else "?"
                cnt = re.search(r"count: (\d+)", body); cnt = int(cnt.group(1)) if cnt else 1
                cnt2 = fld(t, "count")
                if cnt2:
                    cnt = int(re.sub(r"[^0-9]", "", cnt2))
                filt = re.findall(r"item\(([a-z0-9_]+:[a-z0-9_/]+)\)", body)
                tag = re.findall(r"item_tag\(([^)]+)\)", body)
                if filt:
                    iid = "or(" + ",".join(filt) + ")"
                if tag:
                    iid = "tag(" + ",".join(tag) + ")"
                tasks.append(f"{iid} x{cnt}")
            else:
                extra = (fld(t, "dimension") or fld(t, "entity") or fld(t, "structure") or fld(t, "biome")
                         or fld(t, "stat") or fld(t, "advancement") or fld(t, "value") or "")
                tasks.append(f"[{ttype} {extra}]")
        qs.append((qid, x, y, shape, size, opt, deps, tasks))
    qs.sort(key=lambda q: (q[2], q[1]))
    idx = {q[0]: n for n, q in enumerate(qs)}
    for n, (qid, x, y, shape, size, opt, deps, tasks) in enumerate(qs):
        flags = []
        for t in tasks:
            if t.startswith("[") or t.startswith("tag("):
                continue
            ids = re.findall(r"[a-z0-9_]+:[a-z0-9_/]+", t.split(" x")[0])
            miss = [i for i in ids if i not in IDS]
            if miss:
                flags.append(("ALLMISS:" if len(miss) == len(ids) else "some-miss:") + ",".join(miss))
        dep_s = ",".join(f"#{idx.get(d, '?')}" for d in deps)
        print(f"#{n:<3} {qid} ({x:5.1f},{y:5.1f}) {shape or '-':8} s{size} {'opt' if opt=='true' else '   '} deps[{dep_s}] | "
              + " ; ".join(tasks) + ("  <<" + " ".join(flags) if flags else ""))


main()
