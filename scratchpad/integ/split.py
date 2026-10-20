import re, pathlib
Q = pathlib.Path(__file__).resolve().parents[2] / "tools/quests"
def rd(n): return (Q / n).read_text(encoding="utf-8").split("\n")
def wr(n, lines): (Q / n).write_text("\n".join(lines), encoding="utf-8", newline="\n")

def add_mirrors(block, mp):
    """Insert mirror="..." into the first line of each Q(/helper call whose key is in mp."""
    out, seen = [], set()
    for ln in block:
        m = re.match(r'\s+(?:Q|if_furnace|gg|augment)\("([a-z0-9_]+)"', ln)
        if m and m.group(1) in mp:
            k = m.group(1); seen.add(k)
            # insert after the key argument
            ln = ln.replace(f'("{k}", ', f'("{k}", ', 1)
            out.append(("MIRROR", k, ln))
        else:
            out.append((None, None, ln))
    return out, seen

# ---------------- logic -> integrated
L = rd("logic.py")
s = next(i for i, l in enumerate(L) if "===== Menril and Resin" in l)
e = next(i for i, l in enumerate(L) if "===== ComputerCraft" in l)
block = L[s:e]
src = "\n".join(L)
ns = {}
exec(src[src.index("ID_MIRROR = {"):src.index("}", src.index("ID_MIRROR = {")) + 1], ns)
IDM = ns["ID_MIRROR"]
keys = re.findall(r'^\s+Q\("([a-z0-9_]+)"', "\n".join(block), re.M)
assert set(keys) == set(IDM), (set(keys) ^ set(IDM))
def put_mirror_kw(blocktext, mp):
    # add mirror= right after the section=... argument of each quest whose key in mp
    for k, v in mp.items():
        pat = re.compile(r'(Q\("%s", 0, 0, .*?section=S_[A-Z]+,)' % re.escape(k), re.S)
        m = pat.search(blocktext)
        assert m, k
        blocktext = blocktext[:m.end()] + f' mirror="{v}",' + blocktext[m.end():]
    return blocktext
bt = put_mirror_kw("\n".join(block), IDM)
hdr = '''"""Quest chapter: integrated. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py

Mirror of ATM10's "Integrated Dynamics" chapter (user decision 2026-10-20: quest for quest where we have the mod; the
same items, order, clusters and sizes; the text is ours). Split out of logic.py on 2026-10-20 (keys unchanged), so
each quest now carries its ATM10 id. The Integrated Dynamics wrench, logic cables, variable cards and the Integrated
Tunnels interfaces stay on the logistics page (logic.py), where ATM10's Basic Logistics asks for them.

ATM10 Integrated Dynamics quests skipped: the credits checkmark, the Productive Bees menril bee (no Productive Bees),
and five that repeat a Basic Logistics item (wrench, cable, variable card, the interfaces).
"""
from questlib import Q, Chapter, item, dim, tick, kill, anyof, anytag, MAIN, SIDE  # noqa: F401

OPT = dict(optional=True, tokens=1)
S_MENRIL, S_IDL = "Menril and Resin", "Logic Networks"

CHAPTER = Chapter("integrated", "Integrated Dynamics", "integrateddynamics:logic_programmer",
        ["Logic networks grown from resin."], SIDE, mirror="integrated_dynamics", quests=['''.split("\n")
tail = ['], links=[("t3_hull", 0, 0), ("lg_id_variable", 0, 0), ("lg_idt_item", 0, 0)])', ""]
body = bt.split("\n")
while body and body[-1].strip() == "":
    body.pop()
wr("integrated.py", hdr + body + tail)
# remove from logic
L2 = L[:s] + L[e:]
txt = "\n".join(L2)
a = txt.index("# ATM10 \"integrated_dynamics\" quest ids")
b = txt.index("}\n", txt.index("ID_MIRROR = {")) + 2
txt = txt[:a] + txt[b:].lstrip("\n")
txt = txt.replace('S_MENRIL, S_IDL = "Menril and Resin", "Logic Networks"\n', "")
txt = txt.replace("in the Menril and Resin section of this page.", "on the Integrated Dynamics page.")
txt = txt.replace('''It also carries ATM10's "Integrated Dynamics" chapter,
quest for quest, in two sections of its own. The engine takes one mirror target per chapter, so those quests carry
no mirror id; their ATM10 ids are in ID_MIRROR below, ready if the page is ever split out.''',
'''ATM10's "Integrated Dynamics" chapter is its own
page now (integrated.py, split out 2026-10-20 with the keys unchanged).''')
txt = txt.replace("ATM10 Integrated Dynamics quests skipped: the credits checkmark, the Productive Bees menril bee (no Productive\nBees), and five that repeat a Basic Logistics item on this same page (wrench, cable, variable card, the interfaces).\n", "")
wr("logic.py", txt.split("\n"))
print("integrated:", len(keys))

# ---------------- power -> generators
P = rd("power.py")
s = next(i for i, l in enumerate(P) if "===== The Furnace (ATM10 Generators" in l)
e = max(i for i, l in enumerate(P) if l.startswith("], links="))
block = P[s:e]
src = "\n".join(P)
ns = {}
exec(src[src.index("GEN_MIRROR = {"):src.index("}", src.index("GEN_MIRROR = {")) + 1], ns)
GM = ns["GEN_MIRROR"]
keys = re.findall(r'^\s+(?:Q|if_furnace|gg|augment)\("([a-z0-9_]+)"', "\n".join(block), re.M)
assert set(GM) <= set(keys), set(GM) - set(keys)
bt = "\n".join(block)
for k, v in GM.items():
    pat = re.compile(r'((?:Q|if_furnace|gg|augment)\("%s", )' % re.escape(k))
    m = pat.search(bt); assert m, k
    bt = bt[:m.end()] + bt[m.end():]
    # helpers take **kw / extra args: append mirror= as kw at the call's first line end? simpler: insert after key
    bt = bt[:m.start()] + bt[m.start():].replace(m.group(1), m.group(1), 1)
# helper calls: add mirror via a wrapper mapping at build: simpler -> post-process list
helpers_src = src[src.index("GG_8X = ["):src.index("CHAPTER = Chapter(")]
hdr = '''"""Quest chapter: generators. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py

Mirror of ATM10's "Generators" chapter (Iron Furnaces and Generator Galore; user decision 2026-10-20: quest for quest
where we have the mod; the text is ours). Split out of power.py on 2026-10-20 (keys unchanged); every quest carries
its ATM10 id through GEN_MIRROR below.

ATM10 Generators quests skipped: the credits checkmark and "Rainbow Furnace" (a renamed vanilla item, not a real item).
"""
from questlib import Q, Chapter, item, dim, tick, kill, anyof, MAIN, SIDE  # noqa: F401

OPT = dict(optional=True, tokens=1)
IF, GG = "ironfurnaces:", "generatorgalore:"
S_FURN, S_IF, S_RAINBOW, S_AUG, S_GG = "The Furnace", "Iron Furnaces", "The Rainbow Generator", "Furnace Augments", "Generator Galore"

'''.split("\n")
gm_txt = src[src.index("GEN_MIRROR = {"):src.index("}", src.index("GEN_MIRROR = {")) + 1]
gen = hdr + ["# ATM10 \"generators\" quest id of each quest (set on the quests after the list is built).", *gm_txt.split("\n"), ""] \
    + helpers_src.rstrip("\n").split("\n") + ["", "",
    'CHAPTER = Chapter("generators", "Generators", "ironfurnaces:diamond_furnace",',
    '        ["Faster furnaces and a burner for every fuel."], SIDE, mirror="generators", quests=['] \
    + bt.rstrip("\n").split("\n") + [
    '], links=[("gs_furnace", 0, 0), ("pw_iron_gen", 0, 0)])',
    "for _q in CHAPTER.quests:",
    "    if _q.key in GEN_MIRROR:",
    "        _q.mirror = GEN_MIRROR[_q.key]",
    ""]
wr("generators.py", gen)
P2 = P[:s] + P[e:]
txt = "\n".join(P2)
a = txt.index("# ATM10 \"generators\" quest ids")
b = txt.index("}\n", txt.index("GEN_MIRROR = {")) + 2
txt = txt[:a] + txt[b:]
txt = txt.replace(helpers_src, "")
wr("power.py", txt.split("\n"))
print("generators:", len(keys))
