"""Parse an ATM10 chapter: id, pos, size/shape, tasks (items incl. filter strings), deps, title; dump TSV + a cluster view."""
import re, sys, json, pathlib

A = pathlib.Path(r"C:\Users\Grandpawarbucks\curseforge\minecraft\Instances\All the Mods 10 - ATM10\config\ftbquests\quests")
ROOT = pathlib.Path(r"C:\Users\Grandpawarbucks\OneDrive\Desktop\Chem Modpack Dev\Warbucks-Chemistry-Pack")
IDS = {l.split("\t")[0] for l in (ROOT / "test/ids.tsv").read_text(encoding="utf-8").splitlines()}


class P:
    def __init__(self, s):
        self.s, self.i = s, 0

    def ws(self):
        while self.i < len(self.s) and self.s[self.i] in " \t\r\n,":
            self.i += 1

    def val(self):
        self.ws()
        c = self.s[self.i]
        if c == "{":
            self.i += 1
            d = {}
            while True:
                self.ws()
                if self.s[self.i] == "}":
                    self.i += 1
                    return d
                k = self.key()
                self.ws()
                assert self.s[self.i] == ":", self.s[self.i:self.i + 40]
                self.i += 1
                d[k] = self.val()
        if c == "[":
            self.i += 1
            l = []
            # typed arrays [I; ...]
            m = re.match(r"[BIL];", self.s[self.i:self.i + 2])
            if m:
                self.i += 2
            while True:
                self.ws()
                if self.s[self.i] == "]":
                    self.i += 1
                    return l
                l.append(self.val())
        if c == '"':
            return self.str()
        m = re.match(r"[^,\s\]\}]+", self.s[self.i:])
        t = m.group(0)
        self.i += len(t)
        if re.fullmatch(r"-?[0-9.]+[dfbsLl]?", t):
            return float(re.sub(r"[dfbsLl]$", "", t))
        return t

    def key(self):
        if self.s[self.i] == '"':
            return self.str()
        m = re.match(r"[A-Za-z0-9_.\-]+", self.s[self.i:])
        self.i += len(m.group(0))
        return m.group(0)

    def str(self):
        assert self.s[self.i] == '"'
        self.i += 1
        out = []
        while self.s[self.i] != '"':
            if self.s[self.i] == "\\":
                self.i += 1
            out.append(self.s[self.i])
            self.i += 1
        self.i += 1
        return "".join(out)


def load(name):
    d = P((A / "chapters" / f"{name}.snbt").read_text(encoding="utf-8", errors="replace")).val()
    lang = (A / "lang/en_us/chapters" / f"{name}.snbt_merged").read_text(encoding="utf-8", errors="replace")
    titles = dict(re.findall(r'quest\.([0-9A-F]{16})\.title: "(.*?)"\n', lang))
    return d, titles


def task_items(t):
    out = []
    ty = t.get("type", "item")
    if ty == "item":
        it = t.get("item")
        if isinstance(it, dict):
            if it.get("id") == "ftbfiltersystem:smart_filter" and "components" in it:
                f = it["components"].get("ftbfiltersystem:filter", "")
                for m in re.findall(r"item\(([a-z0-9_]+:[a-z0-9_/]+)\)", f):
                    out.append((m, int(t.get("count", it.get("count", 1)))))
                for m in re.findall(r"item_tag\(([a-z0-9_]+:[a-z0-9_/]+)\)", f):
                    out.append(("#" + m, int(t.get("count", it.get("count", 1)))))
                out.append(("<or>", 0))
            elif "id" in it:
                out.append((it["id"], int(t.get("count", it.get("count", 1)))))
            elif "components" in it and "ftbfiltersystem:filter" in str(it):
                for m in re.findall(r"item\(([a-z0-9_]+:[a-z0-9_/]+)\)", json.dumps(it)):
                    out.append((m, int(t.get("count", 1))))
                for m in re.findall(r"item_tag\(([a-z0-9_]+:[a-z0-9_/]+)\)", json.dumps(it)):
                    out.append(("#" + m, int(t.get("count", 1))))
        elif isinstance(it, str):
            out.append((it, int(t.get("count", 1))))
    else:
        out.append((f"<{ty}>", 0))
    return out


def main(name):
    d, titles = load(name)
    qs = []
    for q in d["quests"]:
        items = [i for t in q.get("tasks", []) for i in task_items(t)]
        qs.append(dict(id=q["id"], x=q.get("x", 0), y=q.get("y", 0), size=q.get("size", 1), shape=q.get("shape", ""),
                       deps=q.get("dependencies", []), items=items, title=re.sub(r"&[0-9a-z]", "", titles.get(q["id"], "") or str(q.get("title", ""))),
                       opt=q.get("optional", False)))
    qs.sort(key=lambda q: (q["x"], q["y"]))
    for q in qs:
        have = all((i.startswith("#") or i.startswith("<") or i in IDS) for i, _ in q["items"])
        flag = "OK " if have else "MISS"
        print(f'{q["id"]}\t{q["x"]:6.1f}\t{q["y"]:6.1f}\ts={q["size"]}\t{q["shape"]:8}\t{flag}\t{q["title"][:40]:40}\t'
              f'{" | ".join(f"{i} x{n}" for i, n in q["items"])}\tdeps={",".join(q["deps"])}')
    print(len(qs), "quests")


if __name__ == "__main__":
    main(sys.argv[1])
