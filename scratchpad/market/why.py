import sys, json
sys.path.insert(0, "tools")
import build_market_prices as b
items, names, tags, item_tags, blocks = b.load_registry()
rec = b.load_recipes(items, tags)
for want in sys.argv[1:]:
    print("==", want)
    for rid, t, ins, fluid, outs in rec:
        if outs and outs[0][0] == want:
            print("  ", rid, t, [(sorted(o)[:3], c) for o, c in ins], round(fluid,2), outs[:3])
