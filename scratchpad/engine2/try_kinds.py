import sys
sys.path.insert(0, "tools")
import build_pictures as bp
for kind in ("decor", "machine"):
    img, k = bp._draw({"chapter": "create", "slug": "x", "width": 1.5, "height": 1.5, "kind": kind,
                       "nearby_items": ["create:mechanical_press"], "title": None})
    img.save(f"scratchpad/engine2/behind_{kind}.png")
    print(kind, k, img.size)
