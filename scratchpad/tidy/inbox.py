import sys
sys.path.insert(0,"tools")
import layout_lint as L
book = L.load_book(sys.argv[1])
ch = [c for c in book["chapters"] if c["file"]==sys.argv[2]][0]
for im in ch["images"]:
    x0,y0,x1,y1 = L.image_box(im)
    ins = [q["title"] for q in ch["quests"]+ch["links"] if x0<=q["x"]<=x1 and y0<=q["y"]<=y1]
    print(im["image"].split("/")[-1], (im["x"],im["y"],im["w"],im["h"]), len(ins), ins[:5])
