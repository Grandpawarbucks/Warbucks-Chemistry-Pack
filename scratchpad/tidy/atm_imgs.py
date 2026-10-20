import sys
sys.path.insert(0, "tools")
import layout
for stem in sys.argv[1:]:
    atm = layout.load_mirror(stem)
    Q = atm["quests"]
    print("==", stem, len(Q), "quests", len(atm["images"]), "images")
    for im in atm["images"]:
        x0,y0,x1,y1 = layout._mirror_box(im)
        inside = [q for q in Q.values() if x0<=q["x"]<=x1 and y0<=q["y"]<=y1]
        print(f"  img c=({im['x']:.1f},{im['y']:.1f}) {im['width']:.1f}x{im['height']:.1f} rot={im['rotation']:.0f} inside={len(inside)}")
