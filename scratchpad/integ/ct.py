from book import *
import re, pathlib
src = (pathlib.Path(qd.__file__)).read_text(encoding="utf-8")
blk = src[src.index("CHAPTER_TITLES = {"):src.index("\n}\n", src.index("CHAPTER_TITLES = {"))]
# comment headers give the intended page
cur = None; intended = {}
for line in blk.split("\n"):
    m = re.match(r"\s*# (.*)", line)
    if m: cur = m.group(1); continue
    m = re.match(r'\s*"([a-z0-9_]+)":', line)
    if m: intended[m.group(1)] = cur
roots = {}
for c in qd.PAGES:
    if c.layout == "manual": continue
    c.style = qd.style_of(c)
    try:
        parts = qd._split_page(c)
    except Exception as e:
        print("ERR", c.key, e); continue
    for p in parts: roots[p["root"]] = c.key
gone, moved, unused, keep = [], [], [], []
for k, grp in intended.items():
    if k not in QS: gone.append(k); continue
    q = QS[k]
    retired = q.tasks == [("checkmark",)] and q.tokens == 0 and q.optional and (q.subtitle or "").startswith("Moved")
    if retired: moved.append((k, "retired")); continue
    if k not in roots: unused.append((k, HOME[k], grp)); continue
    keep.append(k)
print("gone", gone); print("retired", moved); print("not a split root", len(unused)); [print("  ", u) for u in unused]; print("keep", len(keep))

import sys
if "--write" in sys.argv:
    keepset = set(keep)
    p = pathlib.Path(qd.__file__)
    a = src.index("CHAPTER_TITLES = {")
    b = src.index("\n}\n", a)
    lines = src[a:b].split("\n")
    out, pending, entry = [lines[0]], None, []
    i = 1
    # group: header comment then entry lines (an entry may continue on the next line)
    groups, cur = [], None
    for line in lines[1:]:
        if re.match(r"\s*# ", line):
            cur = [line, []]; groups.append(cur); continue
        m = re.match(r'\s*"([a-z0-9_]+)":', line)
        if m:
            cur[1].append([m.group(1), line])
        else:
            cur[1][-1][1] += "\n" + line
    for hdr, ents in groups:
        ks = [l for k, l in ents if k in keepset]
        if ks:
            out.append(hdr); out += ks
    new = "\n".join(out)
    src2 = src[:a] + new + src[b:]
    src2 = src2.replace("# Chapter names and subtitles, by the chapter's root quest (the quest the layout names a section after); icon is\n# optional (default: the root quest's item). A chapter not listed here keeps the layout's auto title.",
        "# Chapter names and subtitles, by the chapter's root quest (the quest the layout names a section after); icon is\n# optional (default: the root quest's item). A chapter not listed here keeps the layout's auto title. Only used when\n# SPLIT_TABS splits a group; pruned 2026-10-20 to the roots a split of the current pages would still produce.")
    p.write_text(src2, encoding="utf-8", newline="\n")
    print("written; kept", len(keepset))
