"""Merge the basic_tools mirror into tools/quests/tools.py and retire Silent Gear duplicates."""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[2]
p = ROOT / "tools/quests/tools.py"
s = p.read_text(encoding="utf-8")
head = (ROOT / "scratchpad/c5b/tools_head.txt").read_text(encoding="utf-8")
new = (ROOT / "scratchpad/c5b/tools_new.txt").read_text(encoding="utf-8")

imp = 'from questlib import Q, Chapter, item, dim, tick, kill, anytag, anyof, MAIN, SIDE  # noqa: F401\n\n'
if "def col(" not in s:
    assert s.count(imp) == 1
    s = s.replace(imp, head)
end = '], links=[("gs_silent", -2, 0)'
if 'Q("tc_hub"' not in s:
    assert s.count(end) == 1
    s = s.replace(end, new + end)
if 'mirror="basic_tools"' not in s:
    s = s.replace('("jdt_goo", 2, 17.5)])', '("jdt_goo", 2, 17.5)], mirror="basic_tools")')
    assert 'mirror="basic_tools"' in s

RETIRE = ["tc_salvager", "tc_grader", "tc_sg_catalyst", "tc_sg_glittery", "tc_sg_charger", "tc_sg_recrystallizer",
          "tc_sg_dust", "tc_sg_starmetal", "tc_sg_blocks", "tc_sg_ring", "tc_sg_armor"]
for key in RETIRE:
    m = re.search(r'    Q\("' + key + r'".*?\]\),\n', s, re.S)
    assert m, key
    block = m.group(0)
    title = re.search(r'\]\s*,?\s*\n?\s*"([^"]+)"', block[block.index("["):])
    tm = re.search(r'Q\("' + key + r'", [^\[]*\[.*?\]\)?\],\s*(?:\n\s*)?"([^"]+)"', block, re.S)
    t = tm.group(1) if tm else key
    dm = re.search(r'deps=(\[[^\]]*\])', block)
    deps = dm.group(1) if dm else "[]"
    repl = (f'    Q("{key}", 0, 0, [tick()], "{t}", deps={deps}, xp=0, optional=True, tokens=0,\n'
            f'      subtitle="Retired: now on the Silent Gear page", desc=[\n'
            f'        "&eWhat:&r this quest moved to the Silent Gear page, which covers the same item. Click the check to clear it here."]),\n')
    s = s.replace(block, repl)
p.write_text(s, encoding="utf-8", newline="\n")
print("done")
