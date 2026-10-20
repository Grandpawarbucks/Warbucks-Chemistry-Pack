import sys, pathlib, collections
sys.path.insert(0, "tools")
import layout_lint as L
book = pathlib.Path(r"C:\Users\Grandpawarbucks\curseforge\minecraft\Instances\All the Mods 10 - ATM10\config\ftbquests\quests")
stems = sys.argv[1:]
for s in stems:
    c = L.read_snbt(book / "chapters" / f"{s}.snbt")
    qs = c.get("quests", [])
    ims = c.get("images", [])
    items = collections.Counter()
    for q in qs:
        t = (q.get("tasks") or [{}])[0]
        iid, lab = L.task_icon(t) if t else (None, "")
        items[iid or lab] += 1
    dup = sum(v - 1 for v in items.values() if v > 1)
    xs = [float(q.get("x", 0)) for q in qs]; ys = [float(q.get("y", 0)) for q in qs]
    sizes = collections.Counter(float(q.get("size", 1)) for q in qs)
    print(f"{s:28} q={len(qs):3} img={len(ims):2} links={len(c.get('quest_links', [])):2} dupitems={dup:2} "
          f"x[{min(xs, default=0):g},{max(xs, default=0):g}] y[{min(ys, default=0):g},{max(ys, default=0):g}] sizes={dict(sizes.most_common(4))} shape={c.get('default_quest_shape')!r}")
    for im in ims:
        print(f"     img {im.get('width')}x{im.get('height')} @({im.get('x')},{im.get('y')}) rot={im.get('rotation')} {im.get('image')}")
